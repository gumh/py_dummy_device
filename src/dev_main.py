#!/usr/bin/env python3

import asyncio
import time
from cloud_client import CloudClient
from protocol import CloudProtocol
from config import config_data
from logger import get_logger
import json
from config import runtime
from dummy_dev import DummyDev
from datetime import *
from ui import ui_main

import traceback

class DevMain:

  def __init__(self):
    self.cloud_cli = CloudClient()
    self.cloud_cli.reg_callback(lambda data: self.cloud_recv_callback(data))
    self.logger = get_logger()

  async def cloud_recv_callback(self, data):
    if not data:
      return
  
    try:
      # self.logger.info("<cloud " + json.dumps(data, ensure_ascii=False))
      if data["type"] == "DeviceLogin" and data["data"]["flag"] == "Succ" and runtime["state"] == "CONNECTED":
        # successfully login
        runtime["mode"] = data["data"]["mode"]
        runtime["state"] = "LOGIN"
      elif data["type"] == "BeginUse" and runtime["state"] == "BEGIN_SERVICE":
        runtime["state"] = "IN_SERVICE"
      elif data["type"] == "EndUse" and runtime["state"] == "END_SERVICE":
        runtime["state"] = "LOGIN"

      self.logger.info("current state: %s, current mode: %s" % (runtime["state"], runtime["mode"]))
  
    except Exception as ex:
      self.logger.error(ex)
      traceback.print_exc()

  async def login(self):
    msg = CloudProtocol().login(config_data["dev_id"])
    self.logger.info("now, we send login message..")
    await self.cloud_cli.send(msg)

  async def begin_service(self):
    msg = CloudProtocol().begin_use()
    self.logger.info("now, we send begin service message..")
    await self.cloud_cli.send(msg)

  async def end_service(self):
    msg = CloudProtocol().end_use()
    self.logger.info("now, we send end service message..")
    await self.cloud_cli.send(msg)

  async def get_available_status(self):
    msg = CloudProtocol().dev_available()
    self.logger.info("now, we send get available status message..")
    await self.cloud_cli.send(msg)

  async def publish_consumable(self):
    msg = CloudProtocol().pub_consumable()
    self.logger.info("now, we send publish consumables' status message..")
    await self.cloud_cli.send(msg)

  async def heartbeats(self):
    msg = CloudProtocol().heartbeats()
    self.logger.info("now, we send heartbeats message..")
    await self.cloud_cli.send(msg)

    #while True:
    #  try:
    #    if runtime["status"] == "ReadyWork":
    #      msg = CloudProtocol().pub_consumable()
    #      self.logger.info("now, we send publish consumables' status message..")
    #      await self.cloud_cli.send(msg)
    #  except Exception as ex:
    #    self.logger.error(ex)
    #    traceback.print_exc()
    #  finally:
    #    await asyncio.sleep(5)

  async def connect_cloud(self):
    asyncio.create_task(self.cloud_cli.run())

  async def disconnect_cloud(self):
    asyncio.create_task(self.cloud_cli.end_run())

#if __name__ == "__main__":
#  asyncio.run(dev_main())

