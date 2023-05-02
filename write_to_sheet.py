import json
import pygsheets
from read_cim_symbology import read_cim


proj_path = r'C:\Cache\Maps\Maps.aprx'
map = 'Overlay VT'
layer_number = 18
layer_name = 'Roads - All'

cim_symbology = read_cim(proj_path, map, layer_number, layer_name)

service_json = r'secrets\secrets.json'
gc = pygsheets.authorize(service_file=service_json)
symbology_sheet = gc.open_by_key('1Yqrsg5J19TVo1CnJM6hezax86UgUxRlOUAqch1eK_MQ')

worksheet = symbology_sheet[2]

scale_cells = {1128.497176:2, 2256.994353:3, 4513.988705:4, 9027.977411:5, 18055.954822:6, 36111.909643:7,
               72223.819286:8, 144447.638572:9, 288895.277144:10, 577790.554289:11, 1155581.108577:12,
               2311162.217155:13, 4622324.434309:14, 9244648.868618:15, 18489297.737236:16}

road_cells = {'Interstates':('D', 'E'), 'Ramps and Collectors':('F', 'G'), 'US Highways':('H', 'I'), 'State Highways':('J', 'K'),
             'Major Local Roads Paved':('L', 'M'), 'Other Federal Aid Roads':('N', 'O'),
             'Major Local Roads Not Paved':('P', 'Q'), 'Local Roads':('R', 'S')}

def list_to_string(in_list):
  out_string = ', '.join(str(i) for i in in_list)
  return out_string

for elements in cim_symbology:
    label = elements[0]
    # inner = t[2]
    # case = t[3]
    widths = elements[2]
    # c1 = t[4]
    # c2 = t[5]
    colors = elements[3]
    min = elements[4]
    max = elements[5]

    min_max = [min,max]

    if min in scale_cells and label in road_cells:
        row = scale_cells[min]
        print(row)
        cell_range = road_cells[label]
        update_cells = f'{cell_range[0]}{row}:{cell_range[1]}{row}'
        print(update_cells)
        worksheet.update_values(update_cells, [[widths,colors]])
    else:
        print('not found')
    
