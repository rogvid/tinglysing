#!/usr/bin/env python
"""Code for the Register class.

The Register class handles download, parsing, and registration
of property sales.
"""

import logging
import os
import re

import browser_cookie3 as bc3
import requests
import datetime
import httpx
from bs4 import BeautifulSoup
from dotenv import find_dotenv, load_dotenv
import pathlib

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

# Swap out file register with database


class Register:
    _cadastres: Dict[int, Dict[str, str]]

    def __init__(self, url, dpath):
        logger.info("Initializing register")
        self.url = url
        self.dpath = dpath
        if not isinstance(self.dpath, pathlib.Path):
            self.dpath = pathlib.Path(self.dpath)
        if not self.dpath.exists():
            raise FileNotFoundError(f"No files or folder found at '{dpath}'")
        self._raw = self.dpath / "raw"
        self._interim = self.dpath / "interim"
        self._processed = self.dpath / "processed"
        self._cadastres = {
            f.stem: {
                "fpath": f,
                "mtime": datetime.datetime.fromtimestamp(
                    f.stat().st_mtime, tz=datetime.timezone.utc
                ),
            }
            for f in self._raw.glob("*.txt")
        }
        logger.info(f"Register contains {len(self._cadastres)} cadastral registrations")

    @property
    def cadastres(self):
        return self._cadastres


async def main():
    async with httpx.AsyncClient() as client:
        for number in range(1, 151):
            pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{number}"

            resp = await client.get(pokemon_url)
            pokemon = resp.json()
            print(pokemon["name"])

    async def get_html(client, url):
        resp = await client.get(url, cookies=bc3.firefox())
        resp.json()

    async def sync(self, update=False):
        """Synchronize with Tinglysing."""
        logger.debug("Syncing with online register...")
        async with httpx.AsyncClient() as client:
            for index in range(100000):
                if not (update or (index not in self.cadastres)):
                    continue

                url = self.url + f"/{str(index)}"
                await client.get(url, cookies=bc3.firefox())
            return html_doc
        return None

    def registrate(self, registration_id) -> bool:
        reg = self.download_registration(registration_id)
        # If the session expired, then we need to re download the registration
        if self.is_error(reg):
            return False
        if self.is_logged_in(reg):
            reg = self.download_registration(registration_id)
        if reg is not None:
            self.save(reg, registration_id)
            self.update()
            return True
        else:
            return False
        for index in range(72001):
            if index in self.indices:
                continue
            else:
                _ = self.registrate(index)
                if index % 1000 == 0:
                    print(f"Finished registering {index}")

    def is_error(self, html_doc):
        if "an error occured while processing your request" in html_doc:
            return True
        else:
            return False

    def is_logged_in(self, html_doc):
        soup = BeautifulSoup(html_doc, "html.parser")
        if len(soup.find_all("a", attrs={"href": re.compile(".*RitaInn.*")})) > 0:
            input("You need to login again...")
            return False
        else:
            return True

    def load(self, registration_id):
        logger.debug(f"Loading registration {registration_id}...")
        if registration_id not in self.indices:
            raise KeyError(
                f"No registration found for {str(registration_id)} in register"
            )
        with open(
            os.path.join(self.path, f"{str(registration_id)}.txt"), "r"
        ) as fhandle:
            html_doc = fhandle.read()
            return html_doc

    def save(self, registration, registration_id):
        logger.debug(f"Saving registration {registration_id} to file...")
        with open(
            os.path.join(self.path, f"{str(registration_id)}.txt"), "w"
        ) as fhandle:
            fhandle.write(registration)

    def download_registration(self, registration_id, force=False):
        if force or (registration_id not in self.indices):
            html_doc = requests.get(
                self.url + f"/{str(registration_id)}", cookies=bc3.firefox()
            ).text
            return html_doc
        return None

    def registrate(self, registration_id) -> bool:
        reg = self.download_registration(registration_id)
        # If the session expired, then we need to re download the registration
        if self.is_error(reg):
            return False
        if self.is_logged_in(reg):
            reg = self.download_registration(registration_id)
        if reg is not None:
            self.save(reg, registration_id)
            self.update()
            return True
        else:
            return False

    def parse_registration(html_doc):
        relevant_divs = soup.find_all("div", attrs={"class": "result-container"})[0]
        return relevant_divs
