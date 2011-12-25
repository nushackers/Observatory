from django.core.urlresolvers import reverse
from django.db import models
from Event import Event

class Share(Event):
	class Meta:
		app_label = 'dashboard'

	external_link = models.URLField(blank = True, null = True)
	link_display = models.CharField(max_length=128, blank = True, null = True)

	def autoescape(self):
		return False

	def type_name(self):
	  return "Share"