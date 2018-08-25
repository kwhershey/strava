from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import gpxpy

data_path = 'activities'
data = [f for f in listdir(data_path) if isfile(join(data_path,f))]

lat = []
lon = []

fig = plt.figure(facecolor = '0.05')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)

for activity in data:
    gpx_filename = join(data_path,activity)
    gpx_file = open(gpx_filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat.append(point.latitude)
                lon.append(point.longitude)
    plt.plot(lon, lat, color = 'deepskyblue', lw = 0.8, alpha = 0.4)
    lat = []
    lon = []

plt.scatter(-93.1954600,44.9665240,color = 'deepskyblue',alpha=1)

filename = data_path + '.png'
plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=0, dpi=300)

plt.show()

