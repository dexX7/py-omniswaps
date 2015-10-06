import simplejson


def print_json(parsed):
    print(simplejson.dumps(parsed, indent=2))
