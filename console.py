#!/usr/bin/python3
"""
the Console model
"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.engine.file_storage import FileStorage
import shlex



class HBNBCommand(cmd.Cmd):
    """
    The Console class
    """
    prompt = "(hbnb) "

    valid_classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Amenity": Amenity,
        "City": City,
        "Place": Place,
        "Review": Review,
        "State": State,
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


        stored_objects = storage.all()
        # if not stored_objects:
        #     print("[]")
        #     return
        
        if len(args) == 0:
            print ("** class name missing **")
            return

        elif len(args) >= 1:
            if args[0] not in self.valid_classes:
                print("** class doesn't exist **")
                return
            elif len(args) < 2:
                print("** instance id missing **")
                return
            else:
                instance_key = f"{args[0]}.{args[1]}"
                instance = stored_objects.get(instance_key)
                if not instance:
                    print("** no instance found **")
                    return
                else:
                    print(instance)


    def do_destroy(self, line):
        """
         Delete all string representation of specific instance
        """
        args = self._split_line(line)
        storage = FileStorage()
        base = BaseModel()

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
                    del stored_objects[instance_id]
                    base.save()

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

    def do_update(self, line):
        """
        Update an instance based on the class name and id
        """
        args = shlex.split(line)
        storage = FileStorage()

        stored_objects = storage.all()
        if not stored_objects:
            print("[]")
            return

        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.valid_classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        
        storage_key = f"{args[0]}.{args[1]}"
        if storage_key not in stored_objects:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        # Handle protected attributes
        if args[2] in ['id', 'created_at', 'updated_at']:
            print("** cannot update protected attribute **")
            return

        # Process value
        passed_value = args[3].strip('"\'')
        try:
            passed_value = int(passed_value)
        except ValueError:
            try:
                passed_value = float(passed_value)
            except ValueError:
                pass  # Keep as string

                instance = stored_objects[storage_key]
                setattr(instance, args[2], passed_value)
                instance.save()


    def default(self, line):
        """
        
        """
        id = ""
        if '.' in line and line.endswith('.all()'):
            class_name = line.split('.')[0]
            if class_name in self.valid_classes:
                return self.do_all(class_name)
            else:
                print("** class doesn't exist **")
                return
        elif '.' in line and line.endswith('.count()'):
            class_name = line.split('.')[0]
            if class_name in self.valid_classes:
                storage = FileStorage()
                stored_objects = storage.all()
                obj_count = 0
                for key in stored_objects:
                    if key.startswith(class_name + '.'):
                        obj_count += 1
                print(obj_count)

        elif '.' in line and '.show(' in line and line.endswith(')'):
            try:
                # Split into parts
                class_part, id_part = line.split('.show(')
                class_name = class_part.strip()
                id_value = id_part[:-1].strip()  # Remove trailing )
                
                # Remove surrounding quotes if present
                id_value = id_value.strip('"\'')
                
                if class_name in self.valid_classes:
                    if id_value:
                        return self.do_show(f"{class_name} {id_value}")
                    else:
                        print("** instance id missing **")
                else:
                    print("** class doesn't exist **")
            except Exception:
                print("*** Unknown syntax: {}".format(line))

        elif '.' in line and '.destroy(' in line and line.endswith(')'):
            try:
                # Split into parts
                class_part, id_part = line.split('.destroy(')
                class_name = class_part.strip()
                id_value = id_part[:-1].strip()  # Remove trailing )
                
                # Remove surrounding quotes if present
                id_value = id_value.strip('"\'')
                
                if class_name in self.valid_classes:
                    if id_value:
                        return self.do_destroy(f"{class_name} {id_value}")
                    else:
                        print("** instance id missing **")
                else:
                    print("** class doesn't exist **")
            except Exception:
                print("*** Unknown syntax: {}".format(line))

        elif '.' in line and '.update(' in line and line.endswith(')'):
            try:
                # Split into parts
                class_part, id_part = line.split('.update(')
                class_name = class_part.strip()
                id_value = id_part[:-3].strip()  # Remove trailing )
                attribute_name = id_part[:-2].strip()
                attribute_value = id_part[:-1].strip()
                
                # Remove surrounding quotes if present
                id_value = id_value.strip('"\'')
                
                if class_name in self.valid_classes:
                    if id_value:
                        return self.do_destroy(f"{class_name} {id_value} {attribute_name} {attribute_value}")
                    else:
                        print("** instance id missing **")
                else:
                    print("** class doesn't exist **")
            except Exception:
                print("*** Unknown syntax: {}".format(line))  

if __name__ == '__main__':
    HBNBCommand().cmdloop()