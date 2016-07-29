class MyExceptions(Exception):
    def __init__(self):
        pass
    def __repr__(self):
        return __repr__(self)


def delen(a,b):
    raise MyExceptions
