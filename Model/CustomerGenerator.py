#
# Generate customers using an Exponential distribution with lambda set
# to ft.
#

from Customer import Customer
import random


class CustomerGenerator:

    """
    @param rate - parameter for the exponential distribution.
    """
    def __init__(self, env, rate, max_cust):
        random.seed(999)
        self.env = env
        self.rate = rate
        self.max_cust = max_cust

    """
    Use a uniformly distributed random number in the range [0.0, 1.0)
    to work out the number of bags that a customer is checking in.

    @return - the number of bags.
    """
    def _calc_bags(self):
        prob = random.random()
        if prob < 0.01:
            # could either be 4 or 5 bags
            prob = random.random()
            if prob < 0.5:
                return 4
            else:
                return 5
        if prob < 0.03:
            return 3
        if prob < 0.15:
            # could either be 0 or 2 bags
            prob = random.random()
            if prob < 0.5:
                return 0
            else:
                return 2
        return 1

    def source(self):
        num_cust = 0
        for i in range(self.max_cust):
            num_bags = self._calc_bags()
            cust = Customer(self.env, str(num_cust), num_bags)
            self.env.process(cust.process())
            num_cust += 1
            interarrival_time = random.expovariate(1.0/self.rate)
            yield self.env.timeout(interarrival_time)
