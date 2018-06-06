class CodeBuilder(object):
    """Helper object for constructing source code

    [Public attributes]:
    INDENT_STEP --- the value to add/substract CodeBuilder object's
                    indent_space when the object is in different code level.
    
    [Public methods]:
    add_line --- add a line of source code.
    add_section --- reserve a space in source code 
                    for another codebulder object
    indent --- indent one level
    dedent --- dedent one level
    get_namespace -- get the namespace after the source code is executed.
    """
    INDENT_STEP = 4

    def __init__(self, indent=0):
        """Construct a Codebuilder

        [Keyword arguments]:
        indent --- the initial indent level

        [Attributes]:
        code --- a list stores the lines of source code
        indent_space --- the number of space to indent
        """
        self.code = []
        self.indent_space = indent

    def add_line(self, line):
        """Add a line of source code to self.code

        [Keyword arguments]:
        line --- the code to add in the source code.

        [Description]:
            the preceded indent spaces and trailing newline will
        automatically add the line, and append onto the self.code.
        """
        space = " "*self.indent_space
        self.code.append(space+line+"\n")

    def add_section(self):
        """Return a new Codebuilder object.

        [Return]:
        another Codebuilder object

        [Description]:
            Reserve a space in the source code for another CodeBuilder
        object. This object is for some specific goal, such as variable
        declaration.
        """
        section = CodeBuilder(self.indent_space)
        self.code.append(section)
        return section
        
    def indent(self):
        """Indent a level"""
        self.indent_space += self.INDENT_STEP

    def dedent(self):
        """Dedent a level"""
        self.indent_space -= self.INDENT_STEP

    def get_namespace(self):
        """Execute the code and return the new namespace

        [Return]:
        a namespace which the defined function in source code is stored
        in the returned namespace.

        [Description]:
            Execute the source code stored in self.code list. And return a
        namespace where the defined object in the source code is keep in the
        namespace.
        """
        source_code = str(self)
        namespace = {}
        exec(source_code, namespace)
        return namespace

    def __str__(self):
        """Displat the source code
        
        [Return]:
        the content of the source code
        """
        source_code = "".join(str(c) for c in self.code)
        return source_code
