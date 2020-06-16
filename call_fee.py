import datetime

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


class Phone(object):
    def __init__(self, amount, seconds):
        self.__amount: Money = amount
        self.__seconds: datetime = seconds
        self.__calls: [] = []

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

    def calculate_fee(self):
        result = Money.ZERO

        for call in self.__calls:
            result += self.__amount.times(call.duration.total_seconds() / self.__seconds.total_seconds())

        return result


if __name__ == '__main__':
    money = Money()
    money.wons = 5

    phone = Phone(money, datetime.timedelta(seconds=10))
    phone.call = Call(datetime.datetime(2018, 1, 1, 12, 10, 0), datetime.datetime(2018, 1, 1, 12, 11, 0))
    phone.call = Call(datetime.datetime(2018, 1, 2, 12, 10, 0), datetime.datetime(2018, 1, 2, 12, 11, 0))
    print(phone.calculate_fee())
