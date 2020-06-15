class Invitation(object):
    def __init__(self):
        self._when = None


class Ticket(object):
    def __init__(self):
        self.__fee = 0

    @property
    def fee(self):
        return self.__fee


class TicketOffice(object):
    def __init__(self):
        self.__amount = 0
        self.__tickets = []

    @property
    def ticket(self):
        return self.__tickets.pop(0)

    def __minus_amount(self, amount):
        self.__amount -= amount

    def __plus_amount(self, amount):
        self.__amount += amount

    def sell_ticket_to(self, audience):
        self.__plus_amount(audience.buy(self.ticket))
