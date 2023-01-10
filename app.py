from flask import Flask,jsonify,request,session, render_template
#jsonifyはjsonに変換して渡すライブラリ
from flask_cors import CORS
#flaskに関するライブラリ
import glob
import pickle
import os
import bibtexparser

from module.highlight import highlightParagraph
from module.sectionTitle import sectionTitle, findParagraphSection, createSectionParagraph, processParagraph,processReportNote
from module.clusterInfo import createClusterTable
from module.findRef import findRefSpace
from module.findParagraph import findParagraph
from module.importGraphLayout import importGraphLayout
from module.preprocess.preprocessing import preprocessing

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__, static_folder='dist/static', template_folder='dist')
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
#CORS(app, origins=['http://localhost:8080/', 'http://localhost:8080/report'])

video_link = {
  'note-1020':"https://player.vimeo.com/video/728350445?h=e9468f982d",
  'paper-8813':"https://player.vimeo.com/video/721634409?h=d05601400a",
  'paper-7244':"https://player.vimeo.com/video/728350477?h=095d9dead7",
  'paper-7610':"https://player.vimeo.com/video/728351125?h=b8af283668"
}

prev_link = {
  'note-1020':"https://player.vimeo.com/video/746757051?h=4287011870",
  'paper-8813':"https://player.vimeo.com/video/746757401?h=1f85a8018d",
  'paper-7610':"https://player.vimeo.com/video/746758086?h=5716e57eb7",
  'paper-8813':"https://player.vimeo.com/video/746758229?h=d300b3478a"
}
SELECTFILE = ''
note_info = dict()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@app.route('/report_back', methods=['GET', 'POST'])
def report():
  global SELECTFILE, video_link, sim_data, slide_files, group, report_page_list
  if request.method == 'GET':
    #とりあえず、色々なファイルのパスを定義する
    slide_path = f'dist/static/static/{SELECTFILE}/video_content/correct_slides/*.jpg'
    slide_files = sorted(glob.glob(slide_path))
    slide_names = [file.split('/')[-1] for file in slide_files]
    select_report_path = f'/static/static/{SELECTFILE}/report_content/content'

    ##ページが何ページあるか取得
    report_page_list = sorted(glob.glob(f'dist/static/static/{SELECTFILE}/report_content/content/*.jpg'))
    report_page_list = [int(p.split('/')[-1].split('.')[0]) for p in report_page_list]
    report_page = max(report_page_list)
    print(report_page, report_page_list)

    return_slide_files = [f'/static/static/{SELECTFILE}/video_content/correct_slides/{name}' for name in slide_names]

    audio_path = f'dist/static/static/{SELECTFILE}/video_content/slide_audio.pickle'
    with open(audio_path, mode='rb') as f:
        [sentense_list, s_start_time_list, s_end_time_list, slide_sentense_index] = pickle.load(f)
        
    new_audio_content = []
    for index_list in slide_sentense_index:
        line = ''
        for index in index_list: line += sentense_list[index]
        new_audio_content.append([line])

    #論文のタイトルを持ってくる
    for entry in bib_entries:
      if entry['filename']==SELECTFILE:report_title = entry['title']


    report_path = f'dist/static/static/{SELECTFILE}/report_content/content.pickle'
    with open(report_path, mode='rb') as f:
      [content, section_title, addtion] = pickle.load(f)

    ##ヒートマップに与えるデータを考える
    with open(f'dist/static/static/{SELECTFILE}/report_audio_sim.pickle', mode='rb') as f:
      [sim_data] = pickle.load(f)
    youso_data = sim_data[0]
    
    tfidf_data = [i['tfidf'] for i in youso_data]
    heatmap_data = []
    for index, sim in enumerate(tfidf_data):
      heatmap_data.append({'y':index, 'color':float(sim)})

    ##クラスターの情報を取り出す
    with open(f'dist/static/static/{SELECTFILE}/wordcloud/cluster.pickle', mode='rb') as f:
      [group] = pickle.load(f)
    
    cluster = []
    cluster_slide_path = []
    cluster_group = []
    # 各クラスターに対しての情報を取り出す
    new_cluster = []
    for index, c in enumerate(content):
      isFind = False
      for g in group:
        if index in group[g]:
          new_cluster.append({'x':1, 'y':index, 'isin':g})
          isFind = True
          continue
      if not isFind:new_cluster.append({'x':1, 'y':index, 'isin':-1})
      

    for g in group:
      g_slide_path = []
      g_index = group[g]
      for i, c in enumerate(content):
        if i in g_index: cluster.append({'x':g, 'y':i, 'isin':g})
        else: cluster.append({'x':g, 'y':i, 'isin':-1})
      ##クラスターに所属するスライドのパスを与える
      for i in g_index:
        if i>=len(content):g_slide_path.append('/'.join(slide_files[i-len(content)].split('/')[1:]))
      cluster_slide_path.append(g_slide_path)
    section_title = sectionTitle(SELECTFILE)
    for g in sorted(group.keys()):
      cluster_group.append({'color':'white', 'index':g, 'name':g})

    print(report_page)
    VIDEOLINK = ''
    if SELECTFILE in video_link: VIDEOLINK= video_link[SELECTFILE]
    response_data = {'filename':SELECTFILE, 'slide_files':return_slide_files, 'audio_content':new_audio_content, 'select_report':select_report_path,
      'video_link':VIDEOLINK, 'heatmap_data':heatmap_data, 'cluster_data':new_cluster, 'heat_map_label':list(range(len(content))),
      'cluster_group':cluster_group, 'section_title':section_title, 'report_title':report_title,'cluster_slide_path':cluster_slide_path, 'report_page':report_page}
    #, 'heatmap_data':heatmap_data

    return jsonify(response_data)

  #POSTのとき(つまり、スライドを変更した時)####
  else:
    post_data = request.get_json()
    select_slide = post_data.get('select_slide')
    select_slide = 'dist/static/static/'+'/'.join(select_slide.split('/')[3:])
    youso_data = sim_data[slide_files.index(select_slide)]
    tfidf_data = [i['tfidf'] for i in youso_data]
    heatmap_data = []
    for index, sim in enumerate(tfidf_data):
      heatmap_data.append({'y':index, 'color':float(sim)})
    return jsonify({'heatmap_data':heatmap_data, 'max_index':tfidf_data.index(max(tfidf_data))})

