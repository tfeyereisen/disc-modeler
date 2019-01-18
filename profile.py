import numpy as np
from stl import mesh
import math
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

# Outer Diameter = 0.105 to 0.15
outer_radius = 0.15

# Uniform flight plate area 0.025 to 0.05
uniform_flight_plate_radius = 0.04

# Uniform flight plate thickness < 0.005
uniform_flight_plate_thickness = 0.005

# Inner Rim Depth = 5-12% of Outer Diameter
inner_rim_depth_pct = 0.1
inner_rim_depth = inner_rim_depth_pct * (2 * outer_radius)

# Inner Rim Expansion Factor = 0-1
inner_rim_expansion_factor = 0

# Leading Edge Radius >= 0.0016
leading_edge_radius = 0.0016

# Flight Plate Height - Ambiguous (says <= 0.5 cm)
flight_plate_height = 0.05 * outer_radius

# Flight Plate Dome = 0-1
dome_power = 1000
x_flight_plate_dome_max = 0.5
x_dome_width = outer_radius - uniform_flight_plate_radius
y_max_dome_max = math.log(1 - math.pow(x_flight_plate_dome_max, dome_power))


# Leading Edge Point
x_leading_edge_point = outer_radius - leading_edge_radius
y_leading_edge_point = (-1 * flight_plate_height) - leading_edge_radius

# Rim width <= 0.026
rim_width = 0.026


#region Uniform Flight Plate
upper_plate_length = 100
x_uniform_flight_plate_top = np.empty((upper_plate_length, 1))
x_uniform_flight_plate_bottom = np.empty((upper_plate_length, 1))
y_uniform_flight_plate_top = np.empty((upper_plate_length, 1))
y_uniform_flight_plate_bottom = np.empty((upper_plate_length, 1))

for i in range(0, upper_plate_length):
	x_i = uniform_flight_plate_radius * (i / len(x_uniform_flight_plate_top))
	x_uniform_flight_plate_top[i] = x_i
	x_uniform_flight_plate_bottom[i] = x_i
	y_uniform_flight_plate_top[i] = 0
	y_uniform_flight_plate_bottom[i] = -1 * uniform_flight_plate_thickness
#endregion

#region Leading Edge
leading_edge_length = 20
x_leading_edge_top = np.empty((leading_edge_length, 1))
x_leading_edge_bottom = np.empty((leading_edge_length, 1))
y_leading_edge_top = np.empty((leading_edge_length, 1))
y_leading_edge_bottom = np.empty((leading_edge_length, 1))

for i in range(0, leading_edge_length):
	x_i = x_leading_edge_point + leading_edge_radius * (i / leading_edge_length)
	x_leading_edge_top[i] = x_i
	x_leading_edge_bottom[i] = x_i
	y_leading_edge_top[i] = y_leading_edge_point + math.sqrt(math.pow(leading_edge_radius, 2) - math.pow(x_i - x_leading_edge_point, 2))
	y_leading_edge_bottom[i] = y_leading_edge_point - math.sqrt(math.pow(leading_edge_radius, 2) - math.pow(x_i - x_leading_edge_point, 2))
#endregion

#region Flight Plate Dome
flight_plate_dome_length = 100
x_flight_plate_dome = np.empty((flight_plate_dome_length, 1))
y_flight_plate_dome = np.empty((flight_plate_dome_length, 1))

for i in range(0, flight_plate_dome_length):
	x_i = x_flight_plate_dome_max * math.pow((i / flight_plate_dome_length), 2)
	x_flight_plate_dome[i] = float(uniform_flight_plate_radius + x_i)
	y_flight_plate_dome[i] = float((y_leading_edge_point) * math.log(1 - math.pow(x_i, dome_power)) / y_max_dome_max)

#endregion


plt.plot(x_leading_edge_top, y_leading_edge_top, 'b-', x_leading_edge_bottom, y_leading_edge_bottom, 'b-',
		 x_uniform_flight_plate_top, y_uniform_flight_plate_top, 'b-',
		 x_uniform_flight_plate_bottom, y_uniform_flight_plate_bottom, 'b-',
		 x_flight_plate_dome, y_flight_plate_dome, 'b-')
axes = plt.gca()
axes.set_xlim([0, outer_radius])
axes.set_ylim([-1 * outer_radius, 0])
plt.axis([0, outer_radius, -1 * outer_radius, 0])
plt.show()

exit()

dome = 0.9
plate_thickness = 0.01
inner_rim = 0.8
ridge_point = 1
lower_ridge_flex = 0

rim_wall_height = 0.1
dome_max = 0.1
dome_min = 0.001
dome_multiplier = -1 * dome * (((dome_max - dome_min) * dome) + dome_min)

#region Upper and lower plate
upper_plate_length = 100
x_up = np.empty((upper_plate_length, 1))
y_up = np.empty((upper_plate_length, 1))

lower_plate_length = math.floor(upper_plate_length * inner_rim)
x_lp = np.empty((lower_plate_length, 1))
y_lp = np.empty((lower_plate_length, 1))

for i in range(0, upper_plate_length):
	x_i = i / len(x_up)
	x_up[i] = x_i
	y_up[i] = dome_multiplier * math.pow(x_i, 2)
	if i < lower_plate_length:
		x_lp[i] = x_i
		y_lp[i] = y_up[i] - plate_thickness
#endregion

#region Rim wall
rim_wall_length = 25
x_rw = np.empty((rim_wall_length, 1))
y_rw = np.empty((rim_wall_length, 1))
rim_wall_x = x_lp[lower_plate_length - 1]
rim_wall_y_start = y_lp[lower_plate_length - 1]

for i in range(0, rim_wall_length):
	x_rw[i] = rim_wall_x
	y_rw[i] = rim_wall_y_start - (i + 1) * (rim_wall_height / rim_wall_length)
#endregion

#region Ridge point

end_up_x = x_up[-1]
end_up_y = y_up[-1]
end_rw_x = x_rw[-1]
end_rw_y = y_rw[-1]

x_rp = [(end_up_x - end_rw_x) * ridge_point + end_rw_x]
y_rp = [(end_up_y - end_rw_y) * ridge_point + end_rw_y]

#endregion

#Lower ridge

#endregion

profile = []
for i in range(0, len(x_up)):
	profile.append((x_up[i], y_up[i]))
for i in range(len(x_up), 0):
	profile.append((x_rw[i], y_rw[i]))
for i in range(len(x_lp), 0):
	profile.append((x_lp[i], y_lp[i]))

plt.plot(x_up, y_up, 'b-', x_lp, y_lp, 'b-', x_rw, y_rw, 'b-', x_rp, y_rp, 'ro')
axes = plt.gca()
axes.set_xlim([0, 1.1])
axes.set_ylim([-1, 0.1])
#plt.axis([0, 1, -1, 0])
plt.show()