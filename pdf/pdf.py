""" pdfXBlock main Python class"""

import importlib.resources as pkg_resources
from django.template import Context, Template

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, Boolean
from xblock.fragment import Fragment
from xblockutils.resources import ResourceLoader

from . import static

class pdfXBlock(XBlock):
    loader = ResourceLoader(__name__)

    '''
    Icon of the XBlock. Values : [other (default), video, problem]
    '''
    icon_class = "other"

    '''
    Fields
    '''
    display_name = String(display_name="Display Name",
        default="PDF",
        scope=Scope.settings,
        help="This name appears in the horizontal navigation at the top of the page.")

    url = String(display_name="PDF URL",
        default="http://tutorial.math.lamar.edu/pdf/Trig_Cheat_Sheet.pdf",
        scope=Scope.content,
        help="The URL for your PDF.")
    
    allow_download = Boolean(display_name="PDF Download Allowed",
        default=True,
        scope=Scope.content,
        help="Display a download button for this PDF.")
    
    source_text = String(display_name="Source document button text",
        default="",
        scope=Scope.content,
        help="Add a download link for the source file of your PDF. Use it for example to provide the PowerPoint file used to create this PDF.")
    
    source_url = String(display_name="Source document URL",
        default="",
        scope=Scope.content,
        help="Add a download link for the source file of your PDF. Use it for example to provide the PowerPoint file used to create this PDF.")

    '''
    Util functions
    '''

    @staticmethod
    def resource_string(path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.read_text(static, path)
        return data.decode("utf8")

    def create_fragment(self, context, template, css, js, js_init):
        frag = Fragment()

        frag.add_content(
            self.loader.render_django_template(
                template,
                context=context,
            )
        )

        frag.add_css(self.resource_string(css))

        frag.add_javascript(self.resource_string(js))
        frag.initialize_js(js_init)
        self.include_theme_files(frag)
        return frag

    '''
    Main functions
    '''
    def student_view(self, context=None):
        """
        The primary view of the XBlock, shown to students
        when viewing courses.
        """
        
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'allow_download': self.allow_download,
            'source_text': self.source_text,
            'source_url': self.source_url
        }

        frag = self.create_fragment(
            context,
            template="static/html/pdf_view.html",
            css="static/css/pdf.css",
            js="static/js/pdf_view.js",
            js_init="pdfXBlockInitView"
        )

        return frag

    def studio_view(self, context=None):
        """
        The secondary view of the XBlock, shown to teachers
        when editing the XBlock.
        """
        context = {
            'display_name': self.display_name,
            'url': self.url,
            'allow_download': self.allow_download,
            'source_text': self.source_text,
            'source_url': self.source_url
        }

        frag = self.create_fragment(
            context,
            template="static/html/pdf_edit.html",
            css="static/css/pdf.css",
            js="static/js/pdf_edit.js",
            js_init="pdfXBlockInitEdit"
        )

        return frag

    @XBlock.json_handler
    def save_pdf(self, data, suffix=''):
        """
        The saving handler.
        """
        self.display_name = data['display_name']
        self.url = data['url']
        self.allow_download = True if data['allow_download'] == "True" else False # Str to Bool translation
        self.source_text = data['source_text']
        self.source_url = data['source_url']
        
        return {
            'result': 'success',
        }
