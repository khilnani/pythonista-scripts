# coding: utf-8
import ui
import console
import AssetPickerView

dbo = None
class ElementCreationView(object):
	def __init__(self, saveCallBack, showAssetPickerCallBack, closeAssetPickerCallBack, thememanager):
		self.saveCallBack = saveCallBack
		self.numberOfRows = 7
		self.titleRow = 0
		self.inputTypeRow = 1
		self.outputTypeRow = 2
		self.descriptionRow = 3
		self.iconRow = 4
		self.categoryRow = 5
		self.canHandleListRow = 6
		self.title = ''
		self.inputType = None
		self.outputType = None
		self.description = ''
		self.icon = ''
		self.category = ''
		self.canHandleList = False
		self.showAssetPickerCallBack = showAssetPickerCallBack
		self.closeAssetPickerCallBack = closeAssetPickerCallBack
		self.assetPickerView = AssetPickerView.get_view(self.set_iconcb)
		self.thememanager = thememanager
	
	def reset_view(self):
		self.title = ''
		self.inputType = None
		self.outputType = None
		self.description = ''
		self.icon = ''
		self.category = ''
		
	def tableview_did_select(self, tableview, section, row):
		if row == self.titleRow:
			self.change_title()
		elif row == self.inputTypeRow:
			self.change_input_type()
		elif row == self.outputTypeRow:
			self.change_output_type()
		elif row == self.descriptionRow:
			self.change_description()
		elif row == self.iconRow:
			self.change_icon()
		elif row == self.categoryRow:
			self.change_category()
		
	def tableview_title_for_header(self, tableview, section):
		pass

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return self.numberOfRows
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('value1')
		if row == self.titleRow:
			cell.text_label.text = 'Title'
			if self.title.strip(' ') == '':
				cell.detail_text_label.text = 'Please enter a title'
			else:
				cell.detail_text_label.text = self.title
		elif row == self.inputTypeRow:
			cell.text_label.text = 'Input Type'
			if self.inputType == None:
				cell.detail_text_label.text = 'None'
			else:
				cell.detail_text_label.text = self.inputType
		elif row == self.outputTypeRow:
			cell.text_label.text = 'Output Type'
			if self.outputType == None:
				cell.detail_text_label.text = 'None'
			else:
				cell.detail_text_label.text = self.outputType
		elif row == self.descriptionRow:
			cell.text_label.text = 'Description'
			if self.description.strip(' ') == '':
				cell.detail_text_label.text = 'Please enter a description'
			else:
				cell.detail_text_label.text = self.description
		elif row == self.iconRow:
			cell.text_label.text = 'Icon'
			if self.icon.strip(' ') == '':
				cell.detail_text_label.text = 'Please choose a icon'
			else:
				cell.detail_text_label.text = self.icon
		elif row == self.categoryRow:
			cell.text_label.text = 'Category'
			if self.category.strip(' ') == '':
				cell.detail_text_label.text = 'Please enter a category'
			else:
				cell.detail_text_label.text = self.category
		elif row == self.canHandleListRow:
			cell.text_label.text = 'Can Handle List'
			cell.selectable = False
			switch = ui.Switch()
			switch.name = 'canHandleList'
			switch.value = False
			switch.y = cell.center.y - switch.height/2
			switch.x = cell.width + switch.width/2   
			switch.action = self.canHandleListAction
			cell.add_subview(switch)
		cell.text_label.text_color = self.thememanager.main_text_colour
		cell.detail_text_label.text_color = self.thememanager.main_text_colour
		cell.background_color = self.thememanager.main_background_colour
		return cell
	
	def canHandleListAction(self, sender):
		self.canHandleList = sender.value
		
	@ui.in_background		
	def change_title(self):
		self.title = console.input_alert(title='Enter Element title', message='Space in title will be removed for filename and classname. If element with file exists it will be overwritten without warning.')
		table_view.reload()
		
	@ui.in_background		
	def change_input_type(self):
		self.inputType = console.input_alert(title='Enter Element Input type', message='Enter input type, enter an empty string for None')
		if self.inputType.strip(' ') == '':
			self.inputType = None
		table_view.reload()
		
	@ui.in_background		
	def change_output_type(self):
		self.outputType = console.input_alert(title='Enter Element Output type', message='Enter output type, enter an empty string for None')
		if self.outputType.strip(' ') == '':
			self.outputType = None
		table_view.reload()
	
	@ui.in_background		
	def change_description(self):
		self.description = console.input_alert(title='Enter Element Description', message='Enter a description for the element')
		table_view.reload()
	
	def set_iconcb(self, icon):
		self.icon = icon
		self.closeAssetPickerCallBack(self.assetPickerView)
		table_view.reload()
		
	@ui.in_background		
	def change_icon(self):
		self.showAssetPickerCallBack(self.assetPickerView)
	
	@ui.in_background		
	def change_category(self):
		self.category = console.input_alert(title='Enter Element Category', message='Enter the Element category, this is required')
		if self.category.strip(' ') == '':
			self.category = None
		table_view.reload()
		
	def create_element(self, sender):
		valid = True
		if self.title.strip(' ') == '':
			valid = False
			
		if valid:
			self.saveCallBack(title=self.title, inputType=self.inputType, outputType=self.outputType, description=self.description, icon=self.icon, category=self.category, canHandleList=self.canHandleList)
			self.reset_view()
		else:
			console.hud_alert('Invalid')

table_view = ui.TableView()
def get_view(savecb, apcb, capcb, thememanager):
	dbo = ElementCreationView(saveCallBack = savecb, showAssetPickerCallBack = apcb, closeAssetPickerCallBack = capcb, thememanager = thememanager)
	table_view.name = 'Element'
	table_view.data_source = dbo
	table_view.delegate = dbo
	table_view.right_button_items = [ui.ButtonItem(title='Save Element', action=dbo.create_element)]
	table_view.background_color = thememanager.main_background_colour
	return table_view


	