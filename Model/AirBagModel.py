#
# A model of an airport baggage handling system. This model is based
# off of a model found noted in the paper Riga Airport Baggage Handling
# System Simulation written by Mihails Savrasovs,Alexander Medvedev and
# Elena Sincova. This was last accessed from
# https://www.extendsim.com/downloads/papers/sols_papers_latviaBaggage.pdf
# on September 21, 2015.
#
# SimPy is used to to simulate the system.
#
# At specific moments events will be triggered (NOT YET IMPLEMENTED)
#

from CustomerGenerator import CustomerGenerator
import simpy


class Model:

    """
    Initialise the model.

    :param arrival_rate - customer arrival rate.
    :param max_cust - maximum number of customers that will be simulated.
    :param num_check_in - number of check-in counters.
    :param rand_seed - seed for the pseudorandom number generator.
    """
    def __init__(self, arrival_rate, max_cust, num_check_in, rand_seed):
        self._arrival_rate = arrival_rate
        self._max_cust = max_cust
        self._num_check_in = num_check_in
        self._rand_seed = rand_seed

        self._env = simpy.Environment()
        #self._env = simpy.rt.RealtimeEnvironment(factor=1.0)

    """
    Start the model.
    """
    def start_simulation(self):
        c_gen = CustomerGenerator(self._env, self._arrival_rate,
                                  self._max_cust, num_check_in,
                                  self._rand_seed)
        self._env.process(c_gen.source())
        self._env.run()


if __name__ == "__main__":
    # TODO Get CLI arguments
    arrival_rate = 5
    max_cust = 20
    num_check_in = 7
    rand_seed = 999
    m = Model(arrival_rate, max_cust, num_check_in, rand_seed)
    m.start_simulation()
