#
# A bag which moves along a conveyor and gets processed at different
# stages.
#


class Bag:

    def __init__(self, cust_id, bag_num):
        self.bag_id = str(cust_id) + "-" + str(bag_num)
