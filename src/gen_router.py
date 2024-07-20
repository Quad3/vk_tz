import os
import sys
from jinja2 import Environment, FileSystemLoader


def create_router(kind: str):

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('router_template.py')
    output_from_parsed_template = template.render(kind=kind)

    try:
        os.makedirs(f"rest/routes/{kind}", exist_ok=True)
    except OSError as error:
        print(error)

    with open(f"rest/routes/{kind}/router.py", "w") as f:
        f.write(output_from_parsed_template)


if __name__ == "__main__":
    create_router(sys.argv[1])
