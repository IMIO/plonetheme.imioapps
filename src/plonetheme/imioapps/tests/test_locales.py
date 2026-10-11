"""Translations of locales/ (compiled by zope_i18n_compile_mo_files)."""

from plonetheme.imioapps.testing import INTEGRATION
from zope.component import getUtility
from zope.i18n import translate
from zope.i18n.interfaces import ITranslationDomain

import os
import unittest


LOCALES = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "locales"
)


class TestLocales(unittest.TestCase):

    layer = INTEGRATION

    def test_eea_domain(self):
        """Faceted navigation "More filters" / "Less filters" button (eea.facetednavigation has no fr catalog here)."""
        catalogs = getUtility(ITranslationDomain, "eea").getCatalogsInfo()
        self.assertEqual(
            catalogs["fr"], [os.path.join(LOCALES, "fr", "LC_MESSAGES", "eea.mo")]
        )
        self.assertEqual(
            translate("More filters", domain="eea", target_language="fr"),
            "Recherche avancée",
        )
        self.assertEqual(
            translate("Less filters", domain="eea", target_language="fr"),
            "Recherche avancée",
        )

    def test_plone_domain(self):
        """Our catalog is registered after plone.app.locales': only msgids unknown to Plone are translated by it."""
        catalogs = getUtility(ITranslationDomain, "plone").getCatalogsInfo()["fr"]
        self.assertIn("plone.app.locales", catalogs[0])
        self.assertEqual(
            catalogs[-1], os.path.join(LOCALES, "fr", "LC_MESSAGES", "plone.mo")
        )
        # Plone 4 livesearch_reply advanced search link (msgid not in plone.app.locales, unused since Plone 6)
        self.assertEqual(
            translate(
                "label_advanced_search_full_results",
                domain="plone",
                target_language="fr",
            ),
            "Recherche avancée, avec tous les résultats",
        )
        # Plone 4 searchbox label: no longer in plone.app.locales 7, our msgstr is used (Plone 4: Plone's
        # "Seulement dans le dossier courant" won)
        self.assertEqual(
            translate(
                "label_searchbox_currentfolder_only",
                domain="plone",
                target_language="fr",
            ),
            "Localement",
        )
