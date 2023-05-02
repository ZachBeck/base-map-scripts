import arcpy

# update symbol layer drawing so road symbology can easily be ordered with line cases on the bottom
proj_path = r'C:\Cache\Maps\Maps.aprx'

aprx = arcpy.mp.ArcGISProject(proj_path)
m = aprx.listMaps('Overlay VT')[0]
lyr = m.listLayers()[18]
layer_name = 'Roads - All'
lyr_cim = lyr.getDefinition('V3')

if layer_name == lyr.name:
    print(f'Reading {layer_name} CIM')
else:
    print(f"{lyr.name} doesn't match the layer name {layer_name}")
    exit()

symbol_group = lyr_cim.renderer.groups
symbol_layer_drawing = lyr_cim.symbolLayerDrawing.symbolLayers

new_symbol_lyrs = set()
# color_list = [[45, 10, 100, 100], [40, 75, 100, 100], [40, 65, 100, 100], [40, 45, 100, 100]]
# color_list = [[255, 255, 255, 100], [0, 40, 80, 100], [45, 10, 100, 100], [40, 65, 100, 100],
#               [30, 85, 90, 100], [40, 85, 100, 100], [40, 25, 100, 100]]
# color_list = [[45, 10, 100, 100], [40, 75, 100, 100], [40, 65, 100, 100], [40, 45, 100, 100]]

color_list = [[20, 85, 80, 100], [30, 100, 85, 100], [20, 85, 95, 100]]

for group in symbol_group:
    classes = group.classes
    
    for items in classes:
        sym_label = items.label

        for symbol in items.symbol.symbol.symbolLayers:
            color = symbol.color.values
            
            if color in color_list:
                symbol.name = f'{sym_label} Case'
                lyr.setDefinition(lyr_cim)
                new_symbol_lyrs.add(f'{sym_label} Case')
            else:
                symbol.name = f'{sym_label} Inner'
                lyr.setDefinition(lyr_cim)
                new_symbol_lyrs.add(f'{sym_label} Inner')
       
        for alt in items.alternateSymbols:

            for alt_sym in alt.symbol.symbolLayers:
                alt_color = alt_sym.color.values
                
                if alt_color in color_list:
                    alt_sym.name = f'{sym_label} Case'
                    lyr.setDefinition(lyr_cim)
                    new_symbol_lyrs.add(f'{sym_label} Case')
                else:
                    alt_sym.name = f'{sym_label} Inner'
                    lyr.setDefinition(lyr_cim)
                    new_symbol_lyrs.add(f'{sym_label} Inner')


lyr_cim.symbolLayerDrawing.symbolLayers = []
lyr.setDefinition(lyr_cim)


for name in new_symbol_lyrs:
    #{"type":"CIMSymbolLayerIdentifier", "symbolLayerName":"zzzz"}
    new_group = {"type" : "CIMSymbolLayerIdentifier", "symbolLayerName" : f'{name}'}
    lyr_cim.symbolLayerDrawing.symbolLayers.append(new_group)
    lyr.setDefinition(lyr_cim)
     
print(new_symbol_lyrs)
aprx.save()