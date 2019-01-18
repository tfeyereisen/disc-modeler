import numpy as np
from stl import mesh
import math
from mpl_toolkits import mplot3d
from matplotlib import pyplot

rad_int = 100
theta = 2 * math.pi / rad_int

#profile = [(0,0),(0.1,0),(0.2,0),(0.3,0),(0.4,0),(0.5,0),(0.6,0),(0.7,0),(0.8,0),(0.9,0),(1,0),(1.1,-0.05),
#    (1,-0.1),(0.9,-0.1),(0.8,-0.1),(0.7,-0.1),(0.6,-0.1),(0.5,-0.1),(0.4,-0.1),(0.3,-0.1),(0.2,-0.1),(0.1,-0.1),(0,-0.1)]

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

#profile = [(0,0), (1, 0), (1.05, -0.05), (1, -0.1), (0,-0.1)]

num_interior_prof_points = len(profile) - 2

vertices = np.empty(((num_interior_prof_points * rad_int) + 2, 3), dtype=object)
faces = np.empty((2 * num_interior_prof_points * rad_int, 3), dtype=object)

end_vertex = 1 + (num_interior_prof_points * rad_int)
vertices[0] = (0, 0, 0)
vertices[end_vertex] = (0, 0, -0.1)
count = 0

for r in range(0, rad_int):
	angle = r * theta
	index = (num_interior_prof_points * r) + 1
	adj_index = 1 if r == rad_int - 1 else (num_interior_prof_points * (r + 1)) + 1
	faces[count] = (0, index, adj_index)
	count = count + 1
	index = (num_interior_prof_points * (r + 1))
	adj_index = end_vertex if r == rad_int - 1 else (num_interior_prof_points * (r + 1)) + num_interior_prof_points
	faces[count] = (index, end_vertex, adj_index)
	count = count + 1
	for p in range(1, num_interior_prof_points + 1):
		x = profile[p][0] * math.cos(angle)
		y = profile[p][0] * math.sin(angle)
		z = profile[p][1]
		index = (r * num_interior_prof_points) + p
		vertices[index] = (x, y, z)

		if p < num_interior_prof_points:   # don't do last
			next_index = index + 1
			adj_index = ((r + 1) * num_interior_prof_points) + p if r < rad_int - 1 else p
			adj_next_index = adj_index + 1

			faces[count] = (index, next_index, adj_index)
			count = count + 1
			faces[count] = (adj_index, next_index, adj_next_index)
			count = count + 1


# Create the mesh
disc = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
	for j in range(3):
		disc.vectors[i][j] = vertices[f[j], :]

# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Add the vectors to the plot

mesh = mplot3d.art3d.Poly3DCollection(disc.vectors, facecolor=(0,0,1,0.2), linewidth=0.2, edgecolor=(0,0,0))

#col = mplot3d.art3d.Poly3DCollection(disc.vectors).set_alpha(0.1)
axes.add_collection3d(mesh)
# Auto scale to the mesh size
scale = disc.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
pyplot.show()

# Write the mesh to file "cube.stl"
# cube.save('cube.stl')