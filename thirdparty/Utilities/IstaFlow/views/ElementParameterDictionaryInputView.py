# coding: utf-8
# coding: utf-8
import ui
import dialogs

class ElementParameterDictionaryInputView(object):
	def __init__(self):
		self.dictionary = {}
		self.thememanager = None

	def tableview_did_select(self, tableview, section, row):
		key = self.dictionary.keys()[row]
		value = self.dictionary[key]
		edit_item(key, value)
		
	def tableview_title_for_header(self, tableview, section):
		pass

	def tableview_number_of_sections(self, tableview):
		return 1

	def tableview_number_of_rows(self, tableview, section):
		return len(self.dictionary.keys())
		
	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('value1')
		key = self.dictionary.keys()[row]
		cell.text_label.text = key
		cell.detail_text_label.text = self.dictionary[key]
		cell.background_color = self.thememanager.main_background_colour
		cell.text_label.text_color = self.thememanager.main_text_colour
		cell.detail_text_label.text_color = self.thememanager.main_text_colour
		cell.selectable = True
		return cell
	
	def tableview_can_delete(self, tableview, section, row):
		return True
	
	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		key = self.dictionary.keys()[row]
		self.dictionary.pop(key)
		del_row([row])

table_view = ui.TableView()	
dbo = ElementParameterDictionaryInputView()	
def get_view(thememanager, dictionary={}, title='Dictionary', cb=None):
	dicti = dictionary
	if dicti == None:
	 dicti = {}
	dbo.dictionary=dicti
	dbo.thememanager = thememanager
	table_view.name = title
	table_view.data_source = dbo
	table_view.delegate = dbo
	table_view.right_button_items = [ui.ButtonItem(title='Add', action = add_item), ui.ButtonItem(title='Save', action=cb)]
	table_view.background_color=thememanager.main_background_colour
	return table_view

@ui.in_background
def edit_item(key, value):
	values = dialogs.form_dialog(title='Edit Item', fields=[{'type':'text', 'title':'Key', 'value':key},{'type':'text', 'title':'Value', 'value':value}])
	if not values == None:
		dbo.dictionary[values['Key']] = values['Value']
		table_view.reload()
	
def add_item(sender):
	values = dialogs.form_dialog(title='Add Item', fields=[{'type':'text', 'title':'Key'},{'type':'text', 'title':'Value'}])
	if not values == None:
		dbo.dictionary[values['Key']] = values['Value']
		table_view.reload()
		
def del_row(row):
	table_view.delete_rows(row)