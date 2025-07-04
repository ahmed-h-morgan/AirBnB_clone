#!/usr/bin/python3
"""
the Console model
"""
import cmd, sys


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

    # def emptyline(self):
    #     """Do nothing when an empty line is entered"""
    #     pass




if __name__ == '__main__':
    HBNBCommand().cmdloop()