'''
DATABASE LINK:
https://imperial.mobius.cloud/third-party/ckfinder/ckfinder.html
'''

# Public packages
from jinja2 import Environment, FileSystemLoader
from uuid import uuid4
import argparse
import json
import os
import sys
import shutil
import re
from zipfile import ZipFile

# Custom packages
import templates.filters as filters
import validation

##### GLOBALS #####
class consts:
    SCRIPTS_LOCATION = "/web/Pjohnso000/Public_Html/Scripts/QuestionJavaScript.txt"
    # THEME_LOCATION = "/themes/cad8b55c-b186-4899-a406-b92966ee7766" #OG theme
    # THEME_LOCATION = "/themes/9e91de93-8509-4574-a6a9-083b74422a35" #Vertical tabs theme
    THEME_LOCATION = "/themes/b06b01fb-1810-4bde-bc67-60630d13a866" #Test Question tabs theme
###################

##### FUNCTIONS #####
# Function imports and sets up the question dict for injecting into the template
def importQuestion(question_path, sheet_number, question_number, Q_SCHEMA, R_SCHEMA, RDEFAULTS):
    # Load question data from file
    question = load_json_file(question_path)

    # If the question has not been given a uid yet, give it one
    if ("uid" not in question) or (not question["uid"]) or CLEAR_UIDS:
        question["uid"] = str(uuid4())

        # Save it, this is important for version control
        with open(question_path, 'w') as file:
            json.dump(question, file, indent=3)

    # Run validation test on question data
    validation.validate_question(question_path, question, Q_SCHEMA)

    # Give question its numbers
    question["sheet_number"] = sheet_number
    question["number"] = question_number

    # I don't know a better way to do this part, but we need to give each response area in a question its own unique number, as well as saving them to a list (this is how the manifest.xml question file is structured... with the <1> and <2> tags)
    question["response_areas"] = []
    identifier = 1
    for i in range(len(question["parts"])):
        part = question["parts"][i]

        ### Deal with part level response areas
        # Init Params
        isMaple = False
        responses = []

        # Parse generic single response area
        if "response" in part:
            responses, identifier, isMaple = process_response(identifier, part, question["title"], i)

        # Parse list of response areas
        elif "responses" in part:
            responses, identifier, isMaple = process_responses(identifier, part, question["title"], i)

        # Parse the custom response area
        elif "custom_response" in part:
            responses, identifier, isMaple = process_custom_response(identifier, part, question["title"], i)

        # Append responses to main response list
        question["response_areas"].extend(responses)

        # Set flag
        if isMaple:
            question["parts"][i]["isMaple"] = True

        # If response areas are in main part statement (for warnings)
        res_in_part = responses != []

        ### Deal with structured tutorial level response areas
        showWarning = True
        res_in_struct = 0
        if "structured_tutorial" in part:
            for j in range(len(part["structured_tutorial"])):
                item = question["parts"][i]["structured_tutorial"][j]

                # Init Params
                isMaple = False
                responses = []

                # Parse generic single response area
                if "response" in item:
                    responses, identifier, isMaple = process_response(identifier, item, question["title"], i)

                # Parse list of response areas
                elif "responses" in item:
                    responses, identifier, isMaple = process_responses(identifier, item, question["title"], i)

                # Parse the custom response area
                elif "custom_response" in item:
                    responses, identifier, isMaple = process_custom_response(identifier, item, question["title"], i)

                # Append responses to main response list
                question["response_areas"].extend(responses)

                # Set flag
                if isMaple:
                    question["isMaple"] = True

                # Record if multiple res areas - for warning
                res_in_struct += 1 if responses else 0

            # Give warnings for cases badly handled by the current system
            # Use custom error print function in the future (with custom traceback)
            if res_in_struct > 1:
                print(f"\n[WARNING] Found more than 1 response area ({res_in_struct}) in structured tutorial \n\t- All are marked when check button is pressed \n")
            if res_in_part and res_in_struct:
                print(f"\n[WARNING] Response areas both in main part statement and structured tutorial \n\t- All are marked when check button is pressed \n")

    return question

