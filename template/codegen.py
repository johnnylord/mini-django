
class CodeBuilder(object):

    INDENT_STEP = 4

    def __init__(self, indent=0):
        self.code = []
        self.indent_space = indent

    def add_line(self, line):
        space = " "*self.indent_space
        self.code.append(space+line+"\n")

    def add_section(self):
        section = CodeBuilder(self.indent_space)
        self.code.append(section)
        return section
        
    def indent(self):
        self.indent_space += self.INDENT_STEP

    def dedent(self):
        self.indent_space -= self.INDENT_STEP

    def get_namespace(self):
        source_code = str(self)
        namespace = {}
        exec(source_code, namespace)
        return namespace

    def __str__(self):
        source_code = "".join(str(c) for c in self.code)
        return source_code
