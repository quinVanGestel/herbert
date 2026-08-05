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

class Car:
    def __init__(self, colour: str, horsepower: float, name:str, hornSound:str = "beep") -> None:
        self.colour = colour
        self.horsepower = horsepower
        hi = horsepower
        self.sound = hornSound
        self.name = name
        
    def honk_horn(self) -> None:
        print(self.sound)
        
    def __str__(self) -> str:
        return f"{self.name} {self.sound} {self.horsepower}hp"
        
volvo: Car = Car('purple', 0.5,"volvina")
greet(volvo.name)
volvo.honk_horn()
print(volvo)