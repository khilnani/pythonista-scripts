# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
from  objc_util import *
import console

class OpenLocationinGoogleMaps(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
		
	def setup_params(self):
		self.params.append(ElementParameter(name='mapmode',displayName='Map Mode',display=True,type='list',value='standard',allowedValues=['standard','streetview']))
		self.params.append(ElementParameter(name='viewmode',displayName='View Mode',display=True,type='list',value=None,allowedValues=['satellite', 'traffic', 'transit'],multipleAllowed=True))
		
		self.params.append(ElementParameter(name='zoom',displayName='Zoom',display=True,type='string',value='12'))
		
		self.params.append(ElementParameter(name='query',displayName='Query in area',display=True,type='string'))
	
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
		return 'Opens a location in the Google Maps app'
	
	def get_title(self):
		return 'Open Location in Google Maps'
		
	def get_icon(self):
		return 'iob:map_32'
		
	def get_category(self):
		return 'External App'
	
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		mapmodeparam = self.get_param_by_name('mapmode')
		viewsparam = self.get_param_by_name('viewmode')
		zoomparam = self.get_param_by_name('zoom')
		queryparam = self.get_param_by_name('query')
		url = 'comgooglemaps://?center={latitude},{longitude}'.format(**input.value)
		if mapmodeparam.value:
			url += '&mapmode='+ mapmodeparam.value 
		if viewsparam.value:
			url += '&views=' + viewsparam.value
		if zoomparam.value:
			url += '&zoom=' + zoomparam.value
		if queryparam.value:
			url += '&q=' + queryparam.value
		uia = ObjCClass('UIApplication').sharedApplication()
		if not uia.openURL_(nsurl(url)):
			console.alert(title='Error oppening App',message='Is Google Maps app installed?',button1='Ok',hide_cancel_button=True)
		self.status = 'complete'
