from zope.component import getUtility
from zope.interface import Interface
from zope import schema
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone import api
from plone.z3cform import layout
from plone.directives import form
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.registry.interfaces import IRegistry
from plone.protect.utils import addTokenToUrl
from operator import itemgetter
        
class IEmergencyAlert(Interface):
    """ Marker """
    global_feeds = schema.List(title=u"Global Alert Feeds",
                                description=u"",
                                default = [],
                                value_type=schema.TextLine(required=True),
                                )
                                    
    alerts = schema.Dict(title=u"Alerts",
                         description=u"",
                         default = {},
                         key_type=schema.TextLine(title=u"Alert ID"),
                         value_type=schema.Dict(
                            title=u"Obj",
                            default = {},
                            key_type=schema.TextLine(title=u"Name"),
                            value_type=schema.TextLine(required=True),
                         ),
                        )
                                    
                                    
                                    
class EmergencyAlertEditForm(RegistryEditForm):

    schema = IEmergencyAlert
    label = u"Emergency Alert System"
    template = ViewPageTemplateFile('controlpanel.pt')
    
    def __call__(self):
        self.request.set('disable_border', 1)
        return self.template()
    
    
    def get(self, name):
        registry = getUtility(IRegistry)
        return registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.global_feeds']
    
    def get_alerts(self):
        registry = getUtility(IRegistry)
        alerts = registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts']
        if alerts:
            return alerts
        return {}

    def fmt_daterange(self, obj):
        fmt = 'Starts: '
        if obj['start']:
            fmt += obj['start']
        else:
            fmt +=  "Now"
            
        fmt +=  " - Ends: "
        if obj['end']:
            fmt += obj['end']
        else:
            fmt +=  "Never"
        return fmt
        
    def tokenize(self,url):
        return addTokenToUrl(url)
    
    @property
    def portal(self):
        return api.portal.get()
    
    
class EmergencyAlertManager(ControlPanelFormWrapper):

    form = EmergencyAlertEditForm
    path = 'collective.emergency.alerts.browser.controlpanel.IEmergencyAlert'

    def __call__(self):
        
        if 'form.feed.global.save' in self.request.form:
            registry = getUtility(IRegistry)
            
            feeds = self.request.form.get('form.feed.global.target','')
            if isinstance(feeds, str):
                feeds = [feeds]
                
            global_feeds = []
            for x in feeds:
                if x:
                    global_feeds.append(x.decode('utf-8'))
            registry[self.path + '.global_feeds'] = global_feeds
            
            
        return ControlPanelFormWrapper.__call__(self)
        
        