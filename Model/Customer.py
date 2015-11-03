__author__ = 'Jarrod N. Bakker'

#
# Describes that actions that a customer makes while part of the
# system. A customer brings 0 to 5 bags with them to be processed at
# one of the check-in counters. Once checked in, the customer leaves
# the system and the bags are tracked. A customer will join the
# queue with the least number of customers.
#

from Bag import Bag


class Customer:

    """
    Initialise a customer.

    :param env - SimPy environment.
    :param id - identifier of a customer.
    :param num_bags - number of bags that this customer is checking in.
    :param random - pseudorandom number generator used by the model.
    """
    def __init__(self, env, id, num_bags, random):
        self._env = env
        self._cust_id = id
        self._num_bags = num_bags
        self._random = random

    """
    Determine the number of customers currently in a check-in queue.
    This is the sum of the number of customers waiting in the queue
    and the number of customers currently being served by the queue.

    :param queue - a queue.
    :return - the length of the queue.
    """
    def _len_queue(self, queue):
        return len(queue.queue) + queue.count

    """
    Calculate how long a customer will be queued for. This is
    dependent on the number of bags that a customer is checking in.
    """
    def _service_time(self):
        # return 30 + 15*self._num_bags  # original
        return 10 + 5*self._num_bags

    """
    Process the customer in the simulation.

    :param check_in_counters - a list of queues that a customer can join.
    :param equipment_area_queue - bags are queued here so that they
                                  may be loaded onto their appropriate
                                  planes.
    :param security_check_queue - bags are queued here before
                                  receiving the additional check.
    """
    def process(self, check_in_counters, equipment_area_queue,
                security_check_queue):
        # Customer arrives and chooses the first queue with the
        # shortest length
        time_arrive = self._env.now
        queue_lengths = ([self._len_queue(check_in_counters[i]) for i in
                          range(len(check_in_counters))])
        min_length = min(queue_lengths)
        chosen_counter_id = queue_lengths.index(min_length)
        chosen_counter = (check_in_counters[chosen_counter_id])
        print("[Customer {0}]\tbags: {1},\tArrival time: {"
              "2:.4f}s\tCheck-in counter: {3}").format(self._cust_id,
                                                       self._num_bags,
                                                       time_arrive,
                                                       chosen_counter_id)

        # Customer arrives at queue for service
        service_time = self._service_time()
        request = chosen_counter.request()
        yield request
        yield self._env.timeout(service_time)
        chosen_counter.release(request)
        time_serv = self._env.now
        print("[Customer {0}]\tFinished serving: {1:.4f}s").format(
            self._cust_id, time_serv)
        # The customer has been served and their bags (if any exist) are
        # put on the conveyor.
        for i in range(1, self._num_bags+1):
            bag = Bag(self._env, self._cust_id, i, self._random)
            self._env.process(bag.process(equipment_area_queue,
                                          security_check_queue))
