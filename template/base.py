import re
import os

try:
    setting_path = os.environ.get('SETTING_MODULE')
    settings = import_module(setting_path)
except:
    pass

TOKEN_TEXT = 0
TOKEN_VAR = 1
TOKEN_BLOCK = 2
TOKEN_COMMENT = 3
TOKEN_INCLUDE = 4
TOKEN_CONTENT = 5

TOKEN_MAPPING = {
    TOKEN_TEXT: 'Text',
    TOKEN_VAR: 'Var',
    TOKEN_BLOCK: 'Block',
    TOKEN_COMMENT: 'Comment',
}

# template syntax constants
#FILTER_SEPARATOR = '|'
#FILTER_ARGUMENT_SEPARATOR = ':'
#VARIABLE_ATTRIBUTE_SEPARATOR = '.'
BLOCK_TAG_START = '{%'
BLOCK_TAG_END = '%}'
VARIABLE_TAG_START = '{{'
VARIABLE_TAG_END = '}}'
COMMENT_TAG_START = '{#'
COMMENT_TAG_END = '#}'
#TRANSLATOR_COMMENT_MARK = 'Translators'
#SINGLE_BRACE_START = '{'
#SINGLE_BRACE_END = '}'
# newly added below
INCLUDE_TAG_START = '{+'
INCLUDE_TAG_END = '+}'
CONTENT_TAG_START = '{@'
CONTENT_TAG_END = '@}'



string_from_other_template = []

tag_re = (re.compile('(%s.*?%s|%s.*?%s|%s.*?%s|%s.*?%s|%s.*?%s)' %
          (re.escape(BLOCK_TAG_START), re.escape(BLOCK_TAG_END),
           re.escape(VARIABLE_TAG_START), re.escape(VARIABLE_TAG_END),
           re.escape(COMMENT_TAG_START), re.escape(COMMENT_TAG_END),
           re.escape(INCLUDE_TAG_START), re.escape(INCLUDE_TAG_END),
           re.escape(CONTENT_TAG_START), re.escape(CONTENT_TAG_END))))


class Template:
    def __init__(self, template_string):
        self.token_finder = Token_finder(template_string)

    def render(self, context):
        return self.token_finder.find_token(context)

class Token:
    def __init__(self, token_type, contents, position=None, lineno=None, syntax=None):
        self.token_type = token_type
        self.contents = contents
        self.position = position
        self.lineno = lineno
        self.syntax = syntax


class Token_finder:
    def __init__(self, template_string):
        self.template_string = template_string
        #self.template_split = template_string.split()
        #self.processing = False
        #self.variable_tag_start = False
        #self.var_result = []


    def find_token(self, context):
        self.template_string
        lexar = Lexar(context)
        parse = Parse(context)
        result_token = []
        output = []

        # token categorize
        for bit in tag_re.split(self.template_string):
            if bit:
                result_token.append(lexar.tag_matching(bit))

        # token parse
        for i in result_token:
            if parse.parsing(i):
                output.append(parse.parsing(i))
            else:
                continue


        return self.combine(output)


    def combine(self, template_result):
        a = ""
        for i in template_result:
            a = a + i
        return a



class Lexar:
    def __init__(self, context):
        self.context = context
        self.in_tag = False
        #self.string_for_parse = "" # for compile() & exec()
        #self.verbatim = ""
        #self.block_num = 0
        #self.block_string = [] # a list for store the statements in the block
        self.count = 0
        self.isif = False
        self.iselse = False

    def tag_matching(self, token_string):
        # TOKEN_VAR
        # e.g. {{ my_name }}
        if token_string.startswith("{{") and token_string.endswith("}}"):
            block_content = token_string[2:-2].strip()
            return Token(TOKEN_VAR, block_content)

        # TOKEN_COMMENT
        # e.g. {# I made a comment here hehe #}
        elif token_string.startswith("{#") and token_string.endswith("#}"):
            return Token(TOKEN_COMMENT, None)

        # TOKEN_INCLUDE
        # e.g. {+ "etc/menu.html" +}
        elif token_string.startswith("{+") and token_string.endswith("+}"):
            try:
                file_name = token_string[2:-2].strip()[1:-1]
                for i in settings.INSTALLED_APPS:
                    url = i+"/"+file_name
                    if os.path.isfile(url):
                        global string_from_other_template
                        file = open(url, "r")
                        string_from_other_template.append(file.read())
                        file.close()
                        return Token(TOKEN_INCLUDE, None)
            except:
                print("file not found")
                raise

        # TOKEN_CONTENT
        # e.g. {@ h1_title @} add a content named "h1_title" from the file included
        elif token_string.startswith("{@") and token_string.endswith("@}"):
            block_content = token_string[2:-2].strip()
            return Token(TOKEN_CONTENT, block_content)

        # TOKEN_BLOCK
        elif token_string.startswith("{%") and token_string.endswith("%}"):
            block_content = token_string[2:-2].strip()
            syntax = block_content.split()[0]
            # if tag
            if syntax == "if":
                try:
                    if not self.isif and not self.iselse:
                        self.isif = True
                        self.iselse = False
                        return Token(TOKEN_BLOCK, block_content, syntax="if")
                except:
                    print("\"If\" cannot used more than once")
                    raise
            

            # elif tag
            elif syntax == "elif":
                try:
                    if self.isif and not self.iselse:
                        return Token(TOKEN_BLOCK, block_content, syntax="elif")
                except:
                    print("else has to be between if and else")
                    raise

            # else tag
            elif syntax == "else":
                try:
                    if self.isif and not self.iselse:
                        self.isif = False
                        self.iselse = True
                        return Token(TOKEN_BLOCK, block_content, syntax="else")
                except:
                    print("else has to be at last")
                    raise

            # endif tag
            elif block_content == "endif":
                self.isif = False
                self.iselse = False
                return Token(TOKEN_BLOCK, block_content, syntax="endif")


            # for tag
            # not finished yet
            elif syntax == "for":
                return Token(TOKEN_BLOCK, block_content, syntax="for")

            # endfor tag
            elif block_content == "endfor":
                return Token(TOKEN_BLOCK, block_content, syntax="endfor")

            # static tag
            elif syntax == "static":
                return Token(TOKEN_BLOCK, block_content, syntax="static")




        # NORMAL_TEXT
        else:
            return Token(TOKEN_TEXT, token_string)



