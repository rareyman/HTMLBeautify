# HTMLBeautify (for Sublime Text 2) v0.5
* (Inspired by fhtml.pl by John Watson)
* by Ross A. Reyman on 09/20/12
* url:			http://reyman.name/
* e-mail:		ross@reyman.name

---

A plugin for [Sublime Text 2](http://sublimetext.com/2), that formats (indents) HTML source code.
It makes code easier for humans to read.

---

## Notes
* This script assumes an effort has been made by the user to expand tags to different lines. This script will **not**  automatically expand minimized/compressed code—it will only try to “clean-up” code that needs to be re-indented
* This script uses `\t` characters to create indentation levels and spacing—ST2 appears to honor whether the user prefers spaces or tabs in ST2 settings and adjusts accordingly (TODO: Should this be addressed in the script?)
* Use `tag_pos_inline` setting to define tags that _might_ appear on one line
* If using possible inline tags (`tag_pos_inline`), it is best to use self-closing tags (XHTML-style)

## Installation

* Downnload the zip, re-name resulting folder to: `HTMLBeautify`, then put the folder into your Sublime Text 2 Packages folder.

(Package Control Install later?)

## Usage
* Open a file containing HTML.
* Select HTML code you want to beautify. (If no selection is made the plugin will run on the whole file.)
* Press `super+alt+shift+f` on OS X to run HTMLBeautify or use the Menu item located in the Edit menu.
* You can test out the script with `HTMLBeautifyTest.html`: an HTML file with wacky indenting for you to see how this script works.

## Settings

You can configure which tags should be processed with this script:

* `ignored_tag_opening` : What are the opening tags that tell the script to ignore HTMLBeautify formatting?
* `ignored_tag_closing` : What are the closing tags that tell the script to resume HTMLBeautify formatting?

* `tag_indent` : If one of these opening tags is encountered, the contents (next line) will be indented by one level.
* `tag_unindent` : If one of these closing tags is encountered, the next line will be un-indented one level.

* `tag_pos_inline` : These are special “one line” tags that open and close on the same line, so indenting should be ignored.

## Disclaimer
This script has been tested for basic HTML coding situations, but your mileage may vary—use with caution if using this in a production environment. (Please report bugs or contribute corrections to the script!) Although the script does not remove or modify code directly (it only attempts to adjust indentation levels), be sure to test this script throughly to make sure it works as expected! The author is not responsible for any bugs that might be introduced to your HTML. :)

