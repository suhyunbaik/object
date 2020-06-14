class Invitation(object):
    def __init__(self):
        self._when = None


class Ticket(object):
    def __init__(self):
        self._fee = 0

    def get_fee(self):
        return self._fee


class Bag(object):
    def __init__(self, invitation=None, amount=None):
        self._amount = amount
        self._invitation = invitation
        self._ticket = Ticket

    def has_invitation(self):
        return self._invitation is not None

    def __set_ticket(self, ticket):
        self._ticket = ticket

    def __minus_amount(self, amount):
        self._amount -= amount

    def __plus_amount(self, amount):
        self._amount += amount

    def hold(self, ticket):
        if self.has_invitation():
            self.__set_ticket(ticket)
            return 0
        else:
            self.__set_ticket(ticket)
            self.__minus_amount(ticket.get_fee())
            return self._ticket.get_fee()


class Audience(object):
    def __init__(self):
        self._bag = Bag

    def audience(self, bag):
        self._bag = bag

    def get_bag(self):
        return self._bag

    def buy(self, ticket):
        return self._bag.hold(ticket)


class TicketOffice(object):
    def __init__(self):
        self._amount = 0
        self._tickets = []

    def __get_ticket(self):
        return self._tickets.pop(0)

    def __minus_amount(self, amount):
        self._amount -= amount

    def __plus_amount(self, amount):
        self._amount += amount

    def sell_ticket_to(self, audience):
        self.__plus_amount(audience.buy(self.__get_ticket))


class TicketSeller(object):
    def __init__(self, ticket_office=None):
        self._ticket_office = ticket_office

    def sell_to(self, audience):
        self._ticket_office.sell_ticket_to(audience)


class Theater(object):
    def __init__(self, ticket_seller=None):
        self._ticket_seller = ticket_seller

    def enter(self, audience):
        self._ticket_seller.sell_to(audience)
