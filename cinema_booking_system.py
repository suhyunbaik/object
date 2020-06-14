import abc
from abc import ABCMeta


class DiscountPolicy(metaclass=ABCMeta):
    conditions = []

    def discount_policy(self, conditions):
        self.conditions = conditions

    def calculate_discount_amount(self, screening):
        for condition in self.conditions:
            if condition.is_satisfied_by(screening):
                return self.get_discount_amount(screening)
        return Money.ZERO

    @abc.abstractmethod
    def get_discount_amount(self, screening):
        raise NotImplementedError()


class DiscountCondition(metaclass=ABCMeta):

    @abc.abstractmethod
    def is_satisfied_by(self, screening):
        pass


class SequenceCondition(DiscountCondition):
    def __init__(self):
        self._sequence = 0

    def sequence_condition(self, sequence):
        self._sequence = sequence

    def is_satisfied_by(self, screening):
        return screening.is_sequence(self._sequence)


class Movie(object):
    def __init__(self):
        self._title = ''
        self._running_time = 0
        self._fee = Money
        self._discount_policy = DiscountPolicy

    def movie(self, title, running_time, fee, discount_policy):
        self._title = title
        self._running_time = running_time
        self._fee = fee
        self._discount_policy = discount_policy

    def get_fee(self):
        return self._fee

    def calculate_movie_fee(self, screening):
        return self._fee.minus(self._discount_policy.calculate_discount_amount(screening))


class Screening(object):
    def __init__(self):
        self._movie = Movie
        self._sequence = 0
        self._when_screened = None

    def screening(self, movie, sequence, when_screened):
        self._movie = movie
        self._sequence = sequence
        self._when_screened = when_screened

    def get_start_time(self):
        return self._when_screened

    def is_sequence(self, sequence):
        return self._sequence == sequence

    def get_movie_fee(self):
        return self._movie.get_fee()

    def __calculate_fee(self, audience_count):
        return self._movie.calculate_movie_fee().times(audience_count)


class Money(object):
    ZERO = 0

    def __init__(self, amount):
        self._amount = amount

    def wons(self, amount):
        return Money(amount)

    def plus(self, amount):
        return self._amount.__add__(amount)

    def minus(self, amount):
        return self._amount.__sub__(amount)

    def times(self, percent):
        return self._amount.__mul__(percent)

    def is_less_than(self, other):
        return compare_to(self._amount, other.amount) < 0

    def is_greater_than_or_equal(self, other):
        return compare_to(self._amount, other.amount) >= 0


class Reservation(object):
    def __init__(self):
        self._customer = Customer
        self._screening = Screening
        self._fee = Money
        self._audience_count = 0

    def reservation(self, customer, screening, fee, audience_count):
        self._customer = customer
        self._screening = screening
        self._fee = fee
        self._audience_count = audience_count


class PeriodCondition(DiscountCondition):
    def __init__(self):
        self._day_of_week = DayOfWeek
        self._start_time = LocalTime
        self._end_time = LocalTime

    def period_condition(self, day_of_week, start_time, end_time):
        self._day_of_week = day_of_week
        self._start_time = start_time
        self._end_time = end_time

    def is_satisfied_by(self, screening):
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

    def get_discount_amount(self, screening):
        return self._discount_amount


class PercentDiscountPolicy(DiscountPolicy):
    def __init__(self):
        self._percent = 0

    def percent_discount_policy(self, percent, conditions):
        self._percent = percent

    def get_discount_amount(self, screening):
        return screening.get_movie_fee().times(self._percent)


def compare_to(foo, bar):
    if foo == bar:
        return 0
    elif foo > bar:
        return 1
    else:
        return -1
