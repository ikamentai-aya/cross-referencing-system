import pickle
import glob

def sectionTitle(file_name):
  report_path = f'dist/static/static/{file_name}/report_content/content.pickle'
  with open(report_path, mode='rb') as f:
    [content, section_title, addtion]=pickle.load(f)

  N = len(content)-1
  section_paragraph = []
  start = section_title[0][1]+1
  end = 0
  for i, data in enumerate(section_title[1:]):
    pa_num = data[1]
    section_paragraph.append({'title':section_title[i][0].split()[0], 'start':start-1, 'end':pa_num, 'height':pa_num-start+1})
    start = pa_num+1
  section_paragraph.append({'title':section_title[-1][0].split()[0], 'start':start-1, 'end':N, 'height':N-start+2})

  return section_paragraph

def findParagraphSection(file_name, index):
  report_path = f'dist/static/static/{file_name}/report_content/content.pickle'
  with open(report_path, mode='rb') as f:
    [content, section_title, addtion]=pickle.load(f)
  before = section_title[0]
  if int(index)<before[1]: return ''
  for section in section_title:
    if before[1] <= int(index) and int(index) < section[1]: return before[0]
    before = section
  return before[0]

def createSectionParagraph(file_name):
  report_path = f'dist/static/static/{file_name}/report_content/content.pickle'
  with open(report_path, mode='rb') as f:
    [content, section_title, addtion]=pickle.load(f)
  section_list = [] # セクションタイトルのリスト
  for [title, index] in section_title:
    section_list.append(title)

  # セクションの構造を取得する
  big_section_list = [section for section in section_list if not '.' in section]
  section_kouzou = dict()
  for big_section in big_section_list: section_kouzou[big_section] = []
  for section in list(set(section_list)-set(big_section_list)):
    section_num = section.split('.')[0]
    for big_section in big_section_list:
      if section_num == big_section.split()[0]:
        section_kouzou[big_section].append(section)
  section_structure = [[key, section_kouzou[key]] for key in section_kouzou]

  # 図表に関する情報を取得
  figure_list = sorted(glob.glob(f'dist/static/static/{file_name}/report_content/figure/*.jpg'))
  figure_list = [f.split('/')[-1].split('.')[0] for f in figure_list]
  #初めて図表を参照する場所を探す
  figure_appear_dict = dict()
  for f_i, figure in enumerate(figure_list):
    for index, c in enumerate(content):
      if figure.lower() in c.lower():
        figure_appear_dict[figure] = index
        break
    # この図表が論文内で引用されていなかった場合
    if not figure in figure_appear_dict:
      if f_i == 0: figure_appear_dict[figure] = 0
      else: figure_appear_dict[figure] = figure_appear_dict[figure_list[f_i-1]]
  
  total_section_structure = dict()
  for key in section_kouzou: total_section_structure[key] = section_kouzou[key]
  big_section_index_list = []
  for b in big_section_list:
    for s in section_title:
      if s[0] == b: big_section_index_list.append(s)
  
  # 画像がどのセクションに所属するかの判定
  for figure in figure_appear_dict:
    f_i = figure_appear_dict[figure]

    for index, big_section in enumerate(big_section_index_list[:-1]):
      if big_section_index_list[index][1] <= f_i < big_section_index_list[index+1][1]:
        title = big_section[0]
        if not title in total_section_structure:
          total_section_structure[big_section_index_list[index][0]]= [figure]
        else:
          total_section_structure[title].append(figure)

    if big_section_index_list[-1][1] <= f_i:
      total_section_structure[big_section_index_list[-1][0]].append(figure)

  # print(section_kouzou)
  section_structure = [[key, section_kouzou[key]] for key in section_kouzou]
  total_section_structure = [[key, section_kouzou[key]] for key in total_section_structure]
  
  return section_structure, total_section_structure


def processParagraph(SELECTFILE, post_content, content):
  # 段落についての時のみ処理を行う

  new_content = []
  for c in post_content:
    print(c['content'])
    post_content.remove(c)
    content_split = c['content'].split('-') 
    index = content_split[0]
    sentence = '-'.join(content_split[1:])
    if sentence == '':
      c['sentence'] = content[int(index)]
    else:
      c['sentence'] = sentence
    c['section'] = findParagraphSection(SELECTFILE, index)
    new_content.append(c)
  post_content = new_content

  return post_content

def processReportNote(SELECTFILE, note_info, content, id):
  post_content = [c for c in note_info[id] if c['tag'] in ['report-paragraph', 'report-section', 'report-figure']]
  new_content = []
  for c in post_content:
    if c['tag'] == 'report-section':
      c['isFigure'] = False
      new_content.append(c)
    elif c['tag']== 'report-figure':
      c['isFigure'] = True
      new_content.append(c)
    else:
      print('c-content', c['content'])
      post_content.remove(c)
      if '-' in str(c['content']): content_split = str(c['content']).split('-') 
      else: content_split = [c['content']]
      index = content_split[0]
      sentence = '-'.join(content_split[1:])
      if sentence == '':
        c['sentence'] = content[int(index)]
      else:
        c['sentence'] = sentence
      c['section'] = findParagraphSection(SELECTFILE, index)
      new_content.append(c)
    
  post_content = new_content

  return post_content
