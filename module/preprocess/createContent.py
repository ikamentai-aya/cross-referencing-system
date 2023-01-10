import pickle
import re

#縦並びの画像を上から順番に並べ替え,段落でないものは排除する
def sortLinedArea(path_list, path_coordinate_dict, path_text_dict, section_title):
    
    section_title_join= '|'.join([s[0] for s in section_title])
    
    pathYList = []
    for path in path_list:
        [y1, y2, x1, x2] = path_coordinate_dict[path]
        pathYList.append((y1+y2)/2)
    sortYList, sortPathList = zip(*sorted(zip(pathYList, path_list)))
    sortPathList = list(sortPathList)
    
    #各エリアが段落か判定（段落ならカンマがあるはずでは？？）
    paragraph = []
    notParagraph = []
    figure_pt = re.compile(r'(figure[0-9]+:.*)|(fig[0-9]+:.*)|(table[0-9]+:.*)')
    for path in sortPathList: 
        s = path_text_dict[path]
        line_list = s.split('\n')
        line_len = sum([len(l) for l in line_list])/len(line_list) #各行の平均文字数
        s_not_space = s.replace(' ', '').lower()
        figure_match = figure_pt.match(s_not_space)
        
        if figure_match != None:
            notParagraph.append(path)
        elif '.' in s and line_len > 40:
            paragraph.append(path)
        # elif not '.' in s and not ',' in s:
        elif s in section_title_join:
            paragraph.append(path)
        else:
            notParagraph.append(path)
            
        
    return paragraph, notParagraph


#path_listとpath_coordinate_dict, path_text_dictを与えると、正しい順番に分割してくれる関数
def sortArea(path_list, path_coordinate_dict, path_text_dict, section_title):
    right_area = []
    not_paragraph = []
    left_area = []
    
    #まず順番に左側の画像・右側の画像・段落以外に分割する
    for path in path_list:
        [y1, y2, x1, x2] = path_coordinate_dict[path]
        #右側の画像
        if x2 < 1275: left_area.append(path)
        #左側の画像
        elif x1 > 1275: right_area.append(path)
        #
        else: not_paragraph.append(path)
    
    sort_left_area, not_left = sortLinedArea(left_area, path_coordinate_dict, path_text_dict, section_title)
    sort_right_area, not_right = sortLinedArea(right_area, path_coordinate_dict, path_text_dict, section_title)
    sort_area = sort_left_area + sort_right_area
    not_paragraph += not_left
    not_paragraph += not_right
    
    return sort_area, not_paragraph

#
def changeSectionTitle(txt, section_title, paragraph_num):
    for index, [title, i] in enumerate(section_title):
        if txt in title:
            section_title[index] = [title, paragraph_num]
            return section_title
        

#pathの場所にあるものから段落の内容を取ってくる
def getContent(path, path_text_dict, paragraph_num, section_title):
    
    section_title_join= '|'.join([s[0] for s in section_title])
    content = []    
    txt = path_text_dict[path]
    line_list = txt.split('\n')
    
    #これがセクションタイトルのみからなる小領域の場合
    if len(txt) < 50:
        section_title = changeSectionTitle(txt, section_title, paragraph_num)
        return content, section_title, paragraph_num
    
    p = ''
    start_kuhaku = 0
    
    for line in line_list:
        
        #先頭が空白＝段落の変わり目
        
        if line == ' ':
            content.append(p)
            p = line 
            paragraph_num += 1
        elif line == '':
            content.append(p)
            p = ''
            paragraph_num += 1
        elif line in section_title_join:
            if 'reference' in line.lower():
                print(line)
                content.append(line)
                p = ''
            else:
                section_title = changeSectionTitle(line, section_title,paragraph_num)
                p = ''
        else:p += line
    
    if p != '':
        content.append(p)
    
    return content, section_title, paragraph_num

#このメイン関数
def createContent(file_name):
    content_path = f'dist/static/static/{file_name}/report_content/content.pickle'
    coodinate_path = f'dist/static/static/{file_name}/report_content/content/path_coordinate.pickle'
        
    ## 段落の作成
    with open(coodinate_path, mode='rb') as f:
        [path_coordinate_dict, path_text_dict] = pickle.load(f)
    with open(content_path, mode='rb') as f:
        [content, section_title, addition] = pickle.load(f)
    ##まずページごとに分割する
    page_path = [[] for i in path_coordinate_dict]
    for path in path_coordinate_dict:
        page = int(path.split('/')[-1].split('-')[0])
        page_path[page].append(path)
    #余分な部分を削除する
    page_path = [page for page in page_path if page != []]
    
    #エリアを全て並べ替える
    sortedArea = []
    notParagraph = []
    for path_list in page_path:
        sort_area, not_paragraph = sortArea(path_list, path_coordinate_dict, path_text_dict, section_title)
        sortedArea += sort_area
        notParagraph += not_paragraph
        
    #並べ替えた領域から抽出する
    CONTENT = []
    paragraph_num = 0
    for path in sortedArea:
        content, section_title, paragraph_num = getContent(path, path_text_dict, paragraph_num, section_title)
        CONTENT += content
        
    #参考文献以降をカットする
    for index, c in enumerate(CONTENT):
        if 'REFERENCE' in c:
            print(index)
            CONTENT = CONTENT[:index]
            break
            
        
    with open(content_path, mode='wb') as f:
        pickle.dump([CONTENT, section_title, addition], f)
        