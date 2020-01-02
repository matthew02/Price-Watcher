# -*- coding: utf-8 -*-

"""Retail website item manager."""

import re
import uuid
import requests

from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import Dict

from models.model import Model


@dataclass(eq=False)
class Item(Model):
    """An item for sale on a retail website.

    Attributes:
        url: The url where the item is located.
        html_tag_name: The html tag enclosing the price.
        html_tag_attributes: The attributes of the HTML tag enclosing the price.
        price: The item's most recent price.
    """

    url: str
    html_tag_name: str
    html_tag_attributes: Dict
    price: float = field(default=None)
    _db_collection: str = field(init=False, default='items')
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def fetch_price(self) -> float:
        """Fetches the current price of the item from the website."""
        response = requests.get(self.url)
        content = response.content

        soup = BeautifulSoup(content, 'html.parser')
        element = soup.find(self.html_tag_name, self.html_tag_attributes)

        self.price = self.parse_price(element.text)

        return self.price

    def json(self) -> Dict:
        return {
            '_id': self._id,
            'url': self.url,
            'html_tag_name': self.html_tag_name,
            'html_tag_attributes': self.html_tag_attributes,
            'price': self.price,
        }

    @staticmethod
    def parse_price(element: str) -> float:
        """Extracts a price from a string."""
        pattern = re.compile(r'(\d*,?\d+\.\d{2})')
        match = pattern.search(element)
        return float(match.group(1).replace(',', ''))
