from cinema_booking_system.utils import compare_to


class Money(object):
    ZERO = 0

    def __init__(self):
        self.__amount = 0

    @property
    def wons(self):
        return self.__amount

    @wons.setter
    def wons(self, amount):
        self.__amount = amount

    def plus(self, amount):
        return self.__amount + amount

    def minus(self, amount):
        return self.__amount - amount

    def times(self, percent):
        return self.__amount * percent

    def is_less_than(self, other):
        return compare_to(self.__amount, other.amount) < 0

    def is_greater_than_or_equal(self, other):
        return compare_to(self.__amount, other.amount) >= 0
