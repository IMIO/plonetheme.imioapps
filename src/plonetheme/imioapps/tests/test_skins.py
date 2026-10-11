"""Images of the skin layers (skins/*_images)."""

from plonetheme.imioapps.testing import DMS_INTEGRATION

import os
import unittest


SKINS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skins"
)


def skin_file(path):
    with open(os.path.join(SKINS_DIR, path), "rb") as f:
        return f.read()


class TestImages(unittest.TestCase):

    layer = DMS_INTEGRATION

    def test_images(self):
        portal = self.layer["portal"]
        # used through portal_url/<name> by imio.esign, imio.annex, imio.actionspanel, collective.iconifiedcategory...
        for name in (
            "spinner_small.gif",
            "spinner.gif",
            "help.png",
            "exclamation.gif",
            "search_button_icon.png",
        ):
            self.assertEqual(
                portal.restrictedTraverse(name)._readFile(0),
                skin_file("imioapps_images/" + name),
                name,
            )
        # dmsmailskin's logo and favicon are the site logo and favicon (Plone 6: registry, not skin layers)
        logo = portal.restrictedTraverse("@@site-logo")._getFile()
        self.assertEqual(logo.data, skin_file("dmsmailskin_images/logo.png"))
        self.assertEqual(logo.getImageSize(), (42, 32))
        favicon = portal.restrictedTraverse("@@favicon.ico")
        self.assertEqual(
            favicon._getFile().data, skin_file("dmsmailskin_images/favicon.ico")
        )
        self.assertEqual(favicon._getFile().contentType, "image/vnd.microsoft.icon")
