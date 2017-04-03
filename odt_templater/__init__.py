#!python2
# vim: set fileencoding=utf-8 :
#
"""Simple Open Document Text templating tool

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

"""
import re
import sys
import time
import zipfile


def render_odt_template(template_file, output_file, variables):
    """
    Render an ODT template given a set of variables.

    The file arguments are passed directly to zipfile.ZipFile(), see that
    module's documentation for details on what works and what does not.
    Generally both file-names and file-like-objects should work.

    The variables should be a dictionary of placeholder names to values;
    names should match either a file-name in the ODT ZIP archive (such as
    a path to an image) or placeholders in the text content area.

    Within the content area, variable["foo"] will translate markers @FOO@
    in the ODF file.

    Special behaviour is implemented if the data is a list; in that case
    the template will look for an ODT list or ODT table row containing the
    marker, and will attempt to duplicate the entire list-item or table
    row for each entry of the list.

    Further, if the entries in the list are themselves dicts, then multiple
    substitutions can take place in each new list item or table row.
    """
    tzf = zipfile.ZipFile(template_file, mode="r")
    ozf = zipfile.ZipFile(output_file, mode="w",
                          compression=zipfile.ZIP_DEFLATED)

    def template_replace(data, key, val):
        def e(t):
            return (unicode(t).replace('&', '&amp;')
                              .replace('<', '&lt;')
                              .replace('>', '&gt;')).encode('utf-8')
        try:
            mark = unicode('@%s@' % key).upper().encode('utf-8')
            if isinstance(val, (list, tuple, dict)):
                # Lists/tuples/dicts trigger our list and table mode
                def lexpand(match):
                    tpl = match.group(0)

                    def vexpand(t, v):
                        if isinstance(v, (dict,)):
                            for dk, dv in v.iteritems():
                                dk = unicode(dk).encode('utf-8').upper()
                                t = t.replace('@%s@' % dk, e(dv) or ' ')
                            return t
                        return t.replace(mark, e(v) or ' ')

                    return (''.join([vexpand(tpl, v) for v in val]) or ' ')
                return re.sub((
                    '<(text:list-item|table:table-row)>'
                    '(<(?!table:table-row)[^>]*>)*'
                    '[^>]*%s.*?</\\1>' % mark), lexpand, data)
            else:
                # Other values are simply stringified
                return data.replace(mark, e(val) or ' ')
        except:
            sys.stderr.write('Failed to replace `%s` with `%s`\n' % (mark, val))
            raise

    try:
        fn = '(unknown)'
        for fn in tzf.namelist():
            data = tzf.read(fn)
            if fn.endswith('content.xml'):
                for k, v in variables.iteritems():
                    data = template_replace(data, k, v)
            elif fn in variables:
                data = variables[fn]
            ozf.writestr(fn, data)
    except:
        sys.stderr.write('Failed to process `%s`\n' % fn)
        raise
    finally:
        ozf.close()
        tzf.close()


if __name__ == '__main__':
    render_odt_template(sys.argv[1], sys.argv[2], {
        'name': u'Bjarni Rúnar Einarsson',
        'action': u'Testing stuff at %d' % time.time(),
        'item': [{'item': 'pot', 'units': 1, 'unit_price': 25, 'price': 25},
                 {'item': 'ato', 'units': 3, 'unit_price': 20, 'price': 60}],
        'thing': ['one', 'two', 'three']
    })
