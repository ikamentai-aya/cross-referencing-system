import pickle
import re
import glob
from module.highlight import highlight
from PIL import Image

####引用した論文番号のリストを取得する####
def findCiteNumber(text):
  cite_pt = re.compile(r'\[[0-9, ]+\]')
  cite_list = cite_pt.findall(text)
  new_cite_list = []
  for cite in cite_list:
    new_cite_list += cite.replace('[','').replace(']','').split(',')
  cite_list = [int(i) for i in new_cite_list]
  #引用されている箇所を明示する
  cite_place = dict()
  for c in cite_list:
    for t in text.split('.'):
      if str(c) in t:
        cite_place[str(c)]=t
        break

  return cite_list, cite_place

####選択した段落に最も似た上位3つのスライドを表示する####
def findSimilarSlide(index, SELECTFILE):
  with open(f'dist/static/static/{SELECTFILE}/report_audio_sim.pickle', mode='rb') as f:
    [sim_data] = pickle.load(f)
  tfidf_sim_data = [sim[index]['tfidf'] for sim in sim_data]
  slide_path_list = sorted(glob.glob(f'dist/static/static/{SELECTFILE}/video_content/correct_slides/*.jpg'))
  # max_index = tfidf_sim_data.index(max(tfidf_sim_data))
  # slide_path_list = sorted(glob.glob(f'dist/static/static/{SELECTFILE}/video_content/correct_slides/*.jpg'))
  # max_path = slide_path_list[max_index]
  # max_path = '/'.join(max_path.split('/')[1:])
  # return max(tfidf_sim_data), max_index, max_path

  sort_sim, sort_index = zip(*sorted(zip(tfidf_sim_data, range(len(tfidf_sim_data))),reverse=True))
  sim_path_list = ['/'+'/'.join(slide_path_list[i].split('/')[1:]) for i in sort_index[:3]]
  sim_slide_list = []
  for i, j, k  in zip(sort_sim, sort_index, sim_path_list):
    sim_slide_list.append({'similarity':i, 'index':j, 'path':k})
  print(sim_path_list)
  print(sim_slide_list)
  
  return sim_slide_list

# index版目の段落に似た段落3つを返す
def findSimilarParagraph(index, SELECTFILE):
  color = ['#f4faff', '#eaf4ff','#d5eaff','#aad5ff','#80bfff','#55aaff','#2b95ff','#0080ff','#006ad5','#0055aa']
  with open(f'dist/static/static/{SELECTFILE}/report_sim.pickle', mode='rb') as f:
    [sim_data] = pickle.load(f)
  sort_sim, sort_index = zip(*sorted(zip(sim_data[index], range(len(sim_data)))))
  color_chart = [color[int(i*10//1)] for i in sort_sim[-4:-1]]
  return color_chart, sort_index[-4:-1]


def findParagraph(post_data, SELECTFILE):
  # 各領域に関する情報を入手する
  with open(f'dist/static/static/{SELECTFILE}/report_content/coordinate.pickle', mode='rb') as f:
    [paragraph_coordinate_dict, non_paragraph_coordinate_dict, area_section_index] = pickle.load(f)
  with open(f'dist/static/static/{SELECTFILE}/report_content/content.pickle', mode='rb') as f:
    [content, section_title, addition] = pickle.load(f)

  d_w = 2550
  d_h = 3301
  a_x = post_data['x']*d_w/post_data['width']
  a_y = post_data['y']*d_h/post_data['height']
  isFind = False #対応する段落を見つけた場合

  #このクリックした箇所が所属する領域を探す
  for path in paragraph_coordinate_dict:
    path_page = path.split('/')[-1].split('-')[0]

    #ページ数が違ったらスルーする
    if path_page != str(post_data['page_num']):continue
    [y1, y2, x1, x2] = paragraph_coordinate_dict[path]
    if y1 < a_y < y2 and x1 < a_x < x2:
      isFind = True
      break
  #対応する領域がなかった時
  if not isFind:
    return [], [], [], [], [],[]

  #### 対応領域をハイライトする #####
  save_path = f'dist/static/static/{SELECTFILE}/report_content/content'
  image = highlight([[y1, y2, x1, x2]], post_data['page_num'], save_path)
  image.save(f'dist/static/static/{SELECTFILE}/select.jpg')
  

  refer_pt = re.compile(r'Figure [0-9]+|Table [0-9]')
  area_text = ''
  for index in area_section_index[path]:
    area_text += '\n'+ content[index]
  refs = refer_pt.findall(area_text)
  new_refs = []
  for r in refs:
    new_refs.append({'name':r, 'path':f'static/static/{SELECTFILE}/report_content/figure/{r.lower()}.jpg'})
  cite_list, cite_place = findCiteNumber(area_text)

  if area_section_index[path] != []:
    #max_sim, max_index, slide_path = findSimilarSlide(index, SELECTFILE)
    p_sim, p_sim_index = findSimilarParagraph(index, SELECTFILE)

    # sim_slide = {'similarity':max_sim, 'index':max_index, 'path':slide_path}
    sim_slide = findSimilarSlide(index, SELECTFILE)
    sim_paragraph = []
    for s, i in zip(p_sim, p_sim_index):
      sim_paragraph.append({'similarity':s, 'index':i, 'content':content[i][:30]})
  else:
    sim_slide = None
    sim_paragraph = []

  return area_section_index[path], new_refs, cite_list, cite_place, sim_slide, sim_paragraph[::-1]