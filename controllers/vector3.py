from __future__ import annotations
from math import sin, cos
import numpy as np

class Vector3:
    x: float
    y: float
    z: float

    def __init__(self: Vector3, x: float = None, y: float = None, z: float = None) -> None:
        if x != None and y != None and z != None:
            self.x = x
            self.y = y
            self.z = z
        else:
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
    
    def length(self: Vector3) -> float:
        return (self.x**2 + self.y**2 + self.z**2)**(1.0/2.0)
    
    def normalized(self: Vector3) -> Vector3:
        length = self.length()
        return Vector3() if length == 0 else \
            Vector3(self.x / length, self.y / length, self.z / length)
    
    def rotated(self: Vector3, angle: float, axis: str) -> Vector3:
        if not axis in ["x", "y", "z"]:
            raise ValueError(f"Invalid axis given, expected x, y or z, got \"{axis}\".")
        
        newVector: Vector3 = Vector3(self.x, self.y, self.z)
        if axis == "x":
            newVector.y = cos(angle)*self.y - sin(angle)*self.z
            newVector.z = sin(angle)*self.y + cos(angle)*self.z
        elif axis == "y":
            newVector.x = cos(angle)*self.x - sin(angle)*self.z
            newVector.z = sin(angle)*self.x + cos(angle)*self.z
        else:
            newVector.x = cos(angle)*self.x - sin(angle)*self.y
            newVector.y = sin(angle)*self.x + cos(angle)*self.y
        
        return newVector



    def __add__(self: Vector3, other: Vector3) -> Vector3:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self: Vector3, other: Vector3) -> Vector3:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self: Vector3, mul: float) -> Vector3:
        return Vector3(self.x * mul, self.y * mul, self.z * mul)
    
    def __str__(self: Vector3):
        return f"[{self.x}, {self.y}, {self.z}]"
    

    def toNpArray(self: Vector3) -> np.ndarray:
        return np.array([self.x, self.y, self.z], np.float64)

    @staticmethod
    def fromNpArray(array: np.ndarray) -> Vector3:
        if array.size != 3:
            raise ValueError(f"Expected array size 3, got {array.size}.")
        
        return Vector3(*array)
    