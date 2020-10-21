register_center_schema = {
    "type": "object",
    "properties": {
        "login": {"type": "string"},
        "password": {"type": "string"},
        "address": {"type": "string"}
    },
    "required": ["login", "password", "address"]
}

login_center_schema = {
    "type": "object",
    "properties": {
        "login": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": ["login", "password"]
}

register_update_animal_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "center": {"type": "string"},
        "species": {"type": "string"},
        "age": {"type": "integer"},
        "price": {"type": "integer"},
        "description": {"type": "string"}
    },
    "required": ["name", "center", "species", "age"]
}

register_species_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "price": {"type": "integer"}
    },
    "required": ["name", "description", "price"]
}
