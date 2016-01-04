# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.emergency.alerts.testing import COLLECTIVE_EMERGENCY_ALERTS_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.emergency.alerts is properly installed."""

    layer = COLLECTIVE_EMERGENCY_ALERTS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.emergency.alerts is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.emergency.alerts'))

    def test_browserlayer(self):
        """Test that ICollectiveEmergencyAlertsLayer is registered."""
        from collective.emergency.alerts.interfaces import ICollectiveEmergencyAlertsLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveEmergencyAlertsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_EMERGENCY_ALERTS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.emergency.alerts'])

    def test_product_uninstalled(self):
        """Test if collective.emergency.alerts is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('collective.emergency.alerts'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveEmergencyAlertsLayer is removed."""
        from collective.emergency.alerts.interfaces import ICollectiveEmergencyAlertsLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveEmergencyAlertsLayer, utils.registered_layers())
