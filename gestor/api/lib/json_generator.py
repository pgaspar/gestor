from django.utils import simplejson as json

import datetime
from types import DictType, ListType

def generate_json(structure):
	"Generate a JSON file from a dictionary structure"
	
	if not structure: 
		raise ValueError("A structure is needed.")
	
	if len(structure) != 1:
		raise ValueError("Structure dictionary can only have a root element.")
	
	# Covert every leaf in the dictionary to string
	convert_leaf_to_string(structure)
	
	# Generate the JSON content and dump it as a string
	doc = json.dumps(structure)
	
	return doc
	
def convert_leaf_to_string(structure):
	"""
	Converts every leaf on the dictionary to string recursively.
	"""

	def is_dictionary(obj): return type(obj) == DictType
	def is_list(obj):		return type(obj) == ListType
	
	for key,value in structure.items():

		if is_dictionary(value):
			convert_leaf_to_string(value)
			
		elif is_list(value):
			for element in value:
				convert_leaf_to_string(element)
		
		else:
			structure[key] = unicode(value)
