from .get_html_data import get_question_data

import json
import bs4
import re

"""
Main Methods
"""

def get_sheet_data_from_xml(xml):
    sheet = get_sheet_info(xml)
    sheet["questions"] = []
    questions_list = []

    for question_xml in get_questions(xml):
        question = get_question_from_xml(question_xml)
        sheet["questions"].append(question["title"])
        
        if question["number"]:
            del question["number"]

        questions_list.append(question)

    return {"info": sheet, "questions": questions_list}

def get_question_from_xml(question_xml):
    question = get_question_html_properties(question_xml)
    question.update(get_algorithm(question_xml))
    question.update(get_ids(question_xml))
    
    parts = get_list_of_part_properties(question_xml)
    add_parts_to_question(question, parts)
    
    return question

def get_question_html_properties(question_xml):
    html = get_question_html(question_xml)
    return get_question_data(html)

"""
BeautifulSoup Methods
"""

def get_list_of_part_properties(question_xml):
    return [get_part_properties(p) for p in get_parts(question_xml)]

def add_parts_to_question(question, parts):
    for p in question["parts"]:
        link_response_answers(p, parts)

        if "structured_tutorial" in p:
            for st in p["structured_tutorial"]:
                link_response_answers(st, parts)


def link_response_answers(p, parts):
    if "matrix_response" in p:
        p["response"] = link_matrix_answers(p["matrix_response"], parts)
        del p["matrix_response"]
    elif "custom_response" in p:
        p["custom_response"] = link_custom_answers(p["custom_response"], parts)
    elif "responses" in p and len(p["responses"]) != 0:
        for r in p["responses"]:
            link_response_answers(r, parts)
    elif "response" in p and p["response"] is not None:
        p["response"] = parts[p["response"] - 1]

def link_matrix_answers(matrix_response, parts):
    tags = json.loads(matrix_response)

    if is_empty_matrix(tags):
        print("Empty Matrix")
        return None

    properties = get_all_same_properties(tags, parts)

    if "mode" in properties:
        if properties["mode"] == "Numeric":
            answer_key = "answer"
        elif properties["mode"] == "Maple":
            answer_key = "mapleAnswer"
        else:
            print("Mode not supported for Matrix expansion.")
            return None
    else:
        print("Matrix has conflicting modes.")
        return None
    
    answers = []
    for tags_row in tags:
        answer_row = []

        for tag in tags_row:
            if properties["mode"] == "Numeric":
                answer_row.append(parts[tag - 1]["answer"]["num"])
            elif properties["mode"] == "Maple":
                answer_row.append(parts[tag - 1]["mapleAnswer"])
        
        answers.append(answer_row)

    properties["mode"] = f"Matrix {properties['mode']}"
    properties[answer_key] = answers

    return properties

def link_custom_answers(custom_response, parts):
    properties = {
        "layout": custom_response["layout"],
        "responses": []
    }

    for i in range(custom_response["numberof_tags"]):
        properties["responses"].append(parts[i + custom_response["starting_value"]])

    return properties

def is_empty_matrix(m):
    for row in m:
        if len(row) > 0:
            return False
    return True

def get_all_same_properties(tags, parts):
    properties = parts[tags[0][0]].copy()

    for tags_row in tags:
        for tag in tags_row:
            compare_properties(properties, parts[tag - 1])
        
    return properties

def compare_properties(mutable_dict, immutable_dict):
    for key in [*mutable_dict]:
        if key not in immutable_dict or immutable_dict[key] != mutable_dict[key]:
            del mutable_dict[key]

def get_sheet_info(xml):
    group_xml = xml.find("questionGroups").find("group")

    info = get_sheet_name(group_xml.find("name").text)
    info["description"] = group_xml.find("description").text.strip()
    
    info.update(get_ids(group_xml))

    return info

def get_questions(xml):
    return xml.find_all("question", {"uid": True})

def get_question_html(question_xml):
    html_string = question_xml.find("text").string
    return bs4.BeautifulSoup(html_string, 'html.parser')

def get_parts(question_xml):
    return question_xml.find_all("part")

def get_part_properties(part_xml):
    # finds all children in parts, which are its properties
    return {
        prop_xml.name: get_prop_value(prop_xml) \
        for prop_xml in part_xml.find_all(recursive=False)
    }

"""
JSON Nesting Methods
"""

def get_sheet_name(name_string):
    name_match = re.match(r"^\s+Sheet #(?P<number>\d+) - (?P<name>.+)\b\s+$", name_string)
    sheet_name = name_match.groupdict() if name_match else {}
    
    if "number" in sheet_name:
        sheet_name["number"] = int(sheet_name["number"])
    
    return sheet_name

def get_ids(xml):
    ids_dict = {}

    for key, value in xml.attrs.items():
        if key in ["uid"]: #["uid", "modifiedBy", "school"]:
            ids_dict[key] = value

    return ids_dict

def get_algorithm(xml):
    algorithm_xml = xml.find("algorithm", recursive=False)
    return {"algorithm": algorithm_xml.string} if algorithm_xml else {}

def get_prop_value(prop_xml):
    if prop_xml.find_all(recursive=False):
        return add_deeper_nest(prop_xml)
    elif prop_xml.attrs:
        prop_value = {prop_xml.name: cast_prop_string(prop_xml.string)}
        
        for name, value in prop_xml.attrs.items():
            prop_value[name] = cast_prop_string(value)

        return prop_value
    else:
        return cast_prop_string(prop_xml.string)

def add_deeper_nest(prop_xml):
    children = prop_xml.find_all(recursive=False)
    if all_same_name(children):
        return add_nested_list(prop_xml)
    else:
        return add_nested_dictionary(prop_xml)

def all_same_name(li):
    return len(li) > 0 and all(x.name == li[0].name for x in li)

def add_nested_list(prop_xml):
    return [get_prop_value(child) for child in prop_xml]

def add_nested_dictionary(prop_xml):
    return {child.name:get_prop_value(child) for child in prop_xml}

def cast_prop_string(prop_string):
    if not prop_string:
        return None
    elif prop_string.lower() == "true":
        return True
    elif prop_string.lower() == "false":
        return False
    elif re.match(r'^\d+$', prop_string): # check if int
        return int(prop_string)
    elif re.match(r'^\d+\.\d+$', prop_string): # check if float
        return float(prop_string)
    else:
        return prop_string.strip() # remove whitespace at ends of string from CDATA
