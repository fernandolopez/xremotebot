import json

# Esto tiene que correr desde la parte de tornado para validar
# si el usuario tiene asignado el recurso y para ver el key

def load_commands(string):
    try:
        commands = json.load(string)
    except ValueError:
        commands []



