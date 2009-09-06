from xml.dom.minidom import Document
from types import DictType, ListType

def generate_xml(structure):
    "Generate a XML file from a dictionary structure"
    
    if not structure: return ""
    
    # Create the minidom document
    doc = Document()
    
    if len(structure) != 1:
        raise ValueError("Structure dictionary can only have a root element.")
    
    # Generate the XML content
    root_name = structure.keys()[0]
    root = generate_xml_element(doc, root_name, structure[root_name])
    doc.appendChild(root)
    
    # Generate string of our newly created XML
    return doc.toprettyxml(encoding="utf8", indent="    ")

def generate_xml_element(document, name, value):
    """
    Generate a XML element inside the given document,
    with the given name and the content specified in value.
    
    The value can be:
     - leaf element
     - a dictionary (more xml elements)
     - a list of dictionaries (a list xml elements with the same name)
    """
    
    element = document.createElement(name)
    
    def process_dictionary(dictionary):
        "Traverse the dictionary and generate the correspondent XML elements"
        for key in dictionary.keys():
            child = generate_xml_element(document, key, dictionary[key])
            element.appendChild(child)
    
    def is_dictionary(obj): return type(obj) == DictType
    def is_list(obj):       return type(obj) == ListType
    
    if is_dictionary(value):
        process_dictionary(value)
            
    elif is_list(value):
        for list_value in value:
            if is_dictionary(list_value):
                process_dictionary(list_value)
            else:
                raise ValueError("All list elements must be a dictionary.")
    #Is a leaf        
    else: 
        leaf_content = document.createTextNode(str(value))
        element.appendChild(leaf_content)
    
    return element

