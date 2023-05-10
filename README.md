# TODO
 - Alt text and captions implementation
    - Media numbering
 - Change question importing behaviour to target "name" key in json files
 - Fix single question renders (idk what to do if no number is specified)

Features in the future:
 - Store user profile UIDs locally, so if multiple teachers use the tool for the same module, version control is retained. (modifiedBy and school ids)


# Templating V2
These scripts will generate .xml files to be uploaded directly to mobius

## How to Use
To use the generator, simply run the following commands,
```
python generateGroup.py "[path to sheet folder]"
```

*Note: uids are automatically attributed to each question and group to maintain the link with the files which live on the server.*

## Input Data
This tool is very opinionated when it comes to the structure of the data it can use.

### Folder structure
```
Sheet Folder
├── SheetInfo.json
├── Question.json
├── Another Question.json
├── ...
│
├─── Media
│   ├── image.png
│   ├── video.mp4
│   └── ...
│
└─── renders (generated automatically)
        Example Sheet.xml
        Example Sheet.zip
```

First of all, when generating a sheet, you must make sure that the folder you are selecting contains a `SheetInfo.json`. The folder should also contain all the JSON files for each of the questions in that sheet. Finally, if some questions require media, the folder should also contain a `Media` directory in which all media for the sheet can be placed. When you run the script, the output files will be placed in a `renders` folder in your chosen directory.

### Sheet Info
The `SheetInfo.json` file should appear in the folder for any sheet you want to generate. It contains information about which questions it contains, as well as its name and description.

### Question
These files live in the main sheet directory, and hold the actual content data of each question. This includes any question parts, media references and response areas.
#### Content
#### Response areas

### Media
