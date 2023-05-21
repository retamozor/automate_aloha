from pywinauto.application import WindowSpecification
import sys

class Functions:
	def __init__(self, dlg: WindowSpecification) -> None:
		self.dlg = dlg
		return

	def set_up_chemical(self, chemical: str) -> None:
		self.dlg.type_keys("^h")
		chemical_dlg = self.dlg["Chemical Information"]

		chemical_list = chemical_dlg.child_window(
			auto_id="6",
			control_type="List",
		)

		chemical_list[chemical].select()
		chemical_dlg.type_keys("{ENTER}")
		return

	def set_building_type(self, building: str) -> None:
		self.dlg.Menu3.SiteData.select()

		self.dlg.SiteDataDialog.SiteData.child_window(
			title="Building Type...",
			auto_id="302",
			control_type="MenuItem",
		).select()

		building_dlg = self.dlg["Infiltration Building Parameters"]

		if building == "Enclosed office":
			building_btn = building_dlg.child_window(
				title="Enclosed office building", auto_id="4", control_type="RadioButton")

		elif building == "Single office":
			building_btn = building_dlg.child_window(
				title="Single storied building", auto_id="5", control_type="RadioButton")

		else:
			building_btn = building_dlg.child_window(
				title="Double storied building", auto_id="6", control_type="RadioButton")

		building_btn.select()
		building_dlg.Ok.click()

		return

	def set_atmospheric_options(
		self,
		ground_roughness: str,
		wind_speed: str, 
		wind_is_from: str, 
		cloud_cover: str
	) -> None:
		self.dlg.type_keys('^a')

		atmospheric_dlg = self.dlg['Atmospheric Options']

		wind_speed_edt = atmospheric_dlg.child_window(
			title="Wind Speed is :",
			auto_id="4",
			control_type="Edit",
		)

		wind_is_from_edt = atmospheric_dlg.child_window(
			title="Wind is from    :",
			auto_id="10",
			control_type="Edit",
		)

		if (ground_roughness == 'open country'):
			ground_roughness_btn = atmospheric_dlg.child_window(
				title="Open Country",
				auto_id="26",
				control_type="RadioButton",
			)

		elif (ground_roughness == 'Urban or forest'):
			ground_roughness_btn = atmospheric_dlg.child_window(
				title="Urban or Forest",
				auto_id="27",
				control_type="RadioButton",
			)

		else:
			ground_roughness_btn = atmospheric_dlg.child_window(
				title="Open Water",
				auto_id="28",
				control_type="RadioButton",
			)

		cloud_cover_edt = atmospheric_dlg.child_window(
			auto_id="50",
			control_type="Edit",
		)

		wind_speed_edt.set_text(wind_speed)
		wind_is_from_edt.set_text(wind_is_from)
		ground_roughness_btn.click()
		cloud_cover_edt.set_text(cloud_cover)

		atmospheric_dlg.OK.click()

		try:
			atmospheric_dlg.Dialog3.OK.click()
		except:
			print('No Atmospherical dialog')

		return

	def set_atmospheric_options_2(self, air_temperature: str, humidity: str) -> None:
		atmospheric_2_dlg = self.dlg['Atmospheric Options 2']

		air_temperature_edt = atmospheric_2_dlg.child_window(
			title="Air Temperature is :",
			auto_id="4", 
			control_type="Edit",
		)

		celcius = atmospheric_2_dlg.child_window(
			title="C",
			auto_id="7",
			control_type="RadioButton",
		)

		humidity_edt = atmospheric_2_dlg.child_window(
			title="(0 - 100)",
			auto_id="37",
			control_type="Edit",
		)

		air_temperature_edt.set_text(air_temperature)
		celcius.click()
		humidity_edt.set_text(humidity)

		atmospheric_2_dlg.OK.click()

		try:
			self.dlg['Note !Dialog'].OK.click()
		except:
			print('No dialog 2')
		return

	def set_tank_size_and_orientation(self, tank_type: str, tank_length: str, tank_diameter: str) -> None:
		self.dlg.type_keys('^t')

		tank_dlg = self.dlg['Tank Size and Orientation']

		diameter_edt = tank_dlg.child_window(auto_id="9", control_type="Edit")

		length_edt = tank_dlg.child_window(title="length", auto_id="15", control_type="Edit")
		
		if tank_type == "Horizontal":
			tank_dlg.child_window(title=" ", auto_id="4", control_type="RadioButton").click()
			length_edt.set_text(tank_length)

		elif tank_type == "vertical":
			tank_dlg.child_window(title=" ", auto_id="5", control_type="RadioButton").click()
			length_edt.set_text(tank_length)

		elif tank_type == "Sphere":
			tank_dlg.child_window(title=" ", auto_id="6", control_type="RadioButton").click()

		diameter_edt.set_text(tank_diameter)
		tank_dlg.meters.click()
		tank_dlg.OK.click()
		return
	
	def set_chemical_state_and_temperature(self, temperature: str) -> None:
		tank_dlg = self.dlg['Chemical State and Temperature']
		tank_dlg.type_keys(temperature)
		tank_dlg.type_keys('{ENTER}')
		return

	def set_liquid_mass_or_volume(self, level: str) -> None:
		tank_dlg = self.dlg['Liquid Mass or Volume']
		liquid_level = tank_dlg.child_window(auto_id='11', control_type='Edit')

		liquid_level.set_text(level)
		tank_dlg.OK.click()
		return

	def set_area_and_type_of_leak(self, leak_through: str, opening_diameter: str) -> None:
		area_dlg = self.dlg['Area and Type of Leak']
		opening_diameter_edt = area_dlg.child_window(title='Opening diameter:', auto_id='10', control_type='Edit')

		if (leak_through == 'Hole'):
			leak_through_btn = area_dlg.child_window(title='Hole', auto_id='23', control_type='RadioButton')
		else:
			leak_through_btn = area_dlg.child_window(title='Short pipe/valve', auto_id='24', control_type='RadioButton')
			
		opening_diameter_edt.set_text(opening_diameter)
		leak_through_btn.select()

		area_dlg.OK.click()
		return

	def set_height_of_the_tank_opening(self, height) -> None:
		height_dlg = self.dlg['Height of the Tank Opening']
		height_edt = height_dlg.child_window(title='OR', auto_id='11', control_type='Edit')

		height_edt.set_text(height)
		
		height_dlg.OK.click()
		return

	def export_threat_zone(self, first_run: bool, lat_deg: str, lat_min: str, long_deg: str, long_min: str,index=1):
		self.dlg.Menu3.File.select()
		self.dlg.FileDialog.File.MenuItem6.select()

		export_dlg = self.dlg['Export Threat Zones']

		if (first_run):
			export_dlg.RadioButton2.click()
			export_dlg.child_window(title='Longitude', auto_id='15', control_type='Edit').set_text(lat_deg)
			export_dlg.child_window(auto_id='16', control_type='Edit').set_text(lat_min)
			export_dlg.child_window(auto_id='20', control_type='Edit').set_text(long_deg)
			export_dlg.child_window(auto_id='21', control_type='Edit').set_text(long_min)
		
		export_dlg.Ok.click()

		# write file name
		self.dlg['.*Save Threat Zone.*'].type_keys(index)
		
		# wait user input path to save file
		if (first_run):
			sys.stdout = sys.__stdout__
			input('Press Enter to continue...')
			sys.stdout = open(r'automate_aloha\logs\logs.txt', 'a')

		# save file
		self.dlg['.*Save Threat Zone.*'].type_keys('{ENTER}')