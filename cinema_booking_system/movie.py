import abc
from abc import ABCMeta

from cinema_booking_system.discount import DiscountCondition
from cinema_booking_system.money import Money
from cinema_booking_system.screening import Screening


class Movie(metaclass=ABCMeta):
    def __init__(self, title, running_time, fee, discount_condition, discount_policy):
        self.__title: str = title
        self.__running_time: int = running_time
        self.__fee: Money = fee
        self.__discount_condition: [DiscountCondition] = discount_condition
        self.__discount_policy: discount_policy

    @property
    def fee(self) -> Money:
        return self.__fee

    def _is_discountable(self, screening: Screening) -> bool:
        for condition in self.__discount_condition:
            if condition.is_satisfied_by(screening):
                return True

    def calculate_movie_fee(self, screening: Screening) -> Money:
        if self._is_discountable(screening):
            return self.__fee.minus(self.__calculate_discount_amount())
        return self.__fee

    @abc.abstractmethod
    def __calculate_discount_amount(self):
        raise NotImplementedError()


class AmountDiscountMovie(Movie):
    def __init__(self, title, running_time, fee, discount_amount, discount_condition):
        super().__init__(title, running_time, fee, discount_condition)
        self.__discount_amount: Money = discount_amount

    def _calculate_discount_amount(self):
        return self.__discount_amount


class PercentDiscountMovie(Movie):
    def __init__(self, title, running_time, fee, percent, discount_conditions):
        super().__init__(title, running_time, fee, discount_conditions)
        self.__percent: Money = percent

    def calculate_movie_fee(self, screening: Screening) -> Money:
        return self.fee.times(self.__percent)
