# Numeric Response

Numeric response areas accept a number for an answer. At their simplest, they can be a single input box expecting an exact value. However they can be controlled to accept a physical unit too, or mark answers to a prescribed tolerance.

## Minimum Parameters

The minimum parameters needed to create a numeric response area are:

- __`mode`__ which must be `Numeric`
- __`answer`__ which must be an object containing `num`, which holds correct answer as a number.

  ```json
  {
    "mode": "Numeric",
    "answer": {
      "num": 3.1415
    }
  }
  ```

## Extra Parameters

- __`showUnits`__ must be either `true` or `false`. This determines if the user must also put in a correct unit. If true, then `answer.units` becomes a required parameter. By default, it is false.
- __`units`__ which must be placed within `answer`, must be a string containing the correct physical constant of the answer. This should only be added to properties if `showUnits` is true:

  ```json
  {
    "mode": "Numeric",
    "showUnits": true,
    "answer": {
      "num": 1000,
      "units": "kg"
    }
  }
  ```

- __`negStyle`__ must be either `minus`, `paren` or `both` to allow a minus sign, parentheses or both to be used for negation. By default, it is `minus`.
- __`numStyle`__ must be a string containing certain keywords words separated by a whitepace. These keywords are:
    - `thousands` which allows a user to use commas as a seaparator in their answer. This is included by default.
    - `scientific` which allows a user to use `E+10`, `E-3`, etc. to denote orders of magnitude. This is included by default.
    - `arithmetic` which allows a user to use `+`,`-`,`*`,`/` in their answers.
    - `dollars` which allows a user to use predefined variables from the questions. These are called as `$VARIABLE_NAME`.
- __`grading`__ must be either:
    - `exact_value` which requires the user to give the exact answer. This the default value.
    - `exact_sigd` which requires the user to give an answer correct to a specific number of significant digits. If used, `digits` becomes a required parameter.
    - `toler_abs` which requires the user to give an answer correct to within a specific error. If used, `err` becomes a required parameter.
    - `toler_sigd` which requires the user to give an answer correct to within a specific error at a specific decimal place. This means that if an answer had to be within 0.002, it would have an error of 2 at digit 3. If used, `err` and `digit` become required parameters.
    - `toler_perc` which requires the use to give an answer correct to within a specific percentage of the correct answer. If used, `perc` becomes a required parameter.
- __`err`__ represents an absolute error and must be a float or integer. This should only exist if grading is set to `toler_abs` or `toler_sigd`.
- __`digit`__ represents the nth digit in a number and must be an integer. This should only exist if grading is set to `exact_sigd` or `toler_sigd`.
- __`perc`__ represents a percentage and must be a float or integer. This should only exist if grading is set to `toler_perc`.

## Example Usage

Taken from ME2 Fluid Mechanics tutorial sheet 2, this part contains a Numeric response area with some extra parameters. The response area now requires the user to input both a number and a unit using `answer.units` and `showAnswer`. The user has also been given a tolerance that their answer must fall into using `grading` and `perc`.

In this case, Their answer must be equal to __2 ± 5% m/s__ in order to get the point.

```json
{
  "statement": "We are going to test a \\(1/25\\) scale model of a \\(100\\,\\mathrm{m}\\) long ship. If the maximum velocity of the full-scale ship is \\(10\\,\\mathrm{m/s}\\), what should the maximum speed of the model be?",
  "response": {
    "mode": "Numeric",
    "grading": "toler_perc",
    "perc": 5.0,
    "showUnits": true,
    "answer": {
        "num": 2.0,
        "units": "m/s"
    }
  }
}
```
