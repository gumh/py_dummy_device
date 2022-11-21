#!/usr/bin/env python

import asyncio
import threading
import tkinter as tk
from tkinter import scrolledtext

from datetime import *
from dev_main import DevMain

from logger import create_logger, get_logger
from config import runtime

class ControlFrame(tk.Frame):
  def __init__(self, dev, aloop, parent = None):
    super().__init__(parent)
    self.last_print_state = None
    self.logger = get_logger()

    self.last_login = datetime.fromtimestamp(0)
    self.last_begin = datetime.fromtimestamp(0)
    self.last_end = datetime.fromtimestamp(0)
    self.last_heartbeat = datetime.fromtimestamp(0)
    self.last_pub_consumable = datetime.fromtimestamp(0)

    self.timeout_login = 5
    self.timeout_begin = 5
    self.timeout_end = 5
    self.timeout_heartbeat = 5
    self.timeout_pub_consumable = 5

    self.dev = dev
    self.aloop = aloop

    self.btn_poweron_dev = tk.Button(self, text="打开设备电源", command=self.power_on_dev)
    self.btn_poweron_dev.pack()

    self.btn_poweroff_dev = tk.Button(self, text="关闭设备电源", command=self.power_off_dev)
    self.btn_poweroff_dev.pack()

    self.btn_begin_service = tk.Button(self, text="开始美容服务", command=self.begin_service)
    self.btn_begin_service.pack()

    self.btn_end_service = tk.Button(self, text="结束美容服务", command=self.end_service)
    self.btn_end_service.pack()

    self.update()

    self.check_loop()

  def update(self):
    self.btn_poweron_dev.config(state = tk.DISABLED)
    self.btn_poweroff_dev.config(state = tk.DISABLED)
    self.btn_begin_service.config(state = tk.DISABLED)
    self.btn_end_service.config(state = tk.DISABLED)

    if runtime["state"] == "POWEROFF":
      self.btn_poweron_dev.config(state = tk.NORMAL)
    if runtime["state"] != "POWEROFF":
      self.btn_poweroff_dev.config(state = tk.NORMAL)
    if runtime["state"] == "LOGIN":
      self.btn_begin_service.config(state = tk.NORMAL)
    if runtime["state"] == "IN_SERVICE":
      self.btn_end_service.config(state = tk.NORMAL)

    self.after(1000, self.update)
      
  def check_loop(self):
    now = datetime.now()
    if runtime["state"] == "CONNECTED":
      if now - self.last_login > timedelta(seconds = self.timeout_login):
        future = asyncio.run_coroutine_threadsafe(self.dev.login(), self.aloop)
        self.last_login = now

    if runtime["state"] == "LOGIN"  or runtime["state"] == "BEGIN_SERVICE" or runtime["state"] == "IN_SERVICE":
      if now - self.last_heartbeat > timedelta(seconds = self.timeout_heartbeat):
        future = asyncio.run_coroutine_threadsafe(self.dev.heartbeats(), self.aloop)
        future = asyncio.run_coroutine_threadsafe(self.dev.get_available_status(), self.aloop)
        self.last_heartbeat = now

    if runtime["state"] == "BEGIN_SERVICE":
      if now - self.last_begin > timedelta(seconds = self.timeout_begin):
        future = asyncio.run_coroutine_threadsafe(self.dev.begin_service(), self.aloop)
        self.last_begin = now

    if runtime["state"] == "END_SERVICE":
      if now - self.last_end > timedelta(seconds = self.timeout_end):
        future = asyncio.run_coroutine_threadsafe(self.dev.end_service(), self.aloop)
        self.last_end = now

    if runtime["state"] == "IN_SERVICE":
      if now - self.last_pub_consumable > timedelta(seconds = self.timeout_pub_consumable):
        future = asyncio.run_coroutine_threadsafe(self.dev.publish_consumable(), self.aloop)
        self.last_pub_consumable = now

    if self.last_print_state != runtime["state"]:
      self.logger.info("current state: %s" % (runtime['state']))
      self.last_print_state = runtime["state"]
    self.after(1000, self.check_loop)

  def power_on_dev(self):
    """login cloud"""
    runtime["state"] = "POWERON"
    future = asyncio.run_coroutine_threadsafe(self.dev.connect_cloud(), self.aloop)

  def login(self):
    runtime["state"] = "LOGIN"

  def power_off_dev(self):
    runtime["state"] = "POWEROFF"
    future = asyncio.run_coroutine_threadsafe(self.dev.disconnect_cloud(), self.aloop)

  def begin_service(self):
    runtime["state"] = "BEGIN_SERVICE"

  def end_service(self):
    runtime["state"] = "END_SERVICE"

