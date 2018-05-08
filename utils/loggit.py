import sys
from datetime import datetime
from utils.color import Color
from functools import wraps


def register(color=Color.GREEN, path="stdout"):

    def logit(func):

        @wraps(func)
        def decorator(self, *args, **kwargs):
            """
            Log the called method to File with specific log color
            """
            # Redirect the sys.stdout
            if path == "stdout":
                pass
            else:
                original = sys.stdout
                sys.stdout = open(path, 'a')

            # Extract method metadata
            module = self.__class__.__module__
            cls = self.__class__.__name__
            
            # Log the information to the file
            text = module+"."+cls+":["+func.__name__+"]"
            now = "["+ datetime.now().strftime("%Y-%m-%d|%H:%M:%S") + "]"

            if path == "stdout":
                print(color, now, text, Color.ENDC)
            else:
                print(now, text)
                
            # Args
            # print("\targs:", end=" ")
            # for arg in args:
            #     print(arg, end=" ")
            # print("")

            # # Kwargs
            # print("\tkwargs:", end=" ")
            # print(kwargs.items())
            
            # Recover sys.stdout to original and close file
            if 'original' in locals():
                sys.stdout.close()
                sys.stdout = original
            else:
                pass
            
            return func(self, *args, **kwargs)

        return decorator

    return logit


            
        

