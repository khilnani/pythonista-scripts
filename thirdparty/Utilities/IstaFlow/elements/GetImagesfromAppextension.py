# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import appex
import console

class GetImagesfromAppextension(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return False
	
	def setup_params(self):
		self.params.append(ElementParameter(name='allowMultiple',displayName='Allow Multiple Images',display=True, type='bool',value=False))
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return None
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return 'image'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Returns a list or single image from the app extension'
	
	def get_title(self):
		return 'Get Image(s) from App extension'
		
	def get_icon(self):
		return 'iob:archive_32'
		
	def get_category(self):
		return 'App Extension'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		console.alert(title='Not complete', message='Does not work',button1='Ok',hide_cancel_button=True)
		if not appex.is_running_extension():
			console.alert(title='Error', message='Not running from app extension',button1='Ok',hide_cancel_button=True)
		else:
			try:
				allowMultiple = self.get_param_by_name('allowMultiple').value
				if allowMultiple:
					images = appex.get_images()
				else:
					images = appex.get_image()
				ev = ElementValue(type='image',value=images)
				return ev
			except error:
				console.alert(title='Error', message='error: {}'.format(error),button1='Ok',hide_cancel_button=True)
		