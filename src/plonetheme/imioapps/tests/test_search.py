"""Search (F12): Plone 4 overrode @@search to append "*" to the searched text (browser/overrides.py, dropped).
Plone 6's own @@search (plone.base.utils.munge_search_term) searches word prefixes."""

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plonetheme.imioapps.testing import INTEGRATION
from zope.component import getMultiAdapter

import unittest


class TestSearch(unittest.TestCase):

    layer = INTEGRATION

    def test_results(self):
        portal = self.layer["portal"]
        request = self.layer["request"]
        setRoles(portal, TEST_USER_ID, ["Manager"])
        view = getMultiAdapter((portal, request), name="search")

        def found():
            return [
                b.getId for b in view.results(batch=False, use_content_listing=False)
            ]

        # a word prefix finds the document "Correspondence"
        request.form["SearchableText"] = "Corresp"
        self.assertEqual(found(), ["doc"])
        request.form["SearchableText"] = "Corresp*"
        self.assertEqual(found(), ["doc"])
        request.form["SearchableText"] = "nothing"
        self.assertEqual(found(), [])
        del request.form["SearchableText"]
        # no text but a tag (keywords viewlet link): found (Plone 4 override bug: SearchableText=*, nothing found)
        request.form["Subject"] = "mail"
        self.assertEqual(found(), ["doc"])
        del request.form["Subject"]
