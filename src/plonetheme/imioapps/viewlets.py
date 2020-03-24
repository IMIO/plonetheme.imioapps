# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class EmptyViewlet(ViewletBase):
    """This will display an empty viewlet, it is used to be able to define CSS
       arbitrary between existing viewlets."""
    render = ViewPageTemplateFile('./empty.pt')
