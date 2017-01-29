# coding: utf-8
class ElementValue (object):
	def __init__(self, type, value, isList=False):
		self.type = type
		self.value = value
		self.isList = isinstance(value, list)