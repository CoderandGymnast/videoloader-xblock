"""An XBlock provides capability to store and load video on edX platform."""

import json
import pkg_resources

from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
from webob import Response
from django.core.files.storage import default_storage
from django.core.files import File
from django.template import Context, Template

# TODO: Convert text.
def _(text):
	return text

class VideoLoaderXBlock(XBlock):
	"""
	An XBlock provides capability to store and load video on edX platform.
	"""

	display_name = String(
		display_name=_("Display Name"),
		help=_("Display name for this module"),
		default="Video module",
		scope=Scope.settings,
	)

	def render_template(self, template_path, context):
		template_str = self.resource_string(template_path)
		template = Template(template_str)
		return template.render(Context(context))

	@staticmethod
	def resource_string(path):
		"""Handy helper for getting static resources from our kit."""
		data = pkg_resources.resource_string(__name__, path)
		return data.decode("utf8")

	def student_view(self, context=None):
		"""
		The primary view of the VideoLoader, shown to students
		when viewing courses.
		"""

		student_context = {
			"display_name": self.display_name,
		}
		student_context.update(context or {})

		template = self.render_template("static/html/video_loader.html", student_context)
		frag = Fragment(template)
		frag.add_css(self.resource_string("static/css/video_loader.css"))
		frag.add_javascript(self.resource_string("static/js/src/video_loader.js"))
		frag.initialize_js("VideoLoaderXBlock")
		return frag

	def studio_view(self, context=None):
		"""
		The primary view of the VideoLoaderXBlock, shown to students
		when viewing courses.
		"""
		studio_context = {
			"display_name": self.display_name,
		}
		studio_context.update(context or {})

		template = self.render_template("static/html/video_persister.html", studio_context)
		frag = Fragment(template)
		frag.add_css(self.resource_string("static/css/video_persister.css"))
		frag.add_javascript(self.resource_string("static/js/src/video_persister.js"))
		frag.initialize_js("VideoPersisterXBlock")
		return frag

	@staticmethod
	def json_response(data):
		return Response(
			json.dumps(data), content_type="application/json", charset="utf8"
		)

	# TO-DO: change this handler to perform your own actions.  You may need more
	# than one handler, or you may not need any handlers at all.
	@XBlock.handler
	def studio_submit(self, request, _suffix):

		package_file = request.params["file"].file

		print("Uploaded file name: " + str(package_file.name))
		print("Uploaded file size: " + str(package_file.seek(0, 2)))

		default_storage.save(package_file.name, File(package_file))

		# TODO: Handle errors.
		response = {"result": "success", "errors": []}
		return self.json_response(response)

	# TO-DO: change this to create the scenarios you'd like to see in the
	# workbench while developing your XBlock.
	@staticmethod
	def workbench_scenarios():
		"""A canned scenario for display in the workbench."""
		return [
			("VideoLoaderXBlock", """<videoloader/> """),
			("Multiple VideoLoaderXBlock", """<vertical_demo>
				<videoloader/>
				<videoloader/>
				<videoloader/>
				</vertical_demo> """),
		]
