import os
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class ActivityLog(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    level = ndb.FloatProperty(indexed=False)
    time = ndb.DateTimeProperty(auto_now_add=True)
    
    def FormatTime(self):
      delta = datetime.datetime.now() - self.time
      total_seconds = delta.seconds
      hours = total_seconds // 3600
      minutes = (total_seconds % 3600) // 60
      seconds = total_seconds % 60
      if hours:
        return '{} hours {:02} minutes {:02} seconds ago'.format(hours, minutes, seconds)
      if minutes:
        return '{} minutes {:02} seconds ago'.format(minutes, seconds)
      return '{} seconds ago'.format(seconds)


class StatusPageHandler(webapp2.RequestHandler):
  
  def get(self):
    parent = ndb.Key('ActivityLog', 'default')
    log_query = ActivityLog.query(ancestor=parent).order(-ActivityLog.time)
    logs = log_query.fetch(100)

    template_values = {'logs': logs}
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))


class LogHandler(webapp2.RequestHandler):
  
  def post(self):
    log = ActivityLog(parent=ndb.Key('ActivityLog', 'default'))
    log.level = float(self.request.get('level'))
    log.put()
        
app = webapp2.WSGIApplication(
    [('/', StatusPageHandler),
     ('/log', LogHandler)],
    debug=True)