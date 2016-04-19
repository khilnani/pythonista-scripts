# coding: utf-8
import sys
if not '..' in sys.path:
	sys.path.append('..')
import time

from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
from views.MapView import MapView

sys.path.remove('..')
class ShowlocationonMap(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = None
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return True
	
	def setup_params(self):
		pass
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return 'location'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return None
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Shows a location or list of on a map'
	
	def get_title(self):
		return 'Show location on Map'
		
	def get_icon(self):
		return 'iob:map_32'
		
	def get_category(self):
		return 'Location'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		m = MapView()
		
		if input.isList:
			for loc in input.value:
				title = str(loc['latitude']) + ', ' + str(loc['longitude'])
				if 'title' in loc.keys():
					title = loc['title']
				m.add_pin(lat = loc['latitude'], lon = loc['longitude'],title=title)
		else:
			title = str(input.value['latitude']) + ', ' + str(input.value['longitude'])
			if 'title' in input.value.keys():
				title = input.value['title']
			m.add_pin(lat = input.value['latitude'], lon = input.value['longitude'],title=title)
		m.present()
		while m.on_screen:
			time.sleep(0.1)
		self.status = 'complete'
