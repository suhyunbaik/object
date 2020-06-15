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
    __type: DiscountConditionType
    __sequence: int
    __day_of_week: datetime
    __start_time: datetime
    __end_time: datetime

    def is_discountable(self, screening) -> bool:
        if self.__type == DiscountConditionType.PERIOD:
            return self.is_satisfied_by_period(screening)
        return self.is_satisfied_by_sequence(screening)

    def is_satisfied_by(self, screening) -> bool:
        pass


class SequenceCondition(DiscountCondition):
    def __init__(self, sequence: int):
        self.__sequence: int = sequence

    def is_satisfied_by(self, screening: Screening):
        return screening.is_sequence(self.__sequence)


class AmountDiscountMovie(Movie):
    def __init__(self, title, running_time, fee, discount_amount, discount_condition):
        super().__init__(title, running_time, fee, discount_condition)
        self._discount_amount: Money = discount_amount

    def _calculate_discount_amount(self):
        return self._discount_amount


class PercentDiscountMovie(Movie):
    def __init__(self, title, running_time, fee, percent, discount_conditions):
        super().__init__(title, running_time, fee, discount_conditions)
        self.__percent: Money = percent

    def calculate_movie_fee(self, screening: Screening) -> Money:
        return self.fee.times(self.__percent)


class NoneDiscountMovie(Movie):
    def __init__(self, title, running_time, fee, discount_conditions):
        super().__init__(title, running_time, fee, discount_conditions)

    def _calculate_discount_amount(self):
        return Money.ZERO


class NoneDiscountPolicy(DiscountPolicy):
    def get_discount_amount(self, screening):
        return Money.ZERO


class PeriodCondition(DiscountCondition):
    def __init__(self, day_of_week, start_time, end_time):
        self.__day_of_week: datetime = day_of_week
        self.__start_time: datetime = start_time
        self.__end_time: datetime = end_time

    def is_satisfied_by(self, screening: Screening) -> bool:
        # if screening time is between start time and end time than return true
        if screening.get_start_time().get_day_of_week() == self.__day_of_week:
            if compare_to(self.__start_time, self.__end_time) <= 0:
                return True
            else:
                return False


class AmountDiscountPolicy(DiscountPolicy):
    def __init__(self, discount_amount):
        self.__discount_amount = discount_amount

    def get_discount_amount(self, screening: Screening):
        return self.__discount_amount


class PercentDiscountPolicy(DiscountPolicy):
    def __init__(self, percent):
        self.__percent = percent

    def get_discount_amount(self, screening):
        return screening.get_movie_fee().times(self.__percent)
