# generateGroup.py

## Introduction
`generateGroup.py` is the main script from the Nobius toolset. It will convert your sheet folders into .xml and .zip files which can be imported directly into Mobius. Its main function is to populate the different template files with the question and sheet content you've made in JSON format. However is also validates data passed to it using a schema (ensuring the content uploaded to Mobius will be displayed properly), and takes care of adding defaults when no parameters are given.


## Prerequisites

!!! info
    A list of requirements is available in the requirements.txt file - to install them simply type `pip install -r requirements.txt` in your commandline

In order to use this tool, python 3.6 or higher is required. The main modules used by this script are:

 - `jinja2` - This is the templating engine used by the script to generate the html and xml mobius content. For more information on templating, you can visit [Templating and Jinja][1].
 - `jsonschema` - This package is used to check the format and structure of data coming into the templating engine will be rendered properly and most importantly won't crash Mobius.

 [1]: ../CustomizationAndResources/TemplatesAndJinja.md

## Usage
To use this tool, you should navigate to its location (the `Sheet Generator` folder), and call it using python as so:

```unix
python generateGroup.py FILEPATH [--reset-uid or -uid] [-h]
```

- `FILEPATH` is a required positional argument corresponding to the absolute or relative path to where you have stored the sheet folder you'd like to render.
    * *Note: if the path is susceptible to have spaces in folder names (like with certain OneDrive paths), be sure to encapsulate it in double quotes as shown in the example command*
- `--reset-uid` or `-uid` is an optional flag that will cause all the UIDs from your sheet files to be re-generated (both sheetInfo.json and question files). Use this flag when you've already uploaded a version of the sheet you're rendering to mobius, and you don't want to override it.
    * *Note: if you have changed the order, or names of some of the questions it's a good idea to set this flag and delete the previous version of that sheet from mobius*.

!!! tip
    If you ever forget which arguments are accepted, and what they mean you can run `python generateGroup.py -h` to bring up the help menu for this script!

### Example command
```unix
python generateGroup.py "C:\Users\bob\Desktop\My new sheet" -uid
```
