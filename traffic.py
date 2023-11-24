"""Traffic sample description.

This module allows to load a traffic file
and to access all its flights information.
"""

import enum
import circuit

STEP = 5  # Time step (seconds)
DAY = 24 * 3600 // STEP  # Day duration in time steps
SEP = 70  # Minimal separation (meters)
RWY_SEP = 90  # Runway area width
DT = 120 // STEP  # Conflict anticipation time


# Movement type: departure or arrival
class Movement(enum.Enum):
    DEP = 1
    ARR = 2


def movement_from_string(s):
    if s == 'DEP':
        return Movement.DEP
    elif s == 'ARR':
        return Movement.ARR


class Flight:
    """ Flight data, with the following attributes:
    - call_sign: str
    - type: Movement.DEP | Movement.ARR
    - cat: airport.LIGHT | MEDIUM | HEAVY
    - stand: airport.Point
    - runway: airport.Runway
    - qfu: 0|1 (index of the QFU in the runway)
    - start_t: int (beginning time step)
    - end_t: int (ending time step)
    - rwy_t: int (time step in runway for DEP - or out runway for ARR)
    - slot: None | int (time step of the take-of slot if some)
    - route: airport.XY tuple (assigned route)"""

    def __init__(self, call_sign, flight_type, cat):
        self.call_sign = call_sign
        self.type = flight_type
        self.cat = cat
        self.stand = None
        self.runway = None
        self.qfu = 0
        self.start_t = None
        self.end_t = None
        self.rwy_t = None
        self.slot = None
        self.route = None

    def __repr__(self):
        return "<traffic.Flight {0}>".format(self.call_sign)

    def get_position(self, t):
        return self.route[t - self.start_t]

    def distance(self, other, t):
        return self.get_position(t).distance(other.get_position(t))

    def use_runway(self, t):
        return t <= self.rwy_t if self.type == Movement.ARR else self.rwy_t <= t

    def in_runway(self, runway, t):
        (a, b) = runway.coords
        return self.get_position(t).seg_dist(a, b) <= RWY_SEP

    def conflicts(self, other, t):
        return (self.distance(other, t) < SEP or
                self.use_runway(t) and other.in_runway(self.runway, t) or
                other.use_runway(t) and self.in_runway(other.runway, t))


# Time string conversions

def hms(t):
    """hms(int) return str
    return a formatted string HH:MM:SS for the given time step"""
    s = t * STEP
    return "{:02d}:{:02d}:{:02d}".format(s // 3600, s // 60 % 60, s % 60)


def time_step(str_hms):
    """time_step(str) return int
    return the time step corresponding to a formatted string HH:MM:SS"""
    l = str_hms.replace(':', ' ').split() + [0, 0, 0]
    return (int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])) // STEP
