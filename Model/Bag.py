__author__ = 'Jarrod N. Bakker'

#
# Describes the actions that are performed upon a bag while it is in
# the system. The bag moves along a conveyor and gets processed at
# various points.
#
# Note the following details:
#   - Conveyor length between the check-in counters and the decision
#     point for the additional security check = 14.8 m
#   - Conveyor length between the decision point for the additional
#     security check and the equipment area = 12 m
#   - Conveyor length between the decision point for the additional
#     security check and the additional security check queue = 1.5 m
#   - Conveyor speed = 0.2 m/s
# The _CONVEYOR_TIME_... constants use the above details in order to
# calculate the bag travel times. The times were pre-calculated to
# reduce overhead.
#


class Bag:

    _CONVEYOR_TIME_CHECK_IN_DECISION_POINT = 74  # units: s
    _CONVEYOR_TIME_DECISION_POINT_EQUIP_AREA = 60  # units: s
    _CONVEYOR_TIME_SECURITY_CHECK = 7.5  # units: s

    _PROB_FAIL_XRAY1 = 0.1
    _PROB_FAIL_XRAY2 = 0.03

    _QUEUE_SERV_MU_EQUIP_AREA = 0.076
    _QUEUE_SERV_MU_SECURITY_CHECK = 0.25

    """
    Initialise a bag.

    :param env
    :param cust_id - ID of the customer that owns this bag.
    :param bug_num - identifies what bag this is for a customer.
    :param random - pseudorandom number generator used by the model.
    """
    def __init__(self, env, cust_id, bag_num, random):
        self._env = env
        self._bag_id = str(cust_id) + "-" + str(bag_num)
        self._random = random
        # TODO: create bag object at server. Location: check-in.
        # Status: created.

    """
    Queue the bag for an additional security check.

    :param security_check_queue - bags are queued here before
                                  receiving the additional check.
    """
    def _security_check(self, security_check_queue):
        print("[Bag "+self._bag_id+"] queued for security check.")
        request = security_check_queue.request()
        # TODO: queue size has changed so update the cloud [on service]
        yield request
        service_time = self._random.expovariate(
            self._QUEUE_SERV_MU_SECURITY_CHECK)
        yield self._env.timeout(service_time)
        security_check_queue.release(request)
        # TODO: queue size has changed so update the cloud [off service]
        print("[Bag "+self._bag_id+"] security check complete.")

    """
    Queue the bag in the equipment area so that it may be loaded onto
    its appropriate plane.

    :param equipment_area_queue - bags are queued here so that they
                                  may be loaded onto their appropriate
                                  planes.
    """
    def _equipment_area(self, equipment_area_queue):
        print("[Bag "+self._bag_id+"] queued for loading.")
        request = equipment_area_queue.request()
        # TODO: queue size has changed so update the cloud [on equip]
        yield request
        service_time = self._random.expovariate(
            self._QUEUE_SERV_MU_EQUIP_AREA)
        yield self._env.timeout(service_time)
        equipment_area_queue.release(request)
        # TODO: queue size has changed so update the cloud [off equip]
        print("[Bag "+self._bag_id+"] en route to plane.")

    """
    Process the bag in the simulation.

    :param equipment_area_queue - bags are queued here so that they
                                  may be loaded onto their appropriate
                                  planes.
    :param security_check_queue - bags are queued here before
                                  receiving the additional check.
    """
    def process(self, equipment_area_queue, security_check_queue):
        # Bag travels to decision point where it might receive an
        # additional security check.
        print("[Bag "+self._bag_id+"] on conveyor from check-in.")
        # TODO: update bag location and status. Location: conveyor.
        # Status: en route to first security check.
        yield self._env.timeout(
            self._CONVEYOR_TIME_CHECK_IN_DECISION_POINT)

        prob = self._random.random()
        if prob < self._PROB_FAIL_XRAY1:
            # Looks like this bag requires an extra security check,
            # transport it to the appropriate area.
            # TODO: update bag location and status. Location: conveyor.
            # Status: en route to second security check.
            yield(self._env.timeout(self._CONVEYOR_TIME_SECURITY_CHECK))

            # Queue the bag for scanning
            self._env.process(self._security_check(security_check_queue))

            # Scan the bag
            prob = self._random.random()
            if prob < self._PROB_FAIL_XRAY2:
                # Bag leaves the system as it didn't pass the additional
                # check.
                print("[Bag "+self._bag_id+"] security check failed.")
                return

            # else: Bag passed the check. It travels back to the main
            #       conveyor.
            yield(self._env.timeout(self._CONVEYOR_TIME_SECURITY_CHECK))

        # Bag travels to the equipment area to be loaded onto a plane.
        yield self._env.timeout(
            self._CONVEYOR_TIME_DECISION_POINT_EQUIP_AREA)

        self._env.process(self._equipment_area(equipment_area_queue))
