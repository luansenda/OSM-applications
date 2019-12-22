# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 20:33:45 2018

@author: Senda

E-mail: luansenda@buaa.edu.cn
"""


import os
os.environ["PROJ_LIB"] = "D:\ProgramData\Anaconda3\Library\share" #windows 解决获取地图出错的问题 
import osmnx as ox

######------------------------TEST01：成都-武侯区----------------------------------------######
## download the street network

## 1.按名称下载区域地图，前提是osm有名称信息
city = ox.graph_from_place("武侯区,成都市,中国", network_type = 'drive') 
## 2.按坐标区间下载区域地图,按照(north Lat,sourth Lat,east Lon,west Lon)顺序
city = ox.graph_from_bbox(30.619, 30.567, 104.069, 104.032, network_type='drive') 

## 以graph展示
ox.plot_graph(city)
# saving 
ox.save_graph_shapefile(city,filename='Wuhou_road', folder = r'C:\Users\g\Desktop\chengdu_osm\wuhou_shp\shape_from_osmnx_python')

#用不同color表示长度属性
ec = ox.get_edge_colors_by_attr(city, attr='length')
ox.plot_graph(city, edge_color=ec)

## 很重要：用color表示自定义路段属性，并显示到osm平台
import folium

######------------------------自定义函数：来自ox.plot_graph_filium（只能指定一种颜色）的更改------------------------------######
def plot_graphto_folium(G, graph_map=None, popup_attribute=None, tiles=None, zoom=1, fit_bounds=True, colors=[], edge_width=2, edge_opacity=1):
    ''' 其中的inputs:  tiles:string类型；表示地图样式
        选择项包括('openstreetmap'(默认)、'Stamen  Terrain'、'Stamen Toner'、'Mapbox Bright'、'Mapbox Control Room'等) '''    
    gdf_edges = ox.graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)# create gdf of the graph edges    
    x, y = gdf_edges.unary_union.centroid.xy# get graph centroid
    graph_centroid = (y[0], x[0])
    # create the folium web map if one wasn't passed-in
    if graph_map is None:
        graph_map = folium.Map(location=graph_centroid, zoom_start=zoom, tiles=tiles)
    # add each graph edge to the map
    for ind, row in gdf_edges.iterrows():
        ox.make_folium_polyline(edge=row, edge_color=colors[ind], edge_width=edge_width, edge_opacity=edge_opacity, popup_attribute=popup_attribute).add_to(graph_map)
    # if fit_bounds is True, fit the map to the bounds of the route by passing
    # list of lat-lng points as [southwest, northeast]
    if fit_bounds:
        tb = gdf_edges.total_bounds
        bounds = [(tb[1], tb[0]), (tb[3], tb[2])]
        graph_map.fit_bounds(bounds)
    return graph_map

#city.edges(keys=True, data=True) #获得道路边界，类似postgis信息
rosmid = [data['osmid'] for u, v, key, data in city.edges(keys=True, data=True)] #可以筛选OSMID,完成joincount的匹配
colorlist = ['green','blue','orange','yellow','red']
ec2 = [colorlist[e%5] if (type(e)==int) else ' ' for e in rosmid] # 自定义的各道路(osmid)对应属性的颜色list

graphmap = plot_graphto_folium(city, popup_attribute=None, tiles='Stamen  Terrain', colors = ec2, edge_width=4, edge_opacity=1)
filepath = r'C:\Users\g\Desktop\骑车行为分析\htmlcode\osmtest8.html'
graphmap.save(filepath)

import webbrowser as web # 内置包，无需安装
web.open(filepath) #直接用默认浏览器打开


######------------------------TEST2：一条最短路径-----------------------------------------######
# use networkx to calculate the shortest path between two nodes
import networkx as nx
origin_node = list(city.nodes())[0]
destination_node = list(city.nodes())[-1]
route = nx.shortest_path(city, origin_node, destination_node)
route_map = ox.plot_route_folium(city, route)
filepath = r'C:\Users\Administrator\Desktop\骑车行为分析\htmlcode\osmtest3.html'
route_map.save(filepath)



















