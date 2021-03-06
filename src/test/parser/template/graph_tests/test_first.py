import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.first import TemplateFirstNode
from programy.parser.template.nodes.word import TemplateWordNode
from test.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphFirstTests(TemplateGraphTestClient):

    def test_first(self):
        template = ET.fromstring("""
            <template>
                <first>one two three four</first>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertEquals(1, len(ast.children))

        first_node = ast.children[0]
        self.assertIsNotNone(first_node)
        self.assertIsInstance(first_node, TemplateFirstNode)

        self.assertIsNotNone(first_node.children)
        self.assertEquals(4, len(first_node.children))
        self.assertIsInstance(first_node.children[0], TemplateWordNode)

        self.assertEqual(ast.resolve(None, None), "one")

    def test_first_one_word(self):
        template = ET.fromstring("""
            <template>
                <first>one</first>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)

        self.assertEqual(ast.resolve(None, None), "one")

    def test_first_empty(self):
        template = ET.fromstring("""
            <template>
                <first></first>
            </template>
            """)
        ast = self.parser.parse_template_expression(template)

        self.assertEqual(ast.resolve(None, None), "NIL")