## In-place Function: Process response area
def process_response(identifier, part, q_title, i):
    # Custom flag for displaying the maple help icons
    isMaple = ("Maple" in part["response"]["mode"])

    # Separate case for custom Matrix response area
    if part["response"]["mode"] in ["Matrix Numeric", "Matrix Maple"]:
        data, responses = makeMatrix(part["response"], identifier)
        part["response"] = data
        identifier = data[-1][-1]

    # Every other response area
    else:
        responses = [part["response"]]
        part["response"] = identifier

    # Validate response areas
    r_path = [q_title, "parts", i, "response"]
    validation.validate_response_areas(responses, R_SCHEMA, R_DEFAULTS, r_path)

    # Increment identifier
    identifier += 1

    # Return response areas for this part to be appended to the main list
    return responses, identifier, isMaple

## In-place Function: Process response areas
def process_responses(identifier, part, q_title, i):
    # Custom flag for displaying the maple help icons - is set if one of the response areas in the list is of mode maple
    isMaple = False
    response_areas = []
    for j in range(len(part["responses"])):
        if not isMaple:
            isMaple = ("Maple" in part["responses"][j]["response"]["mode"])

        # Separate case for custom Matrix response area
        if part["responses"][j]["response"]["mode"] in ["Matrix Numeric", "Matrix Maple"]:
            data, responses = makeMatrix(part["responses"][j]["response"], identifier)
            part["responses"][j]["response"] = data
            identifier = data[-1][-1]

        # Every other response area
        else:
            responses = [part["responses"][j]["response"]]
            part["responses"][j]["response"] = identifier

        # Validate response areas
        r_path = [q_title, "parts", i, "responses", j, "response"]
        validation.validate_response_areas(responses, R_SCHEMA, R_DEFAULTS, r_path)

        # Append response areas for this part to the main list
        response_areas.extend(responses)

        # Increment identifier
        identifier += 1

    return response_areas, identifier, isMaple

## In-place Function: Process custom response area
def process_custom_response(identifier, part, q_title, i):
    # User is given the choice of using rich labeling for custom_response areas
    # Case where responses is given in a list
    if isinstance(part["custom_response"]["responses"], list):
        responses = part["custom_response"]["responses"]
        isMaple = sum([("Maple" in response["mode"]) for response in responses])

        # Response area labels (<1>, <2>, ...) are indexed from 1 for a given custom_response, we must shift them based on the current value of the identifier (if the custom response comes in a part after a normal response area for example)
        layout = part["custom_response"]["layout"]
        layout, n = re.subn("(?<=<)(\d+)(?=>)", lambda m: str(int(m.group(1))+identifier-1), layout)
        part["custom_response"] = layout

        # Increment identifier
        identifier += n

    # Case where responses is a dict, the user has chosen to custom-label response area locs
    elif isinstance(part["custom_response"]["responses"], dict):
        isMaple = sum([("Maple" in response["mode"]) for response in part["custom_response"]["responses"].values()])
        layout = part["custom_response"]["layout"]

        # Response area labels here use custom text (<lambda>, <something>...) we need to match response area data with label, and turn them into mobius-understandable labels (<1>, <2>,... )
        responses = []
        for custom_label, resp in part["custom_response"]["responses"].items():
            responses += [resp]

            layout, n = re.subn(f"(?<=<){custom_label}(?=>)", str(identifier), layout)
            if n == 0:
                print(f"[ERROR] {custom_label} not found in custom_response for {q_title} part {i}")
                quit()
            elif n > 1:
                print(f"[ERROR] Multiple {custom_label} found in custom_response for {q_title} part {i}")
                quit()

            # Increment identifier
            identifier += 1

        # "Save" replaced layout back into custom_response
        part["custom_response"] = layout

    # Validate response areas
    r_path = [q_title, "parts", i, "custom_reponse"]
    validation.validate_response_areas(responses, R_SCHEMA, R_DEFAULTS, r_path)

    # Return response areas for this part to be appended to the main list
    return responses, identifier, isMaple


