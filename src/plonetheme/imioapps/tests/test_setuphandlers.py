from plone import api
from plone.base.interfaces import INonInstallable
from plone.formwidget.namedfile.converter import b64decode_file
from plone.registry.interfaces import IRegistry
from plonetheme.imioapps.setuphandlers import HiddenProfiles
from plonetheme.imioapps.setuphandlers import set_logo_and_favicon
from plonetheme.imioapps.testing import INTEGRATION
from zope.component import getUtility

import os
import unittest


SKINS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skins"
)


def skin_file(path):
    with open(os.path.join(SKINS_DIR, path), "rb") as f:
        return f.read()


class TestHiddenProfiles(unittest.TestCase):

    layer = INTEGRATION

    def test_getNonInstallableProfiles(self):
        utility = getUtility(INonInstallable, name="plonetheme.imioapps")
        self.assertIsInstance(utility, HiddenProfiles)
        self.assertEqual(
            utility.getNonInstallableProfiles(),
            ["plonetheme.imioapps:uninstall", "plonetheme.imioapps:testing"],
        )


class TestSetuphandlers(unittest.TestCase):

    layer = INTEGRATION

    def test_set_logo_and_favicon(self):
        def record(name):
            value = api.portal.get_registry_record(name)
            return value and b64decode_file(value)

        # empty site logo and favicon: the skin ones
        set_logo_and_favicon("dmsmailskin")
        self.assertEqual(
            record("plone.site_logo"),
            ("logo.png", skin_file("dmsmailskin_images/logo.png")),
        )
        self.assertEqual(
            record("plone.site_favicon"),
            ("favicon.ico", skin_file("dmsmailskin_images/favicon.ico")),
        )
        self.assertEqual(
            api.portal.get_registry_record("plone.site_favicon_mimetype"),
            "image/vnd.microsoft.icon",
        )
        # already set (by the site manager or another skin): kept
        set_logo_and_favicon("pstskin")
        self.assertEqual(
            record("plone.site_logo"),
            ("logo.png", skin_file("dmsmailskin_images/logo.png")),
        )
        self.assertEqual(
            record("plone.site_favicon"),
            ("favicon.ico", skin_file("dmsmailskin_images/favicon.ico")),
        )
        # urbanskin has no favicon
        registry = getUtility(IRegistry)
        registry["plone.site_logo"] = None
        registry["plone.site_favicon"] = None
        set_logo_and_favicon("urbanskin")
        self.assertEqual(
            record("plone.site_logo"),
            ("logo.png", skin_file("urbanskin_images/logo.png")),
        )
        self.assertIsNone(record("plone.site_favicon"))
