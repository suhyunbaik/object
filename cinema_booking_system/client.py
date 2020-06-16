from cinema_booking_system.discount import AmountDiscountPolicy
from cinema_booking_system.movie import Movie


class Client(object):
    def __init__(self, factory):
        self.__factory = factory

    def create_avatar_movie(self):
        return Movie('title', 120, 1000, AmountDiscountPolicy())

    def get_avatar_fee(self):
        avatar = self.__factory.create_avatar_movie()
        return avatar.get_fee()

