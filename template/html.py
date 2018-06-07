import sys
import re
import os
from importlib import import_module

from template.codegen import CodeBuilder

try:
    setting_path = os.environ.get('SETTING_MODULE')
    settings = import_module(setting_path)
except:
    pass
    

class HtmlTemplite(object):

    def __init__(self, fpath, *contexts):

        # Get the content of html text file
        with open(fpath, 'r') as fin:
            self.text = fin.read()

        # 'all_vars': used for store the variable used in tempalte
        # 'loop_vars': the variable used in => for 'loop_vars' in var:
        self.all_vars = set()
        self.loop_vars = set()
            
        # Combined the contexts into one self.context
        self.context = {}
        for context in contexts:
            self.context.update(context)

        # Helper function
        buffered = []
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
                        self._syntax_error("template 'if' tag error.\n")
                    ops_stack.append('if')
                    coder.add_line('if %s:' % self._expr_code(words[1]))
                    coder.indent()
                elif words[0] == 'for':
                    # {% for loop_var in xxx %}
                    if len(words) != 4 or words[2] != 'in':
                        self._syntax_error("template 'for' tag error.\n")
                    ops_stack.append('for')
                    self._track_variable(words[1], self.loop_vars)
                    coder.add_line(
                        'for c_%s in %s:' % (
                            words[1],
                            self._expr_code(words[3])
                        )
                    )
                    coder.indent()
                elif words[0].startswith('load'):
                    self.static = settings.STATIC_URL

                elif words[0].startswith('static'):
                    if len(words) != 2:
                        self._syntax_error("template 'static' tag error.\n")
                    static_url = words[1][1:-1]
                    static_url = os.path.join(self.static,static_url)
                    coder.add_line("append_result(to_str(%s))" % repr(static_url))
                elif words[0].startswith('end'):
                    # {% endxxx %}
                    if len(words) != 1:
                        self._syntax_error("template 'end' tag error.\n")
                    if len(ops_stack) == 0:
                        self._syntax_error("Too much end tag.\n")
                    end_what = words[0][3:]
                    start_what = ops_stack.pop()
                    if start_what != end_what:
                        self._syntax_error("Unmatch %s tag\n" % start_what)
                    coder.dedent()
                else:
                    # Unknown tag
                    self._syntax_error("Unknown template tag %s\n" % words[0]) 
            else:
                # Literal String
                if token:
                    buffered.append(repr(token))

        # Check the ops_stack is empty
        if ops_stack:
            self._syntax_error("Unmatch %s tag\n" % ops_stack[-1])

        # flush remaining content into 
        flush_buffer()

        #---------- Parsing end -----------# 

        for var_name in self.all_vars - self.loop_vars:
            vars_coder.add_line("c_%s = context.get(%r, None)" % (var_name, var_name))

        coder.add_line("return ''.join(result)")
        coder.dedent()
        # ---------- Codegen end ----------#
        
        self._render_function = coder.get_namespace()['render_function']
    
    def _expr_code(self, expr): 
        if "|" in expr:
            chunks = expr.split('|')
            code = self._expr_code(chunks[0])
            for func in chunks[1:]:
                self._track_variable(func, self.all_vars)
                code = "c_%s(%s)" % (func, code)
        elif "." in expr:
            dots = expr.split('.')
            code = self._expr_code(dots[0])
            args = ", ".join(dots[1:])
            code = "do_dots(%s, %s)" % (code, args)
        else:
            self._track_variable(expr, self.all_vars)
            code = "c_%s" % expr 
        return code

    def _track_variable(self, name, var_set):
        if not re.match(r"[_a-zA-Z][_a-zA-Z0-9]*$", name):
            print("Nameing error")
            sys.exit(1)
        var_set.add(name)

    def _do_dots(self, name, *attrs):    
        for attr in attrs:
            try:
                value = getattr(name, attr)
            except AttributeError:
                value = value[attr]
            if callable(value):
                value = value
        return value

    def _syntax_error(self, msg):
        print(msg)
        sys.exit(1)

    def render(self, context=None): 
        render_context = dict(self.context)
        if context:
            render_context.update(context)

        return self._render_function(render_context, self._do_dots)


if __name__ == '__main__':
    
    t = HtmlTemplite("test.html")
    print(t.render({'name': 'Johnny', 'numbers':[0, 1, 2]}))
