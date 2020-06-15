from cinema_booking_system.audience import Audience


class TickerSeller(object):
    def __init__(self, ticket_office=None):
        self.__ticket_office = ticket_office

    def sell_to(self, audience):
        self.__ticket_office.sell_ticket_to(audience)

    def set_ticket(self, audience):
        if audience.get_bag().has_invitation():
            ticket = self.__ticket_office.get_ticket()
            audience.get_bag().set_ticket(ticket)
        else:
            ticket = self.__ticket_office.get_ticket()
            audience.get_bag().minus_amount(ticket.get_fee())
            self.__ticket_office.plus_amount(ticket.get_fee())
            audience.get_bag().set_ticket(ticket)


class Theater(object):
    def __init__(self, ticket_seller: TickerSeller):
        self.__ticket_seller = ticket_seller

    def enter(self, audience: Audience):
        self.__ticket_seller.set_ticket(audience)
