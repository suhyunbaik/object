from cinema_booking_system.money import Money
from cinema_booking_system.screening import Screening


class Reservation(object):
    def __init__(self, customer, screening, fee, audience_count):
        self._customer: Customer = customer
        self._screening: Screening = screening
        self._fee: Money = fee
        self._audience_count: int = audience_count