class StatusFrame(tk.Frame):
  def __init__(self, dev, parent = None):
    super().__init__(parent)
    self.dev = dev

    w = 20
    self.conn_state = tk.Label(self, text = "连接状态", bg = "red", width = w)
    self.login_state = tk.Label(self, text = "登录状态", bg = "red", width = w)
    self.tenancy_state = tk.Label(self, text = "租期", bg = "gray", width = w)
    self.consumable_state = tk.Label(self, text = "耗材剩余", bg = "gray", width = w)

    self.conn_state.grid(row = 0, column = 0, padx = 2, pady = 1)
    self.login_state.grid(row = 1, column = 0, padx = 2, pady = 1)
    self.tenancy_state.grid(row = 2, column = 0, padx = 2, pady = 1)
    self.consumable_state.grid(row = 3, column = 0, padx = 2, pady = 1)

    self.update()

  def get_status(self):
    status = {
      "connection": False,
      "login": False,
      "tenancy": 1,
      "consumable": 1,
    }

    if runtime["state"] == "POWEROFF" or runtime["state"] == "POWERON":
      status['connection'] = False
    else:
      status['connection'] = True

    if runtime["state"] == "POWEROFF" or runtime["state"] == "POWERON" or runtime["state"] == "CONNECTED":
      status['login'] = False
    else:
      status['login'] = True

    return status

  def update(self):
    status = self.get_status()

    if "connection" in status:
      c1 = "green" if status["connection"] else "red"
    else:
      c1 = "gray"
    self.conn_state.config(bg = c1)

    if "login" in status:
      c1 = "green" if status["login"] else "red"
    else:
      c1 = "gray"
    self.login_state.config(bg = c1)

    if "tenancy" in status:
      c1 = "green" if status["tenancy"] else "red"
    else:
      c1 = "gray"
    self.tenancy_state.config(bg = c1)

    if "consumable" in status:
      c1 = "green" if status["consumable"] else "red"
    else:
      c1 = "gray"
    self.consumable_state.config(bg = c1)

    self.after(1000, self.update)

class LogFrame(tk.Frame):
  def __init__(self, parent = None):
    super().__init__(parent)
    self.log = scrolledtext.ScrolledText(self, width=120, height=50)
    self.log.pack()
    create_logger(self.add_log)

  def add_log(self, text):
    self.log.insert("end", text + '\n')
    self.log.see("end")

class Application(tk.Frame):
  """main frame"""

  def __init__(self, master=None):
    super().__init__(master)

    # init logger
    self.log_frame = LogFrame(self)

    # start asyncio event loop
    self.aloop = asyncio.new_event_loop()
    threading.Thread(target=self.run).start()

    self.dev = DevMain()
    self.control_frame = ControlFrame(self.dev, self.aloop, self)
    self.status_frame = StatusFrame(self.dev, self)

    self.control_frame.grid(row = 0, column = 0, padx = 20)
    self.status_frame.grid(row = 1, column = 0)
    self.log_frame.grid(row = 0, column = 1, rowspan = 2)

  def run(self):
    """start asyncio loop"""
    asyncio.set_event_loop(self.aloop)
    self.aloop.run_forever()

if __name__ == "__main__":
  root = tk.Tk()
  root.title("虚拟设备")
  app = Application(master=root)
  app.pack()
  root.mainloop()
