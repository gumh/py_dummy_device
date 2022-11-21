import asyncio
from aiohttp import ClientSession
import time
from config import config_data
from logger import get_logger

import json

class DAQClient:
  def __init__(self):
    self.session = None
    self.url = config_data["daq_url"]
    self.callbacks = []
    self.control_url = {
      "init": self.url+"/api/control?command=init",
      "connect": self.url+"/api/control?command=connect",
      "config": self.url+"/api/control?command=config",
      "start": self.url+"/api/control?command=start",
      "stop": self.url+"/api/control?command=stop",
      "terminate": self.url+"/api/control?command=terminate"
    }
    
    self.state_url = self.url+"/api/state"
    self.param_url = self.url+"/api/params"

  async def start(self):
    logger = get_logger()
    async with ClientSession() as conn:
      async with conn.get(self.control_url["init"]):
        pass
      async with conn.get(self.control_url["connect"]):
        pass
      async with conn.get(self.control_url["config"]):
        pass
      async with conn.get(self.control_url["start"]):
        pass

  async def stop(self):
    logger = get_logger()
    async with ClientSession() as conn:
      async with conn.get(self.control_url["stop"]):
        pass
      async with conn.get(self.control_url["terminate"]):
        pass

  async def param(self):
    logger = get_logger()
    async with ClientSession() as conn:
      async with conn.get(self.param_url) as resp:
        return json.loads(await resp.text())["message"]

  async def state(self):
    logger = get_logger()
    async with ClientSession() as conn:
      async with conn.get(self.state_url) as resp:
        return json.loads(await resp.text())["message"]

