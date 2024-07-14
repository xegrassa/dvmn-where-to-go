import logging
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import requests
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from pydantic import BaseModel, Field, ValidationError
from requests import Response, HTTPError
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

from places.models import Place


class Coordinate(BaseModel):
    lng: float
    lat: float


class PlaceSchema(BaseModel):
    title: str
    short_description: str = Field(..., alias="description_short")
    long_description: str = Field(..., alias="description_long")
    imgs: list[str]
    coordinates: Coordinate


logger = logging.getLogger(__name__)


def collect_urls(options: dict) -> list[str]:
    """Сбор URL для скачивания.

    Собирает из файла переданный через флаг --file-path
    И переданные напрямую как позиционные аргументы
    """
    urls = []
    if options["file_path"]:
        with open(options["file_path"]) as f:
            for line in f:
                urls.append(line.strip())
    if options["urls"]:
        for url in options["urls"]:
            urls.append(url)

    if not urls:
        raise ValueError(
            "Нет URL для скачивания. Проверте что передали их как позиционный аргумент или как путь до файла"
        )

    debug_message = "\n".join(urls)
    logger.debug(f"Кол-во ссылок на json: {len(urls)}\n {debug_message}")

    return urls


def _download(url: str) -> Response | None:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        logger.debug(f"Не удалось скачать {url}: {e}")
        return None

    return response


def download_jsons(urls: list[str], thread_count: int) -> list[PlaceSchema]:
    places_dto = []
    responses = thread_map(_download, urls, max_workers=thread_count, desc="Downloading json")
    responses = list(filter(lambda resp: resp is not None, responses))
    for r in responses:
        try:
            places_dto.append(PlaceSchema(**r.json()))
        except ValidationError as e:
            logger.debug(f"Невалидный json {r.url}: {e}")

    logger.debug(f"Успешно скачанных json: {len(places_dto)}")

    return places_dto


def download_images(urls: list[str], thread_count: int) -> dict[str, bytes]:
    responses = thread_map(_download, urls, max_workers=thread_count, desc="Downloading images")
    responses = list(filter(lambda resp: resp is not None, responses))
    images = {r.url: r.content for r in responses}

    logger.debug(f"Успешно скачанных изображений: {len(images)}")

    return images


def configure_logger(log):
    log.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(levelname)8s] %(name)s:%(lineno)d %(message)s")
    console_handler.setFormatter(formatter)

    log.addHandler(console_handler)


class Command(BaseCommand):
    help = "Loads places to DB"

    def handle(self, *args, **options):

        if options["verbose"]:
            configure_logger(logger)

        json_urls = collect_urls(options)
        places_dto = download_jsons(json_urls, options["thread_count"])

        image_urls = [img for place in places_dto for img in place.imgs]
        image_results = download_images(image_urls, options["thread_count"])

        for place_dto in places_dto:
            place = Place.objects.create(
                title=place_dto.title,
                short_description=place_dto.short_description,
                long_description=place_dto.long_description,
                longitude=place_dto.coordinates.lng,
                latitude=place_dto.coordinates.lat,
            )

            for img_url in place_dto.imgs:
                file_content = image_results[img_url]
                file_name = os.path.basename(urlparse(img_url).path)

                place.images.create(image=ImageFile(ContentFile(file_content, name=file_name)))

    def add_arguments(self, parser):
        parser.add_argument("--urls", nargs="+", help="URLS для скачивания json файлов")
        parser.add_argument("--thread-count", type=int, default=6, help="Кол-во потоков для скачивания")
        parser.add_argument("--file-path", help="Файл со списком url")
        parser.add_argument("--verbose", action="store_true", help="Вывод логов")
