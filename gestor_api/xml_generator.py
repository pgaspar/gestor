from xml.dom.minidom import Document
from types import DictType, ListType

def generate_xml(structure):
    "Generate a XML file from a dictionary structure"
    
    if not structure: 
        raise ValueError("A structure is needed.")
    
    # Create the minidom document
    doc = Document()
    
    if len(structure) != 1:
        raise ValueError("Structure dictionary can only have a root element.")
    
    # Generate the XML content
    root_name = structure.keys()[0]
    root = generate_xml_element(doc, root_name, structure[root_name])
    doc.appendChild(root)
    
    # Generate string of our newly created XML
    return doc.toxml(encoding="utf-8")

def generate_xml_element(document, name, value):
    """
    Generate a XML element inside the given document,
    with the given name and the content specified in value.
    
    The value can be:
    * Leaf element
        { 'id' : 123 }
        <id> 123 </id>
        
    * A dictionary (more xml elements)
        { 'thing' : { 'id' : 123, 'name' : 'foobar' } }
        <thing> <id> 123 </id> <name> foobar </name> </thing>
    
    * A list of dictionaries (a list xml elements with the same name)
        { 'thing' : [ { 'id' : 1 } , { 'id' : 2 } ] }
        <thing> <id> 1 </id> <id> 2 </id> </thing>
        
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
           
    else: # is a leaf 
        leaf_content = document.createTextNode(unicode(value))
        element.appendChild(leaf_content)
    
    return element

