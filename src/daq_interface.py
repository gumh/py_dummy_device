
from config import runtime
import yaml
import subprocess

class DAQInterface:

  def __init__(self, daq_cli):
    self.daq_cli = daq_cli
    self.run_app_cmd = "docker run --name ed-population --rm -d -v /opt/ed-popularization-daq:/app -p 8080:9085 colegmh/gcc-wrdaq:1.0 bash -c \"source /app/setup.sh; /app/build/src/daq_main\""
    self.kill_app_cmd = "docker stop ed-population"

  def run_app(self):
    runtime["daq_status"]["status"] = "BUSY"
    subprocess.Popen(self.run_app_cmd, shell=True)

  def kill_app(self):
    runtime["daq_status"]["status"] = "BUSY"
    subprocess.Popen(self.kill_app_cmd, shell=True)

  async def start(self):
    runtime["daq_status"]["status"] = "BUSY"
    await self.daq_cli.start()

  async def stop(self):
    runtime["daq_status"]["status"] = "BUSY"
    await self.daq_cli.stop()

  def config(self, data):
    fpath = runtime["daq_config_path"]
    with open(fpath, 'r', encoding='utf-8') as f:
      obj = yaml.load(f, Loader=yaml.FullLoader)

    enable_channels = data["enable_channels"]
    # set effect channels
    self.set_effect_channels(obj, enable_channels)

    # set threshold of channels
    for i in range(0, len(enable_channels)):
      ch = enable_channels[i]
      th = data["thresholds"][i]
      self.set_th(obj, ch, th)

    # set on fire channels
    self.set_on_fire_channels(obj, len(enable_channels))

    runtime["daq_config"] = data

    # write config to file
    with open(fpath, 'w', encoding='utf-8') as f:
      yaml.dump(obj, f)

  async def update_status(self):
    try:
      runtime["daq_status"]["status"] = await self.daq_cli.state()
      runtime["daq_status"]["params"] = await self.daq_cli.param()
    except Exception as ex:
      runtime["daq_status"]["status"] = "NONE"
      runtime["daq_status"]["params"] = {}

  def set_th(self, obj, channel, value):
    for item in obj["fees"][0]["elec_config"]:
      if item["value"]["addr"] == 0x05 and item["value"]["flag"] == channel: 
        item["value"]["data"] = value
      
  def set_effect_channels(self, obj, channels):
    ef_val = 0
    for ch in channels:
      ef_val |= (1<<(ch-1))

    for item in obj["fees"][0]["elec_config"]:
      if item["value"]["addr"] == 0x04 and item["value"]["flag"] == 0x00: 
        item["value"]["data"] = ef_val
    
  def set_on_fire_channels(self, obj, n_channels):
    for item in obj["fees"][0]["elec_config"]:
      if item["value"]["addr"] == 0x03 and item["value"]["flag"] == 0x00: 
        item["value"]["data"] = n_channels

