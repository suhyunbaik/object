from cinema_booking_system.bag import Bag
from cinema_booking_system.ticket_box_system import Ticket


class Audience(object):
    def __init__(self):
        self.__bag = None

    @property
    def bag(self):
        return self.__bag

    @bag.setter
    def bag(self, arg: Bag):
        self.__bag = arg

    def buy(self, ticket):
        if self.__bag.has_invitation():
            self.__bag.ticket(ticket)
            return 0
        else:
            self.__bag.set_ticket(ticket)
            self.__bag.minus_amount(ticket.get_fee())
            return ticket.get_fee()

    def set_ticket(self, ticket: Ticket):
        return self.__bag.ticket(ticket)
