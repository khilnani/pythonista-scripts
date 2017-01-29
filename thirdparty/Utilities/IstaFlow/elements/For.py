# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

class For(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = []
		self.type = 'For'
		self.setup_params()
	
	def can_handle_list(self):
		return False
	
	def setup_params(self):
		self.params.append(ElementParameter(name='forcount',displayName='For Loop Count',display=True,type='int',value=1))
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return None
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return None
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return 'For Loop'
	
	def get_title(self):
		return 'For'
		
	def get_icon(self):
		return 'iob:arrow_return_right_32'
		
	def get_category(self):
		return 'Conditional'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		self.status = 'complete'
		return None
