"""GenericSetup profiles: default, the 4 skin profiles and uninstall."""

from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from plone.base.utils import get_installer
from plone.browserlayer.utils import registered_layers
from plone.formwidget.namedfile.converter import b64decode_file
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.registry.interfaces import IRegistry
from plonetheme.imioapps.interfaces import IThemeSpecific
from plonetheme.imioapps.testing import DMS_INTEGRATION
from plonetheme.imioapps.testing import HELP_URL_RECORD
from plonetheme.imioapps.testing import INTEGRATION
from Products.CMFPlone.resources.browser.resource import ScriptsView
from Products.CMFPlone.resources.browser.resource import StylesView
from zope.component import getMultiAdapter
from zope.component import getUtility

import os
import unittest


SKINS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skins"
)
BUNDLE = "plone.bundles/plonetheme.imioapps"
SKIN = "Plone Default"
MANAGERS = (
    "plone.portaltop",
    "plone.portalheader",
    "plone.abovecontent",
    "plone.abovecontenttitle",
    "plone.belowcontenttitle",
    "plone.abovecontentbody",
    "plone.belowcontentbody",
    "plone.portalfooter",
)
PLONE_HIDDEN_FOOTER = (
    "plone.colophon",
    "plone.site_actions",
)  # Plone 6: footer portlets


def skin_file(path):
    with open(os.path.join(SKINS_DIR, path), "rb") as f:
        return f.read()


class ProfileTestCase(unittest.TestCase):
    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.skins = self.portal.portal_skins
        self.storage = getUtility(IViewletSettingsStorage)

    def skin_path(self):
        return self.skins.getSkinPath(SKIN).split(",")

    def rendered_bundles(self, viewlet_class):
        """data-bundle names of the rendered <link>/<script> tags, in the page order."""
        view = getMultiAdapter((self.portal, self.request), name="view")
        viewlet = viewlet_class(self.portal, self.request, view, None)
        viewlet.update()
        html = viewlet.render()
        return [part.split('"')[0] for part in html.split('data-bundle="')[1:]]

    def assert_skin_profile(self, name, hidden, has_favicon=True):
        """Profile <name> (1.0dev): <name>_images layer in Plone Default (after custom), <name>.css
        rendered after imioapps.css, logo (and favicon) of the skin, hidden viewlets {manager: names}.
        """
        setup = self.portal.portal_setup
        self.assertEqual(
            setup.getLastVersionForProfile("plonetheme.imioapps:" + name), ("1", "0dev")
        )
        layer = name + "_images"
        self.assertEqual(
            self.skins[layer].getDirPath(), "plonetheme.imioapps:skins/" + layer
        )
        self.assertEqual(self.skin_path()[:2], ["custom", layer])
        self.assertIn("imioapps_images", self.skin_path())
        self.assertEqual(self.skins.getSkinSelections(), [SKIN])
        bundle = f"{BUNDLE}_{name}"
        self.assertTrue(api.portal.get_registry_record(bundle + ".enabled"))
        self.assertEqual(
            api.portal.get_registry_record(bundle + ".csscompilation"),
            f"++plone++plonetheme.imioapps/{name}.css",
        )
        bundles = self.rendered_bundles(StylesView)
        self.assertEqual(
            bundles[bundles.index("plonetheme.imioapps") + 1],
            f"plonetheme.imioapps_{name}",
        )
        # post_handler: the skin logo and favicon in the (empty) site records
        logo = b64decode_file(api.portal.get_registry_record("plone.site_logo"))
        self.assertEqual(logo, ("logo.png", skin_file(layer + "/logo.png")))
        favicon = api.portal.get_registry_record("plone.site_favicon")
        if has_favicon:
            self.assertEqual(
                b64decode_file(favicon),
                ("favicon.ico", skin_file(layer + "/favicon.ico")),
            )
        else:
            self.assertIsNone(favicon)
        for manager in MANAGERS:
            self.assertEqual(
                sorted(self.storage.getHidden(manager, SKIN)),
                sorted(hidden.get(manager, ())),
                manager,
            )


