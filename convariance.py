from typing import NoReturn


class Publisher(object):
    def __init__(self):
        pass


class IndependentPublisher(Publisher):
    def __init__(self):
        super().__init__()


class Book(object):
    def __init__(self, publisher: Publisher):
        self.__publisher = publisher


class Magazine(Book):
    def __init__(self, publisher: Publisher):
        super().__init__(publisher)


class BookStall(object):
    def sell(self, independent_publisher: IndependentPublisher) -> Book:
        return Book(independent_publisher)


class MagazineStore(BookStall):
    def sell(self, independent_publisher: IndependentPublisher) -> Book:
        return Magazine(independent_publisher)


class Customer(object):
    def __init__(self, book=None):
        self.__book: Book = book

    def order(self, bookstall: BookStall) -> NoReturn:
        self.__book = bookstall.sell(IndependentPublisher())


if __name__ == '__main__':
    customer = Customer().order(BookStall())
    customers = Customer().order(MagazineStore())
    print(customer, customers)
