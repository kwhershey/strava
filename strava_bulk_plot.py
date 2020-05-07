from os import listdir
from os.path import isfile, join
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import gpxpy
import time
import datetime

tic=time.clock()

home_lat=47.5
home_long=-122

data_path = 'activities'
data = [f for f in listdir(data_path) if isfile(join(data_path,f))]

lat = []
lon = []

fig = plt.figure(facecolor = 'black')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)

for ix,activity in enumerate(data):
    print(str(ix)+ '/' + str(len(data)))
    if activity[-1] == 'x':
        gpx_filename = join(data_path,activity)
        gpx_file = open(gpx_filename, 'r')
        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat.append(point.latitude)
                    lon.append(point.longitude)
                    date=point.time
        if abs(lat[0]-home_lat)<10 and abs(lon[0]-home_long)<10:  
            if date.year==2020:
                plt.plot(lon, lat, color = 'deepskyblue', lw = 0.8, alpha = 0.4)
            elif date.year==2019:
                plt.plot(lon, lat, color = 'fuchsia', lw = 0.4, alpha = 0.4)
            else: 
                plt.plot(lon, lat, color = 'lime', lw = 0.4, alpha = 0.4)

        lat = []
        lon = []

plt.text(.95,.985,'2020',color='deepskyblue',fontsize=4,alpha=.8,transform=plt.gca().transAxes)
plt.text(.95,.975,'2019',color='fuchsia',fontsize=4,alpha=.8,transform=plt.gca().transAxes)
plt.text(.95,.965,'2018',color='lime',fontsize=4,alpha=.8,transform=plt.gca().transAxes)

filename = data_path + 'basic.png'
plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=0, dpi=500)
filename = data_path + 'basic.eps'
plt.savefig(filename, facecolor='black', bbox_inches='tight', pad_inches=0)#, dpi=300)


toc=time.clock()
print(toc-tic)
