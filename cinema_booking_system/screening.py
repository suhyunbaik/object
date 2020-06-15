from cinema_booking_system.movies import Movie
from cinema_booking_system.reservation import Reservation


class Screening(object):
    def __init__(self, movie: Movie, sequence: int, when_screened):
        self._movie: Movie = movie
        self._sequence: int = sequence
        self._when_screened = when_screened

    def get_start_time(self):
        return self._when_screened

    def is_sequence(self, sequence):
        return self._sequence == sequence

    def get_movie_fee(self):
        return self._movie.get_fee()

    def __calculate_fee(self, audience_count: int):
        return self._movie.calculate_movie_fee().times(audience_count)

    def reserve(self, customer, audience_count: int):
        return Reservation(customer, self, self.__calculate_fee(audience_count), audience_count)

    def get_when_screened(self):
        return self._when_screened

    def get_sequence(self):
        return self._sequence
