#!/usr/bin/env python3

import asyncio
import time
from daq_client import DAQClient
from cloud_client import CloudClient

async def send_task1(cli):
  while True:
    print("here")
    await cli.send("hello")
    print("here 1")
    await asyncio.sleep(1)

async def main():
  daq_cli = DAQClient()
  cloud_cli = CloudClient()

  task_list = []
  task_list.append(asyncio.create_task(daq_cli.run()))
  task_list.append(asyncio.create_task(cloud_cli.run()))
  task_list.append(asyncio.create_task(send_task1(cloud_cli)))

  done, pending = await asyncio.wait(task_list, timeout=None)
  # 得到执行结果
  for done_task in done:
    #print(f"{time.time()} 得到执行结果 {done_task.result()}")
    print(f"{time.time()}")

asyncio.run(main())

