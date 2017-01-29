# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import console
import photos

class SaveImagetoCameraRoll(ElementBase):
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
		return 'image'
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return None
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Saves input image to Camera Roll'
	
	def get_title(self):
		return 'Save Image to Camera Roll'
		
	def get_icon(self):
		return 'iob:camera_32'
		
	def get_category(self):
		return 'Image'

	def get_type(self):
		return self.type
		
	def run(self, input):
		try:
			if not photos.save_image(input.value):
				console.alert("didn't work")
		except error:
			console.alert('error: {}'.format(error))
		self.status = 'complete'
