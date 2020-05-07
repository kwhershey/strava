from os import listdir
from os.path import isfile, join
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import colors, cm
import gpxpy
from palettable.cartocolors.sequential import OrYel_2
from palettable.cartocolors.diverging import TealRose_3
import time

tic=time.clock()

home_lat=47.5
home_long=-122

data_path = 'activities'
data = [f for f in listdir(data_path) if isfile(join(data_path,f))]

fig = plt.figure(facecolor = '0.0')
ax = plt.Axes(fig, [0., 0., 1., 1.], )
ax.set_aspect('equal')
ax.set_axis_off()
fig.add_axes(ax)

# find min and max elevation
minel=5000
maxel=-5000

for activity in data:
    if activity[-1] == 'x':
        gpx_filename = join(data_path,activity)
        gpx_file = open(gpx_filename, 'r')
        gpx = gpxpy.parse(gpx_file)

        for track in gpx.tracks:
            p=track.segments[0].points[0]
            if abs(p.latitude-home_lat)<10 and abs(p.longitude-home_long)<10: 
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

#plot the lines
for ix,activity in enumerate(data):
    print(str(ix) + '/' + str(len(data)))
    if activity[-1] == 'x':
        gpx_filename = join(data_path,activity)
        gpx_file = open(gpx_filename, 'r')
        gpx = gpxpy.parse(gpx_file)


        for track in gpx.tracks:
            p=track.segments[0].points[0]
            if abs(p.latitude-home_lat)<10 and abs(p.longitude-home_long)<10: # SEA 
                for segment in track.segments:
                    prev_lat=segment.points[0].latitude
                    prev_lon=segment.points[0].longitude
                    for point in segment.points:
                        lat=point.latitude
                        lon=point.longitude
                        ele=point.elevation
                        
                        cvalue = scalar_map.to_rgba(ele)
                        plt.plot([prev_lon,lon], [prev_lat,lat], color = cvalue, lw = .4, alpha = 0.7)

                        prev_lat=lat
                        prev_lon=lon

cmin= scalar_map.to_rgba(minel)
plt.text(.95,.965,str(minel)+ ' m',color=cmin,fontsize=4,alpha=.3,transform=plt.gca().transAxes)
cmax= scalar_map.to_rgba(maxel)
plt.text(.95,.98,str(maxel)+' m',color=cmax,fontsize=4,alpha=.3,transform=plt.gca().transAxes)



filename = data_path + '.png'
plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=0, dpi=600)
filename = data_path + '.eps'
plt.savefig(filename, facecolor = fig.get_facecolor(), bbox_inches='tight', pad_inches=0)

toc=time.clock()
print(toc-tic)
