"""Stylesheets of browser/static, as served (++plone++plonetheme.imioapps/<name>)."""

from plonetheme.imioapps.testing import DMS_INTEGRATION

import unittest


def normalize(text):
    return " ".join(text.split())


class StaticTestCase(unittest.TestCase):

    layer = DMS_INTEGRATION

    def css(self, name):
        """Stylesheet as served, whitespace normalized."""
        request = self.layer["request"]
        resource = self.layer["portal"].restrictedTraverse(
            "++plone++plonetheme.imioapps/" + name
        )
        return normalize(b"".join(resource(request, request.response)).decode("utf-8"))


class TestImioappsCss(StaticTestCase):
    def test_imioapps_css(self):
        css = self.css("imioapps.css")
        # images of the skin layers at the portal root (the bundle is served at portal_url/++plone++...)
        self.assertIn("background-image: url('../search_button_icon.png');", css)
        # F4 sticky header and navigation bar, F6 red header on the test instances
        self.assertIn("#content-header { position: sticky; top: 0; z-index: 50;", css)
        self.assertIn(
            "#mainnavigation-wrapper { position: sticky; top: var(--imioapps-header-height, 0px); z-index: 50;",
            css,
        )
        self.assertIn(
            "body.imioapps-test-instance { --imioapps-header-bg: #d00; --imioapps-nav-bg: #d00; }",
            css,
        )
        # F5 sticky dashboard table header (heights computed by skin.js)
        self.assertIn(
            "table.faceted-table-results th { position: sticky; "
            "top: calc(var(--imioapps-sticky-height, 0px) - 1px); z-index: 45; }",
            css,
        )
        # F16 workflow state badges, esign states and signers
        self.assertIn(
            ".viewlet_workflowstate span[class^='state-'] { border-radius: 0.5em 0.5em 0.5em 0.5em; "
            "padding: 0 0.5em; color: white !important;",
            css,
        )
        self.assertIn(
            ".viewlet_workflowstate span.state-to_do { background-color: blue; border-color: blue; }",
            css,
        )
        self.assertIn("span.signer-refused { color: red; }", css)
        self.assertIn(
            "span.state-title-refused, span.state-title-errored { color: orange; }", css
        )
        # F9 help icon
        self.assertIn("#imioapp-help { margin: 0 0.5em; }", css)


class TestDmsmailskinCss(StaticTestCase):
    def test_dmsmailskin_css(self):
        css = self.css("dmsmailskin.css")
        self.assertIn(
            "#plone-contentmenu-add-to-default-page { display: none !important; }", css
        )
        self.assertIn(
            ".viewlet_workflowstate { float: right; display: inline-block; }", css
        )
        self.assertIn(
            ".template-view label .required:after, #fieldset-versions legend { display: none; }",
            css,
        )
