from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
import datetime,time,hashlib,json

class EASGenerator(BrowserView):

    template = ViewPageTemplateFile('eas.pt')
   
    def __call__(self):
        self.request.response.setHeader('Content-Type', 'application/javascript')
        self.request.response.setHeader('X-Theme-Disabled', '1')
        self.request.response.setHeader('Cache-Control', 'max-age=15, s-maxage=15, public, must-revalidate')
        self.request.response.setHeader('Vary', 'Accept-Encoding')
        self.request.response.setHeader('Access-Control-Allow-Origin', '*')
        return self.template()
        
        
    def get_feeds(self):
        registry = getUtility(IRegistry)
        
        # add global feeds, use list to clone it otherwise it saves?!
        feeds = list(registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.global_feeds']) 
        if not feeds:
            feeds = []
        else:
            feeds = [x.encode('ascii', 'ignore') for x in feeds]
        feeds.append(self.portal.absolute_url() + '/eas_alerts') # add local feed
        return feeds
        
        
    @property
    def portal(self):
        return api.portal.get()
