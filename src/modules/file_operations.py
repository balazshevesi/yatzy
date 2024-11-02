# file for functions that handle files
from datetime import datetime
import json


def sort_high_scores():
    file_name = "high_scores.json"
    try:
        with open(file_name, "r+") as file:
            json_data = json.load(file)
            json_data["high_scores"].sort(key=lambda x: x[1], reverse=True)
            file.seek(0)
            json.dump(json_data, file, indent=4)
            file.truncate()
    except:
        print(f"something went wrong when reading {file_name}")


def get_high_score():
    file_name = "high_scores.json"
    try:
        with open("high_scores.json", "r") as file:
            data = json.load(file)
        return data
    except:
        print(f"something went wrong when reading {file_name}")


def add_score_to_file(name: str, score: int):
    file_name = "high_scores.json"
    now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    try:
        with open("high_scores.json", "r+") as file:
            json_data = json.load(file)
            json_data["high_scores"].append([name, score, now])
            json_data["high_scores"].sort(key=lambda x: x[1], reverse=True)  # sort
            file.seek(0)
            json.dump(json_data, file, indent=4)
            file.truncate()
    except:
        print(f"something went wrong when reading {file_name}")
