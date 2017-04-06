from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
import datetime,time,hashlib,json

class CSSGenerator(BrowserView):

    template = ViewPageTemplateFile('css.pt')
   
    def __call__(self):
        self.request.response.setHeader('Content-Type', 'text/css')
        self.request.response.setHeader('X-Theme-Disabled', '1')
        self.request.response.setHeader('Cache-Control', 'max-age=15, s-maxage=15, public, must-revalidate')
        self.request.response.setHeader('Vary', 'Accept-Encoding')
        self.request.response.setHeader('Access-Control-Allow-Origin', '*')
        return self.template()
        
        
    def is_eas_active(self):
        registry = getUtility(IRegistry)
        alerts = registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts']
        for k,v in alerts.items():
            if v['is_active'] == 'True':
                return True
        return False
        
        
    @property
    def portal(self):
        return api.portal.get()
