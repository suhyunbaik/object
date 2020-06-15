class Invitation(object):
    def __init__(self):
        self._when = None


class Ticket(object):
    def __init__(self):
        self._fee = 0

    def get_fee(self):
        return self._fee


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
