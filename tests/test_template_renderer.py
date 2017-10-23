from unittest import TestCase
from jen.template_renderer import TemplateRenderer


class TemplateRendererTestCase(TestCase):

    def setUp(self):
        self.renderer = TemplateRenderer('tests/site_example')


class HasPageTestCase(TemplateRendererTestCase):

    def test_simple_path(self):
        self.assertEqual(self.renderer.has_page('/simple'), True)

    def test_index_path(self):
        self.assertEqual(self.renderer.has_page('/'), True)

    def test_subdirectory_simple_path(self):
        self.assertEqual(self.renderer.has_page('/sub-without-index/simple'), True)

    def test_subdirectory_index(self):
        self.assertEqual(self.renderer.has_page('/sub-with-index'), True)

    def test_subdirectory_index_ending_on_slash(self):
        self.assertEqual(self.renderer.has_page('/sub-with-index/'), True)

    def test_missing_page(self):
        self.assertEqual(self.renderer.has_page('/missing'), False)

    def test_ignore_pages_that_starts_with_underscore(self):
        self.assertEqual(self.renderer.has_page('/_base'), False)


class TemplatesForPathTestCase(TemplateRendererTestCase):

    def test_simple_path(self):
        templates = self.renderer._templates_for_path('/simple')
        self.assertEqual(templates, ['simple.html', 'simple/index.html'])

    def test_index_path(self):
        templates = self.renderer._templates_for_path('/')
        self.assertEqual(templates, ['index.html'])

    def test_subdirectory_simple_path(self):
        templates = self.renderer._templates_for_path('/about/project')
        self.assertEqual(templates, ['about/project.html', 'about/project/index.html'])

    def test_subdirectory_index_path(self):
        templates = self.renderer._templates_for_path('/about')
        self.assertEqual(templates, ['about.html', 'about/index.html'])

    def test_path_with_last_part_ending_in_underscore(self):
        templates = self.renderer._templates_for_path('/_base')
        self.assertEqual(templates, [])


class RenderPageTestCase(TemplateRendererTestCase):

    def test_render_simple_page(self):
        rendered = self.renderer.render_page('/simple')
        self.assertEqual(rendered, '<body><h1>Simple</h1></body>')

    def test_render_index_page(self):
        rendered = self.renderer.render_page('/')
        self.assertEqual(rendered, '<body><h1>Index</h1></body>')

    def test_render_subdirectory_simple_page(self):
        rendered = self.renderer.render_page('/sub-without-index/simple')
        self.assertEqual(rendered, '<body><h1>Sub/Simple</h1></body>')

    def test_render_subdirectory_index_page(self):
        rendered = self.renderer.render_page('/sub-with-index')
        self.assertEqual(rendered, '<body><h1>Sub/Index</h1></body>')

    def test_render_subdirectory_index_with_path_ending_on_slash(self):
        rendered = self.renderer.render_page('/sub-with-index/')
        self.assertEqual(rendered, '<body><h1>Sub/Index</h1></body>')

    def test_ignore_pages_that_starts_with_underscore(self):
        rendered = self.renderer.render_page('/_base')
        self.assertEqual(rendered, None)
