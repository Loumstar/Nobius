# Matrix response area
This advanced response area allows the user to generate an array of Numeric or Maple response areas (see "Response Areas/Vanilla" for more information). The idea is that the user sets up the parameters to be used for all the response areas to be generated, with only the answer field changing with each generated response area.

For the input syntax, the general idea was to keep matrix response areas as close as possible to their individual Mobius counterparts (i.e. "answer" for [Numeric][1] and "mapleAnswer" for [Maple][2]).

[1]: ../Vanilla/numeric.md
[2]: ../Vanilla/maple.md

## Minimum Parameters
These are same as for their single Mobius counterpart, the way a matrix response is selected is by adding `Matrix` in front of the usual mode field:

 - __`mode`__ can be either `Matrix Maple` or `Matrix Numeric`

For this response area, the other minimum required parameter is a 2D array of answers relevant to the mode chosen. **It is the shape of this array that will determine the shape of the matrix generated**.

### `Matrix Maple`
- __`mapleAnswer`__ must be a 2D array of strings containing the maple answers for each relevant cell in the matrix

### `Matrix Numeric`
- __`answer`__ **WARNING**: This is different to the vanilla Numeric response area - as units are always disabled in a matrix, this field can be a 2D array of floats. (it doesn't need to be an object containing `num` and `units`)

## Extra Parameters
All the extra parameters relevant to the vanilla version of the response area you chose can be added. Visit their relevant documentations for more information. The only difference is that for `Matrix Numeric`, `showUnits` will always be set to false.

## Example Usage
Example __`Matrix Maple`__ Response Area:
```json
"response": {
  "mode": "Matrix Maple",
  "mapleAnswer": [
    ["2*x", "5*x + y"],
    ["x + y", "-6*y"]
  ]
}
```

Example __`Matrix Numeric`__ Response Area:
```json
"response": {
  "grading": "toler_abs",
  "err": 0.001,
  "mode": "Matrix Numeric",
  "answer": [
    [
      3.2,
      4.6
    ],
    [
      7.6,
      1.0
    ]
  ]
}
```
In this case, the default parameters for `err` and `grading` were changed. This will be reflected in all the response areas which eventually make up this matrix for the student.


*Note: The relevant template for this response area can be found in `templates/matrixResponse.html`*
