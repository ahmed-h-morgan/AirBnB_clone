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

    # def __init__(self):
    #     self.storage = FileStorage()
    #     self.storage.reload()


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
    
    # def _validate_class_name(self, class_name):
    #     """ A helper method to validate class name """
    #     if not class_name:
    #         print("** class name missing **")
    #         return False
    #     elif class_name not in self.valid_classes:
    #         print("** class doesn't exist **")
    #         return False
    #     else:
    #         return True
            

    
    def do_create(self, line):
        """
        Creates a new instance of the class
        saves it (to the JSON file)
        and prints the id
        """
        args = self._split_line(line)

        if not args:
            print("** class name missing **")
            return
        elif args[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return

        new_instance = self.valid_classes[args[0]]()
        print(new_instance.id)
        new_instance.save()

    def do_show(self, line):
        """
         Prints all string representation of specific instance
        """
        args = self._split_line(line)
        storage = FileStorage()

        print(args)
        stored_objects = storage.all()
        if not stored_objects:
            print("[]")
            return
        
        if len(args) == 0:
            print ("** class name missing **")
            return

        elif len(args) >= 1:
            if args[0] not in self.valid_classes:
                print("** class doesn't exist **")
                return
            elif len(args) == 1:
                print("** instance id missing **")
                return
            else:
                instance_id = ".".join([args[0], args[1]])
                if instance_id not in stored_objects:
                    print("** no instance found **")
                    return
                else:
                    print(stored_objects.get(instance_id))
            # elif args[0] in self.valid_classes:
            #     for key, value in stored_objects.items():
            #         x = key.split('.')
            #         if x[0] != args[0]:
            #             print("** class doesn't exist **")
        # elif len(args) == 2:
        #         for key, value in stored_objects.items():
        #             x = key.split('.')
        #             if x[1] != args[1]:
        #                 print("** class doesn't exist **")            



    def do_destroy(self):
        pass

    def do_all(self, line):
        """
         Prints all string representation of all instances
        """
        args = self._split_line(line)
        storage = FileStorage()

        print(args)
        stored_objects = storage.all()
        if not stored_objects:
            print("[]")
            return

        if len(args) == 0:
            obj_list = []
            for obj in stored_objects:
                obj_list.append(str(obj))
            print(obj_list)
        elif len(args) >= 1:
            if args[0] not in self.valid_classes:
                print("** class doesn't exist **")
                return
            elif args[0] in self.valid_classes:
                named_obj_list = []
                for key, value in stored_objects.items():
                    x = key.split('.')
                    if x[0] == args[0]:
                        named_obj_list.append(str(value))
                print(named_obj_list)

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