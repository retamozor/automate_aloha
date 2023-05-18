from pywinauto.application import WindowSpecification
from .Strategy import Strategy
import pandas as pd
import re
import sys

class Case_2(Strategy):

  def __init__(self, dlg: WindowSpecification, lat_deg, lat_min, long_deg, long_min) -> None:
    self.dlg = dlg
    self.lat_deg = lat_deg
    self.lat_min = lat_min
    self.long_deg = long_deg
    self.long_min =long_min
    self.first_run = True

  def set_up_chemical(self) -> None:
    self.dlg.type_keys('^h')
    chemical = self.dlg['Chemical Information']
    chemical_list = chemical.child_window(auto_id="6", control_type="List")
    chemical_list['CYCLOHEXANONE'].select()
    chemical.type_keys('{ENTER}')

  def print_sumary(self, index = 0):
    text = self.dlg['Text Summary'].child_window(auto_id="5001", control_type="Edit")
    # red_orange_yellow = text.get_value().split('THREAT ZONE: ')[1].splitlines()[2:5]
    sumary = text.get_value().split('THREAT ZONE: ')[1]
    red_orange_yellow = re.findall(' [Red|Orange|Yellow].*:.*meters.*---.*[(].*[)]', sumary)
    # for each line in red_orange_yellow: split by ':'

    colors = {'index': [index], 'Red': [''], 'Orange': [''], 'Yellow': ['']}
    for line in red_orange_yellow:
      color = line.split(': ')[0].strip()
      data = line.split(': ')[1].strip()
      #save in dict
      colors[color] = [data]

    # save in csv
    pd.DataFrame.from_dict(colors, orient='columns').to_csv(r'automate_aloha\out\caso_2\Colors.csv', mode='a', header=False)
    
    return
  
  def run(self, data, index) -> None:
    successful_run = True
    # Atmospheric Options
    self.setAtmospheric(data)
    self.setAtmospheric2(data)

    # Source Options
    self.setTankSizeAndOrientation(data)
    self.setChemicalStateAndTemperature(data)
    self.setLiquidMassOrVolume(data)
    self.selectSenario()
    self.setAreaAndTypeOfLeak(data)
    self.setHeightOfTheTankOpening(data)

    # try:
    self.setMaximumPuddleSize()

    self.threatZone(index)
    self.print_sumary(index)

    # except:
    #   print('liquid level is too high')
    #   self.dlg['Height of the Tank Opening'].Dialog3.OK.click()
    #   self.dlg['Height of the Tank Opening'].type_keys('{ESC}')
    #   self.dlg['Area and Type of Leak'].type_keys('{ESC}')
    #   self.dlg['Type of Tank Failure'].type_keys('{ESC}')
    #   self.dlg['Liquid Mass or Volume'].type_keys('{ESC}')
    #   self.dlg['Chemical State and Temperature'].type_keys('{ESC}')
    #   self.dlg['Tank Size and Orientation'].type_keys('{ESC}')
    #   successful_run=False

    if successful_run:
      self.first_run = False

    return

  def setAtmospheric(self, data):
    self.dlg.type_keys('^a')

    atmospheric = self.dlg['Atmospheric Options']

    wind_speed = atmospheric.child_window(
        title="Wind Speed is :", auto_id="4", control_type="Edit")
    wind_is_from = atmospheric.child_window(
        title="Wind is from    :", auto_id="10", control_type="Edit")

    if (data['Ground roughtness'] == 'open country'):
        ground_roughness = atmospheric.child_window(
            title="Open Country", auto_id="26", control_type="RadioButton")
    elif (data['Ground roughtness'] == 'Urban or forest'):
        ground_roughness = atmospheric.child_window(
            title="Urban or Forest", auto_id="27", control_type="RadioButton")
    else:
        ground_roughness = atmospheric.child_window(
            title="Open Water", auto_id="28", control_type="RadioButton")

    cloud_cover = atmospheric.child_window(
        auto_id="50", control_type="Edit")

    wind_speed.set_text(data['Wind speed'])
    wind_is_from.set_text(data['Wind is from'])
    ground_roughness.click()
    cloud_cover.set_text(data['Cloud cover'])
    atmospheric.OK.click()
    try:
      atmospheric.Dialog3.OK.click()
    except:
      print('No dialog')
    
    return

  def setAtmospheric2(self, data):
    atmospheric = self.dlg['Atmospheric Options 2']
    air_temperature = atmospheric.child_window(
      title="Air Temperature is :", auto_id="4", control_type="Edit")
    celcius = atmospheric.child_window(
      title="C", auto_id="7", control_type="RadioButton")
    humidity = atmospheric.child_window(
      title="(0 - 100)", auto_id="37", control_type="Edit")

    air_temperature.set_text(data['Air themperature'])
    celcius.click()
    humidity.set_text(data['Humidity'])

    # atmospheric.print_control_identifiers()
    atmospheric.OK.click()
    try:
      self.dlg['Note !Dialog'].OK.click()
    except:
      print('No dialog 2')
    return

  def setTankSizeAndOrientation(self, data):
    self.dlg.type_keys('^t')

    tank = self.dlg['Tank Size and Orientation']

    diameter = tank.child_window(auto_id="9", control_type="Edit")
    # meters = tank.child_window(
    #     title="meters", auto_id="13", control_type="RadioButton")
    length = tank.child_window(
        title="length", auto_id="15", control_type="Edit")
    
    if data["Tank Type"] == "Horizontal":
      tank.child_window(title=" ", auto_id="4", control_type="RadioButton").click()
      length.set_text(data['Tank length'])
    elif data["Tank Type"] == "vertical":
      tank.child_window(title=" ", auto_id="5", control_type="RadioButton").click()
      length.set_text(data['Tank length'])
    elif data["Tank Type"] == "Sphere":
      tank.child_window(title=" ", auto_id="6", control_type="RadioButton").click()

    diameter.set_text(data['Tank Diameter'])
    tank.meters.click()
    tank.OK.click()
    # tank.print_control_identifiers()
    return

  def setChemicalStateAndTemperature(self, data):
    tank = self.dlg['Chemical State and Temperature']
    tank.type_keys(data['Stored Themperature'])
    tank.type_keys('{ENTER}')
    return

  def setLiquidMassOrVolume(self, data):
    tank = self.dlg['Liquid Mass or Volume']
    liquid_level = tank.child_window(auto_id="11", control_type="Edit")

    liquid_level.set_text(data['Liquid level'])
    tank.OK.click()
    # tank.print_control_identifiers()
    return

  def selectSenario(self):
    senario = self.dlg['Type of Tank Failure']
    senario.child_window(title="Leaking tank, chemical is burning and forms a pool fire", auto_id="7", control_type="RadioButton").click()
    senario.OK.click()
    try:
      senario.Dialog3.Yes.click()
    except:
      print('No dialog 3')
    return

  def setAreaAndTypeOfLeak(self, data):
    area = self.dlg['Area and Type of Leak']
    diameter = area.child_window(title="Opening diameter:", auto_id="10", control_type="Edit")


    if (data['Leak through'] == "Hole"):
      leak_through = area.child_window(title="Hole", auto_id="23", control_type="RadioButton")
    else:
      leak_through = area.child_window(title="Short pipe/valve", auto_id="24", control_type="RadioButton")
      
    
    diameter.set_text(data['Opening Diameter (inches)'])
    leak_through.select()
    area.OK.click()
    # area.print_control_identifiers()

  def setHeightOfTheTankOpening(self, data):
    height_of_the_tank_openinght = self.dlg['Height of the Tank Opening']
    height = height_of_the_tank_openinght.child_window(title="OR", auto_id="11", control_type="Edit")

    height.set_text(data['Height of the Tank opening'])
    
    height_of_the_tank_openinght.OK.click()

  def setPuddleParameters(self):
    puddle_parameters = self.dlg['Puddle Parameters']
    puddle_parameters.Concrete.click()
    puddle_parameters.Ok.click()
  
  def setMaximumPuddleSize(self):
    puddle_parameters = self.dlg['Maximum Puddle Size']
    puddle_parameters.Ok.click()
    
  def setHazardToAnalyze(self):
    self.dlg['Hazard To Analyze'].wait('visible')
    hazard = self.dlg['Hazard To Analyze']
    hazard.child_window(title="Flammable Area of Vapor Cloud", auto_id="6", control_type="RadioButton").click()
    hazard.OK.click()
      
    self.dlg['.*Flamable Level.*'].OK.click()
    return

  def threatZone(self, index=1):
    self.dlg.type_keys('^f')
    self.dlg['Thermal Radiation Level of Concern'].Ok.click()
    
    self.dlg['Thermal Radiation Threat Zone'].wait('visible')
    self.dlg['Thermal Radiation Threat Zone'].Cerrar.click()

    try:
      self.exportThreatZone(index)
    except:
      print('No treat zone graphics {0}'.format(index))
      self.dlg.type_keys('{ESC 2}')

    

  def exportThreatZone(self, index=1):
    self.dlg.Menu3.File.select()
    self.dlg.FileDialog.File.MenuItem6.select()
    export = self.dlg['Export Threat Zones']
    if (self.first_run):
      export.RadioButton2.click()
      export.child_window(title="Longitude", auto_id="15", control_type="Edit").set_text(self.lat_deg)
      export.child_window(auto_id="16", control_type="Edit").set_text(self.lat_min)
      export.child_window(auto_id="20", control_type="Edit").set_text(self.long_deg)
      export.child_window(auto_id="21", control_type="Edit").set_text(self.long_min)
    export.Ok.click()
    self.dlg['.*Save Threat Zone.*'].type_keys(index)
    if (self.first_run):
      sys.stdout = sys.__stdout__
      input("Press Enter to continue...")
      sys.stdout = open(r'automate_aloha\logs\logs.txt', 'a')
    self.dlg['.*Save Threat Zone.*'].type_keys('{ENTER}')
  
