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

from API.AirBagAPI import AirBagAPI


class Bag:

    _CONVEYOR_TIME_CHECK_IN_DECISION_POINT = 30 # original 74  # units: s
    _CONVEYOR_TIME_DECISION_POINT_EQUIP_AREA = 24 # original 60  #
    # units: s
    _CONVEYOR_TIME_SECURITY_CHECK = 3 # original 7.5  # units: s

    _PROB_FAIL_XRAY1 = 0.5  # original 0.1
    _PROB_FAIL_XRAY2 = 0.5  # original 0.03

    _QUEUE_SERV_MU_EQUIP_AREA = 0.076
    _QUEUE_SERV_MU_SECURITY_CHECK = 0.25  # original 0.25

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

        AirBagAPI().bag_enter_system(self._bag_id, "check-in",
                                     "checked in",  "20")

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

        AirBagAPI().bag_update_loc_status(self._bag_id, "conveyor",
                                          "waiting for sec. scan 1")

        # Status: en route to first security check.
        yield self._env.timeout(
            self._CONVEYOR_TIME_CHECK_IN_DECISION_POINT)

        prob = self._random.random()
        if prob < self._PROB_FAIL_XRAY1:
            # Looks like this bag requires an extra security check,
            # transport it to the appropriate area.

            AirBagAPI().bag_update_loc_status(self._bag_id, "conveyor",
                                              "failed sec. check 1")

            # Status: en route to second security check.
            yield(self._env.timeout(self._CONVEYOR_TIME_SECURITY_CHECK))

            # Queue the bag for scanning
            print("[Bag "+self._bag_id+"] queued for security check.")
            request = security_check_queue.request()

            AirBagAPI().bag_update_loc_status(self._bag_id, "sec. scan 2",
                                          "waiting for sec. scan 2")

            yield request
            service_time = self._random.expovariate(
            self._QUEUE_SERV_MU_SECURITY_CHECK)
            yield self._env.timeout(service_time)
            security_check_queue.release(request)
            print("[Bag "+self._bag_id+"] security check complete.")

            # Scan the bag
            prob = self._random.random()
            if prob < self._PROB_FAIL_XRAY2:
                # Bag leaves the system as it didn't pass the additional
                # check.
                AirBagAPI().bag_update_loc_status(self._bag_id, "sec. scan 2",
                                                  "failed sec. scan 2")
                print("[Bag "+self._bag_id+"] security check failed.")
                return

            # else: Bag passed the check. It travels back to the main
            #       conveyor.
            AirBagAPI().bag_update_loc_status(self._bag_id, "conveyor",
                                              "passed sec. check 2")
            yield(self._env.timeout(self._CONVEYOR_TIME_SECURITY_CHECK))

        # Bag travels to the equipment area to be loaded onto a plane.
        AirBagAPI().bag_update_loc_status(self._bag_id, "conveyor",
                                          "to loading-area")
        yield self._env.timeout(
            self._CONVEYOR_TIME_DECISION_POINT_EQUIP_AREA)

        print("[Bag "+self._bag_id+"] queued for loading.")
        request = equipment_area_queue.request()

        AirBagAPI().bag_update_loc_status(self._bag_id, "loading-area",
                                          "waiting for loading")
        yield request
        service_time = self._random.expovariate(
            self._QUEUE_SERV_MU_EQUIP_AREA)
        yield self._env.timeout(service_time)
        equipment_area_queue.release(request)
        print("[Bag "+self._bag_id+"] en route to plane.")
        AirBagAPI().bag_update_loc_status(self._bag_id, "plane",
                                          "delivered to plane")
