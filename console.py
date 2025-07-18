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
from datetime import datetime



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

        # elif '.' in line and '.update(' in line and line.endswith(')'):
        #     try:
        #         # Split into parts
        #         class_part, id_part = line.split('.update(')
        #         class_name = class_part.strip()
        #         id_value = id_part[:-3].strip()  # Remove trailing )
        #         attribute_name = id_part[:-2].strip()
        #         attribute_value = id_part[:-1].strip()
                
        #         # Remove surrounding quotes if present
        #         id_value = id_value.strip('"\'')
                
        #         if class_name in self.valid_classes:
        #             if not id_value:
        #                 # return self.do_update(f"{class_name} {id_value} {attribute_name} {attribute_value}")
        #                 print("** instance id missing **")
        #             elif not attribute_name:
        #                 print("** attribute name missing **")
        #             elif not attribute_value:
        #                 print("** value missing **")
        #             else:
        #                 return self.do_update(f"{class_name} {id_value} {attribute_name} {attribute_value}")
        #                 # print("** instance id missing **")
        #         else:
        #             print("** class doesn't exist **")
        #     except Exception:
        #         print("*** Unknown syntax: {}".format(line))  

        elif '.' in line and '.update(' in line and line.endswith(')'):
            try:
                # Extract the parts between parentheses
                params_str = line.split('.update(')[1][:-1]
                # Use shlex to handle quoted strings
                params = [p.strip('"\'') for p in shlex.split(params_str.replace(',', ' '))]
                
                if len(params) < 3:
                    print("*** Not enough arguments ***")
                    return
                    
                class_name = line.split('.')[0]
                instance_id = params[0]
                attr_name = params[1]
                attr_value = params[2]
                
                # Validate class
                if class_name not in self.valid_classes:
                    print("** class doesn't exist **")
                    return
                    
                # Validate instance exists
                storage = FileStorage()
                key = f"{class_name}.{instance_id}"
                if key not in storage.all():
                    print("** no instance found **")
                    return
                    
                # Protected attributes check
                if attr_name in ['id', 'created_at', 'updated_at']:
                    print("** cannot update protected attribute **")
                    return
                    
                # Type conversion
                try:
                    attr_value = int(attr_value)
                except ValueError:
                    try:
                        attr_value = float(attr_value)
                    except ValueError:
                        pass  # Keep as string
                        
                # Perform update
                instance = storage.all()[key]
                setattr(instance, attr_name, attr_value)
                instance.save()
                
            except Exception as e:
                print("*** Unknown syntax: {} ***".format(line))

        elif '.' in line and '.update(' in line and line.endswith(')'):
            try:
                # Parse the command structure
                class_name = line.split('.')[0]
                params_str = line.split('(', 1)[1][:-1]  # Get content inside parentheses
                
                # Split into ID and dictionary parts
                parts = [p.strip() for p in params_str.split(',', 1)]
                if len(parts) < 2:
                    print("** dictionary missing **")
                    return
                    
                # Clean the instance ID (handle all quote cases)
                instance_id = parts[0].strip(' "\'')
                
                # Handle the dictionary string (may contain commas)
                dict_str = parts[1].strip()
                if not dict_str.startswith('{') or not dict_str.endswith('}'):
                    print("** invalid dictionary **")
                    return
                    
                # Safely evaluate the dictionary
                try:
                    update_dict = eval(dict_str)
                    if not isinstance(update_dict, dict):
                        print("** argument must be a dictionary **")
                        return
                except:
                    print("** invalid dictionary **")
                    return
                    
                # Validate class exists
                if class_name not in self.valid_classes:
                    print("** class doesn't exist **")
                    return
                    
                # Validate instance exists
                storage = FileStorage()
                key = f"{class_name}.{instance_id}"
                all_objs = storage.all()
                if key not in all_objs:
                    print("** no instance found **")
                    return
                    
                # Update instance attributes
                instance = all_objs[key]
                for attr_name, attr_value in update_dict.items():
                    if attr_name in ['id', 'created_at', 'updated_at']:
                        continue  # Skip protected attributes
                        
                    # Convert string numbers to proper types
                    if isinstance(attr_value, str):
                        stripped = attr_value.strip(' "\'')
                        try:
                            attr_value = int(stripped)
                        except ValueError:
                            try:
                                attr_value = float(stripped)
                            except ValueError:
                                attr_value = stripped
                    
                    setattr(instance, attr_name, attr_value)
                
                # Force update timestamp and save
                instance.updated_at = datetime.now()
                instance.save()  # This calls storage.save()
                
            except Exception as e:
                print("*** Unknown syntax: {} ***".format(line))

if __name__ == '__main__':
    HBNBCommand().cmdloop()