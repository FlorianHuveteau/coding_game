import math



def compute_speed(c_x, c_y, c_hspeed, c_vspeed, c_rotation, c_power, delta_rotation, delta_power, delta_time):
    power = c_power + delta_power
    fuel = power * delta_time
    rotation = c_rotation + delta_rotation

    v_acc = math.cos(math.radians(-rotation)) * power - 3.711
    h_acc = math.sin(math.radians(-rotation)) * power
    v_speed = c_vspeed + (v_acc * delta_time)
    h_speed = c_hspeed + (h_acc * delta_time)

    x = c_x + (delta_time * ((h_speed + c_hspeed) / 2))
    y = c_y + (delta_time * ((v_speed + c_vspeed) / 2))

    return x, y, h_speed, v_speed, power, rotation, fuel