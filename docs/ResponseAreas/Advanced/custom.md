# Custom response area Documentation
This type of response area is a superset of the "Vanilla" Mobius response areas. It gives the user full control over the layout, styling and display of input fields by allowing rich HTML input in the `layout field`. Essentially this response area is just a wrapper around vanilla response areas to give more control over their positions and styling. Examples of such control would be in-paragraph response areas, or complex table layouts

## Usage in a question JSON file:
```json
"custom_response": {
  "layout": "Rich HTML",
  "responses": [
    {
      "mode": "",
      "more params..."
    },
    ...
  ]
}
```

### `layout`
The layout field accepts rich HTML for where and how the responses in `responses` should be displayed for the student. The positions for each of the response areas should be marked using `<1>, <2>, <3>, ...` tags. Indexed starting from 1, this denotes which response in the `responses` list to use.

Being stored in a JSON file, the `layout` string should be reduced to one line, and escape any quote characters (" -> \")

*NOTE: This is also how Mobius natively labels its response areas in question XML files*

### `responses`
This is a list containing the params for each of the response areas labelled in `layout`. Any vanilla maple response area ([maple][1], [numeric][2], [list][3], etc..) can be used here. Params use the same format as described in their respective response area documentations.

[1]: ../Vanilla/maple.md
[2]: ../Vanilla/numeric.md
[3]: ../Vanilla/list.md

## Example Usage with a HTML table
```json
"custom_response": {
  "layout": "<p>Input the params for this system:</p> <br> <table> <tr><td>Mass:</td><td><1></td></tr> <tr><td>Speed:</td><td><2></td><tr> </table>",
  "responses": [
    {
      "mode": "Numeric",
      "answer": {
        "units": "kg",
        "num": 15
      }
    },
    {
      "mode": "Numeric",
      "answer": {
        "units": "m/s",
        "num": 19.7
      }
    }
  ]
}
```

A beautified version of the html in the `layout` of this example looks like this:
```html
<p>Input the params for this system:</p>
<br>
<table>
  <tr>
    <td>Mass:</td>
    <td><1></td>
  </tr>
  <tr>
    <td>Speed:</td>
    <td><2></td>
  <tr>
</table>
```

The mass and speed response areas will appear where those `<1>` and `<2>` tags appear respectively.
