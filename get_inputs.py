import pprint, os
import pandas as pd

####################################################################################################
# FILESYSTEM
####################################################################################################

def files_in_folder_byext (folder="", extensions=[".csv"], mode="with folders", print_intermediate=True):
    """
    Input: folder path (optional), list of valid extensions (optional).
        Mode: 'with folders' 'without folders'.
    Objective: find files of certain extensions in the same folder.
    Output: list with filenames.
    """
    # if mode == "with folders":
    # elif mode == "without folders":

    if folder == "":
        # Find file(s) in same folder
        files = os.listdir()
    else:
        # Find file(s) in other folder
        files = os.listdir(folder)

    filepaths = [ folder+"\\"+f for f in files ]
    for e in extensions:
        # Remove extension and change spaces into underscores
        table_names = [ f.replace(e, "") for f in files ]
    if print_intermediate:
        print("Files in folder:", folder)
        print("\nFiles:\n", filepaths)

    # Get a list with just file names
    file_names = []

    if extensions != "":
        for extension in extensions:
            for file in filepaths:
                if file.endswith(extension):
                    file_names.append(file)
        if len (file_names) == 0:
            if print_intermediate:
                print("No file with the searched extensions were found.")
                print("")
        else:
            if print_intermediate:
                print("The following files with the searched extensions were found:")
                pprint.pprint(file_names)
                print("")
    else:
        for file in files:
            file_names.append(file)
        if print_intermediate:
            if len (file_names) == 0:
                print("No files were found.")
                print("")
            else:
                print("The following files were found:")
                pprint.pprint(file_names)
                print("")


    return file_names, table_names

####################################################################################################
# READ FILES
####################################################################################################

def csv_to_dataframe(filename, delimiter=",", print_intermediate=True):
    """
    Input: csv file.
    Output: dataframe.
    """
    # Get dataframe and headers from csv
    df = pd.read_csv(filename, delimiter,header=0)
    header_list = list(df.columns)
    # Remove trailing or initial blanks in column names
    for h in header_list:
        if h[0] == " ":
            h_ = h.replace(" ", "", 1)
            df = df.rename(columns={h:h_})
        if h[-1] == " ":
            h_ = h[:-1]
            df = df.rename(columns={h:h_})
        if " " in h:
            header_list[header_list.index(h)] = "\'"+h+"\'"
            # Deal with columns with spaces in their names

    header_list = list(df.columns)

    # Remove trailing blanks in values, catch commas in numbers
    for h in header_list:
        for i in list(range(len(df.index))):
            value = str(df.iloc[i][h])
            if value[-1] == " ":
                df.iat[i, df.columns.get_loc(h)] = value[:-1]
            if "," in value:
                df.iat[i, df.columns.get_loc(h)] = float(value.replace(",", "."))

    if print_intermediate:
        # Print what we got
        print("\n\n"+filename)
        print("Obtained a dataframe with the following fields:\n")
        print(df.dtypes, "\n")
        print("\nDataframe:")
        print("#"*100+"\n", df, "\n"+"#"*100+"\n")
        print("\nHeaders:")
        print("#"*100,"\n", header_list, "\n"+"#"*100+"\n")

    return df

def dataframe_to_listdict(df, print_intermediate=True):
    """
    Returns a list of dictionaries where the keys are the column names.
    Each item in the list will be one row.
    """
    output = []
    header_list = list(df.columns)
    for i in list(range(len(df.index))):
        row = {h: df.iloc[i][h] for h in header_list}
        output.append(row)
    if print_intermediate:
        pprint.pprint(output)
    return output

####################################################################################################
# MAIN
####################################################################################################

def main(extensions=".csv", delimiter=",", print_intermediate=True):
    """
    Read several .csv files and display their values as lists of dictionaries
    """
    file_names = files_in_folder_byext(folder="data", extensions=extensions, print_intermediate=print_intermediate)
    for f in file_names:
        df = csv_to_dataframe(f, delimiter=delimiter, print_intermediate=print_intermediate)
        dataframe_to_listdict(df)

if __name__ == '__main__':
    main()
