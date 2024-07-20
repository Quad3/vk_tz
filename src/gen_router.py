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
        print(f"Created -> rest/routes/{kind}/router.py")


def create_main(kind: str):

    env = Environment(loader=FileSystemLoader('templates'))
    main_file_template = env.get_template('main_template.py')
    output_from_parsed_template_main = main_file_template.render(kind=kind)

    with open(f"main.py", "w") as f:
        f.write(output_from_parsed_template_main)
        print(f"Created -> main.py")


if __name__ == "__main__":
    kind_name: str = sys.argv[1]
    create_router(kind_name)
    create_main(kind_name)
