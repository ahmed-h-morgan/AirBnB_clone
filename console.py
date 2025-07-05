#!/usr/bin/python3
"""
the Console model
"""
import cmd
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage



class HBNBCommand(cmd.Cmd):
    """
    The Console class
    """
    prompt = "(hbnb) "

    # def do_help(self, arg):
    #     """ Give me more info about method """
    #     return super().do_help(arg)

    def do_quit(self,arg):
        """ Quit command to exit the program """
        return True
    
    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass
    
    def do_create(self):
        pass

    def do_show(self):
        pass

    def do_destroy(self):
        pass

    def do_all(self):
        pass

    def do_update(self):
        pass

    def default(self, line):
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()