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

    valid_classes = {
        "BaseModel": BaseModel,
        }
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

    def _split_line(self, line):
        """ A helper method to split each line """
        try:
            line_parts = line.split()
            return line_parts
        except ValueError as e:
            print(f"Splitting line error: {e}")
            return None
    
    def _validate_class_name(self, class_name):
        """ A helper method to validate class name """
        if not class_name:
            print("** class name missing **")
            return False
        elif class_name not in self.valid_classes:
            print("** class doesn't exist **")
            return False
        else:
            return True
            

    
    def do_create(self, line):
        """
        Creates a new instance of the class
        saves it (to the JSON file)
        and prints the id
        """
        args = self._split_line(line)
        if not args or not self._validate_class_name(args[0]):
            return
        new_instance = self.valid_classes[args[0]]()
        print(new_instance.id)
        new_instance.save()

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
        # """
        # """
        # accepted_classes = {
        #     "BaseModel": BaseModel,
        # }

if __name__ == '__main__':
    HBNBCommand().cmdloop()