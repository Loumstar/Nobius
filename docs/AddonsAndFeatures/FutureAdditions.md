# Future additions

List of all the features we did not get around to implementing:

- Move LaTeX rendering from Mobius to the templating engine (this will considerably speed up load times) by rendering the latex to the html directly. This could be done in a number of ways:
    - Use a command line script to generate MathJax or MathML code
    - Use a python package to generate math equations as SVGs
    - Make a call to a MathJax API, similarly to mobius except this will only have to render upon generating the sheets, not in the browser.

- Storing sheet/question data in CSON or YAML instead of JSON format. This will allow us to:
    - Make use of multiline-strings
    - Have a clearer structure and more readable layout
    - Remove double escpaing backslashes for LaTeX equations.

- If using JSON, add functionality for author to add notes to question and sheetinfo json files. e.g. author_notes. If using another language which supports comments this wouldn't be necessary. (Could also make compatible with generateJSON scraper by adding it in the author notes box in Mobius)

- Bring back submit button and rename it to "Reset" (See where is brings the student when clicked), so that when a sheet needs to be force-graded when changes are made, the students can be asked to "reset" the sheet.

- Current behaviour of response areas in a single part:
    * Response areas in part and structured tutorial are all marked at once, this means the current standard is to only add response areas in one of those blocks
    * For the future:
        - Make custom 'Check' button that calls to the original one once all the hiding has been done properly. Factually we simulate a click on the original check button which is now hidden after all response areas to be hidden are so.

- Automatically generate the Lessons and Assignments for generated sheets to save time

- Give choice of bracket for a matrix response area bracket or square bracket or curly bracket

- Give arrow controls for matrix response areas

- Add a custom defaults file for each sheet - like if we want to change the default grading code for a whole sheet we can change it there. This file would override the tool-wide defaults.

- Fix the "Try Another" button for algorithmic questions. Currently it seems to reload the page without calling QuestionJavascript again, causing our whole custom logic to break down. In the future, we should move that button, and attach an extra event handler which would re-run that script, but it might now be as easy as that idk.

- Improve and get more accurate data collection. For example if a question didn't have any response areas, we probably want a "Mark as Done" button for those.
