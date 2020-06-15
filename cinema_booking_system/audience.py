from cinema_booking_system.bag import Bag
from cinema_booking_system.ticket_box_system import Ticket


class Audience(object):
    def __init__(self, bag: Bag):
        self.__bag: Bag = bag

    @property
    def get_bag(self):
        return self.__bag

    def buy(self, ticket: Ticket):
        return self.__bag.hold(ticket)

    def set_ticket(self, ticket: Ticket):
        return self.__bag.ticket(ticket)