#### FUNCTION NEEDS TO BE MOVED SOMEWHERE ELSE
def makeMatrix(params, id):
    """
    Generate individual response areas which make up the custom matrix response
    For the input syntax, the general idea was to keep them as close as possible to their individual Mobius counterparts (i.e. "answer" for Numeric and "mapleAnswer" for Maple)
    """
    # 2 Cases for a Numeric or Maple response type
    res_areas = []
    if params["mode"] == "Matrix Numeric":
        # Make data based on init identifier
        rows = len(params["answer"])
        cols = len(params["answer"][0])
        data = [[id + j + cols*i for j in range(cols)] for i in range(rows)]

        # Rename mode
        params["mode"] = "Numeric"
        params["showUnits"] = False # We have to set this, or display in the table will look wrong

        # Iterate through answers
        for row in params["answer"]:
            for answer in row:
                curr = params.copy()
                curr["answer"] = {"num": answer}
                res_areas += [curr]

    elif params["mode"] == "Matrix Maple":
        # Make data based on init identifier
        rows = len(params["mapleAnswer"])
        cols = len(params["mapleAnswer"][0])
        data = [[id + j + cols*i for j in range(cols)] for i in range(rows)]

        # Rename mode
        params["mode"] = "Maple"

        # Iterate through answers
        for row in params["mapleAnswer"]:
            for answer in row:
                curr = params.copy()
                curr["mapleAnswer"] = answer
                res_areas += [curr]

    return data, res_areas

def load_json_file(filepath):
    with open(filepath, 'r') as f:
        try:
            json_dictionary = json.load(f)
        except json.JSONDecodeError as e:
            print(validation.get_path_string([os.path.basename(filepath)]))
            sys.tracebacklimit = 0
            raise e

    return json_dictionary


####### LOAD AND SETUP DATA FOR SHEET #######
print("[LOADING] Fetching sheet data")

# Load sheet info schema
SI_SCHEMA = load_json_file(os.path.join("validation", "schemas", "sheet_info.json"))
Q_SCHEMA = load_json_file(os.path.join("validation", "schemas", "question.json"))
R_SCHEMA = load_json_file(os.path.join("validation", "schemas", "response_areas.json"))
R_DEFAULTS = load_json_file(os.path.join("validation", "defaults", "response_areas.json"))

# Parse commandline arguments
parser = argparse.ArgumentParser(description="Rendering JSON question files from a Sheet folder into .xml and .zip files to be understood and uploaded to Mobius")
parser.add_argument("filepath", type=str, help="Path to the sheet folder to be converted (for detailed information about its structure, please visit the Documentation)")
parser.add_argument("--reset-uid", "-uid", help="Set this flag to reset all uids for the question and sheetInfo files. (use when you don't want to override an already existing version of the sheet)", action="store_true")
parser.add_argument("--batch-destination", "-d", type=str, help="Path to destination folder - !ONLY USED BY generateAll.py!")
args = parser.parse_args()

workDir = args.filepath
CLEAR_UIDS = args.reset_uid
outputDir = args.batch_destination

# Fetch group information
try:
    with open(os.path.join(workDir, "SheetInfo.json"), 'r') as file:
        SheetInfo = json.load(file)
except FileNotFoundError:
    print("[ERROR] Folder specified does not contain the SheetInfo.json file")
    quit()

# If the group has not been given a uid yet, give it one
if ("uid" not in SheetInfo) or (not SheetInfo["uid"]) or CLEAR_UIDS:
    SheetInfo["uid"] = str(uuid4())

    # Save it, this is important for version control
    with open(os.path.join(workDir, "SheetInfo.json"), 'w') as file:
        json.dump(SheetInfo, file, indent=3)

