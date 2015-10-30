__author__ = 'Jarrod N. Bakker'

#
# Use AWS API Gateway endpoints to change the state of the system.
# This allows an application to create bags and update their status
# and location within the physical system.
#
# The requests module would have been the preferred way to utilise the
# web API, however as my machine only had Python 2.7.6 connections
# would fail due to Python's SSL certificates being out-of-date. As I
# knew that curl worked I programmed the API to execute curl
# commands. This solution is ugly but it works.
#

import json
import os
import sys


class AirBagAPI:

    _API_URL_BASE =\
        "https://kxy0yszwcb.execute-api.us-west-2.amazonaws.com/Test"
    _API_URL_BAGS = "/baggagetracking/bags"
    _TEXT_ERROR_CONNECTION = "[ERROR] Unable to connect with API " \
                             "endpoint."

    def bag_enter_system(self, bag_id, location, status, weight):
        new_bag = json.dumps({"bag_id": bag_id, "bag_location": location,
                             "bag_weight": str(weight),
                              "bag_status": status})
        try:
            print("[!] Making API call...")
            os.system("curl -X POST {0} -d \'{1}\'".format(
                self._API_URL_BASE+self._API_URL_BAGS, str(new_bag)))
        except:
            print self._TEXT_ERROR_CONNECTION
            print("[!] FATAL EXCEPTION:\n{0}\n"
                  .format(sys.exc_info()))

    def bag_update_loc_status(self, bag_id, location, status):
        bag = json.dumps({"bag_id": bag_id, "bag_location": location,
                              "bag_status": status})
        try:
            print("[!] Making API call...")
            os.system("curl -X PUT {0} -d \'{1}\'".format(
                self._API_URL_BASE+self._API_URL_BAGS, str(bag)))
        except:
            print self._TEXT_ERROR_CONNECTION
            print("[!] FATAL EXCEPTION:\n{0}\n"
                  .format(sys.exc_info()))