@app.route('/cluster', methods=['POST'])
def cluster():
  post_data = request.get_json()
  select_cluster = post_data.get('selectCluster')
  select_file = post_data.get('fileName')
  table_data = createClusterTable(select_cluster, select_file)
  img_files = sorted(glob.glob(f'dist/static/static/{select_file}/wordcloud/{select_cluster}/*.jpg'))
  img_list = []
  
  # ページごとにクラスターの数を取得  
  with open(f'dist/static/static/{select_file}/wordcloud/page_cluster.pickle', mode='rb') as f:
    [page_coordinate_list] = pickle.load(f)

  
  for url in img_files:
    title = url.split('/')[-1].split('.')[0]
    img_list.append({'title':title, 'url':'/'+'/'.join(url.split('/')[1:])}) 
    # , 'place':page_coordinate_list[int(select_cluster)][title]
  return jsonify({'img_list':img_list, 'table_data':table_data})

@app.route('/select', methods=['POST'])
def selectParagraph():
  selectParagraph = request.get_json().get('select_paragraph')
  page = highlightParagraph(SELECTFILE, selectParagraph)

  return jsonify(page)

@app.route('/start', methods=['GET', 'POST'])
def start():
  global SELECTFILE, bib_entries, note_info
  if request.method == 'GET':
    folder_paths = sorted(glob.glob('dist/static/static/*'))
    folder_paths = [file for file in folder_paths if os.path.isdir(file)]
    file_names = [s.split('/')[-1] for s in folder_paths]
    #BibTexファイルのparserを行う
    with open('dist/static/static/session8.bib') as bibtex_file:
      bib_database = bibtexparser.load(bibtex_file)
    bib_entries = bib_database.entries

    return jsonify({'file_name':file_names, 'prev_link':prev_link})
  if request.method == 'POST':
    post_data = request.get_json()
    SELECTFILE = post_data.get('filename')
    with open(f'dist/static/static/{SELECTFILE}/note.pickle', mode='rb') as f:
      note_info = pickle.load(f)
    return jsonify(True)

@app.route('/find_ref', methods=['POST'])
def find_ref():
  global SELECTFILE
  post_data = request.get_json()
  # 画像かどうかのチェック
  ref, name = findRefSpace(post_data['page_num'], post_data['x'], post_data['y'], SELECTFILE, post_data['width'], post_data['height'])
  with open(f'dist/static/static/{SELECTFILE}/report_content/cite.pickle', mode='rb') as f:
    [cite_dict] = pickle.load(f)
  # 段落の場合のチェック
  if ref == None:
    index_list, p_refs,cite_list,cite_place, sim_slide, sim_paragraph =  findParagraph(post_data, SELECTFILE)
    new_cite_list = {'isCite':len(cite_list)>0,'cite_list':cite_list, 'cite_dict':cite_dict, 'cite_place':cite_place}
    add = {'cite':new_cite_list, 'slide':sim_slide, 'paragraph':sim_paragraph}
    if index_list == []: # クリックした場所が段落の時
      tag = 'none'
      index = None
    else:
      tag = 'paragraph'
      index = index_list[0]
  else:
    tag = 'figure'
    index, p_refs = None, []
    add = dict()
    
  return jsonify({'tag':tag, 'table':ref, 'file':name, 'index':index, 'paragraph_ref':p_refs, 'paragraph_add':add})

#Wordcloudを作成するための関数
@app.route('/wordcloud', methods=['POST'])
def wordcloud():
  global SELECTFILE
  post_data = request.get_json()
  cluster_num = 1

  item_list = importGraphLayout('paper-8813', post_data['select_cluster'])
  return jsonify({'item':item_list})

