#!/bin/bash
for i in $( ls *.fit.gz ); do
    gpsbabel -i garmin_fit -f $i -o gpx -F $i.gpx
    rm $i
done
