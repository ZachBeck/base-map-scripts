import arcpy

def list_to_string(in_lst):
    out_string = ', '.join(str(i) for i in in_lst)
    return out_string

# proj_path = r'C:\Cache\Maps\Maps.aprx'
# map = 'Lite VT'
# layer_number = 6

def read_cim(proj_path, map, layer_number, layer_name):

    aprx = arcpy.mp.ArcGISProject(proj_path)
    m = aprx.listMaps(map)[0]
    lyr = m.listLayers()[layer_number]
    lyr_cim = lyr.getDefinition('V3')

    if layer_name == lyr.name:
        print(f'Reading {layer_name} CIM')
    else:
        print(f"{lyr.name} doesn't match the layer name {layer_name}")
        exit()

    symbol_group = lyr_cim.renderer.groups
    symbol_layer_drawing = lyr_cim.symbolLayerDrawing.symbolLayers

    symbol_properties = []
    symbol_elements = []

    for group in symbol_group:
        classes = group.classes

        for items in classes:
            sym_label = items.label

            width_list = []
            color_list = []
            
            for symbol in items.symbol.symbol.symbolLayers:
                sym_grp_name = symbol.name
                width = symbol.width
                width_list.append(width)
                color = str(symbol.color.values)
                print(color)
                color_list.append(color)
                minscale = items.symbol.minScale
                maxscale = items.symbol.maxScale
                        
            symbol_properties.append([sym_label, sym_grp_name, list_to_string(width_list), list_to_string(color_list), minscale, maxscale])

            for alt in items.alternateSymbols:

                alt_minscale = alt.minScale
                alt_maxscale = alt.maxScale

                alt_width_list = []
                alt_color_list = []

                for alt_sym in alt.symbol.symbolLayers:
                    alt_grp_name = alt_sym.name
                    alt_width = alt_sym.width
                    alt_width_list.append(alt_width)
                    alt_color = str(alt_sym.color.values).replace(',', '')
                    alt_color_list.append(alt_color)
                    
                symbol_properties.append([sym_label, alt_grp_name, list_to_string(alt_width_list), list_to_string(alt_color_list), alt_minscale, alt_maxscale])

        return symbol_properties

# print(symbol_properties) 
# for prop in symbol_properties:
#     print(prop[3])


# for sym_lyr in symbol_layer_drawing:
#     sym_lyr_name = sym_lyr.symbolLayerName
#     print(sym_lyr_name)


