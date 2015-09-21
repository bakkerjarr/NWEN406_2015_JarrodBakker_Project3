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

if __name__ == "__main__":
    # TODO Get CLI arguments
    env = simpy.Environment()
    #env = simpy.rt.RealtimeEnvironment(factor=1.0)
    arrival_rate = 5
    max_cust = 100
    c_gen = CustomerGenerator(env, arrival_rate, max_cust)
    env.process(c_gen.source())
    env.run()
