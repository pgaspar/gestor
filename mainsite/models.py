from django.db import models

class Noticia(models.Model):
	"""(Noticia description)"""
	

	class Admin:
		list_display = ('',)
		search_fields = ('',)

	def __str__(self):
		return "Noticia"
