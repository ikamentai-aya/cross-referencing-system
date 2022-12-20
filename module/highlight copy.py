from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import os
import pickle
import re

####spaceのエリアをハイライトする関数####
def highlight(space, page_number, save_path):
    
    original = cv2.imread(f'{save_path}/{page_number}.jpg')
    
    for coodinate in space:
        height = coodinate[1]-coodinate[0]
        width = coodinate[3]-coodinate[2]
        
        #ブランク画像
        blank = np.zeros((height, width, 3))
        blank += [255,236,0][::-1] #RGBで青指定
        
        y_offset = coodinate[0]
        x_offset = coodinate[2]
        original[y_offset:y_offset+height, x_offset:x_offset+width] = original[y_offset:y_offset+height, x_offset:x_offset+width]*0.8+blank*0.2
        
    image = Image.fromarray(original)
    return image
    

def findSpace(input_text, path_coordinate_dict, path_text_dict):
    word_list = input_text.split()
    word_num = len(word_list)
    coodinate = []
    page = 0
    for i in path_coordinate_dict:
        if input_text in path_text_dict[i]:
            print('-------')
            print(input_text)
            print(path_text_dict[i])
        txt_words = path_text_dict[i].split()
        
        if txt_words[:word_num]==word_list or input_text in path_text_dict[i]:
            coodinate = path_coordinate_dict[i]
            page=i.split('/')[-1].split('-')[0]
            
    return coodinate, page
            
#ハイライトしたい部分の先頭を与えると、ハイライトした画像で返してくれる
def highlightTextList(text_list, path_coordinate_dict, path_text_dict, save_path):
    c_p_list = []
    for text in text_list:
        coodinate, page = findSpace(text, path_coordinate_dict, path_text_dict)
        if [coodinate, page] in c_p_list:continue
        if len(coodinate) == 0:
            continue
        c_p_list.append([coodinate, page])
        
    print(c_p_list)
    p_c_dict = dict()
    for c, p in c_p_list:
        if p in p_c_dict:p_c_dict[p].append(c)
        else: p_c_dict[p] = [c]
        
    image_list = []
    for p in p_c_dict: 
        image = highlight(p_c_dict[p], p, save_path)
        image_list.append(image)
        
    page_list = [p for p in p_c_dict]
    return image_list, page_list

def highlightParagraph(file_name, index):
    
    wordcloud_path = f'dist/static/static/{file_name}/wordcloud'

    ##クラスターの情報を取得する
    with open(f'{wordcloud_path}/cluster.pickle', mode='rb') as f:
        [group] = pickle.load(f)
        
    ## 文章のインポート
    report_path = f'dist/static/static/{file_name}/report_content/content.pickle'
    with open(report_path, mode='rb') as f:
        [content, section_title, addtion]=pickle.load(f)
        
    ##レイアウト情報のインポート
    save_path = f'dist/static/static/{file_name}/report_content/content'
    with open(save_path+'/path_coordinate.pickle', mode='rb') as f:
        [path_coordinate_dict, path_text_dict] = pickle.load(f)
    
    s = ' '.join(content[index].split()[0:3])       
    print(s)   
    if re.match(r'[0-9a-zA-Z]', s[0])==None:s = ' '.join(content[index].split()[1:4])
    
    image_list, page_list = highlightTextList([s], path_coordinate_dict, path_text_dict, save_path)
    if len(page_list) >0:
      image_list[0].save(f'dist/static/static/{file_name}/select.jpg')
      return page_list[0]
    else: return -1 

   
    
