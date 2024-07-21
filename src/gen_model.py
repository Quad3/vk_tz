import os
import sys
import json


dir_path = os.path.dirname(os.path.realpath(__file__))
ROUTER_NAMES = f"{dir_path}/router_names.txt"


def gen_model(filename: str) -> None:
    with open(filename) as f:
        data = json.load(f)

        try:
            os.makedirs(f"{dir_path}/rest/models/{data['kind']}", exist_ok=True)
        except OSError as error:
            print(error)

        print(f"mkdir -> {dir_path}/rest/models/{data['kind']}")
        os.system(f"datamodel-codegen --input {filename} --output {dir_path}/rest/models/{data['kind']}/model.py")
        print(f"run -> datamodel-codegen --input {filename} --output model.py")

        with open(ROUTER_NAMES, "a") as rf:
            rf.write(f"{data['kind']}\n")


if __name__ == "__main__":
    gen_model(sys.argv[1])
