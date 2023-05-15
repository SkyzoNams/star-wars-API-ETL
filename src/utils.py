import json

def write_file(file_path: str, data: str) -> None:
    # Open the file in write mode and write the data
    with open(file_path, "w") as json_file:
        json.dump(data, json_file)
        
        
def read_from_file(file_path: str) -> str:
    # Open the file in read mode and load the data
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data