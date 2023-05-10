import xml_scraper
import os.path
import json
import lxml
import bs4

def generate_json_file(target, dest, no_uid):
    print(f"Reading {os.path.basename(target)}\n")
    
    with open(target, 'r') as xml_file:
        xml = bs4.BeautifulSoup(xml_file, 'lxml-xml')

    group = xml_scraper.get_sheet_data_from_xml(xml)
    
    if no_uid:
        remove_group_ids(group)

    sheet_info_filename = os.path.join(dest, "SheetInfo.json")

    if os.path.exists(sheet_info_filename):
        print(f"\nOverwriting 'SheetInfo'.")
    else:
        print("\nWriting 'SheetInfo'.")

    with open(sheet_info_filename, "w") as sheet_info_file:
        json.dump(group["info"], sheet_info_file, indent=4)
    
    for question in group["questions"]:
        filename = f"{question['title']}.json"
        filepath = os.path.join(dest, filename)
        
        if os.path.exists(filepath):
            print(f"Overwriting '{question['title']}'.")
        else:
            print(f"Writing '{question['title']}'.")

        with open(filepath, "w") as question_file:
            json.dump(question, question_file, indent=4)

    print("\nDone.")

def remove_group_ids(group):
    if "uid" in group["info"]:
        del group["info"]["uid"]

    for question in group["questions"]:
        if "uid" in question:
            del question["uid"]

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get arguments for converting Mobius xml files back to JSON")
    
    parser.add_argument("filepath", type=str, help="path to the xml file to be converted")
    parser.add_argument("--destination", "-d", type=str, help="path to the directory where the JSON files will be saved to")
    parser.add_argument("--no-uid", action="store_true", help="remove uids from all JSON files")

    args = vars(parser.parse_args())

    destination = args["destination"] \
        if args["destination"] is not None \
        else os.path.dirname(args["filepath"])

    generate_json_file(args["filepath"], destination, args["no_uid"])
