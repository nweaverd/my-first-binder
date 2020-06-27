#!/usr/bin/env python
## object orbiting the Earth
from visual import *
 
M   = 6.0e24   # mass of Earth in kg
R   = 6.378e6  # Radius of Earth, in meters
G   = 6.67e-11 # Newton's constant of gravity in SI units; Nm^2/kg^2

m   = 1.0    # mass of object; IRRELEVANT and cancels out
h   = 3.6e7  # initial height above Earth's surface

# at first, make it so that motion is circular
v0 = sqrt(G*M/(R+h))

# later, try to launch
#v0 = 1.38*sqrt(G*M/(R+h))

# position is fixed and unchanging
Earth  = sphere(pos=vector(0, 0, 0), radius=R, color=color.red)

# object initially in (x, 0, 0); position will be changing later
object_pos_init = vector(R+h,0,0) # initial distance = 36000 km = 3.6e6 m
object          = sphere(pos=object_pos_init, radius=R/5, color=color.green,
                             make_trail=True, trail_type="points",interval=10)

F     = vector(0,   0, 0)     # gets defined  in loop
v     = vector(0, v0, 0)      # gets defined  in loop
p     = m*v                   # initial momentum
r     = object.pos-Earth.pos  # gets redefined in loop

t=0

# max time = 1 (or a few) circular periods
T_circ = 2*pi*(R+h)/v0

dt=0.001*T_circ


while t < 100*T_circ:
    rate(1000)

    # force on object
    F = -G*M*m/mag2(r)*norm(r)

    # momentum and velocity
    p = p + F*dt
    v = p/m

    # update object position
    object.pos = object.pos + v*dt

    # radius vector from Earth to object
    r = object.pos - Earth.pos 

    # update time  
    t = t + dt



