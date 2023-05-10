# Sheet File Structure
The Nobius set of tools is very opinionated in the structure of its input data. Content should be separated in different questions which belong in sheets. Each sheet should have its own folder containing its relevant [questions][1], media and [`SheetInfo.json`][2] file which dictates some of its parameters.

## Folder structure
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

First of all, when generating a sheet, you must make sure that the folder you are selecting contains a [`SheetInfo.json`][2]. The folder should also contain all the JSON files for each of the [questions][1] in that sheet. Finally, if some questions require media, the folder should also contain a `Media` directory in which all media for the sheet can be placed. When you run the script, the output files will be placed in a `renders` folder in your chosen directory.

!!! info
    All .json files contained in a sheet will be given uids when they are first rendered by [`generateGroup`][3] or [`generateAll`][4]

[1]: Questions.md
[2]: SheetInfo.md
[3]: ../Usage/generateGroup.md
[4]: ../Usage/generateAll.md

## Question
These files live in the main sheet directory, and hold the actual content data of each question. This includes any question parts, media references and response areas.
