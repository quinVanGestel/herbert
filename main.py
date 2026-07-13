from typing import Final
from datetime import datetime

print("Hello world")

NAME: Final[str] = "Herbert"
number: int = 10
names: list[str] = [NAME, "I'm not a name..."]

# NAME = "Roger"
print("Hi I'm "+names[0])

names[1] = "Charlene"
print("Hello I'm "+names[1])


def show_date() -> None:
    print ("the time rn is")
    print(datetime.now())
    
show_date()

def greet(name:str) -> None:
    print(f"Hiii I'm {name} :3")

greet(names[0])

