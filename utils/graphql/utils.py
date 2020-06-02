from graphql_relay import from_global_id


def from_globad_bulk(items, data):
    for item in items:
        if item in data:
            data[item] = from_global_id(data[item])[1]
    return data

