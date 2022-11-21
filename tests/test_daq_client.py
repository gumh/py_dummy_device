#!/usr/bin/env python

from daq_client import DAQClient
import asyncio

async def main():
  cli = DAQClient()
  print(await cli.state())
  print(await cli.param())

asyncio.run(main())
