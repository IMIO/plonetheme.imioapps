# -*- coding: utf-8 -*-

from plone import api

import logging

logger = logging.getLogger('plonetheme.imioapps: migrations')


def migrate(context):
    logger = logging.getLogger('plonetheme.imioapps: migrate to 2.16')
    logger.info("starting migration steps")
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile('profile-plonetheme.imioapps:default', 'plone.app.registry')
    logger.info("migration done!")
