from pywinauto.application import Application
from aloha_bot.cases import Context, Case_1, Case_2
import pandas as pd
import re

class Aloha:

  def __init__(self, path: str, run_case="1", close=True):
    self.path = path

    self.app = Application(backend="uia")
    try:
      self.app.connect(path=r'{}'.format(self.path))
      self.dlg = self.app['ALOHA 5.4.7']
      if close:
        self.close()
    except:
      print('not open')

    if not close:
      return

    self.app.start(self.path)
    self.dlg = self.app['ALOHA 5.4.7']

    # return
    self.dlg["ALOHA's Limitations"].wait('visible')
    self.dlg["ALOHA's Limitations"].OK.click()

    # get location
    self.dlg.type_keys('^l')
    self.dlg['Location Information'].Modify.click()
    location = self.dlg['Location Input']
    self.lat_deg = location.child_window(title="Longitude", auto_id="22", control_type="Edit").get_value()
    self.lat_min = location.child_window(auto_id="23", control_type="Edit").get_value()
    self.long_deg = location.child_window(auto_id="25", control_type="Edit").get_value()
    self.long_min = location.child_window(auto_id="26", control_type="Edit").get_value()
    location.type_keys('{ESC}')
    self.dlg['Location Information'].type_keys('{ESC}')

    if run_case == "1":
      self.context = Context(Case_1(self.dlg, self.lat_deg, self.lat_min, self.long_deg, self.long_min))
    elif run_case == "2":
      self.context = Context(Case_2(self.dlg, self.lat_deg, self.lat_min, self.long_deg, self.long_min))
    else:
      self.context = Context(Case_1(self.dlg, self.lat_deg, self.lat_min, self.long_deg, self.long_min))
    return

  def print_self(self):
    self.app['ALOHA 5.4.7'].print_control_identifiers()
    return

  def run(self, data, index):
    self.context.strategy.run(data, index)
    pass    
    
  
  def close(self):
    self.app.kill()
    return
