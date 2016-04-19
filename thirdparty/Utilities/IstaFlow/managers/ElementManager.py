# coding: utf-8
import os
# from os import listdir # -> Is not an issue however it is neater to just import os
# from os.path import isfile, join, splitext # --> join is a builtin method causing name space issues
from importlib import import_module
import sys
import copy
sys.path.append('elements')


class ElementManager (object):
	def __init__(self):
		self.elementsFolder = 'elements'
		self.elementExclusionList = ('ElementBase.py','__init__.py','Template.py','ElementParameter.py','ElementValue.py')
		self.requiredElementInstanceMethods = ('get_status', 'get_input', 'get_output','get_input_type', 'get_output_type', 'get_params','set_params', 'get_description', 'get_title','get_category', 'get_icon', 'run')
		self.extraElements = {'For':['End For'], 'Foreach':['End Foreach']}
		sys.path.append('elements')

	def get_all_elements(self, element_type=None):
		elements = [
		os.path.splitext(f) for f in os.listdir(self.elementsFolder)
		if os.path.isfile(os.path.join(self.elementsFolder, f)) and
		not f in self.elementExclusionList
		]
		validElements = []
		invalidElements = []
		for i in elements:
			mod = import_module(i[0])
			reload(mod)
			klass = getattr(mod,i[0])
			klassIsValid = True
			for method in self.requiredElementInstanceMethods:
				if not hasattr(klass, method):
					klassIsValid = False
					break
			if klassIsValid:
				validElements.append(klass())
			else:
				invalidElements.append(klass())

		if not element_type:
			return {'valid':validElements, 'invalid':invalidElements}
		elif element_type == 'valid':
			return validElements
		elif element_type == 'invalid':
			return inValidElements
		else:
			return []

	def get_extra_elements_for_element(self, element):
		elementsToReturn = []
		if element.get_title() in self.extraElements:
			for ele in self.extraElements[element.get_title()]:
				elementsToReturn.append(self.get_element_with_title(ele))
		return elementsToReturn
		
	def get_element_class(self, element):
		# The element class is element.__class__
		return element.__class__.__name__

	def get_element_with_title(self, title):
		elements = self.get_all_elements('valid')
		for element in elements:
			if element.get_title() == title:
				return copy.deepcopy(element)
		return None

	def create_element(self, title, inputType, outputType, description, icon, category, canHandleList):
		if not inputType == None:
			inputType = "'"+inputType+"'"
		if not outputType == None:
			outputType = "'"+outputType+"'"
		titleValidated = title.replace(" ","")
		templatePath = os.path.join(self.elementsFolder, 'Template.py')
		elementPath = os.path.join(self.elementsFolder, "{fileName}.py".format(fileName=titleValidated))
		if os.path.isfile(elementPath):
			print 'Element Already Exists'
			return
		with open(templatePath, 'r') as f:
			# str.format thinks that on line 8 ```self.params = {}``` and
			# on line 27 ```def set_params(self, params = {})``` are fomatting values
			tem = f.read().format(**{'title':titleValidated, 'title_space':title, 'input_type':inputType, 'output_type':outputType,'description':description,'icon':icon,'category':category,'canHandleList':canHandleList})
		with open(elementPath, 'w') as f:
			f.write(tem)


if __name__ == '__main__':
	sys.path[-1] = '../elements'
	ElementManager.elementsFolder = '../elements'
	manager = ElementManager()
	print manager.get_all_elements()
	print manager.get_element_with_title('newElement')
	manager.create_element('newElement1')