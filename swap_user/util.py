import simplejson


def printJson(parsed):
    print(simplejson.dumps(parsed, indent=2))
