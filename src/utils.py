def get_router_names() -> list[str]:
    filename = "router_names.txt"

    try:
        with open(filename, 'r') as f:
            router_names = f.read().splitlines()
    except FileNotFoundError:
        return []

    return router_names
