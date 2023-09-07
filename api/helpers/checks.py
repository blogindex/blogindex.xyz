def schema_check(schema):
    try:
        print(schema)
        check = True
    except ValidationError:
        check = False
    return check