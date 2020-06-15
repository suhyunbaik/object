from typing import NoReturn

from cinema_booking_system.ticket_box_system import Ticket


class Bag(object):
    def __init__(self, ticket, invitation=None, amount=None):
        self.__amount = amount
        self.__invitation = invitation
        self.__ticket: Ticket = ticket

    def __has_invitation(self) -> bool:
        return self.__invitation is not None

    @property
    def ticket(self):
        return self.__ticket

    @ticket.setter
    def ticket(self, arg: Ticket) -> NoReturn:
        self.__ticket = arg

    def __minus_amount(self, amount) -> NoReturn:
        self.__amount -= amount

    def __plus_amount(self, amount) -> NoReturn:
        self.__amount += amount

    def hold(self, ticket: Ticket) -> int:
        if self.__has_invitation():
            self.ticket(ticket)
            return 0
        else:
            self.ticket(ticket)
            self.__minus_amount(ticket.get_fee())
            return self.__ticket.get_fee()
