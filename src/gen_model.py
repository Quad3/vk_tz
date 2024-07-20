import os
import sys
import json


def gen_model(filename: str) -> None:
    with open(filename) as f:
        data = json.load(f)

        try:
            os.makedirs(f"rest/models/{data['kind']}", exist_ok=True)
        except OSError as error:
            print(error)

        print(f"mkdir -> rest/models/{data['kind']}")
        os.system(f"datamodel-codegen --input {filename} --output rest/models/{data['kind']}/model.py")
        print(f"run -> datamodel-codegen --input {filename} --output model.py")


if __name__ == "__main__":
    gen_model(sys.argv[1])
