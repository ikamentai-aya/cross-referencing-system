from xml.dom import minidom
import re

## save_path先にあるSVGからwordcloudのレイアウト情報を取得する
def importGraphInfo(save_path):

    node_indices = [] #ノードのインデックス
    x_list = []; y_list = [] #ノードのx,y座標
    rx_list = []; ry_list = [] #ノードの縦横さいず
    font_size_list = [];
    title_list = []

    #SVGの幅・高さを取得
    doc = minidom.parse(save_path+'.svg')
    width = doc.getElementsByTagName('svg')[0].getAttribute('width')
    height = doc.getElementsByTagName('svg')[0].getAttribute('height')
    width = int(re.findall(r'[0-9]+', width)[0])
    height = int(re.findall(r'[0-9]+', height)[0])

    for g in doc.getElementsByTagName('g'):

        nodeclass = g.getAttribute('class')
        #classがnodeだった時
        if nodeclass == 'node':
            ids = g.getElementsByTagName('title')[0].childNodes[0].nodeValue
            x = g.getElementsByTagName('text')[0].getAttribute('x')
            y = g.getElementsByTagName('text')[0].getAttribute('y')
            font_size = g.getElementsByTagName('text')[0].getAttribute('font-size')
            title = g.getElementsByTagName('title')[0].childNodes[0].nodeValue
            int_font_size = int(re.findall(r'[0-9]+', font_size)[0])
            # x = int(re.findall(r'[0-9]+', x)[0]) - int_font_size * len(title)
            x = int(re.findall(r'[0-9]+', x)[0]) 
            y = int(re.findall(r'[0-9]+', y)[0]) + int_font_size
            
            x_list.append(x); y_list.append(y)
            font_size_list.append(int_font_size)
            title_list.append(title)
            
    return x_list, y_list, font_size_list, title_list, width, height

#600*400に描画できるように調整する
def transformScale(x_list, y_list, font_size_list, title_list, width, height):

    #文字の左端、右端、上辺、下辺を計算する
    left_x = []; right_x = []
    top_y = []; bottom_y = []
    for i,x in enumerate(x_list):
      half_font = round(font_size_list[i]/2)
      left_x.append(x-half_font*len(title_list[i]))
      right_x.append(x+half_font*len(title_list[i]))
      top_y.append(y_list[i]+half_font)
      bottom_y.append(y_list[i]-half_font)

    #一番左端が０、一番下辺が0になるように調整を行う
    min_x = min(left_x); min_y = min(bottom_y)
    x_list = [x-min_x for x in x_list]
    #left_x = [x-min_x for x in left_x]
    y_list = [y-min_y for y in y_list]
    right_x = [x-min_x for x in right_x]
    #top_y = [y-min_y for y in top_y]

    # right_x = []
    # top_y = []; bottom_y = []
    # for i,x in enumerate(x_list):
    #   half_font = round(font_size_list[i]/2)
    #   right_x.append(x+half_font*len(title_list[i])*2.2)
    #   top_y.append(y_list[i]+half_font)
    #   bottom_y.append(y_list[i]-half_font)

    # min_x = min(x_list); min_y = min(bottom_y)
    # x_list = [x-min_x for x in x_list]
    # y_list = [y-min_y for y in y_list]
    # right_x = [x-min_x for x in right_x]
    # top_y = [y-min_y for y in top_y]

    for i, x in enumerate(x_list[:5]):
      print(title_list[i],x,y_list[i])
    width = round(max(right_x)); height = round(max(top_y))
    print(width, height)

    resize = max(width/600, height/400) #縮尺の計算
    resize_x = width/600 #x方向の縮尺
    resize_y = height/400 #y方向の縮尺
    size = [f'{round(float(s)/resize)*0.9}pt' for s in font_size_list]
    x_list = [x//resize_x for x in x_list]
    right_x = [x//resize_x for x in right_x]
    y_list = [400-y//resize_y for y in y_list]
    print(min(left_x), max(right_x), min(y_list),max(y_list))

    item_list = []
    for i, title in enumerate(title_list):
      item_list.append({'title':title, 'x':x_list[i], 'y':y_list[i], 'size':size[i]})

    return item_list

# このモジュールのメイン関数
def importGraphLayout(file_name, cluster_num):
  save_path = f'dist/static/static/{file_name}/wordcloud/svg/{cluster_num}'
  x_list, y_list, font_size_list, title_list, width, height = importGraphInfo(save_path)
  item_list = transformScale(x_list, y_list, font_size_list, title_list, width, height)
  return item_list