class Parse:
    def __init__(self, context):
        self.context = context
        self.block_process = Block_process(context)
        #self.isif = False
        #self.iselse = False
        self.endif = True
        self.endfor = True
        self.nextif = False # if True, skip the codes under that if statement
        self.didif = False # first if statement is true
        self.didelif = False

    def parsing(self, tok):
        if not self.nextif:
            # TOKEN_VAR
            if tok.token_type == TOKEN_VAR:
                try:
                    return str(self.context.dict_[tok.contents])
                except:
                    print(block_content + " not found")
                    raise

            # NORMAL_TEXT
            elif tok.token_type == TOKEN_TEXT:
                return tok.contents

            # TOKEN_COMMENT
            elif tok.token_type == TOKEN_COMMENT:
                pass

            # TOKEN_INCLUDE
            elif tok.token_type == TOKEN_INCLUDE:
                pass

            # TOKEN_CONTENT
            elif tok.token_type == TOKEN_CONTENT:
                searching_re = (re.compile('(%s.*?%s)' % (re.escape(CONTENT_TAG_START), re.escape(CONTENT_TAG_END))))
                recording = False
                store = ""
                for i in string_from_other_template:
                    for j in searching_re.split(i):
                        if not recording and j.startswith("{@") and j.endswith("@}"):
                            block_content = j[2:-2].strip()
                            if block_content == tok.contents:
                                recording = True
                                continue
                        elif recording:
                            if not j.startswith("{@") and not j.endswith("@}"):
                                store += j.strip()

                            elif j.startswith("{@") and j.endswith("@}"):
                                if j[2:-2].strip() == "end":
                                    # a recursion to compile some tokens in the blocks
                                    recording = False
                                    to_parse = Token_finder(store)
                                    return to_parse.find_token(self.context)
                                else:
                                    print("no end block")
                                    raise

        # TOKEN_BLOCK
        if tok.token_type == TOKEN_BLOCK:
            # if block
            if tok.syntax == "if":
                self.nextif = True
                self.endif = False
                a = self.block_process.process(tok.contents[2:], "if")
                if a:
                    self.nextif = False
                    self.didif = True
                else:
                    self.nextif = True

            elif tok.syntax == "elif":
                self.nextif =  True
                if not self.didif:
                    a = self.block_process.process(tok.contents[4:], "if")
                    if a:
                        self.nextif = False
                        self.didelif = True
                    else:
                        self.nextif = True

            elif tok.syntax == "else":
                self.nextif = True
                if not self.didif and not self.didelif:
                    self.nextif = False

            # end if processing
            elif tok.syntax == "endif":
                self.endif = True
                self.nextif = False

            # make sure that it won't skip due to if statement
            elif not self.nextif:
                if tok.syntax == "static":
                    url = tok.contents.split()[1][1:-1]
                    static_url = os.path.join(settings.STATIC_URL, url)
                    return static_url




class Block_process:
    def __init__(self, context):
        self.context = context

    def process(self, block_content, syntax):
        #print("enter to process")
        if syntax == "if":
            for qieop, qpoqp in self.context.dict_.items():
                ijwefnj = qieop + "=" + "qpoqp"
                exec(ijwefnj)

            #print(eval(block_content))
            return eval(block_content)

        #elif syntax == "for":


class Context:
    def __init__(self, dict_):
        self.dict_ = dict_


