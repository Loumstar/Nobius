# Maple-Graded Response

Maple Graded response areas allow a user to write an equation as their answer. Maple graded questions are designed so that any mathematically equivalent equation can be marked as correct. However, they are only capable algebraic equations, as opposed to integrals or more complicated operators.

## Minimum Parameters

The minimum parameters needed to create a maple response area are:

- __`mode`__ must be `Maple`.
- __`mapleAnswer`__ must be a string containing the answer in maple syntax.

## Extra Parameters

- __`type`__ must be either `formula` or `maple`. This determines what maths engine is used to evaluate mathematically equivalent equations.
- __`plot`__ should always be an empty string, as we do not know how this works exactly.
- __`allow2d`__ must always be `0` for text entry only, `1` text or symbolic entry from which the student can choose, or `2` for symbolic entry only.
- __`mathConversionMode`__ should always be `0` as we do not know exactly how this works.
- __`maple`__ is a string of maple code which determines how the answer is graded using the `$ANSWER` and `$RESPONSE` variables. By default this is `evalb(($ANSWER)-($RESPONSE)=0);`.

Although `type` may be set to `formula`, we recommend keeping it as `maple` as this will allow students to choose between symbolic and text entry. If students choose symbolic, it may cause the UI design to break. For the same reason, we also recommend keeping `allow2d` set to `0`.

## Example Usage

Taken from ME2 Fluids Mechanics tutorial sheet 1, this part contains a Maple response area where the user needs to type a maple equation that is mathematically equivalent to __(pi/6)\*(rho\*(U^2)\*(R^2))__ into the textbox in order to get the point.

```json
{
  "statement": "The drag force \\(F\\) of the submarine (insert \\(\\rho\\) as \\(rho\\)).",
  "response": {
    "mode": "Maple",
    "mapleAnswer": "(pi/6)*(rho*(U^2)*(R^2))"
  },
  "final_answer": {
    "text": "\\( \\boxed{F = \\frac{\\pi}{6}\\rho U^2 R^2} \\)"
  }
}
```
