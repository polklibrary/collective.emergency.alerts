from plone import api
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
import datetime,time,hashlib,json,md5

class Alert(object):

    id = None
    _struct = {}
    
    def __init__(self, id):
        self._struct = {
            u'title' : u'',
            u'body' : u'',
            u'start' : u'',
            u'end' : u'',
            u'level' : u'0',
            u'is_active' : u'False',
            u'url' : u'',
        }
        if id:
            registry = getUtility(IRegistry)
            alerts = registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts']
            self.id = id.decode('utf-8')
            if self.id in alerts:
                self._struct = alerts[self.id]
        else:
            self.id = hashlib.sha1(str(time.time())).hexdigest().decode('utf-8')
            
    def save(self):
        registry = getUtility(IRegistry)
        alerts = registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts']
        if not alerts:
            alerts = {}
        alerts[self.id] = self._struct 
        registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts'] = alerts
        
        # Force the save of a dictionary to be persistant
        registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts'] = registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts']
            
    def delete(self):
        registry = getUtility(IRegistry)
        alerts = registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts']
        del alerts[self.id]
        registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts'] = alerts
        
        # Force the save of a dictionary to be persistant
        registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts'] = registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts']
           
            
    def set(self, name, value):
        if isinstance(value, str):
            value = value.decode('utf-8')
        self._struct[name] = value
            
    def get(self, name):
        return self._struct[name]
        
    # def _reset(self):
        # registry = getUtility(IRegistry)
        # alerts = registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts']
        # if not alerts:
            # registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts'] = {}
            # # Force the save of a dictionary to be persistant
            # registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts'] = registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts']
         

        
        
class AlertEdit(BrowserView):

    template = ViewPageTemplateFile('edit_alert.pt')
    alert = None
    error = False
   
    def __call__(self):
        self.alert = None #default
        self.error = None #default
        id = self.request.form.get('id', None)
        
        try:
            self.alert = Alert(id)
        except Exception as e:
            self.error = True
            
        if 'form.widgets.submit' in self.request.form:
            self.alert.set(u'title', self.request.form.get('form.widgets.title', 'Missing title'))
            self.alert.set(u'body', self.request.form.get('form.widgets.body', 'No details available at this time'))
            
            self.alert.set(u'start', self.request.form.get('form.widgets.start', ''))
            self.alert.set(u'end', self.request.form.get('form.widgets.end', ''))
            self.alert.set(u'url', self.portal.absolute_url() + '/alert?id=' + str(self.alert.id))
            
            active = u'False'
            if self.request.form.get('form.widgets.active', 'off') == 'on':
                active = u'True'
            self.alert.set(u'is_active', active)
            
            self.alert.set(u'level', self.request.form.get('form.widgets.level', '0'))
            
            self.alert.save()
            return self.request.response.redirect(self.portal.absolute_url() + '/@@emergency_manager')
            
        if 'alert.state' in self.request.form:
            state = self.request.form.get('alert.state')
            if state == 'False':
                self.alert.set('is_active', u'True')
            else: 
                self.alert.set('is_active', u'False')
            self.alert.save()
            return self.request.response.redirect(self.portal.absolute_url() + '/@@emergency_manager')
            
        if 'alert.remove' in self.request.form:
            self.alert.delete()
            return self.request.response.redirect(self.portal.absolute_url() + '/@@emergency_manager')
            
        return self.template()
        
    @property
    def portal(self):
        return api.portal.get()
        
        
class AlertView(BrowserView):

    template = ViewPageTemplateFile('alert.pt')
    alert = None
    
    def __call__(self):
    
        self.alert = None #default
        self.error = None #default
        id = self.request.form.get('id', None)
        
        try:
            self.alert = Alert(id)
        except Exception as e:
            self.error = True
            
        return self.template()
        
        
class AlertsBroadcaster(BrowserView):
   
    def __call__(self):
        data = []
        now = datetime.datetime.now()
        
        registry = getUtility(IRegistry)
        alerts = registry['collective.emergency.alerts.browser.controlpanel.IEmergencyAlert.alerts']
        if alerts:
            for k,v in alerts.items():
                if v['is_active'] == 'True':
                    start = datetime.datetime.strptime(self.dict_get(v, 'start', '1999-12-25 13:12'), '%Y-%m-%d %H:%M')
                    end = datetime.datetime.strptime(self.dict_get(v, 'end', '2050-12-25 13:12'), '%Y-%m-%d %H:%M')
                    if start <= now and now <= end:
                        data.append(v)
                        
        # Determine Format
        self.request.response.setHeader('ETag', md5.new(str(self._data)).hexdigest())
        self.request.response.setHeader('Cache-Control', 'max-age=60, s-maxage=60, public, must-revalidate')
        self.request.response.setHeader('Vary', 'Accept-Encoding')
        self.request.response.setHeader('Content-Type', 'application/json')
        self.request.response.setHeader('Access-Control-Allow-Origin', '*')
        return self.toJSONP(data)
        
    def dict_get(self,v,key,default):
        if key in v:
            if not v[key]:
                return default
            return v[key]
            
    def toJSON(self, data):
        return json.dumps(data)
        
    def toJSONP(self, data):
        return '_EAS.loaded(' + self.toJSON(data) + ')'
        

        
        