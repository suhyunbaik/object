from cinema_booking_system.discount import DiscountConditionType, DiscountCondition
from cinema_booking_system.money import Money
from cinema_booking_system.screening import Screening
from cinema_booking_system.utils import compare_to


class Customer(object):
    def customer(self):
        pass


class Reservation(object):
    def __init__(self, customer, screening, fee, audience_count):
        self.__customer: Customer = customer
        self.__screening: Screening = screening
        self.__fee: Money = fee
        self.__audience_count: int = audience_count


class ReservationAgency(object):

    def reserve(self, screening, customer, audience_count):
        fee = screening.calculate_fee(audience_count)
        return Reservation(Customer, screening, fee, audience_count)

    def check_discountable(self, screening: Screening) -> bool:
        # return screening.get_movie().get_discount_conditions().stream().anymatch(
        #     condition -> condition.is_discountable(screening))
        pass
