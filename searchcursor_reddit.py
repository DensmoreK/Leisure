import arcpy

fc = 'c:/data/base.gdb/pointlayer'
fields = ['yourIDfieldname']

#setting up the max value variables
zone1=0
zone2=0
zone3=0

# For each row in the attribute table, use if statements
# to determine which category it is in and if it is bigger
# than the current max value for that category, update the
# max value variable
with arcpy.da.SearchCursor(fc, fields) as cursor:
    for row in cursor:
      if row[0]<2000 and row[0]>zone1:
        zone1=row[0]
      elif row[0]<3000 and row[0]>zone2:
        zone2=row[0]
      elif row[0]<4000 and row[0]>zone3:
        zone3=row[0]
      #keep adding elif statements to cover the rest of the zones

#this will print out the last number used in the zone category
print "zone1="+str(zone1)
print "zone2="+str(zone2)
print "zone3="+str(zone3)


        
