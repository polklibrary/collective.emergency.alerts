# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.emergency.alerts


class CollectiveEmergencyAlertsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.emergency.alerts)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.emergency.alerts:default')


COLLECTIVE_EMERGENCY_ALERTS_FIXTURE = CollectiveEmergencyAlertsLayer()


COLLECTIVE_EMERGENCY_ALERTS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_EMERGENCY_ALERTS_FIXTURE,),
    name='CollectiveEmergencyAlertsLayer:IntegrationTesting'
)


COLLECTIVE_EMERGENCY_ALERTS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_EMERGENCY_ALERTS_FIXTURE,),
    name='CollectiveEmergencyAlertsLayer:FunctionalTesting'
)


COLLECTIVE_EMERGENCY_ALERTS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_EMERGENCY_ALERTS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveEmergencyAlertsLayer:AcceptanceTesting'
)
