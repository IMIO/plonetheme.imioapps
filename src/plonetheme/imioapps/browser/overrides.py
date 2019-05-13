# -*- coding: utf-8 -*-

from plone.app.layout.globals.layout import LayoutPolicy


class ImioLayoutPolicy(LayoutPolicy):
    """ """

    def renderBase(self):
        """Do not include portal_factory in URL."""
        url = super(ImioLayoutPolicy, self).renderBase()
        if 'portal_factory' in url:
            portal_factory_index = url.index('portal_factory')
            url = url[:portal_factory_index]
        return url
