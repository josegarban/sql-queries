import pprint
import dbhandler, get_inputs, filegenerator

####################################################################################################

def build_tables(folder="data", extensions=[".csv"], print_intermediate=True):
    """
    Output: nested dictionary where the external keys are file names, the internal keys are row numbers, and the second-order internal keys are columns
    """
    results = dict()

    # Retrieve files that will become the tables
    file_names, table_names = get_inputs.files_in_folder_byext(folder, extensions, print_intermediate)
    for f, t in zip(file_names, table_names):
        df = get_inputs.csv_to_dataframe(f, delimiter=",", print_intermediate=print_intermediate)
        # We get a dictionary where the keys are the file names (future table names) mapped to the lists of values
        results_as_listdict = get_inputs.dataframe_to_listdict(df)
        results[t] = {x: results_as_listdict[x] for x in range(len(results_as_listdict))}
    if print_intermediate: pprint.pprint(results)

    return results

####################################################################################################

def populate_db(data, dbfilename="database.sqlite", folder="data", extensions=[".csv"], print_intermediate=True):
    """
    Input: blank, if set by user. For testing, a dictionary may be used to simulate user input.
    Objective: call other functions to populate a database from a .xls or .xlsx file.
    Output: .sqlite database.
    """
    output_string, output_filename = "", dbfilename[:-7] + "_history.txt"
    results = dict()
    string = ""

    # Convert lists into a nested dictionary
    results = build_tables(folder, extensions, print_intermediate)

    # Prepare the output file
    timestamp = filegenerator.generate_timestamp()

    fieldvalues, fieldnames = list(), list()
    for table in results:
        string1 = dbhandler.create_table(results[table], dbfilename, table, print_intermediate)
        string += string1
        string2 = dbhandler.add_dbrows(results[table], dbfilename, table, "id", print_intermediate)
        string += string2

        # Generate report
        output_string += (filegenerator.generate_timestamp() + "\n"*2 + string)

    filegenerator.string_to_txt(output_filename, output_string)

    return results

####################################################################################################

def main(print_intermediate=True):
    """
    Objective: call other functions to populate a database from .csv files.
    Output: a .sqlite database.
    """

    data = build_tables(folder="data", extensions=[".csv"], print_intermediate=True)
    populate_db(data, dbfilename="database.sqlite", folder="data", extensions=[".csv"], print_intermediate=True)

    return None


if __name__ == '__main__':
    main()
