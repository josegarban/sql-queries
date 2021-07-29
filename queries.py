import sqlite3, pprint, json
from pathlib import Path

TEST_QUERIES = [
    ("See all records in table Orders", "SELECT * FROM Orders"),
]

def get_queries(jsonfilename="queries.json", print_intermediate=False):
    """
    Make a list of tuples of the form (description, query) from an adjacent .json file
    """
    with open(Path(jsonfilename),'r') as json_file:
        queries = json.load(json_file)

    queries = [ queries[k] for k in list(queries.keys()) ]
    if print_intermediate: pprint.pprint("The following queries will be executed:\n{0}".format(queries))
    return queries

def perform_queries(queries=TEST_QUERIES, database="database.sqlite"):
    """
    Perform queries from a list of queries.
    Input: Each element in queries is a tuple of the form (description, query)
    """
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    for q in queries:
        print("\n")
        print("#"*50)
        print("Executing query:")
        print(q[0])
        print(q[1])
        print("")
        cursor.execute(q[1])
        pprint.pprint(cursor.fetchall())
        print("#"*50)

    connection.commit()
    connection.close()
    return None

def main():
    queries = get_queries()
    perform_queries(queries)

if __name__ == '__main__':
    main()
