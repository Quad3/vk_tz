import os
import sys
import json
from jinja2 import Environment, FileSystemLoader


dir_path = os.path.dirname(os.path.realpath(__file__))


def create_router(filename: str) -> None:
    with open(filename) as f:
        data = json.load(f)
        kind = data["kind"]

    env = Environment(loader=FileSystemLoader(f"{dir_path}/templates"))
    template = env.get_template('router_template.py')
    output_from_parsed_template = template.render(kind=kind)

    try:
        os.makedirs(f"{dir_path}/rest/routes/{kind}", exist_ok=True)
    except OSError as error:
        print(error)

    with open(f"{dir_path}/rest/routes/{kind}/router.py", "w") as f:
        f.write(output_from_parsed_template)
        print(f"Created -> {dir_path}/rest/routes/{kind}/router.py")


if __name__ == "__main__":
    filename: str = sys.argv[1]
    create_router(filename)
