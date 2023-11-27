# Function to convert dictionaries to frozensets (immutable sets)
def dict_to_frozenset(d):
  return frozenset(d.items())