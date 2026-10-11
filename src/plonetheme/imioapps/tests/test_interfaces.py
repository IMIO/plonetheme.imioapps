from collective.messagesviewlet.interfaces import ICollectiveMessagesviewletLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.base.utils import get_installer
from plonetheme.imioapps.interfaces import IThemeSpecific
from plonetheme.imioapps.testing import INTEGRATION
from Products.CMFPlone.browser.search import Search
from zope.component import getMultiAdapter
from zope.event import notify
from zope.interface import noLongerProvides
from zope.traversing.interfaces import BeforeTraverseEvent

import unittest


class TestIThemeSpecific(unittest.TestCase):

    layer = INTEGRATION

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

    def traversing_request(self):
        """New request traversing the portal (plone.browserlayer marks the installed layers)."""
        request = self.request.clone()
        noLongerProvides(
            request, IThemeSpecific
        )  # the clone keeps the layers of the test request
        notify(BeforeTraverseEvent(self.portal, request))
        return request

    def test_layer(self):
        self.assertTrue(IThemeSpecific.extends(ICollectiveMessagesviewletLayer))
        # Plone 6: a browser layer of the installed product (Plone 4: bound to the 5 theme skins)
        request = self.traversing_request()
        self.assertTrue(IThemeSpecific.providedBy(request))
        # Plone's @@search (the Plone 4 override of the layer is dropped)
        self.assertIsInstance(
            getMultiAdapter((self.portal, request), name="search"), Search
        )
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        get_installer(self.portal).uninstall_product("plonetheme.imioapps")
        self.assertFalse(IThemeSpecific.providedBy(self.traversing_request()))
