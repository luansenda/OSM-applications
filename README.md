# OSM-applications
# download map/shp files, data mining applications based on it

import os

os.environ["PROJ_LIB"] = "D:\ProgramData\Anaconda3\Library\share" #windows 解决获取地图出错的问题 

import osmnx as ox

## download the street network

## 1.按名称下载区域地图，前提是osm有名称信息

city = ox.graph_from_place("武侯区,成都市,中国", network_type = 'drive') 

## 2.按坐标区间下载区域地图,按照(north Lat,sourth Lat,east Lon,west Lon)顺序

#city = ox.graph_from_bbox(30.619, 30.567, 104.069, 104.032, network_type='drive')

# saving 

ox.save_graph_shapefile(city,filename='Wuhou_road', folder = r'C:\Users\g\Desktop')

## 以graph展示

ox.plot_graph(city)

![image](https://github.com/luansenda/OSM-applications/blob/master/test1.png)

## 很重要：用color表示自定义路段属性，并显示到osm平台

import folium

## 自定义函数：来自ox.plot_graph_filium（只能指定一种颜色）的更改
def plot_graphto_folium(G, graph_map=None, popup_attribute=None, tiles=None, zoom=1, fit_bounds=True, colors=[], edge_width=2, edge_opacity=1):

    gdf_edges = ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)# create gdf of the graph edges    
    
    x, y = gdf_edges.unary_union.centroid.xy# get graph centroid
    
    graph_centroid = (y[0], x[0])
    
    if graph_map is None:
    
        graph_map = folium.Map(location=graph_centroid, zoom_start=zoom, tiles=tiles)
        
    for ind, row in gdf_edges.iterrows():
    
        ox.make_folium_polyline(edge=row, edge_color=colors[ind], edge_width=edge_width, edge_opacity=edge_opacity, popup_attribute=popup_attribute).add_to(graph_map)
        
    if fit_bounds:
    
        tb = gdf_edges.total_bounds
        
        bounds = [(tb[1], tb[0]), (tb[3], tb[2])]
        
        graph_map.fit_bounds(bounds)
        
    return graph_map

rosmid = [data['osmid'] for u, v, key, data in city.edges(keys=True, data=True)] #可以筛选OSMID,完成joincount的匹配

colorlist = ['green','blue','orange','yellow','red']

ec2 = [colorlist[e%5] if (type(e)==int) else ' ' for e in rosmid] # 自定义的各道路(osmid)对应属性的颜色list

graphmap = plot_graphto_folium(city, popup_attribute=None, tiles='Stamen  Terrain', colors = ec2, edge_width=4, edge_opacity=1)

filepath = r'C:\Users\g\Desktop\骑车行为分析\htmlcode\osmtest8.html'

graphmap.save(filepath)

import webbrowser as web # 内置包，无需安装

web.open(filepath) #直接用默认浏览器打开

![image](https://github.com/luansenda/OSM-applications/blob/master/osm_pic.jpg)
