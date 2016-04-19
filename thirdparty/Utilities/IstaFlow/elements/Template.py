# coding: utf-8
from ElementBase import ElementBase
from ElementParameter import ElementParameter
from ElementValue import ElementValue

class {title}(ElementBase):
	def __init__(self):
		self.status = 'running'
		self.output = None 
		self.params = None
		self.type = 'Standard'
		self.setup_params()
	
	def can_handle_list(self):
		return {canHandleList}
	
	def setup_params(self):
		pass
	
	def get_status(self):
		return self.status
		
	def get_input_type(self):
		return {input_type}
	
	def get_output(self):
		return self.output
		
	def get_output_type(self):
		return {output_type}
		
	def get_params(self):
		return self.params
		
	def set_params(self, params = None):
		self.params = params or []
		
	def get_description(self):
		return '{description}'
	
	def get_title(self):
		return '{title_space}'
		
	def get_icon(self):
		return '{icon}'
		
	def get_category(self):
		return '{category}'
		
	def get_type(self):
		return self.type
		
	def run(self, input=''):
		#where the magic happens, put element logic here input is only used if input type is not None, return something if output type is not None, NOTE: for future changes please set self.status to 'complete' if successful or 'error' if error required
		pass
