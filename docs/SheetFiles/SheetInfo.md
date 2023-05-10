# SheetInfo
The `SheetInfo.json` file should appear in the folder for any sheet you want to generate. It contains information about which questions it contains, as well as its name and description.

## Parameters
`name`
:   The sheet's name (string)

`number`
:   When you have multiple sheets, it might be useful to give it a number. This number will be appended to the front of each question rendered in this sheet (i.e. Q2.2 is the second question from sheet number 2)

`description`
:   Optional parameter, will display some text under the Mobius group when uploaded, only for the author to see.

`questions`
:   List of strings corresponding to the filenames of the [question][1] json files to be imported in this sheet. The order matters here as each questions will be numbered according to its place in this list.

`uid`
:    Don't worry about this parameter, it will be automatically generated when you render the sheet

[1]: Questions.md

## Example SheetInfo.json
```json
{
   "name": "The Navier-Stokes equations",
   "description": "V1.1 last edited 02/10/2020",
   "questions": [
      "Fundamentals",
      "Kinematics in Cartesian coordinates",
      "Kinematics in cylindrical coordinates",
      "Rigid-body rotation-1",
      "Rigid-body rotation-2",
      "Free vortex",
      "Flow between two parallel plates"
   ],
   "number": 10,
   "uid": "43d2d5aa-57bb-48e0-b9f6-617211ccc4ed"
}
```
