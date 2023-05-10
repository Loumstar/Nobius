# True/False Response

True/False response areas are a simpler form of Multiple Choice. Only two choices can exist which are `true` and `false` by default, and they are always displayed vertically.

## Minimum Parameters

The minimum parameters needed to create a true/false response area are:

- __`mode`__ must be `True False`.
- __`answer`__ must be an integer. This value refers to the index (starting from 1) of the correct answer in the choices array. If using the preset, `1` refers to `true` and `2` refers to `false`.

## Extra Parameters

- __`choices`__ must be a list containing two strings. This is `["true", "false"]` by default, but it can be any text, HTML or LaTeX if escaped using `\\(` and `\\)`.

## Example Usage

Taken from ME2 Fluid Mechanics tutorial sheet 11, this part contains a simple True/False response area, where the user must choose `False`, as in the list of choices, this is the second option.

```json
{
  "statement": "The Navier-Stokes equations imply a constant and uniform density field.",
  "response": {
    "mode": "True False",
    "answer": 2
  }
}
```
