# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

from objc_util import *

class OpenLocationinAppleMaps(ElementBase):
	map_mode_dict = {'standard': 'm', 'satellite': 'k', 'hybrid': 'h', 'transit': 'r'}

	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
		
	def setup_params(self):
		self.params.append(ElementParameter(name='mapmode',displayName='Map Mode',display=True,type='list',value='standard',allowedValues=sorted(self.map_mode_dict.keys())))
		self.params.append(ElementParameter(name='zoom',displayName='Zoom',display=True,type='string',value='12'))
	
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
		return 'Opens a location in the Apple Maps app'
	
	def get_title(self):
		return 'Open Location in Apple Maps'
		
	def get_icon(self):
		return 'iob:map_32'
		
	def get_category(self):
		return 'External App'
	
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		mapmodeparam = self.get_param_by_name('mapmode')
		zoomparam = self.get_param_by_name('zoom')
		url = 'http://maps.apple.com/?ll={latitude},{longitude}'.format(**input.value)
		mm = self.map_mode_dict.get(mapmodeparam.value, '')
		if mm:
			url += '&t=' + mm 
		if zoomparam.value:
			url += '&z=' + zoomparam.value
		uia = ObjCClass('UIApplication').sharedApplication()
		if not uia.openURL_(nsurl(url)):
			console.alert(title='Error oppening App',message='Something went wrong!',button1='Ok',hide_cancel_button=True)
		self.status = 'complete'
