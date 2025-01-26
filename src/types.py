class PirateType:
    def __init__(self, value: any, type_name: str = None):
        self.value = value
        if isinstance(value, dict):
            self.type_name = 'dict'
        else:
            self.type_name = type_name or type(value).__name__
            
    def __getitem__(self, key):
        if isinstance(self.value, (list, dict)):
            return self.value[key]
        raise PirateException(f"{self.type_name} doesn't support indexing")

    def __setitem__(self, key, value):
        if isinstance(self.value, dict):
            self.value[key] = value
        elif isinstance(self.value, list):
            self.value[key] = value
        else:
            raise PirateException(f"{self.type_name} doesn't support item assignment")

    def __repr__(self):
        return f"{self.value}"

    def __eq__(self, other):
        if isinstance(other, PirateType):
            return self.value == other.value
        return self.value == other

    def perform_op(self, other, op):
        if isinstance(other, PirateType):
            other = other.value
        return PirateType(op(self.value, other))

    def __add__(self, other): return self.perform_op(other, lambda x, y: x + y)
    def __sub__(self, other): return self.perform_op(other, lambda x, y: x - y)
    def __mul__(self, other): return self.perform_op(other, lambda x, y: x * y)
    def __truediv__(self, other): return self.perform_op(other, lambda x, y: x / y)
    def __mod__(self, other): return self.perform_op(other, lambda x, y: x % y)
    def __pow__(self, other): return self.perform_op(other, lambda x, y: x ** y)

    def __gt__(self, other): return self.perform_op(other, lambda x, y: x > y)
    def __lt__(self, other): return self.perform_op(other, lambda x, y: x < y)
    def __ge__(self, other): return self.perform_op(other, lambda x, y: x >= y)
    def __le__(self, other): return self.perform_op(other, lambda x, y: x <= y)