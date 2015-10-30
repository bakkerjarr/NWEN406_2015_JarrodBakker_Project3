__author__ = 'Jarrod N. Bakker'
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

#
# TODO - Allow the collection of queue statistics so that they may be
#        processed by AWS Lambda, for example queue sizes and expected
#        waiting times.
#

from CustomerGenerator import CustomerGenerator
import argparse
import simpy


class Model:

    """
    Initialise the model.

    :param arrival_rate - customer arrival rate.
    :param max_cust - maximum number of customers that will be simulated.
    :param num_check_in - number of check-in counters.
    :param rand_seed - seed for the pseudorandom number generator.
    :param time_factor - scaling factor for real-time simluation.
    """
    def __init__(self, arrival_rate, max_cust, num_check_in,
                 rand_seed, time_factor):
        self._arrival_rate = arrival_rate
        self._max_cust = max_cust
        self._num_check_in = num_check_in
        self._rand_seed = rand_seed

        # Initialise the SimPy environment
        self._env = simpy.rt.RealtimeEnvironment(factor=time_factor)

        # Create the necessary queues
        self._check_in_counters = []
        for i in range(num_check_in):
            self._check_in_counters.append(simpy.Resource(self._env))
        self._equipment_area_queue = simpy.Resource(self._env)
        self._security_check_queue = simpy.Resource(self._env)
        # TODO: create queue object in server

    """
    Start the model.
    """
    def start_simulation(self):
        c_gen = CustomerGenerator(self._env, self._arrival_rate,
                                  self._max_cust,
                                  self._check_in_counters,
                                  self._equipment_area_queue,
                                  self._security_check_queue,
                                  self._rand_seed)
        self._env.process(c_gen.source())
        self._env.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Model an airport "
                                                 "baggage handling "
                                                 "system for "
                                                 "departing customers.")
    parser.add_argument("max_cust", metavar="N", type=int,
                        help="The number of customers to be processed "
                             "by the system.")
    parser.add_argument("-c", dest="num_check_in", default=7,
                        type=int, help="The number of check-in "
                                       "counters (default is 7).")
    parser.add_argument("-s", dest="time_factor", default=1, type=float,
                        help="Scaling factor for real-time simulation "
                             "(default is 1.0 or clock time.")

    args = parser.parse_args()

    arrival_rate = 4
    rand_seed = 999
    m = Model(arrival_rate, args.max_cust, args.num_check_in,
              rand_seed, args.time_factor)
    print("[!] Starting simulation.\n\tTotal number of customers: {0}"
          "\n\tNumber of check-in counters: {1}\n\tTime scaling "
          "factor: {2}\n").format(args.max_cust, args.num_check_in,
                                  args.time_factor)
    m.start_simulation()
    print("\n[!] Simulation complete.")
