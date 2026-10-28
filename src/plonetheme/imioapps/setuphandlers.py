from plone import api
from plone.base.interfaces import INonInstallable
from plone.formwidget.namedfile.converter import b64encode_file
from zope.interface import implementer

import os


SKINS = os.path.join(os.path.dirname(__file__), "skins")


@implementer(INonInstallable)
class HiddenProfiles:
    def getNonInstallableProfiles(self):
        return ["plonetheme.imioapps:uninstall", "plonetheme.imioapps:testing"]


def _set_image(record, skin, filename):
    """Store skins/<skin>_images/<filename> in the empty site logo/favicon record."""
    path = os.path.join(SKINS, f"{skin}_images", filename)
    if api.portal.get_registry_record(record) or not os.path.exists(path):
        return False
    with open(path, "rb") as f:
        api.portal.set_registry_record(record, b64encode_file(filename, f.read()))
    return True


def set_logo_and_favicon(skin):
    """Plone 6 takes the logo and favicon from the registry, not from skin layers."""
    _set_image("plone.site_logo", skin, "logo.png")
    if _set_image("plone.site_favicon", skin, "favicon.ico"):
        api.portal.set_registry_record(
            "plone.site_favicon_mimetype", "image/vnd.microsoft.icon"
        )


def post_install_dmsmailskin(context):
    set_logo_and_favicon("dmsmailskin")


def post_install_plonemeetingskin(context):
    set_logo_and_favicon("plonemeetingskin")


def post_install_pstskin(context):
    set_logo_and_favicon("pstskin")


def post_install_urbanskin(context):
    set_logo_and_favicon("urbanskin")
