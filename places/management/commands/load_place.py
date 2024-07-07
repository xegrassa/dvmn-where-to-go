import logging
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import requests
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from pydantic import BaseModel
from requests import Response
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

from places.models import Place


class Coordinate(BaseModel):
    lng: float
    lat: float


class PlaceSchema(BaseModel):
    title: str
    description_short: str
    description_long: str
    imgs: list[str]
    coordinates: Coordinate


logger = logging.getLogger(__name__)


def download_json(url: str) -> Response | None:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.debug(f"Не удалось скачать {url}: {e}")
        return None

    return response


def download_image(url, idx: int = 0) -> tuple[int, str, bytes] | None:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.debug(f"Не удалось скачать {url}: {e}")
        return None

    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    return idx, file_name, response.content


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

        urls = []
        if options["file_path"]:
            with open(options["file_path"]) as f:
                for line in f:
                    urls.append(line.strip())
        if options["urls"]:
            for url in options["urls"]:
                urls.append(url)

        debug_message = "\n".join(urls)
        logger.debug(f"Кол-во ссылок на json: {len(urls)}\n {debug_message}")

        responses = thread_map(download_json, urls, max_workers=options["thread_count"], desc="Downloading json files")
        places_dto = [PlaceSchema(**r.json()) for r in responses if r]
        logger.debug(f"Успешно скачанных json: {len(places_dto)}")

        image_results = []
        with ThreadPoolExecutor(options["thread_count"]) as executor:
            futures = []
            for idx, place in enumerate(places_dto):
                futures.extend([executor.submit(download_image, url, idx) for url in place.imgs])

            for future in tqdm(futures, desc="Downloading images", unit="file"):
                image_results.append(future.result())

        d = defaultdict(list)
        for img in image_results:
            idx, file_name, content = img
            d[idx].append((file_name, content))

        for idx, p in enumerate(places_dto):
            p_obj = Place.objects.create(
                title=p.title,
                description_short=p.description_short,
                description_long=p.description_long,
                longitude=p.coordinates.lng,
                latitude=p.coordinates.lat,
            )

            for images in d[idx]:
                file_name, content = images

                p_obj.image_set.create(image=ImageFile(ContentFile(content, name=file_name)))

    def add_arguments(self, parser):
        parser.add_argument("--urls", nargs="+", help="URLS до json файлов")
        parser.add_argument("--thread-count", type=int, default=6, help="Кол-во потоков для скачивания")
        parser.add_argument("--file-path", help="Файл со списком url")
        parser.add_argument("--verbose", action="store_true", help="Вывод логов")
