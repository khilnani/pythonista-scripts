uicomponents
============

Various ui components for pythonista

- BoxLayout.py	in work, layout out compents in a row or column
- InputAlert.py	replacement for `console.input_alert` that works with ui.View.  Add to your root subview, then call inout_alert from a ui.in_backgrounded function

- PopupButton.py	custom button which pops up another subview when pressed and held.
- RootView.py	      A extendable RootView, which fixes get_keyboard_frame, get_orientation, and convert_point
- fixed_convert_and_kbframe.py	modularize better, created subclassable RootView	27 days ago
- flowcontrol.jpg	screenshot of uicontainer.FlowControl
- keyboard_example.jpg	screensHOT
- keyboard_example.py	Proof of concept of a custom keyboard 
- uiCheckBox.py	  checkbox type control
- uicontainer.py contains FlowContainer, which automatically wraps subviews
- AdvancedTextView   textView with programatic undo and redo capability
- ZoomView  touch zoomable and movable window
- TouchDispatcher  implements a way to intercept touch events before sending to underlying views
- TabbedView  implements a tab container
