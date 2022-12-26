#ページ数をもらうとその中のfigureの位置を知らせる
import pickle
from module.highlight import highlight
import re

#lの単語のいずれかがsに含まれているかの確認
def figTableIn(n, s):
  word_list = [f'figure{n}', f'fig{n}', f'table{n}']
  isIn = False
  for word in word_list:
    if word in s.lower().replace(' ', '').replace('.', ''):
      isIn = True
  return isIn


def findClickedFigure(page, x, y, figure_area_dict, file_name):
  print(x,y)
  for name in figure_area_dict:
    [p, coodinate] = figure_area_dict[name]
    print(coodinate)
    if p != str(page):
      continue
    elif coodinate[0]<y<coodinate[1] and coodinate[2]<x<coodinate[3]:
      img = highlight([coodinate], p, f'dist/static/static/{file_name}/report_content/content')
      img.save(f'dist/static/static/{file_name}/select.jpg')
      return name

def findRefSpace(page, x, y, file_name, width, height):
  with open(f'dist/static/static/{file_name}/report_content/figure/coodinate.pickle', mode='rb') as f:
    [figure_area_dict] = pickle.load(f)
  with open(f'dist/static/static/{file_name}/report_content/content.pickle', mode='rb') as f:
    [content, section_title, addition] = pickle.load(f)
  d_w = 2550
  d_h = 3301
  a_x = x*d_w/width
  a_y = y*d_h/height
  print(a_x, a_y)
  name = findClickedFigure(page, a_x, a_y, figure_area_dict, file_name)
  if name == None: return None, ''
  ref = []
  for i, c in enumerate(content):
    name_num = re.search(r'[0-9]+', name).group(0)
    # if name in c.lower():
    if figTableIn(name_num, c):
      ref.append(i)

  ##セクションタイトルの取得
  table_data = []
  section_index = 0
  for i in ref:
    if i > len(content):break
    while(i > section_title[section_index][1]):
      section_index += 1
    
    s = list(content[i].split())
    if len(s) > 8:start = ' '.join(s[:8])
    else: start = content[i]

    if section_index == 0:
      table_data.append({'start':start, 'section':'', 'index':i})
    else:
      table_data.append({'start':start, 'section':section_title[section_index-1][0].split()[0], 'index':i})

  return table_data, name

