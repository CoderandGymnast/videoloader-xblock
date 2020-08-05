"""An XBlock provides capability to store and load video on edX platform."""

import json
import pkg_resources

from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String, Boolean
from webob import Response
from django.core.files.storage import default_storage
from django.core.files import File
from django.template import Context, Template

# TODO: Read configuration from file.
CONFIG_PATH = "../config.yml"
def read_configuration(): 
	with open(CONFIG_PATH) as reader: 
		return

# TODO: Convert text.
def _(text):
	return text

class VideoLoaderXBlock(XBlock):
	"""
	An XBlock provides capability to store and load video on edX platform.
	"""

	display_name = String(
		display_name=_("Display Name"),
		help=_("Display name of the uploaded video"),
		default="HACHIUM lesson video", # XBlock automatically access "default" attribute.
		scope=Scope.settings,
	)

	# NOTE: Must declare url as String to get rid of errors.
	internal_video_url = String(
		default="",
		scope=Scope.settings,
	)

	message = String(
		default="'EDIT' this unit to add video.",
		scope=Scope.settings,
	)

	video_embedded_url = String(
		default="",
		scope=Scope.settings,
	)

	was_url_embedded = Boolean(
		default=False,
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

	# NOTE: Could not assign "Scope.settings" fields inside student view or error "xblock.exceptions.InvalidScopeError" would occur.
	def student_view(self, context=None):
		"""
		The primary view of the VideoLoader, shown to students
		when viewing courses.
		"""

		student_context = {
			"display_name": self.display_name,
			"video_embedded_url": self.video_embedded_url,
			"message": self.message,
			"internal_video_url": default_storage.url(self.internal_video_url) if self.internal_video_url else None,
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
			"display_name": self.fields["display_name"],
			"was_url_embedded": self.was_url_embedded,
			"videoloader_xblock": self,
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

		# NOTE: The following code snippet is used to store video on default storage of Django.
		# package_file = request.params["file"].file

		# path = default_storage.save(package_file.name, File(package_file))
		# self.internal_video_url = path

		self.display_name = request.params["display_name"]

		# TODO: Move these configuration to a seperated file.
		YOUTUBE_SHORT_VIDEO_URL_PREFIX = "https://youtu.be/"
		YOUTUBE_VIDEO_URL_PREFIX = "https://www.youtube.com/watch?v="
		YOUTUBE_EMBEDDED_URL_PREFIX = "https://www.youtube.com/embed/"

		video_url = request.params["video_url"]
		
		self.update_xblock_status(video_url)

		# NOTE: "0" is the starting index of the substring.
		if video_url.find(YOUTUBE_SHORT_VIDEO_URL_PREFIX) == 0:
			video_id = video_url[17:]
			self.video_embedded_url = YOUTUBE_EMBEDDED_URL_PREFIX + video_id
		elif video_url.find(YOUTUBE_VIDEO_URL_PREFIX) == 0:
			video_id = video_url[32:]
			self.video_embedded_url = YOUTUBE_EMBEDDED_URL_PREFIX + video_url[32:]
		elif video_url.find(YOUTUBE_EMBEDDED_URL_PREFIX) == 0: 
			self.video_embedded_url = video_url
		elif not video_url:
			self.video_embedded_url = None
		else: 
			self.video_embedded_url = YOUTUBE_EMBEDDED_URL_PREFIX + video_url

		# TODO: Handle errors.
		response = {"result": "success", "errors": []}
		return self.json_response(response)
	
	def update_xblock_status(self, video_url): 
		self.was_url_embedded = True if video_url else False

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
