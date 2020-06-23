import abc
import datetime
from abc import ABC
from enum import Enum

from cinema_booking_system.money import Money


class Call(object):
    def __init__(self, _from, _to):
        self.__from: datetime = _from
        self.__to: datetime = _to

    @property
    def duration(self):
        duration = self.__to - self.__from
        return duration

    @property
    def _from(self):
        return self.__from

    @property
    def _to(self):
        return self.__to


class PhoneType(Enum):
    REGULAR = 'regular'
    NIGHTLY = 'nightly'


class AbstractPhone(metaclass=ABC):
    def __init__(self, tax_rate=None):
        self.__calls: [Call] = []
        self.__tax_rate: float = tax_rate

    @property
    def tax_rate(self):
        return self.__tax_rate

    @tax_rate.setter
    def tax_rate(self, arg):
        self.__tax_rate = arg

    def calculate_fee(self) -> Money:
        result = Money.ZERO

        for call in self.__calls:
            result += self.calculate_call_fee(call)
        return result + (result * self.__tax_rate)

    @abc.abstractmethod
    def calculate_call_fee(self, call: Call):
        NotImplementedError()


class RegularPhone(AbstractPhone):
    LATE_NIGHT_HOUR = 22

    def __init__(self, amount=None, seconds=None, tax_rate=None):
        super().__init__(tax_rate)
        self.__calls: [Call] = []
        self.__amount: Money = amount
        self.__seconds: datetime = seconds

    @property
    def call(self):
        return self.__calls

    @call.setter
    def call(self, arg):
        self.__calls.append(arg)

    @property
    def amount(self):
        return self.__amount

    @property
    def seconds(self):
        return self.__seconds

    @seconds.setter
    def seconds(self, arg):
        self.__seconds = arg

    def calculate_call_fee(self, call: Call) -> Money:
        return self.__amount.times(call.duration.total_seconds() / self.__seconds.total_seconds())


class NightlyDiscountPhone(AbstractPhone):
    LATE_NIGHT_HOUR = 22

    def __init__(self, regular_amount=None, nightly_amount=None, seconds=None, tax_rate=None):
        super().__init__(tax_rate)
        self.__regular_amount: int = regular_amount
        self.__nightly_amount: int = nightly_amount
        self.__seconds: datetime = seconds

    @property
    def seconds(self):
        return self.__seconds

    @seconds.setter
    def seconds(self, arg):
        self.__seconds = arg

    @property
    def nightly_amount(self):
        return self.__nightly_amount

    @nightly_amount.setter
    def nightly_amount(self, arg):
        self.__nightly_amount = arg

    @property
    def regular_amount(self):
        return self.__regular_amount

    @regular_amount.setter
    def regular_amount(self, arg):
        self.__regular_amount = arg

    def calculate_call_fee(self, call: Call) -> Money:
        if call.__from.hour() >= self.LATE_NIGHT_HOUR:
            return self.__nightly_amount.times(call.duration.total_seconds() / self.__seconds.total_seconds())
        else:
            return self.__regular_amount.times(call.duration.total_seconds() / self.__seconds.total_seconds())


if __name__ == '__main__':
    money = Money()
    money.wons = 5

    phone = Phone(money, datetime.timedelta(seconds=10))
    phone.call = Call(datetime.datetime(2018, 1, 1, 12, 10, 0), datetime.datetime(2018, 1, 1, 12, 11, 0))
    phone.call = Call(datetime.datetime(2018, 1, 2, 12, 10, 0), datetime.datetime(2018, 1, 2, 12, 11, 0))
    print(phone.calculate_fee())
