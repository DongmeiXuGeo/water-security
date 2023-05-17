import arcpy
from arcpy import env
from arcpy.sa import *
env.workspace = "D:\Desktop\DEM200mm"
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("Spatial")
inBeforeRaster = "dem_sz.tif"
inputraster=Raster("dem_sz.tif")
highmax=100
highmin=1
hourmax=25
valuefill=[i for i in range(highmax)]
valuehigh=[i for i in range(hourmax)]
# set rain 200mm in 24 hour:(0.00833m/h)
speed=0.00833
# set rain 100mm in 24 hour:(0.00417m/h)
# speed=0.00417
area=2000180700

for hh in range(highmin,highmax,10):
     outCon=Con(inputraster<(hh/10.0),(hh/10.0),inputraster)
     inAfterRaster = outCon
     outRaster = "tryfill_"+str(hh)+".tif"
     arcpy.CutFill_3d(inBeforeRaster, inAfterRaster, outRaster, 1)
     intable = outRaster
     casefield = "#"
     stats = [["VOLUME", "Sum"]]
     outtable = "sumstats_"+str(hh)
     arcpy.Statistics_analysis(intable, outtable, stats, casefield)
     filltable=arcpy.SearchCursor(outtable)     
     for row in filltable:
         valuefill[hh]=row.getValue("sum_volume")
         # print hh
         # print valuefill[hh]
f=open("high.txt", "a")
count=0
for hour in range(12,hourmax,12):
    for hh in range(highmin+count,highmax):
        while (hour*speed*area+valuefill[hh])>0:
             hh=hh+1
        count=hh-highmin
        print "count="+str(count)
        if abs(hour*speed*area+valuefill[hh])<abs(hour*speed*area+valuefill[hh-1]):
           valuehigh[hour]=hh/10.0
        else:
             valuehigh[hour]=(hh-1)/10.0
        print hour
        print valuehigh[hour]             
        f.write(str(valuehigh[hour]))
        f.write("\n")
        break 
print "done"

