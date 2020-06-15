import abc
from abc import ABCMeta
from enum import Enum
import datetime
from typing import NoReturn

from cinema_booking_system.utils import compare_to


class Money(object):
    ZERO = 0

    def __init__(self, amount):
        self._amount = amount

    def wons(self, amount):
        return Money(amount)

    def plus(self, amount):
        return self._amount.__add__(amount)

    def minus(self, amount):
        return self._amount.__sub__(amount)

    def times(self, percent):
        return self._amount.__mul__(percent)

    def is_less_than(self, other):
        return compare_to(self._amount, other.amount) < 0

    def is_greater_than_or_equal(self, other):
        return compare_to(self._amount, other.amount) >= 0
