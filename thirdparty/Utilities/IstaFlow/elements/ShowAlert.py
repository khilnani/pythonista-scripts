# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import console

class ShowAlert(ElementBase):
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
		return '*'
		
	def get_output(self):
		self.output
		
	def get_output_type(self):
		return None
		
	def get_params(self):
		return self.params
		
	def set_params(self, params=[]):
		self.params = params
		
	def get_description(self):
		return "This show an alert from the string that is in the input parameter"
	
	def get_title(self):
		return 'Show Alert'
		
	def get_icon(self):
		return 'iob:alert_circled_32'
		
	def get_category(self):
		return 'Utility'
		
	def get_type(self):
		return self.type
	
	def run(self, input):
		self.status = 'complete'
		input = str(input.value)
		title = __file__.rpartition('/')[2].partition('.')[0] or 'Message'
		console.alert(title=title, message=input, button1='Ok', hide_cancel_button=True)
