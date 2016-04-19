# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

class ForEach(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = None
		self.type = 'Foreach'
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
		return self.output
		
	def get_output_type(self):
		return '*'
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'Pull each element of a list out'
	
	def get_title(self):
		return 'Foreach'
		
	def get_icon(self):
		return 'iob:arrow_return_right_32'
		
	def get_category(self):
		return 'Conditional'
	
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		if not isinstance(input.value, list):
			print 'List not provided to foreach'
		self.status = 'complete'
		return input
