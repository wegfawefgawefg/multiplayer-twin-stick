def dict_diff(a, b):
    return {key: value for key, value in b if a[key] != value}
