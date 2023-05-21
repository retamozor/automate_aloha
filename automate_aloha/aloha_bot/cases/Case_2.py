from pywinauto.application import WindowSpecification
from .Strategy import Strategy
from .Functions import Functions
import pandas as pd
import re

class Case_2(Strategy):

  def __init__(self, dlg: WindowSpecification, lat_deg, lat_min, long_deg, long_min) -> None:
    self.dlg = dlg
    self.lat_deg = lat_deg
    self.lat_min = lat_min
    self.long_deg = long_deg
    self.long_min =long_min
    self.first_run = True
    self.functions = Functions(dlg)

  def set_up_chemical(self) -> None:
    self.functions.set_up_chemical('CYCLOHEXANONE')
    return

  def print_sumary(self, index = 0):
    text = self.dlg['Text Summary'].child_window(auto_id='5001', control_type='Edit')
    sumary = text.get_value().split('THREAT ZONE: ')[1]
    source = text.get_value().split('SOURCE STRENGTH:')[1].split(' THREAT ZONE: ')[0]
    red_orange_yellow = re.findall(' [Red|Orange|Yellow].*:.*meters.*---.*[(].*[)]', sumary)
    # for each line in red_orange_yellow: split by ':'

    colors = {
      'index': [index],
      'Red': [''],
      'Orange': [''],
      'Yellow': [''],
      'Max Flame Length': [re.findall('Max Flame Length: .*meters', source)[0].split(': ')[1].strip()],
      'Burn Duration': [re.findall('Burn Duration: .*', source)[0].split(': ')[1].strip()],
      'Max Burn Rate': [re.findall('Max Burn Rate: .*', source)[0].split(': ')[1].strip()],
      'Total Amount Burned': [re.findall('Total Amount Burned: .*', source)[0].split(': ')[1].strip()],
    }
    for line in red_orange_yellow:
      color = line.split(': ')[0].strip()
      data = line.split(': ')[1].strip()
      #save in dict
      colors[color] = [data]

    # save in csv
    pd.DataFrame.from_dict(colors, orient='columns').to_csv(r'automate_aloha\out\caso_2\Colors.csv', mode='a', header=False, index=False)
    
    return
  
  def run(self, data, index) -> None:
    successful_run = True

    # Set Building Type
    self.functions.set_building_type(data['Building'])

    # Atmospheric Options
    self.functions.set_atmospheric_options(
      data['Ground roughtness'],
      data['Wind speed'],
      data['Wind is from'],
      data['Cloud cover'],
    )
    self.functions.set_atmospheric_options_2(
      data['Air themperature'],
      data['Humidity'],
    )

    # Source Options
    self.functions.set_tank_size_and_orientation(
      data['Tank Type'],
      data['Tank length'],
      data['Tank Diameter'],
    )
    self.functions.set_chemical_state_and_temperature(data['Stored Themperature'])
    self.functions.set_liquid_mass_or_volume(data['Liquid level'])
    self.select_senario()
    self.functions.set_area_and_type_of_leak(
      data['Leak through'],
      data['Opening Diameter (inches)'],
    )
    self.functions.set_height_of_the_tank_opening(data['Height of the Tank opening'])

    try:
      self.set_maximum_puddle_size()

      self.threat_zone(index)
      self.print_sumary(index)

    except:
      print('liquid level is too high')
      self.dlg['Height of the Tank Opening'].Dialog3.OK.click()
      self.dlg['Height of the Tank Opening'].type_keys('{ESC}')
      self.dlg['Area and Type of Leak'].type_keys('{ESC}')
      self.dlg['Type of Tank Failure'].type_keys('{ESC}')
      self.dlg['Liquid Mass or Volume'].type_keys('{ESC}')
      self.dlg['Chemical State and Temperature'].type_keys('{ESC}')
      self.dlg['Tank Size and Orientation'].type_keys('{ESC}')
      successful_run=False

    if successful_run:
      self.first_run = False

    return

  def select_senario(self) -> None:
    senario = self.dlg['Type of Tank Failure']
    senario.child_window(title='Leaking tank, chemical is burning and forms a pool fire', auto_id='7', control_type='RadioButton').click()
    senario.OK.click()
    try:
      senario.Dialog3.Yes.click()
    except:
      print('No dialog 3')
    return
  
  def set_maximum_puddle_size(self) -> None:
    puddle_parameters_dlg = self.dlg['Maximum Puddle Size']
    puddle_parameters_dlg.Ok.click()
    return

  def threat_zone(self, index=1):
    self.dlg.type_keys('^f')
    self.dlg['Thermal Radiation Level of Concern'].Ok.click()
    
    self.dlg['Thermal Radiation Threat Zone'].wait('visible')
    self.dlg['Thermal Radiation Threat Zone'].Cerrar.click()

    try:
      self.functions.export_threat_zone(
        first_run = self.first_run,
        lat_deg = self.lat_deg,
        lat_min = self.lat_min,
        long_deg = self.long_deg,
        long_min = self.long_min,
        index = index,
      )
    except:
      print('No treat zone graphics {0}'.format(index))
      self.dlg.type_keys('{ESC 2}')
