'''
=======
widgets
=======

Tools relating to ipywidgets

'''
from collections import OrderedDict
import collections.abc, inspect

from IPython import display
import ipywidgets

from .renderers import html_table


def explore(obj):
    '''
    Interactive object explorer

    Args:
        obj: Object to introspect

    This widget displays an object and some information about it (eg: its
    signature, if it's callable) and provides a dropdown to select one of its
    attributes.  The selected attribute is displayed in the same way (including
    a dropdown of the attribute's attributes.)
    '''
    def show_markdown(markdown):
        display.display(display.Markdown(markdown.replace('>', '\\>')))
    flag_predicates = {'callable': callable}
    flag_predicates.update({k: v for k, v in vars(inspect).items() if k.startswith('is') and callable(v)})
    show_markdown('### {typ}'.format(typ=type(obj).__name__))
    display.display(obj)
    flag_names = sorted(k[2:] for k, v in flag_predicates.items() if v(obj))
    if flag_names:
        show_markdown('_({})_'.format(', '.join(flag_names)))
    if callable(obj):
        try:
            sig = inspect.signature(obj)
        except:
            show_markdown('_No signature available_')
            sig = None
        if sig is not None:
            param_attrs = ['name', 'kind', 'default', 'annotation']
            display.display(display.Markdown('##### Parameters'))
            def str_or_null(x):
                return '' if x is inspect._empty else str(x)
            display.display(display.HTML(str(html_table([[str_or_null(getattr(p, a)) for a in param_attrs] for p in sig.parameters.values()],
                                                        header_row=param_attrs))))
    attr_descriptions = OrderedDict([('', None)])
    retval_key = '<return value>'
    if callable(obj):
        attr_descriptions[retval_key] = retval_key
    attr_descriptions.update(('{val} ({typ})'.format(typ=type(getattr(obj, k)).__name__, val=k), k) for k in dir(obj))
    @ipywidgets.interact(attribute=attr_descriptions)
    def explore_attr(attribute):
        if attribute is not None:
            explore(obj() if attribute == retval_key else getattr(obj, attribute))

def _replace_literals(template, substitutions):
    '''
    Make multiple literal replacements in a template string.

    This can be more convenient than :meth:`str.format` when the format
    string contains {} characters.

    Args:
        template (str): Template string in which to make replacements
        substitutions (:class:`collections.ABC.Mapping` or :class:`collections.ABC.Iterable`): pairs of: (<string to replace>, <replacement>)

    Returns: str

    Example:
        >>> _replace_literals('soup to nuts', {'soup': 'farewell', 'nuts': 'arms'})
        'farewell to arms'
        >>> js_template = 'function my_fun() {x = 1/*replace this*/; return x;}'
        >>> replacements = {'1/*replace this*/': 3}
        >>> _replace_literals(js_template, replacements)
        'function my_fun() {x = 3; return x;}'
    '''
    result = template
    for k, v in (substitutions.items() if isinstance(substitutions, collections.abc.Mapping) else substitutions):
        result = result.replace(str(k), str(v))
    return result

def source_code_display_toggle_button(show_initially=True):
    '''
    Add a button to toggle display of source code cells in a Jupyter notebook

    Args:
        show_initially (bool): Begin with source code visible
    '''
    js_template = '''
        <script>
               code_show=true/* Set to opposite of show_initially */;
               function code_toggle() {
                    code_show = !code_show
                    if (code_show){$('div.input').show();} else {$('div.input').hide();}
                   }
               $( document ).ready(code_toggle);
           </script>
           <form action="javascript:code_toggle()">
               <input type="submit" value="Toggle code display">
           </form>
       '''
    substitutions = {'true/* Set to opposite of show_initially */': str(not show_initially).lower()}
    display.display(display.HTML(_replace_literals(template = js_template, substitutions=substitutions)))

def notebook_full_width():
    '''
    Make the cells in the notebook the full width of the browser window.
    '''
    display.display(display.HTML("<style>.container { width:100% !important; }</style>"))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
