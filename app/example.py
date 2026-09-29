def someExecution(func):
    def wrapper(*args, **kwargs):
        print("Starting execution")
        result = func(*args, **kwargs)
        print("Execution completed")
        return result
    return wrapper

@someExecution
def someFunction(name: str):
    print("Some function")

someFunction("John")  

class SomeClass:
    def __init__(self, name: str):
        self._name = name
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        del self._name

someInstance = SomeClass("John")
print(someInstance.name)
someInstance.name = "Jane"
print(someInstance.name)
del someInstance.name
print(someInstance.name)
