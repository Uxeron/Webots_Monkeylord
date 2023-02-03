from __future__ import annotations
from math import pi
from controller import Robot, Motor, PositionSensor
from vector3 import Vector3
import tinyik

# Leg servo naming diagram:
#  Naming imagines the leg fully extended downwards.
#       ____
#      /   /_ <- servoLower
#     / __/  \________
#    / /   \   \  |   | <- servoUpper
#   / /     \   \_|___|
#  / /       \___/
# /_/          ^ servoMiddle
#

class Leg():
    servoUpper: Motor = None
    servoMiddle: Motor = None
    servoLower: Motor = None

    sensorUpper: PositionSensor = None
    sensorMiddle: PositionSensor = None
    sensorLower: PositionSensor = None

    legName: str = None
    motorNames: list[str] = ["motor_1", "motor_2", "motor_3"]

    ik: tinyik.Actuator
    defaultEE: Vector3

    def __init__(self: Leg, robot: Robot, legName: str) -> None:
        self.legName = legName

        self.ik = tinyik.Actuator(['y', [-0.3706, 0.0, 0.0], 'z', [-0.511, 0.36, 0.0], 'z', [-0.3204, -1.05, 0.0]])
        self.defaultEE = Vector3.fromNpArray(self.ik.ee)

        self.servoUpper = robot.getDevice(f"{legName}_{self.motorNames[0]}")
        self.servoMiddle = robot.getDevice(f"{legName}_{self.motorNames[1]}")
        self.servoLower = robot.getDevice(f"{legName}_{self.motorNames[2]}")

        self.sensorUpper = self.servoUpper.getPositionSensor()
        self.sensorMiddle = self.servoMiddle.getPositionSensor()
        self.sensorLower = self.servoLower.getPositionSensor()

        self.sensorUpper.enable(32)
        self.sensorMiddle.enable(32)
        self.sensorLower.enable(32)
    

    def setServoPositions(self: Leg, positions: Vector3) -> None:
        self.servoUpper.setPosition(positions.x)
        self.servoMiddle.setPosition(positions.y)
        self.servoLower.setPosition(positions.z)
    
    def getServoPositions(self: Leg) -> Vector3:
        return Vector3(self.sensorUpper.getValue(), self.sensorMiddle.getValue(), self.sensorLower.getValue())


    def setPosition(self: Leg, position: Vector3) -> None:
        self.ik.ee = position.toNpArray()
        self.setServoPositions(Vector3.fromNpArray(self.ik.angles))
    
    def getPosition(self: Leg) -> Vector3:
        return Vector3.fromNpArray(self.ik.ee)
    

    def setRelativePosition(self: Leg, position: Vector3) -> None:
        self.setPosition(self.defaultEE + position)
    
    def getRelativePosition(self: Leg) -> Vector3:
        return self.defaultEE - self.getPosition() 




class Hexapod(Robot):
    legNames = \
        ["leg_fl", "leg_fr", \
         "leg_ml", "leg_mr", \
         "leg_bl", "leg_br"]

    legAngles = \
        [-pi / 4.0, -pi / 4.0 * 3.0, \
         0.0, pi, \
         pi / 4.0, pi / 4.0 * 3.0]

    position: Vector3 = None
    direction: Vector3 = None

    legs: list[Leg] = None

    def __init__(self):
        super(Hexapod, self).__init__()
        self.timeStep = 32

        self.position = Vector3(0.0, 0.0, 0.0)
        self.offset = Vector3(0.1, 0.0, 0.0)
        self.direction = Vector3(0.0, 0.0, -0.15)
        self.legs = [Leg(self, legName) for legName in self.legNames]

    def run(self):
        # TODO: Precompute the motor positions for basic walking instead of using IK
        while self.step(self.timeStep) != -1:
            if abs(self.position.z) >= 0.4:
                self.direction *= -1.0
            
            self.position += self.direction

            for i in range(6):
                leg: Leg = self.legs[i]
                height: Vector3 = Vector3(0.0, (0.5 - abs(self.position.z)) / 2.5, 0.0)
                if self.direction.z < 0.0:
                    if i in [0, 3, 4]:
                        leg.setRelativePosition(self.position.rotated(self.legAngles[self.legs.index(leg)], "y") + height + self.offset)
                    else:
                        leg.setRelativePosition((self.position * -1.0).rotated(self.legAngles[self.legs.index(leg)], "y") + self.offset)
                else:
                    if i in [0, 3, 4]:
                        leg.setRelativePosition(self.position.rotated(self.legAngles[self.legs.index(leg)], "y") + self.offset)
                    else:
                        leg.setRelativePosition((self.position * -1.0).rotated(self.legAngles[self.legs.index(leg)], "y") + height + self.offset)

