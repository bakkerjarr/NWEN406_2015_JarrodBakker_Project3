#
# A customer which brings 0 to 5 bags with them to be processed.
#


class Customer:

    """
    @param id - identifier of a customer.
    """
    def __init__(self, env, id, num_bags):
        self.env = env
        self.id = id
        self.num_bags = num_bags

    """
    Process the customer in the Simulation.
    """
    def process(self):
        time_arrive = self.env.now
        print("["+str(self.id)+"] bags: " + str(self.num_bags) +
              "\tArrival time: " + str(time_arrive))
        yield self.env.timeout(1)
