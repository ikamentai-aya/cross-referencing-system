from module.preprocess.createFolder import createFolder

from module.preprocess.deriveReportContent import deriveReport
from module.preprocess.deriveReportFigure import deriveFigure
from module.preprocess.devideAreaByParagraph import deriveArea
from module.preprocess.selectReportFigure import makeCorrectFigure

from module.preprocess.splitVideo import splitVideo
from module.preprocess.reomoveSimilarSlide import createCorrectSlides
from module.preprocess.deriveSlideText import deriveSentense
from module.preprocess.deriveSlideFigure import deriveSlideFigure

from module.preprocess.findSimilarFigure import findSimilarFigures
from module.preprocess.arangeAudio import arangeAudio
from module.preprocess.sentenceVector import catchContent
from module.preprocess.calculateSimilarity import calculateSimilarity

from module.preprocess.clustering import clustering
from module.preprocess.createWordCloud import createWordCloud
from module.preprocess.highlightCluster import highlightCluster

import os
import shutil
import glob


#論文に対する前処理
def reportProcess(file_name):
    paper_path = f'dist/static/static/{file_name}/{file_name}.pdf'
    #論文からテキストの抽出
    deriveReport(paper_path)
    #論文から図表の抽出
    deriveFigure(paper_path)
    coodinate_path = f'dist/static/static/{file_name}/report_content/content/path_coordinate.pickle'
    content_path = f'dist/static/static/{file_name}/report_content/content.pickle'
    deriveArea(coodinate_path, content_path)

    #論文内の図表の作成
    subfigure_folder_path = f'dist/static/static/{file_name}/report_content/not_paragraph'
    subfigure_coodinate_path = f'dist/static/static/{file_name}/report_content/not_paragraph/coordinate.pickle'
    makeCorrectFigure(subfigure_folder_path, subfigure_coodinate_path)

#動画に関する前処理
def videoProcess(file_name):
    video_path = f'dist/static/static/{file_name}/{file_name}.mp4'
    second = 10
    #動画をsecond秒ごとに分割
    splitVideo(video_path, second)
    frame_path = f'dist/static/static/{file_name}/video_content/{file_name}'
    #類似したフレームの削除
    createCorrectSlides(frame_path)
    slide_path = f'dist/static/static/{file_name}/video_content/correct_slides'
    #スライドから文字を抽出
    deriveSentense(slide_path)
    #スライドから図表を抽出
    deriveSlideFigure(slide_path)

#対応関係の抽出
def relationship(file_name):
    slide_path = f'dist/static/static/{file_name}/video_content/correct_slides'
    #論文とスライド内で類似した画像がないか探す関数
    findSimilarFigures(file_name)
    #スライドと文字起こしの対応関係の整理
    audio_path = f'dist/static/static/{file_name}/video_content/audio-transcribe.json'
    arangeAudio(audio_path, slide_path)

    #音声と論文の段落をベクトル化
    catchContent(file_name)

    report_path = f'dist/static/static/{file_name}/report_content/content.pickle'
    audio_pickle_path = f'dist/static/static/{file_name}/video_content/slide_audio.pickle'
    vector_path = f'dist/static/static/{file_name}/vector.pickle'
    #文字起こしと論文の段落の類似度を計算
    calculateSimilarity(vector_path, report_path, audio_pickle_path)

#クラスタリングの関数
def clusterProcess(file_name):
    #クラスタリングを行う関数
    clustering(file_name)

    #クラスターに関するWOrdCLoudを作る関数
    createWordCloud(file_name)

    #クラスターのハイライトを行う関数
    highlightCluster(file_name)

#不要なファイルの削除
def deleteFile(file_name):
    #ビデオの削除
    video_path = f'dist/static/static/{file_name}/{file_name}.mp4'
    os.remove(video_path)

    #論文の文字起こしの削除
    txt = glob.glob(f'dist/static/static/{file_name}/report_content/*.txt')
    for t in txt:os.remove(t)

    #論文の部分領域の削除
    path_list = glob.glob(f'dist/static/static/{file_name}/report_content/content/*-*.jpg')
    for path in path_list: os.remove(path)

    #論文のサブ領域の削除
    path_list = glob.glob(f'dist/static/static/{file_name}/report_content/not_paragraph/*.jpg')
    for path in path_list: os.remove(path)

    path_list = glob.glob(f'dist/static/static/{file_name}/report_content/content/paragraph/*-*.jpg')
    for path in path_list: os.remove(path)

    #フレームの削除
    shutil.rmtree(f'dist/static/static/{file_name}/video_content/{file_name}')
    #スライド内の画像の削除
    shutil.rmtree(f'dist/static/static/{file_name}/video_content/correct_slides_figure')

#前処理のメイン関数
def preprocessing(file_name):
    #ファイルの移動
    # createFolder(file_name)

    reportProcess(file_name)

    videoProcess(file_name)

    relationship(file_name)

    clusterProcess(file_name)

    deleteFile(file_name)

    