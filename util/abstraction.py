import inspect

# from https://stackoverflow.com/questions/13937500/inherit-a-parent-class-docstring-as-doc-attribute
def inheritdocstring(cls):
    for base in inspect.getmro(cls):
        if base.__doc__ is not None:
            cls.__doc__ = base.__doc__
            break
    return cls