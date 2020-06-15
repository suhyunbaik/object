from cinema_booking_system.utils import compare_to


class Money(object):
    ZERO = 0

    def __init__(self, amount):
        self.__amount = amount

    def wons(self, amount: int):
        return Money(amount)

    def plus(self, amount):
        return self.__amount.__add__(amount)

    def minus(self, amount):
        return self.__amount.__sub__(amount)

    def times(self, percent):
        return self.__amount.__mul__(percent)

    def is_less_than(self, other):
        return compare_to(self.__amount, other.amount) < 0

    def is_greater_than_or_equal(self, other):
        return compare_to(self.__amount, other.amount) >= 0
