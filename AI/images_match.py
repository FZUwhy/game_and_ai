#coding:utf8
import os
from PIL import Image,ImageDraw,ImageFile,ImageChops
import numpy as np
#import pytesseract
import cv2
import imagehash
import collections
import cut

def compare(picture_o , picture_q):
    """比较题目图片和原图"""
    false_cnt = 0
    image_index_q = 0
    image_sequence =  [ [] * 3 for i in range(3)]#用于储存图片序列的列表
    #原图切割并获取切割后的路径
    image_file_list1 = cut.get_image_cut(picture_o, "images_cut_o")
    #题目切割并获取切割后的路径
    image_file_list2 = cut.get_image_cut(picture_q, "images_cut_q")
    #循环9X9次比对这些图片，匹配成功则给其标上匹配到的原图中1-9的相应编号，未匹配到的设为0(即为0的编号超过1，就判定为比对失败，就重新找剩余图片进行比对)
    for image_file2 in image_file_list2:
        is_false = True#匹配失败标志
        image_index_q += 1
        image_index = 0#表示原图切块的索引
        for image_file1 in image_file_list1:
            image_index += 1
            #调用compare_image_with_hash逐块比对
            if compare_image_with_hash("images_cut_o/" + image_file1, "images_cut_q/" + image_file2):
                image_sequence[(image_index_q-1)//3].append(image_index)
                if image_index_q == 9:
                    #print(image_sequence)
                    return True,image_sequence
                is_false = False
                break#说明题目中的这小块匹配中了，继续匹配题目中的下一块
        
        if is_false:#若是这小块没有匹配成功
            image_sequence[(image_index_q-1)//3].append(0)
            #记下缺失的数字
            false_cnt += 1
            if false_cnt > 1:
                return False,image_sequence#考虑到空白块是必定匹配失败的，所以至少有两小块匹配失败，才结束匹配
        if image_index_q == 9:
            #print(image_sequence)
            return True,image_sequence


def compare_image_with_hash(image_file1, image_file2, max_dif=0):
        """
        max_dif: 允许最大hash差值, 越小越精确,最小为0
        """
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        hash_1 = None
        hash_2 = None
        with open(image_file1, 'rb') as fp:
            hash_1 = imagehash.phash(Image.open(fp))
            #print(hash_1)
        with open(image_file2, 'rb') as fp:
            hash_2 = imagehash.phash(Image.open(fp))
            #print(hash_2)
        dif = hash_1 - hash_2
        #print(dif)
        if dif < 0:
            dif = -dif
        if dif <= max_dif:
            return True
        else:
            return False
