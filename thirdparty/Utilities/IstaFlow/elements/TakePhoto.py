# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import photos
import console
import time

class TakePhoto(ElementBase):
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
		return 'image'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Take a photo using the devices camera and returns it.'
		
	def get_title(self):
		return 'Take Photo'
		
	def get_icon(self):
		return 'iob:ios7_camera_32'
		
	def get_category(self):
		return 'Image'
		
	def get_type(self):
		return self.type
		
	def run(self):
		self.status = 'complete'
		#console.alert(title='Known Issue',message='Take Photo sometimes freezes the ui and pythonista needs to be killed.',button1='Ok',hide_cancel_button=True)
		time.sleep(.5)
		return ElementValue(type = self.get_output_type(), value = photos.capture_image())
