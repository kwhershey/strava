from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import gpxpy
import glob

data_path = 'activities'
data = [f for f in listdir(data_path) if isfile(join(data_path,f))]

#data=glob.glob('activities/*.gpx')


lat = []
lon = []

fig = plt.figure(facecolor = 'black')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
#ax.set_facecolor('black')
fig.add_axes(ax)

for activity in data:
    if activity[-1] == 'x':
        gpx_filename = join(data_path,activity)
        gpx_file = open(gpx_filename, 'r')
        gpx = gpxpy.parse(gpx_file)
        #gpx = gpxpy.parse(activity)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat.append(point.latitude)
                    lon.append(point.longitude)
        if abs(lat[0]-44.9)<1 and abs(lon[0]+93.2)<1: # MSP
        #if abs(lat[0]-41.5)<1 and abs(lon[0]+81.7)<1: # CLE 
            plt.plot(lon, lat, color = 'deepskyblue', lw = 0.4, alpha = 0.2)
        lat = []
        lon = []

#plt.scatter(-93.1954600,44.9665240,color = 'deepskyblue',alpha=1)

filename = data_path + '.eps'
plt.savefig(filename, facecolor='black', bbox_inches='tight', pad_inches=0)#, dpi=300)

plt.show()

