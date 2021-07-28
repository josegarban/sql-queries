"""
Sqlite functions
"""

import pprint, sqlite3

####################################################################################################
# INSTRUCTION CREATION
####################################################################################################

def dictfieldnames_to_tuplist(input_dict):
    """
    Inputs: dictionary.
    Objective: gets fields in a dictionary and converts them to a list.
            Supports cases when different items in a dictionary don't all have the same fields.
    Returns: list containing tuples of the form (fieldname, fieldtype)
    """
    output_list = []

    # Check if the primary key is an integer or a string
    primarykey_istext = True
    for k in list(input_dict.keys()):
        try:
            if type(k) is int: primarykey_istext = False
        except:
            primarykey_istext = True
            continue # At the first sight of a non-integer key, the loop will end

    if   primarykey_istext: output_list.append(("id", "VARCHAR(32) PRIMARY KEY"))
    else                  : output_list.append(("id", "INTEGER PRIMARY KEY"))

    # Search all inner dictionaries in a dictionary
    for fieldname in input_dict:  # It should not matter if the dictionary contains dictionaries or a list
        if   type(fieldname) is int  : fieldtype = "INTEGER"
        elif type(fieldname) is str  : fieldtype = "TEXT"
        elif type(fieldname) is bool : fieldtype = "BINARY"
        elif type(fieldname) is float: fieldtype = "REAL"
        else : fieldtype = "TEXT"
        if   (fieldname, fieldtype) not in output_list : output_list.append((fieldname, fieldtype))

    return output_list

####################################################################################################

def dictfieldnames_to_tup(input_dict):
    """
    Inputs: dictionary.
    Objective: gets fields in a dictionary and converts them to a list.
            Supports cases when different items in a dictionary don't all have the same fields.
    Returns: tuple containing fieldnames only
    """
    fieldfullinfo = dictfieldnames_to_tuplist(input_dict)
    fieldnames = [x[0] for x in fieldfullinfo]

    return tuple(fieldnames)

####################################################################################################

def dictfields_to_string(input_dict):
    """
    Inputs: dictionary.
    Objective: gets fields in a dictionary and converts them
                to a string representation of a list for use in SQL instructions.
    Returns: string.
    """
    # Field_list is a list containing tuples of the form (fieldname, fieldtype)
    field_list = dictfieldnames_to_tuplist(input_dict)

    output_string = ""
    for field_tup in field_list:
        field_string = "{0} {1}, ".format(field_tup[0], field_tup[1])
        output_string = output_string + field_string
    output_string = "(" + output_string[:-2] + ")" # -2 to remove the last comma and space

    return output_string

####################################################################################################

def dictfieldnames_to_string(input_dict):
    """
    Inputs: dictionary.
    Objective: gets field names in a dictionary and converts them
                to a string representation of a list for use in SQL instructions.
    Returns: string.
    """
    # Field_list is a list containing tuples of the form (fieldname, fieldtype)
    field_list = dictfieldnames_to_tuplist(input_dict)

    output_string = ""
    for field_tup in field_list:
        field_string = "{0}, ".format(field_tup[0])
        output_string = output_string + field_string
    output_string = "(" + output_string[:-2] + ")" # -2 to remove the last comma and space

    return output_string

####################################################################################################
# SQL MANIPULATION
####################################################################################################

def create_connector(sql_filename):
    """
    Inputs: filename or path.
    Objective: open the sqlite database.
    Outputs: connector.
    """
    # Open the Sqlite database we're going to use (my_cursor)
    my_connector = sqlite3.connect(sql_filename)

    return my_connector

####################################################################################################
# ADDING TABLES
####################################################################################################

def create_table(input_dict, sql_filename = "", sql_table = "", print_intermediate = True):
    """
    Inputs: filename, table that will be updated or created, and a dictionary.
            The table won't be created if it already exists.
            print_intermediate will let some intermediate stepts to be reported on-screen
    Objective: a table in a sql table will be created but not filled with data,
            based on the dictionary.
    Outputs: none.
    """

    # Open the database and get the table name if none has been set
    my_connector = create_connector(sql_filename)
    my_cursor    = my_connector.cursor()
    if sql_table == "": sql_table = input("Insert table name:")

    # When columns are in an inner dictionary, the column names are in the first row
    first_row = input_dict[list(input_dict.keys())[0]]
    fieldnames = [ "\'"+f+"\'" if " " in f else f for f in first_row ]
    # Build the instruction to be executed to create the table
    fieldnames_str = ""
    for f in fieldnames: fieldnames_str += f+", "
    fieldnames_str = "("+fieldnames_str[:-2]+")"
    print (fieldnames_str)

    # Build the instruction to be executed to create the table
    instruction = """CREATE TABLE IF NOT EXISTS {0} {1}""".format(sql_table, fieldnames_str)

    # Create the table
    if print_intermediate == True: print("Executing instruction:", instruction)
    my_cursor.execute(instruction)

    return "Instruction executed: "+instruction

####################################################################################################
# ROW OPERATIONS
####################################################################################################

def add_dbrows(input_dict,
               sql_filename = "",
               sql_table = "",
               dbkey_column = "id",
               print_intermediate = True):
    """
    Inputs: filename, name of the table that will be updated or created, and a nested dictionary.
            The dictionary has row numbers as external keys, and column names as inner keys
            The table won't be created if it already exists.
    Objective: a table in a sql table will be filled with data,
                or edited if existing, from a dictionary.
    Outputs: string reporting changes.
    """
    output_string = ""

    # Open the database and get the table name if none has been set
    my_connector = create_connector(sql_filename)
    my_cursor    = my_connector.cursor()
    if sql_table == "": sql_table = input("Insert table name:")

    # When columns are in an inner dictionary, the column names are in the first row
    first_row = input_dict[list(input_dict.keys())[0]]
    fieldnames = [ "\'"+f+"\'" if " " in f else f for f in first_row ]

    # Build the instruction to be executed to create the table
    fieldnames_str = ""
    for f in fieldnames: fieldnames_str += f+", "
    fieldnames_str = "("+fieldnames_str[:-2]+")"
    print (fieldnames_str)
    questionmarks  = "(" + (("?, ")*len(fieldnames))[:-2] + ")"
    instruction    = """INSERT OR IGNORE INTO {0} {1} VALUES {2}""".format(
        sql_table, fieldnames_str, questionmarks)

    # Get the values in the instruction
    for outer_key in input_dict:
        values     = [outer_key] # This is the id
        for value in input_dict[outer_key].values():
            values.append(value)
        values = values [1:]

    # Execute the instruction
        row_string = "Instruction executed: {0} in table {1} in {2}.\nValues: {3}\n".format(
            instruction, sql_table, sql_filename, tuple(values))
        if print_intermediate == True: print("Executing instruction:", row_string)

        my_cursor.execute(instruction, tuple(values))
        output_string = output_string + row_string

    # Commit and report the changes
    my_connector.commit()
    my_connector.close()

    return output_string
