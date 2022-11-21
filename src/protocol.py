
from datetime import *
import hashlib

request_data = {
    "type": "",
    "data": ""
}

class CloudProtocol:
  def __init__(self):
    pass

  def login(self, dev_id):
    t = int(datetime.now().timestamp())
    request_data = {
      "type": "DeviceLogin",
      "direction":"DeviceRequest",
      "data": {
        "id": dev_id,
        "time": t,
        "sign": hashlib.md5(bytes(str(t) + 'yimei1', 'utf-8')).hexdigest(),
      }
    }
    return request_data

  def dev_available(self):
    request_data = {
      "type":"Available",
      "direction":"DeviceRequest"
    }
    return request_data

  def begin_use(self):
    return {
      "type":"BeginUse",
      "direction":"DeviceRequest",
      "data": {
        "service": "anmo"
      }
    }

  def end_use(self):
    return {
      "type":"EndUse",
      "direction":"DeviceRequest",
      "data": {
        "service": "anmo"
      }
    }

  def pub_consumable(self):
    return {
      "type":"ConsumablesData",
      "direction":"DevicePush",
      "data":{
        "typeId":"1003",
        "id":"11111",
        "number":"10000"
      }
    }

  def heartbeats(self):
    return {
      "type":"Heartbeats",
      "direction":"DeviceReqest",
      "data":{}
    }

