import jsonschema
import pprint
import sys
import os

"""
Main methods
"""

def validate_response_areas(response_areas, r_schema, r_defaults, path=[]):
    """
    Method to validate a list of response areas.
    ---
    Does not return anything. An error is thrown if the validation fails and a warning is
    printed if there are unused properties.

    Requires:
    ---
    - List of response area instances
    - The schema for a response area
    - The defaults for a response area
    - (Optional) A list showing the path to the part containing the response areas
    """
    for response_area in response_areas:
        validate_response_area(response_area, r_schema, r_defaults, path)

def validate_response_area(response_area, r_schema, r_defaults, path=[]):
    """
    Method to validate a response area.
    ---
    Does not return anything. An error is thrown if the validation fails and a warning is
    printed if there are unused properties.

    Requires:
    ---
    - The response area instance
    - The schema for a response area
    - The defaults for a response area
    - (Optional) A list showing the path to the question
    """
    add_response_area_defaults(response_area, r_defaults, path)
    validate(response_area, r_schema, path=path)

def validate_question(filepath, question, q_schema):
    """
    Method to validate a question.
    ---
    Does not return anything. An error is thrown if the validation fails and a warning is
    printed if there are unused properties.

    Requires:
    ---
    - The filepath or filename of the question.json file.
    - The question instance
    - The schema for a question
    """
    filename = os.path.basename(filepath)
    validate(question, q_schema, path=[filename], ignores=["response", "responses"])

def validate_sheet_info(filepath, sheet_info, schema):
    """
    Method to validate a sheet info instance.
    ---
    Does not return anything. An error is thrown if the validation fails and a warning is
    printed if there are unused properties.

    Requires:
    ---
    - The filepath or filename of the sheet_info.json file.
    - The sheet info instance
    - The schema for sheet info
    """
    filename = os.path.basename(filepath)
    validate(sheet_info, schema, path=[filename])

"""
Method for adding response area defaults
"""

def add_response_area_defaults(response_area, defaults, path):
    """
    Method to add default properties to a response area.
    ---
    Does not return anything. Changes the response area instance referenced in the
    arguments and will throw an error if the mode value is not in the set of defaults.
    """
    if "mode" not in response_area or response_area["mode"] not in defaults:
        print()
        sys.tracebacklimit = 0
        
        invalid_mode_msg = "'mode' in response area either doesn't exist or is invalid."
        raise ValueError(json_traceback(path, invalid_mode_msg))

    recursively_add_defaults(response_area, defaults[response_area["mode"]])

def recursively_add_defaults(instance, defaults):
    """
    Method to recursively add defaults into an instance.
    ---
    This is done by looping through the keys in the default dictionary, adding values
    into the instance if they do not exist already.

    If a key is in the instance, but has a different value type, then a ValueError is
    thrown. Else if a key exists but its value is also a dict, the method is called again
    within that dict (hence recursive).

    Returns the same instance which has the added defaults.
    """
    for key, value in defaults.items():
        if key not in instance:
            instance[key] = value
        elif type(instance[key]) == dict and type(value) == dict:
            recursively_add_defaults(instance[key], value)

"""
Methods for validation
"""

def validate(instance, schema, **kwargs):
    """
    Method to validate an instance.
    ---
    Does not return anything. An error is thrown is the validation fails and a warning is
    printed if there are unused properties.

    The unused properties are found by searching through the tree for subschemas and
    combining all the required fields. Any property within the instance that doesn't
    exist in the required list is considered an 'unused property'.
    """
    path = kwargs.get("path", [])
    ignores = kwargs.get("ignores", [])

    try:
        jsonschema.validate(instance, schema)
    except jsonschema.ValidationError as error:
        print()
        sys.tracebacklimit = 0

        full_error_path = path + list(error.path)
        validation_msg = "The validator raised the following exception:"
        raise jsonschema.ValidationError(json_traceback(full_error_path, validation_msg, error.message))

    unused_props = check_unused_props(instance, schema, ignores)

    if unused_props:
        unused_props_msg = "Some properties were ignored as they are not used in the template"
        print(json_traceback(path, unused_props_msg, unused_props))

