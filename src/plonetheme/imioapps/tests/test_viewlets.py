from collective.messagesviewlet.browser.messagesviewlet import GlobalMessagesViewlet
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plonetheme.imioapps.browser.viewlets import HelpViewlet
from plonetheme.imioapps.browser.viewlets import WorkflowState
from plonetheme.imioapps.interfaces import IThemeSpecific
from plonetheme.imioapps.testing import create_global_message
from plonetheme.imioapps.testing import HELP_URL_RECORD
from plonetheme.imioapps.testing import INTEGRATION
from Products.Five import BrowserView
from zope.component import getMultiAdapter
from zope.event import notify
from zope.interface import noLongerProvides
from zope.traversing.interfaces import BeforeTraverseEvent
from zope.viewlet.interfaces import IViewletManager

import unittest


def normalize(html):
    return " ".join(html.split())


class ViewletTestCase(unittest.TestCase):

    layer = INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        notify(BeforeTraverseEvent(self.portal, self.request))  # marks IThemeSpecific
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def request_without_layer(self):
        request = self.request.clone()
        noLongerProvides(request, IThemeSpecific)
        return request

    def viewlets(self, manager_name, context=None, request=None):
        """{name: viewlet} shown by the viewlet manager (hidden viewlets filtered out), in their order."""
        context = context or self.portal
        request = request or self.request
        manager = getMultiAdapter(
            (context, request, BrowserView(context, request)),
            IViewletManager,
            name=manager_name,
        )
        manager.update()
        return [(viewlet.__name__, viewlet) for viewlet in manager.viewlets]


class TestWorkflowState(ViewletTestCase):
    def test_state_infos(self):
        doc = self.portal.folder.doc
        viewlet = WorkflowState(doc, self.request, BrowserView(doc, self.request), None)
        self.assertEqual(
            viewlet.state_infos(), {"state_name": "private", "state_title": "Private"}
        )
        api.content.transition(doc, "publish")
        self.assertEqual(
            viewlet.state_infos(),
            {"state_name": "published", "state_title": "Published"},
        )

    def test_index(self):
        doc = self.portal.folder.doc
        viewlet = WorkflowState(doc, self.request, BrowserView(doc, self.request), None)
        viewlet.update()
        # label_state has no English text: empty label
        self.assertEqual(
            normalize(viewlet.render()),
            '<div class="viewlet_workflowstate"> <span></span>&nbsp; '
            '<span class="state-private">Private</span> </div>',
        )


class TestHelpViewlet(ViewletTestCase):
    def test_update(self):
        viewlet = HelpViewlet(
            self.portal, self.request, BrowserView(self.portal, self.request), None
        )
        viewlet.update()
        self.assertEqual(viewlet.help_url, "")
        api.portal.set_registry_record(HELP_URL_RECORD, "https://docs.imio.be/iadocs")
        viewlet.update()
        self.assertEqual(viewlet.help_url, "https://docs.imio.be/iadocs")

    def test_index(self):
        # registered in the header without layer
        for request in (self.request, self.request_without_layer()):
            self.assertIsInstance(
                dict(self.viewlets("plone.portalheader", request=request))[
                    "plonetheme.imioapps.help"
                ],
                HelpViewlet,
            )
        viewlet = dict(self.viewlets("plone.portalheader"))["plonetheme.imioapps.help"]
        self.assertEqual(normalize(viewlet.render()), "")
        api.portal.set_registry_record(HELP_URL_RECORD, "https://docs.imio.be/iadocs")
        viewlet.update()
        self.assertEqual(
            normalize(viewlet.render()),
            '<a id="imioapp-help" title="Help" accesskey="H" href="https://docs.imio.be/iadocs"> '
            '<img alt="" src="http://nohost/plone/help.png"/> </a>',
        )


class TestMessageViewlet(ViewletTestCase):
    """collective.messagesviewlet's GlobalMessagesViewlet, re-registered above the content for the theme layer
    (Plone 4: in the portal top, dropped by Barceloneta's Diazo rules on Plone 6)."""

    def test_render(self):
        create_global_message("<p>The site will be down tonight</p>")
        above = dict(self.viewlets("plone.abovecontent"))
        self.assertIsInstance(above["message-viewlet"], GlobalMessagesViewlet)
        html = normalize(above["message-viewlet"].render())
        self.assertIn('<div id="messagesviewlet">', html)
        self.assertIn('class="portalMessage error"', html)
        self.assertIn("<p>The site will be down tonight</p>", html)
        # hidden in the header (default profile), where collective.messagesviewlet registers it
        self.assertNotIn("message-viewlet", dict(self.viewlets("plone.portalheader")))
        # without the theme layer: only in the header (hidden there)
        request = self.request_without_layer()
        self.assertNotIn(
            "message-viewlet",
            dict(self.viewlets("plone.abovecontent", request=request)),
        )
        self.assertNotIn(
            "message-viewlet",
            dict(self.viewlets("plone.portalheader", request=request)),
        )
