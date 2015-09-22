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

    """
    Give a bag an additional security check.

    :return - True if the bag passed, False otherwise.
    """
    def _security_check(self):
        pass
        # Bag gets scanned

        prob = self._random.random()
        if prob < self._PROB_FAIL_XRAY2:
            # Bag fails check
            return False
        else:
            # Bag passes check
            return True

    """
    Process the bag in the simulation.
    """
    def process(self):
        pass
        # Bag travels to decision point where it might receive an
        # additional security check.
        yield self._env.timeout(
            self._CONVEYOR_TIME_CHECK_IN_DECISION_POINT)

        prob = self._random.random()
        if prob < self._PROB_FAIL_XRAY1:
            # Looks like this bag requires an extra check.
            yield(self._env.timeout(self._CONVEYOR_TIME_SECURITY_CHECK))
            result = self._security_check()
            if not result:
                # Bag leaves the system as it didn't pass the additional
                # check.
                return
            # else: The bag passed the check! It travels back to the
            # main conveyor.
            yield(self._env.timeout(self._CONVEYOR_TIME_SECURITY_CHECK))

        # Bag travels to the equipment area to be loaded onto a plane.
        yield self._env.timeout(
            self._CONVEYOR_TIME_DECISION_POINT_EQUIP_AREA)
