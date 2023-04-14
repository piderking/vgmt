import os
import json


class ConfigClass:
    def __init__(self, filePath:str) -> None:
        """_summary_

        Args:
            file (str): Path to file, absoulute path
        """
        with open(filePath, "r") as f:
            data = json.load(f)
            # print(data)
            self.version: str = data["version"]
            self.title: str = data["title"]
            self.prod: str = data["prod"]
            self.debug: str = data["debug"]
            self.doc_url: str = data["doc_url"]
            self.csv_local_path: str = os.path.abspath(data["csv_local_path"])
            # Fill this out for all options in the config path

    