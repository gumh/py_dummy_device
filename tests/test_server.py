#!/usr/bin/env python

import asyncio
from websockets import serve
import logging
import json
import sys
from aioconsole import get_standard_streams
import traceback
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

mode = "Limit"

async def producer_handler(websocket, reader):
  global mode
  while True:
    input_data = await reader.readline()
    d = str(input_data, encoding='utf-8').strip()
    request = None

    m1 = re.match(r"mode (.*)", d)
    if m1 and m1.group(1) == "Limit":
      mode = "Limit"
      logger.info("mode = %s" % (mode))
    elif m1 and m1.group(1) == "NoLimit":
      mode = "NoLimit"
      logger.info("mode = %s" % (mode))

    if request != None:
      await websocket.send(json.dumps(request))

async def consumer_handler(websocket):
  async for data in websocket:
    logger.info("recv %s" % data)
    data = json.loads(data)
    if data["type"] == "DeviceLogin":
      response = {
        "type": "DeviceLogin",
        "direction": "PlatformResponse",
        "data": {
            "flag": "Succ",
            "mode": "Limit"
        }
      }
    elif data["type"] == "BeginUse":
      response = {
        "direction": "PlatformResponse",
        "type": "BeginUse",
        "data": {}
      }
    elif data["type"] == "EndUse":
      response = {
        "direction": "PlatformResponse",
        "type": "EndUse",
        "data": {}
      }
    elif data["type"] == "Available":
      response = {
        "type":"Available",
        "direction":"PlatformResponse",
        "data" : {
          "ElectronicConsumables":[
            {
              "id":"耗材id",
              "type":"电子耗材类型ID",
              "number":"次数"
            }
          ],
          "Consumables":[
            {
              "type":"耗材类型",
              "count":"数量（1）"
            },
            {
              "type":"耗材类型",
              "count":"数量（1）"
            },
            {
              "type":"耗材类型",
              "count":"数量（1）"
            }
          ],
          "prohibited":"是否禁止使用true,false",
          "flag":"限制类型",
          "number":"次数",
          "time":"到期时间"
        }
      }

    await websocket.send(json.dumps(response))

async def test_server(websocket, reader):
  logger.info("connected")
  try: 
    consumer_task = asyncio.create_task(consumer_handler(websocket))
    producer_task = asyncio.create_task(producer_handler(websocket, reader))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()

  except Exception as ex:
    traceback.print_exc()
    print(ex)
    print(ex)
    return 

  logger.info("disconnected")

async def main():
  reader, writer = await get_standard_streams()
  async with serve(lambda websocket: test_server(websocket, reader), "localhost", 8765):
    await asyncio.Future()

asyncio.run(main())

