import gpxpy
import matplotlib.pyplot as plt

gpx_file = open('Morning_Run.gpx', 'r')
gpx = gpxpy.parse(gpx_file)

lat = []
lon = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            lat.append(point.latitude)
            lon.append(point.longitude)

fig = plt.figure(facecolor = '0.05')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)
plt.plot(lon, lat, color = 'deepskyblue', lw = 0.2, alpha = 0.8)

plt.show()
