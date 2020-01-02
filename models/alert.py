# -*- coding: utf-8 -*-

"""Alert management."""

import uuid

from dataclasses import dataclass,  field
from typing import Dict

from libs.mailgun import Mailgun
from models.item import Item
from models.model import Model
from models.user.user import User


@dataclass(eq=False)
class Alert(Model):
    """A conditional alert for when an item's price reaches a target.

    Attributes:
        item_name: The name of the item.
        item_id: The unique identifier of the item.
        price_floor: The price threshold, below which the alert triggers.
        user_email: The email address of the user to whom this alert belongs.
    """

    item_name: str
    item_id: str
    price_floor: float
    user_email: str
    _db_collection: str = field(init=False, default='alerts')
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self) -> None:
        self.item = Item.fetch_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def fetch_item_price(self) -> float:
        """Fetches the current price of the item."""
        return self.item.fetch_price()

    def notify_if_price_reached(self) -> None:
        """Sends a notification if the target price is reached."""
        if self.item.price < self.price_floor:
            print(f'Item {self.item} has reached a price below '
                  f'{self.price_floor}.\n Latest price: {self.item.price}.')
            Mailgun.send_mail(['jamesbulk@gmail.com'], 'Test Subj',
                              'This is a test.', '<p>This is an HTML test.</p>')

    def json(self) -> Dict:
        return {
            '_id': self._id,
            'item_name': self.item_name,
            'item_id': self.item_id,
            'price_limit': self.price_floor,
            'user_email': self.user_email,
        }
