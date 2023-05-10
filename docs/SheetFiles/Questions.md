# Question File Documentation

When authoring using Nobius, question files will be the ones you will spend most of your time in. These are the files which hold all information and content to be rendered into Mobius questions and sheets. Since all your work is saved in .json files, it lives separate from its form as Mobius content. This tool focuses on converting data from question files into Mobius-understandable content, however these files could be used anywhere else to generate .pdf, or LaTeX documents for example.

## Parameters

### `title`
Optional but recommended, this string holds the title for the question file

??? abstract "Example"
    ```json
    "title": "Decompose a flow field"
    ```

### `master_statement`
Optional but recommended, this string contains the question statement to appear over each part. It should hold general information relevant to all parts of the question, exposing the problem.

??? abstract "Example"
    ```json
    "master_statement": "Verify the given theorem for the given function (by evaluating BOTH the volume integral and the six surface integrals)"
    ```

### `media`
Optional, this is a list strings containing the filenames (including extensions) for all media to import and display alongside the `master_statement`. Accepted file extensions include: `.jpg`, `.png`, `.mp4`.

??? abstract "Example"
    ```json
    "media": ["cat.png", "teacup.jpg", "windmill.mp4"]
    ```

!!! warning
    The file names you add in a media block are not checked with media files you've added to a sheet's Media folder. There is not active link between the files you reference in a question and the ones in that folder. This means it's the author's job to ensure import and uploads for media are done correctly

### `icon_data`
Optional, This dictionary holds information about the icons displayed at the top right of the page.

??? abstract "Example"
    ```json
    "icon_data": {
       "difficulty": 3,
       "par_time": [30, 45],
       "statement": "Add a comment about the question here, maybe some context for why the question is asked."
    }
    ```

#### `difficulty`
This can be an integer from 1 to 3, corresponding to the amount of stars shown in the icons. They should be an indication of the relative difficulty of the question in that sheet.

#### `par_time`
This should be a array of length 2, containing the lower and upper bounds for the time required to complete the question, in minutes. These will be shown as a range on the clock icon, and used in the time analysis for a sheet shown to the author.

### `parts`
This parameter holds information about each part of a question, it is a list of `part` objects. These have a great degree of customization and lots of features, which is why they get their own page in the docs! [Take me to the part docs][4]

??? abstract "Example"
    ```json
    "parts": [
      {
        "statement": "Simplify 4*x + 3*x",
        "response": {
          "mode": "Maple",
          "mapleAnswer": "7*x"
        },
        "final_answer": {
          "text": "7*x"
        }
      },
      {
        "statement": "Plot y = 2x + 4"
      }
    ]
    ```

[1]: Questions.md#master_statement
[2]: Questions.md#statement
[3]: Questions.md#
[4]: Parts.md

## Best Practices

!!! info
    Both the [`master_statement`][1], [`statement`][2] and [`text`][3] fields accept raw HTML, so if you want to embed a video, add a table or image outside of the normal available places you can! **Warning: This HTML isn't checked so make sure you close all the tags you've opened**

### Single Part questions
There are multiple ways of dealing with this case, a question that only has a single part (so just one statement). The general idea for something like this is:

- If the question doesn't require a response area, or help module (final answer, worked solutions, ...) then the question can entirely be created without a `parts` list, all in the `master_statement`.
- If the question does then the `master_statement` field should be removed or left empty, and all information added to a single part inside of the `parts` list.
