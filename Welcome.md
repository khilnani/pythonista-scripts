#  Welcome to Pythonista

Thank you for downloading Pythonista! You now have everything you need to build and run Python scripts directly on your iPhone or iPad. 

To give you an idea of what you can do with the app, various sample scripts are included in the *Examples* folder. Feel free to use them as starting points for your own experiments. To share your creations, get help with coding problems, or just to meet fellow Pythonistas, please visit our [community forum](http://forum.omz-software.com).


#  Getting Started

If you're new to Pythonista, here are some tips to help you get up and running:

*	To create a new script, first tap `≡` to reveal the library, then `+` (at the bottom). You can also use left and right swipe gestures to switch between the file browser, editor, and console panels.

*	The settings ("gear" button in the file browser) contain useful options to customize the editor font, color theme, indentation type (tabs/spaces), and much more.

*	Swipe left to show the **console** panel. This is where text output appears, and you can use the prompt at the bottom to evaluate individual lines of Python code directly.

*	You'll also find the included **documentation** in the console panel; simply tap the `(?)` button to open it in a separate tab. Reference documentation is also available while you're editing code -- simply select a word (e.g. a function name), and choose *Help…* from the menu.

*	For easier navigation in long scripts, tap the file name at the top to show a list of classes and functions. This is also where you can rename the current file.

*	If you enjoy coding in Pythonista, please consider leaving a rating or review in the App Store. Thank you!
	💚

#  Tips

*	Tap and hold the run (▷) button for some additional options, e.g. to pass arguments (`sys.argv`) to your scripts, or to run the integrated PEP8 style checker.

*	Tap the *Edit* button in the "wrench" menu to add your own script shortcuts there. You can use this to launch your favorite scripts more quickly, or to extend the editor's functionality with the `editor` module.

*	A lot of keys on Pythonista's extra keyboard row have multiple mappings. For example, you can tap and hold the tab key to get an unindent option.

*	Tap with two fingers in the editor to select an entire line of code.

*	You can run Pythonista scripts directly within other apps that support the standard iOS share sheet. To get started, open the share sheet in a supported app (e.g. Safari, Notes, Maps...) and select "More..." to add the Pythonista action extension. You can use the `appex` module to access data that was passed to the share sheet (e.g. the current URL in Safari, location data in Maps, etc.).

*	If you use Pythonista with an external (Bluetooth) keyboard, you can show a list of available shortcuts by pressing and holding the `Cmd` key.

*	Swipe left on a file in the script library to open it in a new tab or move it to the trash. 


#  What's New in 3.1

For full release notes, please have a look at the "What's New in Pythonista" section in the documentation. These are just the highlights:

*	The console contains a new object inspector panel that allows you to view a list of all global variables and their attributes/members. Tap the `(i)` button to show or hide it.

*	The new Pythonista Today widget allows you to run a script in Notification Center (or on the home/lock screen). You can find more information in the `appex` module documentation, and various examples of widget scripts are available in the updated *Examples* folder.

*	Python 2 mode now uses Python 2.7.12 instead of 2.7.5.

*	When using the share sheet extension with a file input (e.g. sharing a Mail attachment), an additional "Import File" option is shown for non-Python files.

*	The `speech` module contains new functions for speech recognition, in addition to speech synthesis (iOS 10 only).

*	The `sound` module contains a new `Recorder` class for recording audio files from the microphone. `sound.play_effect` and `sound.Player` have also been improved to support stereo panning.


# Feedback

I hope you enjoy coding in Pythonista. If you have any feedback, please send an email to <pythonista@omz-software.com>, or visit the [community forum][forum] to share code and get help with your programming questions. You can also find me on Twitter:[@olemoritz][twitter].

---

[forum]: https://forum.omz-software.com
[twitter]: http://twitter.com/olemoritz
