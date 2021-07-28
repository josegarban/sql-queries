import time, datetime

####################################################################################################
# FILESYSTEM
####################################################################################################

def generate_timestamp ():
    """
    Inputs: None
    Returns: String with a timestamp to be appended to a file name
    """
    now = datetime.datetime.now()
    timestamp = now.fromtimestamp(time.time()).strftime("%Y%m%d_%H%M%S")

    return timestamp

####################################################################################################
# OTHER FILETYPES MANIPULATION
####################################################################################################

def string_to_txt(filename, string):
    """
    Inputs: output filename, string.
    Objective: converts a string to a text file.
    Outputs: none.
    """

    text_file = open(filename, "a")
    text_file.write(string)
    text_file.write("\n"*2)
    text_file.close()

    return None
