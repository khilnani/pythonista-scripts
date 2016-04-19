# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue
import clipboard

class GetClipboardText(ElementBase):
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
		return 'string'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return "This gets the text value of the system clipboard"
	
	def get_title(self):
		return 'Get Clipboard Text'
		
	def get_icon(self):
		return 'iob:ios7_copy_32'
		
	def get_category(self):
		return 'Text'
	
	def get_type(self):
		return self.type
		
	def run(self):
		clip = clipboard.get()
		self.status = 'complete'
		return ElementValue(type = self.get_output_type(), value = clip)
