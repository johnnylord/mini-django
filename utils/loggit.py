import sys
from datetime import datetime
from utils.color import Color
from functools import wraps


def register(color=Color.GREEN, stream="stdout"):
    """Log a function or method with some customized information

    [Keyword arguments]:
    color --- the color of the logging message.
    stream --- the string that indicates the io stream for the logging message.

    [Return]:
    Return a decorator with customized color and stream information

    [Description]
        Use the returned decorator to logg the calling function or method.
    Provide detailed information about how the functions were called, and the
    order of called functions.
    """

    def logit(func):
        """Log a function or method

        [Keyword arguments]:
        func --- the function to log
        
        [Return]:
        a decorated function
        """
        @wraps(func)
        def decorator(self, *args, **kwargs):
            """Print some information of the function to be called

            [Keyword arguments]:
            self --- the instance object of any class
            args --- a list of args passed to the method of self
            kwargs --- a dict of kwargs passed to the method of self

            [Return]:
            the value that the non-decorated function should return

            [Description]:
            Do some works before calling the real function to work.
            """
            # Redirect the sys.stdout to another stream if value of
            # stream is not "stdout"
            if stream != "stdout":
                try:
                    original = sys.stdout
                    sys.stdout = open(stream, 'a')
                except:
                    raise

            # Extract method metadata
            cls_name = self.__class__.__name__
            module_name = self.__class__.__module__
            
            # Logged function message
            text = (module_name + "." + cls_name + "." + func.__name__)

            # The time when the method was called
            now = "["+ datetime.now().strftime("%Y-%m-%d|%H:%M:%S") + "] "
                
            # Logged function's arg information
            type_args = [str(type(arg)) for arg in args]
            args_text = ', '.join(type_args)

            # Logged function's kwargs information
            type_kwargs = [str(type(v))+":"+k for k, v in kwargs.items()]
            kwargs_text = ', '.join(type_kwargs)
            
            # Display colored message on the terminal
            if stream == "stdout":
                print(color + now + text + Color.ENDC, end="(")
                print(args_text, kwargs_text, end=")\n")
            else:
                print(now + text, end="(")
                print(args_text, kwargs_text, end=")\n")

            # Recover sys.stdout to original and close file
            if 'original' in locals():
                sys.stdout.close()
                sys.stdout = original
            
            return func(self, *args, **kwargs)

        return decorator

    return logit


            
        

