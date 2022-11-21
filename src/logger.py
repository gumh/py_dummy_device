
import logging

logger = None

class MyLogHandler(logging.Handler, object):
  """
  自定义日志handler
  """

  def __init__(self, name, add_log, other_attr=None, **kwargs):
    logging.Handler.__init__(self)
    self.add_log = add_log
    #print('初始化自定义日志处理器：', name)
    #print('其它属性值：', other_attr)

  def emit(self, record):
    """
    emit函数为自定义handler类时必重写的函数，这里可以根据需要对日志消息做一些处理，比如发送日志到服务器
    发出记录(Emit a record)
    """
    try:
      msg = self.format(record)
      # print('获取到的消息为：', msg)
      self.add_log(msg)
      #for item in dir(record):
      #  if item in ['process', 'processName', 'thread', 'threadName']:
      #    print(item, '：', getattr(record, item))
    except Exception:
      self.handleError(record)

def create_logger(add_log):
  global logger
  logger = logging.getLogger()
  logger.setLevel('DEBUG')
  BASIC_FORMAT = "[%(asctime)s][%(levelname)s]%(message)s"
  DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
  formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
  chlr = logging.StreamHandler() # 输出到控制台的handler
  chlr.setFormatter(formatter)
  chlr.setLevel('INFO')  # 也可以不设置，不设置就默认用logger的level
  fhlr = logging.FileHandler('example.log') # 输出到文件的handler
  fhlr.setFormatter(formatter)
  myh = MyLogHandler("AA", add_log)
  myh.setFormatter(formatter)
  myh.setLevel('INFO')
  logger.addHandler(myh)
  return logger
  #logger.addHandler(fhlr)
  
def get_logger():
  global logger
  return logger
