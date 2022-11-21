#!/usr/bin/env python3

from protocol import CloudProtocol
from config import config_data 

class TestUnitsAll: 
  def testCloudProtocol(self):
    p = CloudProtocol()
    print(p.login(config_data["school_id"]))
    print(p.status("RUNNING", eventRate = 123))