# Run validation test on sheet info
validation.validate_sheet_info(os.path.join(workDir, "SheetInfo.json"), SheetInfo, SI_SCHEMA)

# Setup list of question files to import into the sheet
question_paths = [os.path.join(workDir, f"{path}.json") for path in SheetInfo["questions"]]

# Fetch each question, storing them in a list
questions = []
question_number = 1
for question_path in question_paths:
    questions += [importQuestion(question_path, SheetInfo['number'], question_number, Q_SCHEMA, R_SCHEMA, R_DEFAULTS)]
    question_number += 1

# Provide time analysis (for author to gauge estimated time range), only carry this out if not called from generateAll
if not outputDir:
    times = [0, 0]
    qs = []
    for question in questions:
        try:
            times = map(sum, zip(question["icon_data"]["par_time"], times))
            qs += [(question["title"], question["icon_data"]["par_time"])]
        except KeyError:
             pass

    print(f"[TIME ANALYSIS] Estimated student time required summary ([min, max] mins):")
    for d in qs: print(f"\t└── {d[0]}: {d[1]}")
    print(f"\t└── Total: {list(times)}\n")

####### SETUP TEMPLATING ENVIRONMENT #######
# Configure jinja environment
env = Environment(loader=FileSystemLoader(f"./templates"),
                  trim_blocks=True,
                  lstrip_blocks=True)

# Load globals into the Jinja2 environment
env.globals.update(
    consts=consts,
    sheetName=SheetInfo['name'],
    alphabet="abcdefghijklmnopqrstuvwxyz",
    arc=filters.get_arc_path,
    ticks=filters.get_ticks
)

# Load master template from environment
master = env.get_template("master.xml")

####### RENDER, SORT OUT MEDIA AND EXPORT #######

# PUT PDF COMPILATION HERE

# Render sheet data using master template
renderedXML = master.render(questions=questions, SheetInfo=SheetInfo)
print("[LOADING] XML Rendered Successfully")

# Create an output folder in the workdir if it doesn't already exist
if not os.path.exists(os.path.join(workDir, "renders")):
    os.mkdir(os.path.join(workDir, "renders"))

# Save rendered XML to that folder
with open(os.path.join(workDir, "renders", f"{SheetInfo['name']}.xml"), 'w', encoding="utf-8") as file:
    file.write(renderedXML)

# Used when deffering output of render
if outputDir:
    with open(os.path.join(outputDir, "xml", f"{SheetInfo['name']}.xml"), 'w', encoding="utf-8") as file:
        file.write(renderedXML)

# If there is media to import, will need to zip .xml and web_folders together
media_path = os.path.join(workDir, "media")
if os.path.isdir(media_path) and os.listdir(media_path):
    print("[LOADING] Detected Media folder -> bundling media files and .xml")

    # Bundle all media files and xml in a zip
    with ZipFile(os.path.join(workDir, "renders", f"{SheetInfo['name']}.zip"), "w") as zip:
        # Write the xml file
        zip.write(os.path.join(workDir, "renders", f"{SheetInfo['name']}.xml"), arcname=f"manifest.xml")

        # Write media to web_folders inside of the zip file
        for media_file in os.listdir(media_path):
            zip.write(os.path.join(media_path, media_file), arcname=os.path.join("web_folders", f"{SheetInfo['name']}", media_file))

    # This is only really used for generateAll.py
    if outputDir:
        output_media_path = os.path.join(outputDir, "web_folders", f"{SheetInfo['name']}")
        # Copy media to separate folder
        if os.path.exists(output_media_path):
            shutil.rmtree(output_media_path)
        os.mkdir(output_media_path)

        # Write media to separate folder in renders
        for media_file in os.listdir(media_path):
            shutil.copy(os.path.join(media_path, media_file), output_media_path)

print("[DONE]")
