# coding: utf-8

# @lukaskollmer
# https://gist.github.com/anonymous/92dcfb41c7c9ca7c671112627b25247a


from objc_util import *
import sys
import console
import webbrowser

LSApplicationWorkspace = ObjCClass('LSApplicationWorkspace')

workspace = LSApplicationWorkspace.defaultWorkspace()


# Get all installed apps
apps = workspace.allApplications()

# Get all public URL schemes
public_url_schemes = workspace.publicURLSchemes()

# Get app private URL schemes
private_url_schemes = workspace.privateURLSchemes()

# Open app with bundle ID (does not require root access!, user not asked)
#workspace.openApplicationWithBundleID_('me.kollmer.MattSnake')


def get_application_with_bundle_id(bundle_id):
	app = workspace.allApplications()[0]
	print('\n'.join(dir(app)))
	print(app.appTags())
	print(bundle_id)
	for app in workspace.allApplications():
		print(app.itemName(), app.applicationIdentifier())

if __name__ == '__main__':
	console.clear()

	#notes = get_application_with_bundle_id('com.apple.noteswpponipad')

	#print(notes)

	#sys.exit()
	print('*'*10 + ' .allApplications() ' + '*'*10)
	print(apps)
	print('\n'*3)

	print('*'*10 + ' .publicURLSchemes() ' + '*'*10)
	print(public_url_schemes)
	print('\n'*3)

	print('*'*10 + ' .privateURLSchemes() ' + '*'*10)
	print(private_url_schemes)
	print('\n'*3)