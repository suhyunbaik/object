from cinema_booking_system.movie import Movie
from cinema_booking_system.reservation import Reservation


class Screening(object):
    def __init__(self, movie: Movie, sequence: int, when_screened):
        self.__movie: Movie = movie
        self.__sequence: int = sequence
        self.__when_screened = when_screened

    def get_start_time(self):
        return self.__when_screened

    def is_sequence(self, sequence):
        return self.__sequence == sequence

    def get_movie_fee(self):
        return self.__movie.fee

    def __calculate_fee(self, audience_count: int):
        return self.__movie.calculate_movie_fee().times(audience_count)

    def reserve(self, customer, audience_count: int):
        return Reservation(customer, self, self.__calculate_fee(audience_count), audience_count)

    def get_when_screened(self):
        return self.__when_screened

    def get_sequence(self):
        return self.__sequence
