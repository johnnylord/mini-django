import sys
import re
import os
from importlib import import_module

from utils.color import Color
from template.codegen import CodeBuilder

try:
    setting_path = os.environ.get('SETTING_MODULE')
    settings = import_module(setting_path)
except:
    pass

class Error(Exception):
    pass

class TempliteSyntaxError(Error):
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return repr(self.message)

class HtmlTemplite(object):
    """Html template engine

    [Public methods]:
    render --- return a complete html text file.

    [Description]:
        Generate a complete html text file to the user.
    """

    def __init__(self, fpath, *contexts):
        """Compile the html template file to python source code

        [Keyword argument]:
        fpath --- the path to html template file
        contexts --- a dict object the compiled python source code refers to
                    when generate a html text file.

        [Attributes]:
        text --- html template's content
        source --- the compiled source code
        all_vars --- a dict bookkeeping the variable in template file
        loop_vars --- a dict bookkeeping the loop variable in template file
        context --- a dict object the compiled python code refers to when
                    generate a html text file
        _render_function --- the render function
        
        [Description]:
            Based on the html template file user passed into. Compile
        the html template file to a python source code, which can help
        user solve the tag(e.g 'if', 'for') in the template file.
            Execute the compiled python source code to generate a complete
        html text file.
        """
        try:
            # Get the content of html text file
            with open(fpath, 'r') as fin:
                self.text = fin.read()
        except:
            raise
            
        # all_vars --- bookkeep all variable names and their type 
        #               used in html template file
        # loop_vars --- bookkeep the variable names and their type
        #               used in 'for' tag. eg. {% for loop_var in vars %} 
        self.all_vars = dict()
        self.loop_vars = dict()
            
        # Combined the contexts into one self.context
        self.context = {}
        for context in contexts:
            self.context.update(context)

        # Simple html text and some variable content
        buffered = []

        # Helper function to flush the content in buffered to source code.
        def flush_buffer():
            if len(buffered) == 1:
                coder.add_line("append_result(%s)" % buffered[0])
            elif len(buffered) > 1:
                coder.add_line("extend_result([%s])" % ", ".join(buffered))
            else:
                pass
            del buffered[:]
            
        # ----- Code Generation Start -----#
        coder = CodeBuilder()

        coder.add_line("def render_function(context, do_dots):")
        coder.indent()

        # Reserve a section for variable declaration
        vars_coder = coder.add_section()

        # shortcut function
        coder.add_line("result = []")
        coder.add_line("append_result = result.append")
        coder.add_line("extend_result = result.extend")
        coder.add_line("to_str = str")
        
        # ----- Tokenize ------ #
        tokens = re.split(r'(?s)({#.*?#}|{{.*?}}|{%.*?%})', self.text)
        # ----- Tokenize end ---#

        # ----- Parse ------ #
        ops_stack = []
        for token in tokens:
            
            if token.startswith("{#"):
                # Comment in template file
                continue
            elif token.startswith("{{"):
                # Expression in the template file {{ expr }}
                expr = token[2:-2].strip()
                code = self._expr_code(expr)
                buffered.append("to_str(%s)" % code)
            elif token.startswith("{%"):
                # action tag: if, for, end
                flush_buffer()
                words = token[2:-2].strip().split()

                if words[0] == 'if':
                    # {% if expr %}
                    if len(words) != 2:
                        self._syntax_error("[Template] \'if\' tag error\n")
                    ops_stack.append('if')
                    coder.add_line('if %s:' % self._expr_code(words[1]))
                    coder.indent()
                elif words[0] == 'for':
                    # {% for loop_var in xxx %}
                    if len(words) != 4 or words[2] != 'in':
                        self._syntax_error("[Template] \'for\' tag error\n")
                    ops_stack.append('for')
                    self._track_variable(words[1], self.loop_vars)
                    coder.add_line(
                            'for c_%s in %s:' % (
                                words[1],
                                self._expr_code(words[3], list)
                                )
                            )
                    coder.indent()
                elif words[0] == 'static':
                    # {% static 'url' %}
                    if len(words) != 2:
                        self._syntax_error("[Template] \'static\' tag error.\n")
                    static_url = words[1][1:-1]
                    static_url = os.path.join(settings.STATIC_URL, static_url)
                    coder.add_line(
                            "append_result(to_str(%s))" 
                            % repr(static_url)
                            )
                elif words[0].startswith('end'):
                    # {% endxxx %}
                    if len(words) != 1:
                        self._syntax_error("[Template] \'end\' tag error\n")
                    if len(ops_stack) == 0:
                        self._syntax_error("[Template] too much \'end\' tag\n")
                    end_what = words[0][3:]
                    start_what = ops_stack.pop()
                    if start_what != end_what:
                        self._syntax_error(
                                "[Template] Unmatch %s tag\n"
                                % start_what
                                )
                    coder.dedent()
                else:
                    # Unknown tag
                    self._syntax_error(
                            "[Template] unknown template tag %s\n"
                            % words[0]
                            ) 
            else:
                # Literal String
                if token:
                    buffered.append(repr(token))

        # Check the ops_stack is empty
        if ops_stack:
            self._syntax_error(
                    "[Template] unmatch \'%s\' tag\n"
                    % ops_stack[-1]
                    )

        # flush out remaining content
        flush_buffer()

        #---------- Parsing end -----------# 

        # Variable declaration
        # Variable that user needs to provide is the difference set
        # of self.all_vars and self.loop_vars.
        for var, type_ in self.all_vars.items():
            if var not in self.loop_vars.keys():
                if type_ == list:
                    vars_coder.add_line(
                            "c_%s = context.get(%r, [])"
                            % (var, var)
                            )
                else:
                    vars_coder.add_line(
                            "c_%s = context.get(%r, None)"
                            % (var, var)
                            )

        # Return statement in the source code
        coder.add_line("return ''.join(result)")
        coder.dedent()
        self.source = str(coder)
        # ---------- Codegen end ----------#
        
        # Extract the render_function defined in source code to the
        # attribute of this object.
        self._render_function = coder.get_namespace()['render_function']
    
    def _expr_code(self, expr, type_=object): 
        """Convert the expr in html template file into python expr and return
        
        [Keyword arguments]:
        expr --- the expression in html template file
        type_ --- the type of variable

        [Return]:
        python expression in the format of string
        """
        if "|" in expr:
            # Filter expression in template file
            # e.g: {{ var|filter1|filter2 }}
            # Convert to python expression
            # e.g: c_filter2(c_filter1(c_var))
            chunks = expr.split('|')
            code = self._expr_code(chunks[0])
            for func in chunks[1:]:
                self._track_variable(func, self.all_vars, type_)
                code = "c_%s(%s)" % (func, code)
        elif "." in expr:
            # Basic variable reference with dot access
            # e.g {{ var.attr }}
            # Convert tp python expression
            # e.g: do_dots(c_var, attr)
            dots = expr.split('.')
            code = self._expr_code(dots[0])
            args = ", ".join(dots[1:])
            code = "do_dots(%s, %s)" % (code, args)
        else:
            # Basic variable reference
            # e.g {{ var }}
            # Convert to python expression
            # e.g c_var
            self._track_variable(expr, self.all_vars, type_)
            code = "c_%s" % expr 
        return code

    def _track_variable(self, name, var_set, type_=object):
        """Bookkeep the name in the var_set
        
        [Keyword arguemnts]:
        name --- variable name
        var_set --- a set of variable name
        type_ --- the type of variable
        """
        # Check if the name conforms to the python naming rules
        if not re.match(r"[_a-zA-Z][_a-zA-Z0-9]*$", name):
            print("Nameing error")
            sys.exit(1)

        # Bookkeep the variable name and type
        var = { name: type_ }
        var_set.update(var)

    def _do_dots(self, var, *attrs):
        """Do the dot access of a variable and return the value

        [Keyword arguments]:
        name --- variable
        attrs --- a list of attribute name

        [Return]:
        the value of the var with dot access
        """
        for attr in attrs:
            try:
                value = getattr(var, attr)
            except AttributeError:
                value = value[attr]
            if callable(value):
                value = value
        return value

    def _syntax_error(self, message):
        """Raise a Template syntax error
        
        [Keyword arguments]:
        messge --- the message of the template syntax error
        """
        raise TempliteSyntaxError(message)
        
    def render(self, context=None): 
        """Render the html file and return the html file content

        [Keyword arguments]:
        context --- a dict object that the variable used in the template file
                    must be define in the context.

        [Return]:
        the content of the complete html text file.
        """
        render_context = dict(self.context)
        if context:
            render_context.update(context)

        return self._render_function(render_context, self._do_dots)


if __name__ == '__main__':
   
    # Construct the Html template engine
    t = HtmlTemplite("test.html")

    # Render complete html file
    # print(t.source)
    print(t.render({'name': 'Johnny'}))
