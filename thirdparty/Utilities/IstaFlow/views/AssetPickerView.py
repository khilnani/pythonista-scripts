# coding: utf-8
# original script from https://forum.omz-software.com/topic/2440/asset-picker-in-a-scene/7

import os
import json
import ui
import scene
import Image

def get_asset_folder():
	try:
		p = os.path.dirname(scene.get_image_path('emj:Airplane'))[:-10]
	except:
		p = os.path.dirname(scene.get_image_path('Airplane'))+'/'
	return p

def get_collection_info(asset_type=''):
	folder = get_asset_folder()
	try:
		with open(folder+os.listdir(folder)[0], 'r') as f:
			return [asset for asset in json.load(f)['collections'] if asset['type'] == asset_type]
	except ValueError:
		return os.listdir(folder)

class AssetPicker (ui.View):
	def __init__(self, source, selected_cb, name='', dark_cells=False, object_type='none', parent=None):
		w, h = ui.get_screen_size()
		self.frame = (0, 0, w, h)
		self.name = name
		self.source = source
		self.dark_cells = dark_cells
		self.parent = parent
		self.object_type = object_type
		self.picked_asset = None
		self.selected_cb = selected_cb
		self.load_button_items()
		self.create_table_view()

	def is_main(self):
		return all([1 if isinstance(i, dict) else 0 for i in self.source])

	def load_button_items(self):
		if self.is_main():
			self.left_button_items = [ui.ButtonItem('Cancel', action=lambda s: self.navigation_view.close())]
		else:
			self.right_button_items = [ui.ButtonItem('Done', action=lambda s: self.navigation_view.close())]

	def create_table_view(self):
		table_view = ui.TableView()
		table_view.name = 'tableview'
		table_view.flex = 'WH'
		table_view.width = self.width
		table_view.height = self.height
		table_view.delegate = self
		table_view.data_source = self
		self.add_subview(table_view)

	def tableview_number_of_rows(self, tableview, section):
		return len(self.source)

	def tableview_cell_for_row(self, tableview, section, row):
		cell = ui.TableViewCell('subtitle')
		cell.accessory_type = 'disclosure_indicator'
		if self.is_main():
			text = self.source[row]['title']
			cell.text_label.text = text
			if 'copyright' in self.source[row]:
				cell.detail_text_label.text = self.source[row]['copyright']
		else:
			cell.text_label.text = self.source[row]
			tableview.row_height = 48
			cell.image_view.image = ui.Image.named(self.source[row])
			if self.dark_cells:
				cell.image_view.background_color = 'black'
		return cell

	def tableview_did_select(self, tableview, section, row):
		if not self.is_main():
			if self.parent:
				pass
				# do something with asset
			# example:
			self.selected_cb(self.source[row])
			self.navigation_view.pop_view()
			return		
		path = os.path.join(get_asset_folder(), self.source[row]['path'])
		if not os.path.isdir(path):
			with open(path, 'r') as f:
				source = eval(f.read())
		else:
			source = sorted(list(set([path.split('/')[-1]+':'+(i.split('@')[0] if '@' in i else i.split('.')[0]) for i in os.listdir(path)])))
		dark_cells = 1 if 'darkBackground' in self.source[row] else 0
		self.navigation_view.push_view(AssetPicker(source, name=self.source[row]['title'], dark_cells=dark_cells, object_type=self.object_type, parent=self.parent, selected_cb=self.selected_cb))

def get_view(selected_cb, parent=None, object_type='none'):
	source = get_collection_info(asset_type='image')
	main_view = AssetPicker(source, name='Assets', object_type=object_type, parent=parent, selected_cb=selected_cb)
	return main_view