# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.
import os
import octoprint.plugin
from octoprint.events import Events
from flask_babel import gettext # !! Note todo
# import pprint # !! Note

# On start detect
# On success no report else notification
# disable fan
# check mode if on start enable fan
PRINTMODE_STARTUP = "s"
PRINTMODE_PRINT = "p"

#https://docs.octoprint.org/en/master/plugins/gettingstarted.html

class FancontrolPlugin(octoprint.plugin.StartupPlugin,
					   octoprint.plugin.ShutdownPlugin,
					   octoprint.plugin.SettingsPlugin,
					   octoprint.plugin.TemplatePlugin,
					   octoprint.plugin.EventHandlerPlugin
					   ):

	##~~ StartupPlugin

	def on_after_startup(self):
		if self.is_enabled() and self._settings.get(['print_mode']) == PRINTMODE_STARTUP:
			self.enable_fan()

	##~~ ShutdownPlugin

	def on_shutdown(self):
		if self.is_enabled() and self._settings.get(['print_mode']) == PRINTMODE_STARTUP:
			self.disable_fan()

	##~~ SettingsPlugin

	def get_settings_defaults(self):
		return dict(
			enabled=True,
			gpio_pin=21,
			print_mode=PRINTMODE_STARTUP)

	##~~ TemplatePlugin

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False),
		]

	def on_event(self, event, payload):
		if self.is_enabled():
			if event == Events.PRINT_STARTED:
				self.enable_fan()
			elif event == Events.PRINT_DONE or event == Events.PRINT_FAILED:
				self.disable_fan()

		# self._logger.info("Got event " + event + " Payload " + pprint.pformat(payload))
		self._logger.info("Got event " + event )

	def is_gpio_enabled(self):
		os.path.isfile('./path_of_file')

	def is_enabled(self):
		return self._settings.get_boolean(["enabled"]) == True

	def enable_fan(self):
		self._logger.info("Should enable fans")

	def disable_fan(self):
		self._logger.info("Should shutdown fans")

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
		# for details.
		return dict(
			fancontrol=dict(
				displayName="Fancontrol Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="johnnymast",
				repo="OctoPrint-Fancontrol",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/johnnymast/OctoPrint-Fancontrol/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Fancontrol"


# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
# __plugin_pythoncompat__ = ">=2.7,<3" # only python 2
# __plugin_pythoncompat__ = ">=3,<4" # only python 3
# __plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = FancontrolPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
