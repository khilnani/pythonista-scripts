# coding: utf-8
# author: Shaun Hevey
# toast.py is the implementation of a android inspired toast for pythonista.

import ui
import time
def display_toast(view, help_text, width = 220, height = 110, show_duration=2, fade_duration=0.5, background_colour=(.42, .42, .42), text_colour= (.96, .96, .96), corner_radius=10):

	w, h = ui.get_screen_size()

	help_view = ui.View(frame=((w/2)-(width/2),(h/2)-height, width, height))
	help_view.background_color = background_colour
	help_view.corner_radius = corner_radius

	label = ui.Label()
	label.text = help_text
	label.flex = 'H'
	label.width = help_view.width * 0.9
	label.alignment = ui.ALIGN_CENTER
	label.x = (help_view.width / 2) - (label.width / 2)
	label.y = (help_view.height / 2) - (label.height / 2)
	label.number_of_lines = 3

	label.text_color = text_colour

	help_view.add_subview(label)

	def animation_fade_in():
		help_view.alpha = 1.0
	def animation_fade_out():
		help_view.alpha = 0.0

	help_view.alpha = 0.0
	view.add_subview(help_view)
	ui.animate(animation_fade_in, duration=fade_duration)
	time.sleep(show_duration+fade_duration)
	ui.animate(animation_fade_out, duration=fade_duration)
	time.sleep(fade_duration)
	view.remove_subview(help_view)

if __name__=='__main__':
	view = ui.View()
	view.flex = 'WH'
	view.background_color = (1.0, 1.0, 1.0)
	view.present()
	display_toast(view=view, help_text='Show me a toast in pythonista')