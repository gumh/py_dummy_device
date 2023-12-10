#!/usr/bin/env python

import asyncio
from websockets import connect
from config import config_data
from logger import get_logger
import json
import traceback

from config import runtime

class CloudClient:
  def __init__(self):
    self.session = None
    self.callbacks = []
    self.url = config_data["cloud_ws_url"]
    self.logger = get_logger()

  async def send(self, data):
    if self.session != None:
      self.logger.info(">\n" + json.dumps(data, indent=2))
      await self.session.send(json.dumps(data))

  def reg_callback(self, cb):
    self.callbacks.append(cb)

  async def end_run(self):
    self.is_run = False

  async def run(self):
    self.is_run = True
    while self.is_run:
      try:
        async with connect(self.url) as self.session:
          self.logger.info("CloudClient, connected")
          runtime['state'] = 'CONNECTED'
          while self.is_run:
            try:
              data = await asyncio.wait_for(self.session.recv(), 1)
              data = json.loads(data)
              self.logger.info("<\n" + json.dumps(data, ensure_ascii=False, indent=2))
              for cb in self.callbacks:
                await cb(data)
            except asyncio.TimeoutError:
              pass
      except Exception as ex:
        self.logger.error(ex)

      self.session = None
      self.logger.info("CloudClient, disconnected")
      runtime['state'] = 'POWEROFF'
      await asyncio.sleep(2)

