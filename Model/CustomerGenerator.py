#
# Generate customers using an Exponential distribution with lambda set
# to rate. Once generated, a customer joins a queue for a check-in
# counter.
#

from Customer import Customer
import random
import simpy


class CustomerGenerator:

    _PROB_FOUR_FIVE_BAGS = 0.01
    _PROB_THREE_BAGS = 0.03
    _PROB_ZERO_TWO_BAGS = 0.15

    """
    Initialise the customer generator.

    :param env - SimPy environment.
    :param rate - parameter for the exponential distribution.
    :param max_cust - maximum number of customers that will be simulated.
    :param num_check_in - number of check-in counters.
    :param rand_seed - seed for the pseudorandom number generator.
    """
    def __init__(self, env, rate, max_cust, check_in_counters,
                 equipment_area_queue, security_check_queue, rand_seed):
        random.seed(rand_seed)
        self._env = env
        self._rate = rate
        self._check_in_counters = check_in_counters
        self._equipment_area_queue = equipment_area_queue
        self._secuirty_check_queue = security_check_queue
        self._max_cust = max_cust

    """
    Use a uniformly distributed random number in the range [0.0, 1.0)
    to work out the number of bags that a customer is checking in.

    :return - the number of bags.
    """
    def _calc_bags(self):
        prob = random.random()
        if prob < self._PROB_FOUR_FIVE_BAGS:
            # could either be 4 or 5 bags
            prob = random.random()
            if prob < 0.5:
                return 4
            else:
                return 5
        if prob < self._PROB_THREE_BAGS:
            return 3
        if prob < self._PROB_ZERO_TWO_BAGS:
            # could either be 0 or 2 bags
            prob = random.random()
            if prob < 0.5:
                return 0
            else:
                return 2
        return 1  # probability of 1 bag is 0.65

    """
    Generates customers with exponentially distributed interarrival
    times.
    """
    def source(self):
        num_cust = 0
        for i in range(self._max_cust):
            num_bags = self._calc_bags()
            cust = Customer(self._env, str(num_cust), num_bags, random)
            self._env.process(cust.process(self._check_in_counters,
                                           self._equipment_area_queue,
                                           self._secuirty_check_queue))
            num_cust += 1
            interarrival_time = random.expovariate(1.0/self._rate)
            yield self._env.timeout(interarrival_time)
