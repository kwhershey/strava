from os import listdir
from os.path import isfile, join
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import gpxpy
import time
import datetime
from matplotlib import colors, cm
from palettable.cartocolors.sequential import OrYel_2
from palettable.cartocolors.diverging import TealRose_3
import time


tic=time.clock()

home_lat=47.612 #55
home_long=-122.314 #27

data_path = 'activities'
data = [f for f in listdir(data_path) if isfile(join(data_path,f))]


minel=5000
maxel=-5000

# find max
for activity in data:
    if activity[-1] == 'x':
        gpx_filename = join(data_path,activity)
        gpx_file = open(gpx_filename, 'r')
        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            p=track.segments[0].points[0]
            if abs(p.latitude-home_lat)<.3 and abs(p.longitude-home_long)<.3: 
                for segment in track.segments:
                    for point in segment.points:
                        if point.elevation<minel:
                            minel=point.elevation
                        elif point.elevation>maxel:
                            maxel=point.elevation
print('Minimum Elevation: ' + str(minel))
print('Maximum Elevation: ' + str(maxel))

cnorm  = colors.Normalize(vmin=minel, vmax=maxel)
#scalar_map = cm.ScalarMappable(norm=cnorm, cmap=OrYel_2.mpl_colormap)
scalar_map = cm.ScalarMappable(norm=cnorm, cmap=TealRose_3.mpl_colormap)


# plot

lat = []
lon = []
col = []

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
                    ele=point.elevation
                    cvalue = scalar_map.to_rgba(ele)
                    col.append(cvalue)
                    date=point.time
        if abs(lat[0]-home_lat)<.3 and abs(lon[0]-home_long)<.3:  
           
            #plt.scatter(lon, lat, color = 'deepskyblue', s=.2,lw = 0.2, alpha = 0.4)
            plt.scatter(lon, lat, color = col, s=.05,lw = 0.2, alpha = 0.7)


        lat = []
        lon = []
        col = []

cmin= scalar_map.to_rgba(minel)
plt.text(.93,.965,str(int(minel*3.28084))+ ' ft',color=cmin,fontsize=4,alpha=.8,transform=plt.gca().transAxes)
cmax= scalar_map.to_rgba(maxel)
plt.text(.93,.98,str(int(maxel*3.28084))+' ft',color=cmax,fontsize=4,alpha=.8,transform=plt.gca().transAxes)

plt.plot([-122.25144,-122.2369472],[47.527,47.527],color='deepskyblue',alpha=.8)
plt.text(-122.25,47.53,'1 mi',fontsize=5,color='deepskyblue',alpha=.8)


filename = data_path + 'basic.png'
plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=0, dpi=500)
#filename = data_path + 'basic.eps'
#plt.savefig(filename, facecolor='black', bbox_inches='tight', pad_inches=0)#, dpi=300)


toc=time.clock()
print(toc-tic)