## odt_templater - a simple Open Document Text templating tool

This is a minimal module for creating ODT files based on ODT templates and
dictionaries of values.
    
Note that the template rendering is based on regular expression matches on
the ODT internal XML data; as such it should not be considered robust and
will most certainly fail on some inputs. However, it's "good enough" to be
very useful considering the tiny code footprint - there are more lines of
documentation than code here!
    
Just be sure to test your templates...
    
Example:
    
    from odt_template import render_odt_template

    # Assuming a template that has:
    #   - A @TO@ marker somewhere on the page
    #   - A table with a row containing @CHILD@ and @NAUGHTY@ markers
    #   - An embedded image named XMAS.png
    #
    render_odt_template('xmas-template.odt', 'simpsons-family.odt', {
        'to': 'Santa Claus',
        'child': [
            {'child': 'Bart', 'naughty': 'yes'},
            {'child': 'Lisa', 'naughty': 'no'},
            {'child': 'Maggie', 'naughty': 'no'}
        ],
        'Pictures/XMAS.png': open('pretty-tree.png', 'r').read()
    })


### Contributions and bug reports

Please file pull requests or open issues on this project's Github repository,
at <https://github.com/BjarniRunar/odt-templater/>.


### Copyright and License (MIT)

This code is (C) Copyright 2017, Bjarni Rúnar Einarsson.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
