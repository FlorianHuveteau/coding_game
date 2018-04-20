import numpy as np
from time import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from training.mars_lander.ship_physics import ShipPhysics

target_power = 0
target_rotation = 0
time_elapsed = 0


def update_power(val):
    global target_power
    target_power = val


def update_rotation(val):
    global target_rotation
    target_rotation = val


def animate(i):
    global time_elapsed, prev
    now = time()
    dt = now - prev
    prev = now
    time_elapsed += dt
    ship.update(target_power=target_power, target_rotation=target_rotation, delta_time=dt)
    # ship_position.set_xdata(np.append(ship_position.get_xdata(), i))
    ship_position.set_xdata(ship.x)
    ship_position.set_ydata(ship.y)
    set_ui()
    # print(dt, ship, ship.power, dt)
    return ship_position,


def set_ui():
    time_text.set_text("time: {:.2f} s".format(time_elapsed))
    hs_lbl.set_text("hs: {:.2f}".format(ship.h_speed))
    vs_lbl.set_text("vs: {:.2f}".format(ship.v_speed))
    power_text.set_text("power: {}".format(ship.power))
    rotation_text.set_text("rotation: {}".format(ship.rotation))

# Init only required for blitting to give a clean slate.
def init():
    ship_position.set_data([2500], [2500])
    time_text.set_text('')
    power_text.set_text('')
    # line.set_ydata(np.ma.array(ship.y, mask=True))
    return ship_position,


# ship instance
ship = ShipPhysics(x=2500, y=2500, h_speed=0, v_speed=0, fuel=500, rotation=0, power=0)
dt = 1. / 40

fig, ax = plt.subplots()
ax.set_position([0.1,0.2,0.8,0.7])
ship_position, = ax.plot(ship.x, ship.y, 'bo', ms=6)

# SLIDERS
ax_power = plt.axes([0.2, 0.02, 0.5, 0.02])
ax_rotation = plt.axes([0.2,0.08,0.5,0.02])
slider_power = plt.Slider(ax_power, 'Power', valmin=0, valmax=4, valinit=0, valstep=1)
slider_rotation = plt.Slider(ax_rotation, 'Rotation', valmin=-90, valmax=90, valinit=0, valstep=1)
slider_power.on_changed(update_power)
slider_rotation.on_changed(update_rotation)


#  TEXTS
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
power_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
rotation_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)
hs_lbl = ax.text(0.02, 0.80, '', transform=ax.transAxes)
vs_lbl = ax.text(0.02, 0.75, '', transform=ax.transAxes)

ax.set_xlim(0, 7000)  # time
ax.set_ylim(0, 3000)

prev = time()
# interval = 1000 * dt - (t1 - t0)

ani = animation.FuncAnimation(fig, animate, interval=50, init_func=init)
plt.show()