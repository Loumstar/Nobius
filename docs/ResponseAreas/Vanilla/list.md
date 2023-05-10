# List Response

List response areas are similar to Multiple Choice except they are able to be inline with text. These response areas are drop-down menus by default, but can also be a text field where user must write the answer without knowing the options. Weightings are given to each option, so multiple answers can be graded as correct.

## Minimum Parameters

The minimum parameters needed to create a list response area are:

- __`mode`__ must be `List`.

- __`answer`__ must be an array of strings that are the options a student can pick from. The strings cannot contain any HTML as this will not be rendered.

- __`credit`__ must be an array of numbers that correspond to the weighting of each answer. The points scored for any answer will be its weighting divided by the maximum weighting.

## Extra Parameters

- __`display`__ must be an object containing two parameters, `display` and `permute`:
    - `display` must be either `menu` or `text`. This determines whether the list is presented as a drop-down menu of options, or as a text field that the user must fill in. By default, this is set to `menu`.
    - `permute` determines whether the set of options are randomly ordered. Must be a boolean and is `true` by default.

    ```json
    "display": {
      "display": "menu",
      "permute": true
    }
    ```

- __`grader`__ determines how answers in a text field are graded. This parameter is only necessary for text fields. There are several options:
    - `exact` requires a student's response to match an answer exactly in order to gain points.
    - `relaxed` requires a student's response to match an answer in order to gain points, but is not case sensitive.
    - `regex` requires a student's response to match a regular expression, which would be set in the list of answers.

## Example Usage

Taken from ME2 Fluids Mechanics tutorial sheet 13, this List response area creates a drop-down menu below the question statement, and the user needs to choose __The boundary layer is thin__ in order to get the point.

```json
{
  "statement": "What observation did we make about the boundary layer to start the approximation?",
  "response": {
    "mode": "List",
    "answers": [
        "The boundary layer is fast",
        "Air is not a fluid",
        "The boundary layer is thick",
        "The boundary layer is thin",
        "Water is wet"
    ],
    "credits": [
        0,
        0,
        0,
        1,
        0
    ]
  }
}
```
