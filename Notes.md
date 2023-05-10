# courseModule
General info:
 - data wrapped in `<![CDATA[  ]]>`, is not parsed by the .xml parser, it is treated as raw character data

__!Differences!__
 - Had to modify answer, choice and credit keys to be plural in the datasouce validator as lists had to be parsed differently here
 - the `display` parameter for a list response area is the only one to feature the permute variable as an attribute (ie <display permute="true"></display>)

## module
 - It seems that only the `autoModule` tag is necessary when importing a single question (my guess is that it enables some script that automatically registers it in the correct module)

## Question
### Question
 - `uid`
   - Question with the same uid (attribute for the <question> element) will be overridden with new one on import
   - Generating a custom random uid does work
      - For version control, will need to make sure that we use the same one when re-uploading edited versions (save a uid to the .json if it's not there already...)
 - `school` and `modifiedBy` are not required (they correspond to what is displayed in the "Authors" section)
   - Might be nice to have authors in here nonetheless (at least Imperial)

#### text
This tag contains the html of the question we create, with response areas denoted using <n> tags (n an integer that starts from 1). The number in the tag will correspond to the n-th `<part>` described in `<parts>`.

#### parts
This element contains all the information to be used when loading the response areas in the question (using <1>, <2>, ...)

##### part
Element contains necessary data for a response area
*Note: A whole bunch of extra settings are applied here, but they are not necessary (they're shown below). It might be worth looking into them at a later date.*
```xml
  <name><![CDATA[  responseNan  ]]></name>
  <editing>useHTML</editing>
  <numberOfAttempts>1</numberOfAttempts>
  <numberOfAttemptsLeft>1</numberOfAttemptsLeft>
  <numberOfTryAnother>0</numberOfTryAnother>
  <numberOfTryAnotherLeft>0</numberOfTryAnotherLeft>
  <allowRepublish>false</allowRepublish>
  <attributeAuthor>false</attributeAuthor>
  <difficulty>0.0</difficulty>
  <text><![CDATA[    ]]></text>
  <width>0.0</width>
```
The rest of the settings are the same ones as in the `data-source` tag in the actual question source, however instead of being stored in URL-encoded strings, they're just placed inside of tags. String values are wrapped in that CDATA tag.


## webResources, authors, schools
 - Don't need these when uploading the .xml file on its own
