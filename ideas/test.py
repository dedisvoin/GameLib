from functools import singledispatch


@singledispatch
def sum(a, b):
    ...


@sum.register((int, int))
def _(a, b):
    print("int")
    return a + b

@sum.register(str)
def _(a, b):
    print("str")
    return a + b

print(sum(1, "1"))