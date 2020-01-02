# -*- coding: utf-8 -*-

"""Online retail store manager."""

import re
import uuid

from dataclasses import dataclass,  field
from typing import Dict

from models.model import Model


@dataclass(eq=False)
class Store(Model):
    """Represents an online retailer.

    Attributes:
        name: The store's name.
        domain: The store's website domain.
        html_tag_name: The name of the HTML tag enclosing the price.
        html_tag_attributes: The attributes of the HTML tag enclosing the price.
    """

    name: str
    domain: str
    html_tag_name: str
    html_tag_attributes: Dict
    _db_collection: str = field(init=False, default='stores')
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return {
            '_id': self._id,
            'name': self.name,
            'domain': self.domain,
            'html_tag_name': self.html_tag_name,
            'html_tag_attributes': self.html_tag_attributes,
        }

    @classmethod
    def find_by_name(cls, name: str) -> "Store":
        """Finds a store in the database."""
        return cls.find_one('name', name)

    @classmethod
    def find_by_domain(cls, domain: str) -> "Store":
        """Finds a store in the database."""
        regex = {'$regex': '^{}'.format(domain)}
        return cls.find_one('domain', regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Store":
        """Finds a store in the database."""
        pattern = re.compile(r'(https?://.*?/)')
        return cls.find_by_domain(pattern.search().group(1))