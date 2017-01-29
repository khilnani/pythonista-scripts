# coding: utf-8
# The get battery code is highly based of the battery level example in pythonista 2.0

from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
from objc_util import *

class GetBatteryDetails(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = None
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
		
	def setup_params(self):
		pass
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return None
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'battery'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Get details about the current state of the battery.'
	
	def get_title(self):
		return 'Get Battery Details'
		
	def get_icon(self):
		return 'iob:battery_half_32'
		
	def get_category(self):
		return 'Battery'
	
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		battery_states = {1: 'unplugged', 2: 'charging', 3: 'full'}
		device = ObjCClass('UIDevice').currentDevice()
		device.setBatteryMonitoringEnabled_(True)
		battery_percent = device.batteryLevel() * 100
		state = device.batteryState()
		device.setBatteryMonitoringEnabled_(False)
		batteryDetails = {'Level': battery_percent, 'State': battery_states.get(state, 'unknown')}
		self.status = 'complete'
		return ElementValue(type=self.get_output_type(), value=batteryDetails)
