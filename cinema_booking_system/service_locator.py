class ServiceLocator(object):
    def __init__(self):
        self.__sole_instance = ServiceLocator()
        self.__discount_policy = None

    @property
    def discount_policy(self):
        return self.__discount_policy

    @discount_policy.setter
    def discount_policy(self, arg):
        self.__discount_policy = arg

    def provide(self, discount_policy):
        self.__sole_instance.discount_policy = discount_policy
