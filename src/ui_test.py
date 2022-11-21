#!/usr/bin/env python

import asyncio
import threading
import tkinter as tk
from tkinter import scrolledtext

from datetime import datetime
from dev_main import DevMain

from logger import create_logger

class Application(tk.Frame):
  """main frame"""

  def __init__(self, master=None):
    super().__init__(master)
    self.pack()
    self.add_controls()
    create_logger(self.add_log)

    self.dev_main = DevMain()
    self.master = master

    # start asyncio event loop
    self.loop = asyncio.new_event_loop()
    threading.Thread(target=self.run).start()

  def add_log(self, text):
    self.log.insert("end", text + '\n')

  def add_controls(self):
    """Add button to start the action
    """
    self.btn_poweron_dev = tk.Button(self, text="打开设备电源", command=self.power_on_dev)
    self.btn_poweron_dev.pack()

    self.btn_login = tk.Button(self, text="打开设备电源后，发送登录", command=self.login)
    self.btn_login.pack()

    self.btn_heartbeats = tk.Button(self, text="心跳", command=self.heartbeats)
    self.btn_heartbeats.pack()

    self.btn_get_available_status = tk.Button(self, text="查看设备可用状态", command=self.get_available_status)
    self.btn_get_available_status.pack()

    self.btn_publish_consumable = tk.Button(self, text="发布耗材状态", command=self.publish_consumable)
    self.btn_publish_consumable.pack()

    self.btn_begin_service = tk.Button(self, text="开始美容服务", command=self.begin_service)
    self.btn_begin_service.pack()

    self.btn_end_service = tk.Button(self, text="结束美容服务", command=self.end_service)
    self.btn_end_service.pack()

    self.btn_poweroff_dev = tk.Button(self, text="关闭设备电源", command=self.power_off_dev)
    self.btn_poweroff_dev.pack()

    self.log = scrolledtext.ScrolledText(self, width=150, height=20)
    self.log.pack()

  def power_on_dev(self):
    """login cloud"""
    future = asyncio.run_coroutine_threadsafe(self.dev_main.connect_cloud(), self.loop)
    #future.result()

  def login(self):
    future = asyncio.run_coroutine_threadsafe(self.dev_main.login(), self.loop)
    #future.result()

  def heartbeats(self):
    future = asyncio.run_coroutine_threadsafe(self.dev_main.heartbeats(), self.loop)

  def get_available_status(self):
    future = asyncio.run_coroutine_threadsafe(self.dev_main.get_available_status(), self.loop)
    #future.result()

  def publish_consumable(self):
    future = asyncio.run_coroutine_threadsafe(self.dev_main.publish_consumable(), self.loop)
 
  def power_off_dev(self):
    future = asyncio.run_coroutine_threadsafe(self.dev_main.disconnect_cloud(), self.loop)
    #future.result()

  def begin_service(self):
    future = asyncio.run_coroutine_threadsafe(self.dev_main.begin_service(), self.loop)
    #future.result()

  def end_service(self):
    future = asyncio.run_coroutine_threadsafe(self.dev_main.end_service(), self.loop)
    #future.result()

  def run(self):
    """start asyncio loop"""
    asyncio.set_event_loop(self.loop)
    self.loop.run_forever()

if __name__ == "__main__":
  root = tk.Tk()
  root.title("虚拟设备")
  app = Application(master=root)
  app.mainloop()
