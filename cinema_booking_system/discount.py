import abc
from abc import ABCMeta
from enum import Enum
import datetime
from typing import NoReturn

from cinema_booking_system.money import Money
from cinema_booking_system.movie import Movie
from cinema_booking_system.screening import Screening
from cinema_booking_system.utils import compare_to


class MovieType(Enum):
    AMOUNT_DISCOUNT = 0
    PERCENT_DISCOUNT = 1
    NONE_DISCOUNT = 2


class DiscountConditionType(Enum):
    SEQUENCE = 0
    PERIOD = 1


class DiscountPolicy(metaclass=ABCMeta):
    conditions = []

    def discount_policy(self, conditions):
        self.conditions = conditions

    def calculate_discount_amount(self, screening: Screening):
        for condition in self.conditions:
            if condition.is_satisfied_by(screening):
                return self.get_discount_amount(screening)
        return Money.ZERO

    @abc.abstractmethod
    def get_discount_amount(self, screening):
        raise NotImplementedError()


class DiscountCondition(metaclass=ABCMeta):
    type: DiscountConditionType
    sequence: int
    day_of_week: datetime
    start_time: datetime
    end_time: datetime

    def period_condition(self, day_of_week, start_time, end_time) -> NoReturn:
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time

    @abc.abstractmethod
    def is_satisfied_by(self, screening: Screening) -> bool:
        raise NotImplementedError()


class PeriodCondition(DiscountCondition):
    def is_satisfied_by(self, screening: Screening) -> bool:
        pass


class SequenceCondition(DiscountCondition):
    def __init__(self, sequence: int):
        self._sequence: int = sequence

    def is_satisfied_by(self, screening: Screening):
        return screening.is_sequence(self._sequence)


class AmountDiscountMovie(Movie):
    def __init__(self, title, running_time, fee, discount_amount, discount_condition):
        super().__init__(title, running_time, fee, discount_condition)
        self._discount_amount: Money = discount_amount

    def _calculate_discount_amount(self):
        return self._discount_amount


class PercentDiscountMovie(Movie):
    def __init__(self, title, running_time, fee, percent, discount_conditions):
        super().__init__(title, running_time, fee, discount_conditions)
        self._percent: Money = percent

    def calculate_movie_fee(self, screening: Screening) -> Money:
        return self.get_fee().times(self._percent)


class NoneDiscountPolicy(DiscountPolicy):
    def get_discount_amount(self, screening):
        return Money.ZERO


class PeriodCondition(DiscountCondition):
    def __init__(self, day_of_week, start_time, end_time):
        self._day_of_week: datetime = day_of_week
        self._start_time: datetime = start_time
        self._end_time: datetime = end_time

    def is_satisfied_by(self, screening) -> bool:
        # if screening time is between start time and end time than return true
        if screening.get_start_time().get_day_of_week() == self._day_of_week:
            if compare_to(self._start_time, self._end_time) <= 0:
                return True
            else:
                return False


class AmountDiscountPolicy(DiscountPolicy):
    def __init__(self):
        self._discount_amount = Money

    def amount_discount_policy(self, discount_amount, conditions):
        self._discount_amount = discount_amount

    def get_discount_amount(self, screening: Screening):
        return self._discount_amount


class PercentDiscountPolicy(DiscountPolicy):
    def __init__(self):
        self._percent = 0

    def percent_discount_policy(self, percent, conditions):
        self._percent = percent

    def get_discount_amount(self, screening):
        return screening.get_movie_fee().times(self._percent)
