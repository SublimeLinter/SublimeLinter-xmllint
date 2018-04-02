SublimeLinter-xmllint
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-xmllint.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-xmllint)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [xmllint](http://xmlsoft.org/xmllint.html).
It will be used with files that have the "XML" syntax.

## Installation
SublimeLinter must be installed in order to use this plugin. 

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

Before using this plugin, ensure that `xmllint` is installed on your system.
On recent versions of Mac OS X, `xmllint` comes pre-installed. To install `xmllint` on other platforms, do the following:

1. On Linux:

     ```text
     [sudo] apt-get install libxml2-utils
     ```

2. On Windows, follow the instructions [here](http://flowingmotion.jojordan.org/2011/10/08/3-steps-to-download-xmllint/). There is another version on code.google.com, but that version is incompatible with this plugin.

Please make sure that the path to `xmllint` is available to SublimeLinter.
The docs cover [troubleshooting PATH configuration](http://sublimelinter.com/en/latest/troubleshooting.html#finding-a-linter-executable).

## Settings
- SublimeLinter settings: http://sublimelinter.com/en/latest/settings.html
- Linter settings: http://sublimelinter.com/en/latest/linter_settings.html

`xmllint` has many possible command line arguments ("args") which may be passed via the Linter settings.

