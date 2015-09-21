#
# Describes the actions that are performed upon a bag while it is in
# the system. The bag moves along a conveyor and gets processed at
# various points.
#


class Bag:

    def __init__(self, cust_id, bag_num):
        self._bag_id = str(cust_id) + "-" + str(bag_num)
