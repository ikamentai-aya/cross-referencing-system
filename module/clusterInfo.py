import pickle 
from sklearn.feature_extraction.text import TfidfVectorizer

##cluster vue内の表で表示するデータの作成###
def createClusterTable(select_cluster, file_name):
  #セクションタイトルの取得
  report_path = f'dist/static/static/{file_name}/report_content/content.pickle'
  with open(report_path, mode='rb') as f:
    [content, section_title, addtion]=pickle.load(f)

  ## 段落ごとのタグクラウド表示 ##
  vectorizer = TfidfVectorizer(stop_words='english')
  X = vectorizer.fit_transform(content)
  names = vectorizer.get_feature_names_out()
  
  #クラスター情報の取得
  cluster_path = f'dist/static/static/{file_name}/wordcloud/cluster.pickle'
  with open(cluster_path, mode='rb') as f:
    [group]=pickle.load(f)
  table_data = []
  #選択したクラスターのインデックス
  index_list = group[select_cluster]
  section_index = 0
  for i in index_list:
    if i > len(content):break
    #セクションタイトルの取得
    while(i > section_title[section_index][1]):
      section_index += 1

    #　タグクラウドの取得(TFIDF上位５単語)
    sorted_tfidf, sorted_index = zip(*sorted(zip(X.toarray()[i],range(len(X.toarray()[0]))),reverse=True))
    tags = [names[index] for index in sorted_index[:5]]
    
    #先頭の数単語の取得
    s = list(content[i].split())
    if len(s) > 6:start = ' '.join(s[:6])
    else: start = content[i]

    if section_index == 0:
      table_data.append({'start':start, 'section':'', 'index':i, 'tag':', '.join(tags), 'all':content[i], 'color':'white'})
    else:
      table_data.append({'start':start, 'section':section_title[section_index-1][0], 'index':i, 'tag':', '.join(tags),'all':content[i],'color':'white'})
      
  return table_data