class TestDefaultProfile(ProfileTestCase):

    layer = INTEGRATION

    def test_install(self):
        setup = self.portal.portal_setup
        self.assertEqual(
            setup.getLastVersionForProfile("plonetheme.imioapps:default"), ("2500",)
        )
        self.assertTrue(
            get_installer(self.portal).is_product_installed("plonetheme.imioapps")
        )
        self.assertIn(IThemeSpecific, registered_layers())
        # skins: the images layer in Plone Default (the only skin), after custom
        self.assertEqual(
            self.skins["imioapps_images"].getDirPath(),
            "plonetheme.imioapps:skins/imioapps_images",
        )
        self.assertEqual(self.skins.getSkinSelections(), [SKIN])
        self.assertEqual(self.skins.getDefaultSkin(), SKIN)
        self.assertEqual(self.skin_path()[:2], ["custom", "imioapps_images"])
        # bundle: imioapps.css after Barceloneta's CSS (diazo), skin.js deferred
        self.assertTrue(api.portal.get_registry_record(BUNDLE + ".enabled"))
        self.assertEqual(api.portal.get_registry_record(BUNDLE + ".depends"), "all")
        self.assertTrue(api.portal.get_registry_record(BUNDLE + ".load_defer"))
        self.assertEqual(
            self.rendered_bundles(StylesView)[-2:], ["diazo", "plonetheme.imioapps"]
        )
        self.assertEqual(self.rendered_bundles(ScriptsView)[-1], "plonetheme.imioapps")
        # the bundle files are served (content: test_static for the CSS, robot for skin.js)
        for key, path in (
            ("csscompilation", "++plone++plonetheme.imioapps/imioapps.css"),
            ("jscompilation", "++plone++plonetheme.imioapps/skin.js"),
        ):
            value = api.portal.get_registry_record(f"{BUNDLE}.{key}")
            self.assertEqual(value, path)
            self.assertTrue(
                b"".join(
                    self.portal.restrictedTraverse(value)(
                        self.request, self.request.response
                    )
                )
            )
        # registry
        self.assertEqual(api.portal.get_registry_record(HELP_URL_RECORD), "")
        # viewlets: the messagesviewlet viewlet is hidden in the header
        self.assertEqual(
            self.storage.getHidden("plone.portalheader", SKIN), ("message-viewlet",)
        )
        self.assertEqual(self.storage.getHidden("plone.abovecontent", SKIN), ())


class TestDmsmailskinProfile(ProfileTestCase):

    layer = DMS_INTEGRATION

    def test_install(self):
        self.assert_skin_profile(
            "dmsmailskin",
            # the default list is kept (skinname="*" adds to it): message-viewlet stays hidden
            {
                "plone.portalheader": [
                    "message-viewlet",
                    "plone.app.i18n.locales.languageselector",
                ],
                "plone.portalfooter": list(PLONE_HIDDEN_FOOTER) + ["plone.analytics"],
            },
        )
        # the colophon and site actions footer portlets are removed
        manager = getUtility(IPortletManager, "plone.footerportlets")
        mapping = getMultiAdapter((self.portal, manager), IPortletAssignmentMapping)
        self.assertEqual(list(mapping.keys()), ["footer"])


class TestPlonemeetingskinProfile(ProfileTestCase):

    layer = INTEGRATION

    def test_install(self):
        applyProfile(self.portal, "plonetheme.imioapps:plonemeetingskin")
        self.assert_skin_profile(
            "plonemeetingskin",
            {
                "plone.portalheader": [
                    "message-viewlet",
                    "plone.app.i18n.locales.languageselector",
                ],
                "plone.portalfooter": list(PLONE_HIDDEN_FOOTER),
            },
        )


class TestPstskinProfile(ProfileTestCase):

    layer = INTEGRATION

    def test_install(self):
        applyProfile(self.portal, "plonetheme.imioapps:pstskin")
        self.assert_skin_profile(
            "pstskin",
            {
                "plone.portalheader": [
                    "message-viewlet",
                    "plone.app.i18n.locales.languageselector",
                ],
                "plone.portalfooter": list(PLONE_HIDDEN_FOOTER)
                + ["plone.footer", "plone.analytics"],
            },
        )


class TestUrbanskinProfile(ProfileTestCase):

    layer = INTEGRATION

    def test_install(self):
        applyProfile(self.portal, "plonetheme.imioapps:urbanskin")
        self.assert_skin_profile(
            "urbanskin",
            {
                "plone.portalheader": ["message-viewlet"],
                "plone.belowcontenttitle": [
                    "imio.history.documentbyline",
                    "plone.documentbyline",
                    "document-generation-link",
                ],
                "plone.belowcontentbody": ["collective.task.list_tasks"],
                "plone.portalfooter": list(PLONE_HIDDEN_FOOTER),
            },
            has_favicon=False,
        )


class TestUninstallProfile(ProfileTestCase):

    layer = INTEGRATION

    def test_uninstall(self):
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        applyProfile(self.portal, "plonetheme.imioapps:dmsmailskin")
        installer = get_installer(self.portal)
        installer.uninstall_product("plonetheme.imioapps")
        self.assertFalse(installer.is_product_installed("plonetheme.imioapps"))
        self.assertNotIn(IThemeSpecific, registered_layers())
        # image layers removed, no skin created (Plone 4 created an empty dmsmailskin skin)
        self.assertEqual(self.skins.getSkinSelections(), [SKIN])
        for layer in ("imioapps_images", "dmsmailskin_images"):
            self.assertNotIn(layer, self.skins.objectIds())
            self.assertNotIn(layer, self.skin_path())
        # registry records and bundles removed
        registry = getUtility(IRegistry)
        self.assertNotIn(HELP_URL_RECORD, registry)
        self.assertFalse([key for key in registry.records.keys() if "imioapps" in key])
        self.assertNotIn("plonetheme.imioapps", self.rendered_bundles(StylesView))
        # message-viewlet shown again in the header, other hidden viewlets and the logo kept
        self.assertEqual(
            self.storage.getHidden("plone.portalheader", SKIN),
            ("plone.app.i18n.locales.languageselector",),
        )
        self.assertTrue(api.portal.get_registry_record("plone.site_logo"))
