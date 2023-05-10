# Multiple Choice Response

Multiple Choice response areas give a user a set of choices that they must pick from. There is only one correct answer, unlike list response areas where points can be allocated to each option.

## Minimum Parameters

The minimum parameters needed to create a multiple choice response area are:

- __`mode`__ must be `Non Permuting Multiple Choice`.
- __`choice`__ must be an array of strings, in which can be any valid HTML, or LaTeX using `\\(` and `\\)`.
- __`answer`__ must be an integer to which item in the choice array is the correct (first position would be 1).

## Extra Parameters

- __`display`__ must be either `horizontal` or `vertical`. This determines which way the choices are list. By default this is `vertical`.

Please note, the UI has only been designed for `vertical` display, so using `horizontal` may affect the page style.

## Example Usage

Taken from a test Fluid Mechanics sheet, this part contains a Multiple Choice response area that displays the options vertically. The user needs to choose the second option into the textbox in order to get the point. Note here that HTML and LaTeX are being rendered for each choice.

```json
{
  "statement": "Which of the following gives the correct expression for the magnitude of the power, \\(P\\), required to drive the rotor?",
  "response": {
    "mode": "Non Permuting Multiple Choice",
    "answer": 2,
    "choices": [
        "<p>\\(P = \\frac{2\\pi L\\omega^2 R^3 \\mu}{d}\\)</p>",
        "<p>\\(P = \\frac{2\\pi L\\omega R^3 \\mu}{d}\\)</p>",
        "<p>\\(P = \\frac{\\pi L\\omega^2 d^3 \\mu}{R^2}\\)</p>",
        "<p>\\(P = \\frac{2\\pi L\\omega^3 d^2 \\mu^2}{R^2}\\)</p>"
    ]
  }
}
```
