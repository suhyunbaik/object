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


class Phone(object):
    def __init__(self, tax_rate=None):
        self.__calls: [Call] = []
        self.__rate_policy: RatePolicy = None

    @property
    def rate_policy(self):
        return self.__rate_policy

    @rate_policy.setter
    def rate_policy(self, arg):
        self.__rate_policy = arg

    @property
    def calls(self):
        return self.__calls

    def calculate_fee(self) -> Money:
        return self.__rate_policy.calculate_fee(self)

    @abc.abstractmethod
    def calculate_call_fee(self, call: Call):
        NotImplementedError()


class RatePolicy(metaclass=ABC):
    def calculate_fee(self, phone) -> Money:
        NotImplementedError()


class AdditionalRatePolicy(RatePolicy):
    def __init__(self):
        self.__next: RatePolicy = None

    def calculate_fee(self, phone) -> Money:
        fee = self.__next.calculate_fee(phone)
        return self.after_calculated(fee)

    @abc.abstractmethod
    def after_calculated(self, fee: Money):
        NotImplementedError()


class BasicRatePolicy(RatePolicy):
    def calculate_fee(self, phone) -> Money:
        result = Money.ZERO

        for call in self.__calls:
            result.plus(self.calculate_call_fee(call))
        return result

    @abc.abstractmethod
    def calculate_call_fee(self, call: Call):
        NotImplementedError()


class FixedFeePolicy(BasicRatePolicy):
    def __init__(self, amount=None, seconds=None):
        super().__init__()
        self.__amount: Money = amount
        self.__seconds = seconds

    def calculate_call_fee(self, call: Call):
        return self.__amount.times(call.duration.total_seconds() / self.__seconds.total_seconds())


class NightlyDiscountPolicy(BasicRatePolicy):
    LATE_NIGHT_HOUR = 22

    def __init__(self, nightly_amount=None, regular_amount=None, seconds=None):
        super().__init__()
        self.__nightly_amount: Money = nightly_amount
        self.__regular_amount: Money = regular_amount
        self.__seconds = seconds

    def calculate_call_fee(self, call: Call):
        if call.__from.hours() >= self.LATE_NIGHT_HOUR:
            return self.__nightly_amount.times(call.duration.total_seconds() / self.__seconds.total_seconds())
        return self.__regular_amount.times(call.duration.total_seconds() / self.__seconds.total_seconds())


class TaxablePolicy(AdditionalRatePolicy):
    def __init__(self, tax_ratio, _next):
        super().__init__()
        self.__tax_ratio: float = tax_ratio

    def after_calculated(self, fee: Money):
        return fee.plus(fee.times(self.__tax_ratio))


class RateDiscountablePolicy(AdditionalRatePolicy):
    def __init__(self, discount_amount, _next):
        super().__init__()
        self.__discount_amount: Money = discount_amount

    def after_calculated(self, fee: Money):
        return fee.minus(self.__discount_amount)


if __name__ == '__main__':
    money = Money()
    money.wons = 10


    # phone = Phone(money, datetime.timedelta(seconds=10))
    # phone.call = Call(datetime.datetime(2018, 1, 1, 12, 10, 0), datetime.datetime(2018, 1, 1, 12, 11, 0))
    # phone.call = Call(datetime.datetime(2018, 1, 2, 12, 10, 0), datetime.datetime(2018, 1, 2, 12, 11, 0))
    # print(phone.calculate_fee())
