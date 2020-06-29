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
    AMOUNT_DISCOUNT = 'amount_discount'
    PERCENT_DISCOUNT = 'percent_discount'
    NONE_DISCOUNT = 'none_discount'


class DiscountConditionType(Enum):
    SEQUENCE = 'sequence'
    PERIOD = 'period'


class DiscountPolicy(metaclass=ABCMeta):

    @property
    def conditions(self):
        return self._conditions

    @conditions.setter
    def conditions(self, arg: [DiscountCondition]):
        self._conditions = arg

    @staticmethod
    def __check_precondition(screening: Screening) -> NoReturn:
        assert screening is not None, screening.get_start_time() >= datetime.datetime.now()

    @staticmethod
    def __check_postcondition(amount: Money) -> NoReturn:
        assert amount is not None, amount.is_greater_than_or_equal(Money.ZERO)

    def calculate_discount_amount(self, screening: Screening):
        self.__check_precondition(screening)

        amount = Money.ZERO
        for condition in self.conditions:
            if condition.is_satisfied_by(screening):
                self.__check_postcondition(amount)
                return amount
        amount = screening.get_movie_fee()
        self.__check_postcondition(amount)
        return amount

    def switch_conditions(self, conditions) -> NoReturn:
        self.conditions = conditions

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
    def get_discount_amount(self, screening: Screening):
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


class OverlappedDiscountPolicy(DiscountPolicy):
    def __init__(self, discount_policies):
        self.__discount_policies: [DiscountPolicy] = discount_policies

    def get_discount_amount(self, screening):
        result = Money.ZERO
        for _ in self.__discount_policies:
            result = result.__add__(_.calculate_discount_amount(screening))
        return result
