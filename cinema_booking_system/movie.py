import abc
from abc import ABCMeta

from cinema_booking_system.discount import DiscountCondition
from cinema_booking_system.money import Money
from cinema_booking_system.screening import Screening


class Movie(metaclass=ABCMeta):
    def __init__(self, title, running_time, fee, discount_condition):
        self._title: str = title
        self._running_time: int = running_time
        self._fee: Money = fee
        self._discount_condition: [DiscountCondition] = discount_condition

    def get_fee(self):
        return self._fee

    def _is_discountable(self, screening: Screening) -> bool:
        for condition in self._discount_condition:
            if condition.is_satisfied_by(screening):
                return True

    def calculate_movie_fee(self, screening: Screening) -> Money:
        if self._is_discountable(screening):
            return self._fee.minus(self.calculate_discount_amount())
        return self._fee

    @abc.abstractmethod
    def _calculate_discount_amount(self):
        raise NotImplementedError()


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
