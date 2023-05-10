'''
NOTE: This is very inefficient and follows every bad practice in the world

Ideally we could have a script similar to generateGroup, which would bundle all sheets using templates, however we have run out of time to make changes to those templates - this is the quickest (implementation, not script speed) bodge I could think of.

HOW IT WORKS:
 - Scrape all folders in the given "Sheets" directory
 - Iterate through them, running generateGroup.py for each
    - An extra param is fed to that script which also renders to the specified folder
 - Iterate through all rendered .xml and compile them into one big manifest.xml file
 - Zip all the media files into one file for easy importing
'''

import os, sys, subprocess, re, json
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from zipfile import ZipFile
import argparse


def get_question_timings(sheet_directory):
  timings = {
    "Total": [0, 0]
  }

  try:
    with open(f"{sheet_directory}/SheetInfo.json") as f:
      sheet_info = json.load(f)
  except (FileNotFoundError, NotADirectoryError):
      print(f"SheetInfo.json not found in {sheet_directory} directory. Moving to next folder")
      return {}

  sheet_names = sheet_info["questions"]

  for s in sheet_names:
    with open(f"{sheet_directory}/{s}.json") as g:
      timings[s] = json.load(g)["icon_data"]["par_time"]

      timings["Total"][0] += timings[s][0]
      timings["Total"][1] += timings[s][1]

  return timings
  
def get_timings_summary(t):
  timings_string = ""
  for q, ts in t.items():
    timings_string += f"{q}: {ts['Total'][0]}-{ts['Total'][1]} mins total.\n"
    
    for name, mins in ts.items():
      if name != 'Total':
        timings_string += f"    {name}: {mins[0]}-{mins[1]} mins.\n"

  return timings_string

# Parse cmdline args
parser = argparse.ArgumentParser(description="[wrapper for generateGroup.py] Render Sheets in batch -> JSON question files from each sheet get rendered through generateGroup.py, and merged into one .xml file. All media is agglomerated into one zip file as well")
parser.add_argument("sheets_dir", type=str, help="Path to the folder containing all the sheet folders to be converted. The folder names don't matter, as long as they follow a valid structure for this tool (for detailed information  please visit the Documentation)")
parser.add_argument("output_dir", type=str, help="Path to destination folder in which to store and merge all xml and media files. (all internal file structure is generated automatically, this can just be an empty folder)")
parser.add_argument("--reset-uid", "-uid", help="Set this flag to reset all uids for all question and sheetInfo files. (use when you don't want to override already existing versions of the sheets)", action="store_true")

args = parser.parse_args()
workDir = args.sheets_dir
outputDir = args.output_dir
CLEAR_UIDS = args.reset_uid

# Prepare output folder
if not os.path.exists(os.path.join(outputDir, "web_folders")):
    os.mkdir(os.path.join(outputDir, "web_folders"))

if not os.path.exists(os.path.join(outputDir, "xml")):
    os.mkdir(os.path.join(outputDir, "xml"))

sheet_timings = {}

# Iterate through each folder in Sheets
for sheet in os.listdir(workDir):
    sheet_path = os.path.join(workDir, sheet)
    
    # Execute command
    res = subprocess.run(["python", "generateGroup.py", sheet_path, "-d", f"{outputDir}", "--reset-uid"][:5 + CLEAR_UIDS], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    question_timings = get_question_timings(sheet_path)

    # Show progress
    if res.returncode == 0 and question_timings != {}:
        sheet_timings[sheet] = question_timings
        print(f"[RENDERING] Sheet {sheet} done. Sheet length: {question_timings['Total'][0]}-{question_timings['Total'][1]} minutes.")
    else:
        print(f"[ERROR] Sheet {sheet} aborted")
        print(res.stderr)
        if input("Continue? (y/n): ") != "y":
            quit()

##### Merge all xml files into one
# Initialize output file
skeleton = """
<courseModule>
    <module>
    <autoModule>true</autoModule>
    </module>

    <questionGroups>
    </questionGroups>

    <questions>
    </questions>

    <webResources>
    <folder id="0">
      <name>
        <![CDATA[  web_folders  ]]>
      </name>
      <description>
        <![CDATA[    ]]>
      </description>
      <uri>
        <![CDATA[  web_folders  ]]>
      </uri>
    </folder>
    </webResources>
</courseModule>
"""

manifest = ET.fromstring(skeleton)

for sheet in os.listdir(os.path.join(outputDir, "xml")):
    print(f"[MERGING] {sheet}")
    # Open file and load into ET
    tree = ET.parse(os.path.join(outputDir, "xml", sheet))
    root = tree.getroot()

    # Copy group
    group = root.find("./questionGroups/group")
    num = re.search(r'#(\d+)', group.find("name").text)[1]
    group.set("weight", f"{num}.0")
    manifest.find("./questionGroups").append(group)

    # Copy questions
    questions = root.findall("./questions/question")
    for question in questions:
        manifest.find("./questions").append(question)

# Write bundled manifest to xml
with open(os.path.join(outputDir, "all_sheets.xml"), "wb") as file:
    file.write(ET.tostring(manifest))

print("[DONE] Saved content to all_sheets.xml")

# Bundle media in a zip
media_manifest = """
<courseModule>
  <module>
    <autoModule>true</autoModule>
  </module>

  <webResources>
    <folder id="0">
      <name>
        <![CDATA[  web_folders  ]]>
      </name>
      <description>
        <![CDATA[    ]]>
      </description>
      <uri>
        <![CDATA[  web_folders  ]]>
      </uri>
    </folder>
  </webResources>
</courseModule>
"""

with open(os.path.join(outputDir, "question_timings.txt"), 'w') as f:
  f.write(get_timings_summary(sheet_timings))

with ZipFile(os.path.join(outputDir, f"all_media.zip"), "w") as zip:
    # Write the xml file
    zip.writestr("manifest.xml", media_manifest)

    # Write media to web_folders inside of the zip file
    for media_folder in os.listdir(os.path.join(outputDir, "web_folders")):
        for media_file in os.listdir(os.path.join(outputDir, "web_folders", media_folder)):
            zip.write(os.path.join(outputDir, "web_folders", media_folder, media_file), arcname=os.path.join("web_folders", media_folder, media_file))

print("[DONE] Compiled Media zip file to all_media.zip")