# メモに関するビューで必要な情報を与える
@app.route('/note_info', methods=['POST'])
def note_info():
  # 論文に関する情報を持ってくる
  global note_info, content, slide_files

  report_path = f'dist/static/static/{SELECTFILE}/report_content/content.pickle'
  with open(report_path, mode='rb') as f:
    [content, section_title, addtion] = pickle.load(f)
  section_list = [] # セクションタイトルのリスト
  section_head_list = dict() # 各セクションの最初の一行
  for [title, index] in section_title:
    section_list.append(title)
    section_head_list[title] = '.'.join(content[index].split('.')[:2])+'...'
  # 図表のリストを取得する
  figure_list = sorted(glob.glob(f'dist/static/static/{SELECTFILE}/report_content/figure/*.jpg'))
  figure_name_list = [path.split('/')[-1].split('.')[0] for path in figure_list]
  figure_path_list = [f'/static/static/{SELECTFILE}/report_content/figure/{name}.jpg' for name in figure_name_list]
  word_list = list(' '.join(content).replace(',', '').replace('.', '').split(' '))
  word_list = [a for a in word_list if word_list.count(a) >= 3]
  word_list = list(set(word_list))

  # セクションの構造を取得する

  section_structure, total_section_structure = createSectionParagraph(SELECTFILE)
  new_slide_files = ['/'+'/'.join(path.split('/')[1:]) for path in slide_files]
  
  return jsonify({'content':content, 'section_list':section_list,  'section_head':section_head_list, 'section_structure':section_structure,
    'figure_name_list':figure_name_list, 'figure_path_list':figure_path_list, 'file':SELECTFILE, 'word_list':word_list, 'slide_files':new_slide_files,
    'total_section_structure':total_section_structure, 'report_max_page':len(report_page_list)})
  
# メモを保存する関数
@app.route('/note_save', methods=['POST'])
def note_save():
  global SELECTFILE, note_info

  post_data = request.get_json()
  id = str(post_data['id'])
  print(id, post_data)
  if id in note_info:
    note_info[id].append(post_data)
  else:
    note_info[id] = [post_data]
  with open(f'dist/static/static/{SELECTFILE}/note.pickle', mode='wb') as f:
    pickle.dump(note_info, f)
  return jsonify({'note':note_info})

@app.route('/note_get', methods=['POST'])
def note_get():
  global SELECTFILE, note_info, content, video_link
  post_data = request.get_json()
  # print(post_data['tag'])
  # for note in note_info['0']:
  #   print(note['tag'])
  # print(findParagraphSection(SELECTFILE, 5))
  id = post_data['id']
  if id == None: id = ''
  post_content = []
  if id in note_info:
    post_content = [c for c in note_info[id] if c['tag'] == post_data['tag'] ]
  # 段落についての時のみ処理を行う
  if post_data['tag'] == 'report-paragraph':
    post_content = processParagraph(SELECTFILE, post_content, content)
  if post_data['tag'] == 'report-all':
    print('report-all')
    post_content = processReportNote(SELECTFILE, note_info, content,id)
  
  return jsonify({'content':post_content, 'selectfile':SELECTFILE, 'report_max_page':len(report_page_list), 'videoLink':video_link[SELECTFILE]})

@app.route('/note_delete', methods=['POST'])
def note_delete():
  global SELECTFILE, note_info

  post_data = request.get_json()
  item = post_data['item']
  # itemを消去する
  if item in note_info['0']:
    note_info['0'].remove(item)
    with open(f'dist/static/static/{SELECTFILE}/note.pickle', mode='wb') as f:
      pickle.dump(note_info, f)
  return jsonify({'message':'メモを消去しました'})
  
@app.route('/uploadFile', methods=['POST'])
def importFile():
  pdf = request.files['userpdf']
  video = request.files['uservideo']
  json = request.files['userjson']
  preview = request.files['userjson']
  name = request.form['name']
  bib = request.form['bibtex']
  
  os.mkdir(f'dist/static/static/{name}')
  os.mkdir(f'dist/static/static/{name}/video_content')
  os.mkdir(f'dist/static/static/{name}/preview')
  os.mkdir(f'dist/static/static/{name}/report_content')

  path = f'dist/static/static/{name}/'
  pdf.save(f'{path}{name}.pdf')
  video.save(f'{path}{name}.mp4')
  json.save(f'{path}video_content/audio-transcribe.json')
  preview.save(f'{path}preview/{name}.mp4')
  
  # print(post_data['video'])
  preprocessing(name)
  bib_before = ','.join(bib.split(',')[:-1])
  bib_after = bib.split(',')[-1]
  new_bib = f'{bib_before}, filename = '+'{'+name+'}'+f',{bib_after}'
  with open('dist/static/static/session8.bib', mode="a") as f:
    f.write(f'{new_bib}\n')

  note_info = dict()
  with open(f'dist/static/static/{name}/note.pickle', mode='wb') as f:
    pickle.dump(note_info, f)
  
  return jsonify({'text':'テキスト'})


if __name__=='__main__':
  app.run(port=5051)
