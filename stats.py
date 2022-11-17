import datetime
import json


def update_stats(num_of_strings: int) -> None:
    # Read current stats
    with open(file="stats.json", mode="r") as f:
        json_object = json.load(f)

    files_extracted = json_object["filesExtracted"]
    strings_extracted = json_object["stringsExtracted"]

    # Add 1 to the number of extracted files
    # and parameter num_of_strings to the number of extracted strings
    new_data = {
        "filesExtracted": files_extracted + 1,
        "stringsExtracted": strings_extracted + num_of_strings,
        "lastTimeUsed": datetime.datetime.now().strftime("%Y-%m-%d")
    }

    json_object = json.dumps(obj=new_data, indent=4)

    # Write stats back to JSON file
    with open(file="stats.json", mode="w") as f:
        f.write(json_object)


def read_stats() -> dict:
    with open(file="stats.json", mode="r") as f:
        return json.load(f)
