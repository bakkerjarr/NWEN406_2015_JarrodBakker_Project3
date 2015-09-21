#
# Describes that actions that a customer makes while part of the
# system. A customer brings 0 to 5 bags with them to be processed at
# one of the check-in counters. Once checked in, the customer leaves
# the system and the bags are tracked. A customer will join the
# queue with the least number of customers.
#


class Customer:

    """
    :param id - identifier of a customer.
    """
    def __init__(self, env, id, num_bags):
        self._env = env
        self._cust_id = id
        self._num_bags = num_bags

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
    Process the customer in the Simulation.

    :param check_in_counters - a list of queues that a customer can join.
    """
    def process(self, check_in_counters):
        # Customer arrives
        time_arrive = self._env.now
        print("["+str(self._cust_id)+"] bags: " + str(self._num_bags) +
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
        print("["+str(self._cust_id)+"] Finished serving: " + str(
            time_serv))
