# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import location

class GetCurrentLocation(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
		
	def setup_params(self):
		self.params.append(ElementParameter(name='title',displayName='Title',display=True,type='string',value='Current Location'))
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return None
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'location'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Get current location of the device'
	
	def get_title(self):
		return 'Get Current Location'
		
	def get_icon(self):
		return 'iob:location_32'
		
	def get_category(self):
		return 'Location'
	
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		location.start_updates()
		loc = location.get_location()
		location.stop_updates()
		titleParam = self.get_param_by_name('title').value
		loc['title'] = titleParam or 'Current Location'
		return ElementValue(type = self.get_output_type(), value = loc)
