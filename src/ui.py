#!/usr/bin/env python

import asyncio
import tkinter as tk

class tk_async_window(tk.Tk):
    def __init__(self, loop, update_interval=1/20):
        super(tk_async_window, self).__init__()
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.geometry('400x100')
        self.loop = loop
        self.tasks = []
        self.update_interval = update_interval

        self.status = 'working'
        self.status_label = tk.Label(self, text=self.status)
        self.status_label.pack(padx=10, pady=10)

        self.close_event = asyncio.Event()

    def close(self):
        self.close_event.set()

    async def ui_update_task(self, interval):
        while True:
            self.update()
            await asyncio.sleep(interval)

    async def status_label_task(self):
        """
        This keeps the Status label updated with an alternating number of dots so that you know the UI isn't
        frozen even when it's not doing anything.
        """
        dots = ''
        while True:
            self.status_label['text'] = 'Status: %s%s' % (self.status, dots)
            await asyncio.sleep(0.5)
            dots += '.'
            if len(dots) >= 4:
                dots = ''

    def initialize(self):
        coros = (
            self.ui_update_task(self.update_interval),
            self.status_label_task(),
            # additional network-bound tasks
        )
        for coro in coros:
            self.tasks.append(self.loop.create_task(coro))

async def ui_main():
    gui = tk_async_window(asyncio.get_event_loop())
    gui.initialize()
    await gui.close_event.wait()
    gui.destroy()

