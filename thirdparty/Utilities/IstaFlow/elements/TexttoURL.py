# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import console

class TexttoURL(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		pass
	
	def setup_params(self):
		self.params.append(ElementParameter(name='protocol',displayName='Protocol',display=True,type='list',value='http://',allowedValues=['http://','https://','ftp://']))
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return 'string'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'url'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = []):
		self.params = params
		
	def get_description(self):
		return 'Takes a string input and converts to a URL'
	
	def get_title(self):
		return 'Text to URL'
		
	def get_icon(self):
		return 'iob:ios7_world_outline_32'
		
	def get_category(self):
		return 'Url'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		stringUrl = input.value
		protoParam = self.get_param_by_name('protocol').value
		if not stringUrl:
			console.alert(title='Error',message='No url was given',button1='Ok',hide_cancel_button=True)
			return None
		if stringUrl[:len(protoParam)].find(protoParam) == -1:
			if not '//' in stringUrl:
				stringUrl = protoParam + stringUrl
			else:
				console.alert(title='Information',message='Url passed with incorrect protocol given',button1='Ok',hide_cancel_button=True)
		return ElementValue(type='url',value=stringUrl)
