# get the path to the shapefiles for Crimes and Dsitricts
Crime = "S:/682/Spring20/rklara/Final Project/682_final_data/Crime_Incidents_in_2017.shp"
Shotspotter = "S:/682/Spring20/rklara/Final Project/682_final_data/Shot_Spotter_Gun_Shots.shp"
Wards = "S:/682/Spring20/rklara/Final Project/682_final_data/Ward_from_2012.shp"
 
# The format is:
# vlayer = QgsVectorLayer(data_source, layer_name, provider_name)

CrimeDC = iface.addVectorLayer(Crime, "DC", "ogr") #loads crime into QGIS
if not CrimeDC.isValid():
    print("Layer failed to load!") #catch my errors

ShotspotterDC = iface.addVectorLayer(Shotspotter, "DC", "ogr") #loads Police Districts into GIS
if not ShotspotterDC.isValid():
    print("Layer failed to load!") #catch my erros

WardsDC = iface.addVectorLayer(Wards, "DC", "ogr") #loads Police Districts into GIS
if not WardsDC.isValid():
    print("Layer failed to load!") #catch my erros
    
#Perform Spatial Join
processing.run("qgis:joinbylocationsummary",{'INPUT':WardsDC,'JOIN':CrimeDC,'PREDICATE':1,'SUMMARIES':0,'OUTPUT':"S:/682/Spring20/rklara/Final Project/682_final_data/Crime_Wardsjoin.shp"})
processing.run("qgis:joinbylocationsummary",{'INPUT':WardsDC,'JOIN':ShotspotterDC,'PREDICATE':1,'SUMMARIES':0,'OUTPUT':"S:/682/Spring20/rklara/Final Project/682_final_data/Shotspotter_Wardsjoin.shp"})

Crime_Wardsjoin = "S:/682/Spring20/rklara/Final Project/682_final_data/Crime_Wardsjoin.shp"
Shotspotter_Wardsjoin = "S:/682/Spring20/rklara/Final Project/682_final_data/Shotspotter_Wardsjoin.shp"

#add the layers spatially joined
Crime_Wardsjoin1 = iface.addVectorLayer(Crime_Wardsjoin, "Join", "ogr") #loads crime into QGIS
if not Crime_Wardsjoin1.isValid():
    print("Layer failed to load!") #catch my errors
    
Shotspotter_Wardsjoin1 = iface.addVectorLayer(Shotspotter_Wardsjoin, "Join", "ogr") #loads crime into QGIS
if not Shotspotter_Wardsjoin1.isValid():
    print("Layer failed to load!") #catch my errors

#Add new field for calculating crime per 10k people
from qgis.PyQt.QtCore import QVariant
CW_Attr = Crime_Wardsjoin1.dataProvider()
CW_Attr.addAttributes([QgsField("Per10k", QVariant.Int)])
Crime_Wardsjoin1.updateFields()

from qgis.PyQt.QtCore import QVariant
SW_Attr = Shotspotter_Wardsjoin1.dataProvider()
SW_Attr.addAttributes([QgsField("Per10k", QVariant.Int)])
Shotspotter_Wardsjoin1.updateFields()

Crime_Wardsjoin1 .updateFields()

expression1 = QgsExpression('"CCN_count"/"POP_2010"*10000')
context = QgsExpressionContext()
context.appendScopes(\
QgsExpressionContextUtils.globalProjectLayerScopes(Crime_Wardsjoin1))

with edit(Crime_Wardsjoin1):
    for f in Crime_Wardsjoin1.getFeatures():
        context.setFeature(f)
        f['Per10k'] = expression1.evaluate(context)
        Crime_Wardsjoin1.updateFeature(f)
        
Shotspotter_Wardsjoin1 .updateFields()

expression1 = QgsExpression('"ID_count"/"POP_2010"*10000')
context = QgsExpressionContext()
context.appendScopes(\
QgsExpressionContextUtils.globalProjectLayerScopes(Shotspotter_Wardsjoin1))

with edit(Shotspotter_Wardsjoin1):
    for f in Shotspotter_Wardsjoin1.getFeatures():
        context.setFeature(f)
        f['Per10k'] = expression1.evaluate(context)
        Shotspotter_Wardsjoin1.updateFeature(f)