def json_traceback(path, msg, *args):
    """
    Method to generate a string for errors and warnings in a json file.
    ---
    The function creates a custom traceback in the json file using path, which is a list
    of strings and integers that are the property names and indcies that point to the 
    location of the error in the json file.

    Both msg and the items in args are looped through and printed on new lines below.

    If an item in args is a dict or a list, they are pretty printed, where the max width
    is equal to the length of the message.
    """
    main_string = f"{get_path_string(path)}\n{msg}\n"
    
    for i in args:
        item_string = pprint.pformat(i, width=len(msg)) \
            if type(i) in [list, dict] else str(i)
        
        main_string += f"{item_string}\n"

    return main_string
    
def get_path_string(path):
    """
    Method to return a string showing the path to a question, response area or sheet info.
    ---
    This is done by formatting the names into lines, using prepositions and tab space to
    show hierachy.

    The path must be a list of names as strings and indices as integers, which are in
    order of decreasing heirachy.
    """
    lines = [""]
    
    for i, item in enumerate(path):
        tabs = "  " * i
        ending = ":" if i == len(path) - 1 else ","
        name = f"index {item}" if type(item) == int \
            else f"'{item}'"

        if i == 0:
            prep = "From" if len(path) != 1 else "In"
        elif i == len(path) - 1:
            prep = "the value at"
        elif type(item) == int:
            prep = "at"
        else:
            prep = "in"

        lines.append(f"{tabs}{prep} {name}{ending}")
    
    if len(path) != 1:
        lines.append("")

    return "\n".join(lines)

def check_unused_props(instance, schema, ignores=[]):
    """
    Method to check for properties in an instance that aren't required in the schema
    ---
    Returns a dictionary containing the unused properties and their values.

    This is done by combining the defined properties of all subschemas into a single 
    dictionary. If a property in an instance is not in the list of defined properties,
    it is added to the dictionary of unused properties.

    This works recursively so if a property holds an object, the function is called on
    that object and its content is returned to the property in the first call.
    
    Alternatively, if a property holds an array, its items will be checked and returned
    to the property in the first call.
    """
    defined_props = get_all_defined_properties(instance, schema)
    
    if type(instance) != dict:
        return {}

    unused_props = {}
    for prop, value in instance.items():
        prop_schema = defined_props.get(prop, {})
        
        if prop not in defined_props:
            unused_props[prop] = value

        elif type(value) == dict and prop not in ignores:
            unused_subprops = check_unused_props(value, prop_schema, ignores)
            
            if unused_subprops:
                unused_props[prop] = unused_subprops
        
        elif type(value) == list and prop not in ignores:
            items_schema = prop_schema.get("items", {})
            unused_subprops = []
            
            for prop_item in value:
                unused_subprops.append(check_unused_props(prop_item, items_schema, ignores))
    
            if is_not_empty_matrix(unused_subprops):
                unused_props[prop] = unused_subprops

    return unused_props

def is_not_empty_matrix(m):
    for row in m:
        if len(row) > 0:
            return True
    return False

def get_all_defined_properties(instance, schema):
    """
    Method to return a dictionary of all defined properties by searching through a schema.
    ---
    Returns a dictionary of defined property names and subschemas.

    The method also checks for conditional and `allOf` keywords in a schema and adds the
    defined properties from those subschemas.
    """
    defined_props = schema.get("properties", {}).copy()
    conditional_schema = get_schema_conditional(instance, schema)

    if conditional_schema:
        defined_props.update(get_all_defined_properties(instance, conditional_schema))

    if "allOf" in schema:
        for subschema in schema["allOf"]:
            defined_props.update(get_all_defined_properties(instance, subschema))
    
    return defined_props

def get_schema_conditional(instance, schema):
    """
    Method to return the correct subschema from a condition within the schema.
    ---
    Returns a dictionary of the schema if one exists, else an empty dictionary.
    """
    if "if" in schema:
        if is_valid(instance, schema["if"]):
            return schema["then"]
        elif "else" in schema:
            return schema["else"]
    
    return {}

def is_valid(instance, schema):
    """
    Method to return a whether a instance is valid.
    ---
    Returns a boolean.
    """
    return jsonschema.Draft7Validator(schema).is_valid(instance)
