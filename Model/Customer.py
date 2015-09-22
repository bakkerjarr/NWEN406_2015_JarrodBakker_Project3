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
        return 30 + 15*self._num_bags

    """
    Process the customer in the simulation.

    :param check_in_counters - a list of queues that a customer can join.
    """
    def process(self, check_in_counters, equipment_area_queue,
                security_check_queue):
        # Customer arrives
        time_arrive = self._env.now
        print("[Customer "+str(self._cust_id)+"]\tbags: " + str(
            self._num_bags) +
              ",\tArrival time: " + str(time_arrive))

        # Customer chooses the first queue with the shortest length
        queue_lengths = ([self._len_queue(check_in_counters[i]) for i in
                          range(len(check_in_counters))])
        min_length = min(queue_lengths)
        chosen_counter = (check_in_counters[queue_lengths.index(
            min_length)])

        # Customer gets served
        service_time = self._service_time()
        request = chosen_counter.request()
        yield request
        yield self._env.timeout(service_time)
        chosen_counter.release(request)
        time_serv = self._env.now
        print("[Customer "+str(self._cust_id)+"]\tFinished serving: " +
              str(
            time_serv))
        # The customer has been served and their bags (if any exist) are
        # put on the conveyor.
        ### Create self._num_bags bags and number them
        for i in range(1, self._num_bags+1):
            bag = Bag(self._env, self._cust_id, i, self._random)
            self._env.process(bag.process(equipment_area_queue,
                                          security_check_queue))
