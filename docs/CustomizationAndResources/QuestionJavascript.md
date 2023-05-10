# QuestionJavaScript.js
This script is crucial to the proper display of questions created using Nobius. Its features can be broken down into ones which alter Mobius' defaults and design, and ones which dictate the logic for our custom modules.

This file is saved on the Mobius file server (as a .txt as .js files are not allowed), it is imported by every question created by this tool. This allows for changes in logic to be made to a single file, and reflected on all questions which import it at once.

## Mobius Alterations
Although Mobius is a very featureful system, it doesn't provide its users with the upmost level of customization. This script gets around that by modifying the elements on the page when it has already been loaded.

### The 'How did I do?' button
This script heavily modifies the behaviour of this button for our system. By default, Mobius will include one of these at the bottom of a page, which once clicked will mark all of the response areas on the page. However, our system includes question parts under different tabs, which could each contain response areas. We don't want hidden response areas to be marked. The solution therefore developed works as follows:

* The button is copied next to response areas in each of the tabs
* Its styling and text is modified to better fit our custom theme
* Response areas that are on tabs which are currently not in view are "soft hidden". This mean their ids are modified to that Mobius cannot detect them if the "Check" button is pressed.
* This 'soft hiding' mechanic is carried out whenever the active tab changes (the newly appeared response areas are reactivated, and the previous ones are 'soft hidden' again)
* Mobius will make the "Check" button disappear when it has been pressed, in order to bring it back on tab change, we trigger a click event on the now hidden response area.
* An added feature given is the ability to trigger the "Check" button on pressing enter in a response area.

### Styles
* Bottom navigation banner changes:
    * Remove unused buttons (like "Save" and "Next Unit Item")
    * Remove mention of "Page"
* Page style changes:
    * Remove border around question container on hover
    * Remove questionButtons (the How did I Do button is dealt with)
    * Remove Number/Unit help buttons
* Maple question buttons
    * Remove unused buttons
    * Insert custom preview button
    * Insert custom Maple Help button


## Custom logic
All of the JavaScript event handlers for the custom tabs and buttons are declared in this script. These include:

* Question part tabs
* Help button
* Final answer, worked solutions and structured tutorial buttons
* Step by step worked solutions navigation buttons
* Warning tooltips for answer help buttons
* Injecting Comment thread HTML and event handlers
