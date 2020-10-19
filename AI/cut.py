from PIL import Image, ImageDraw
import sys
import os
import random

os.chdir(sys.path[0])

def get_images_path(filepack_name):
    os.getcwd()#获取当前路径
    return os.listdir(filepack_name)#获取文件夹下所有文件名
#先将 input image 填充为正方形

def cut_image(image):
    width, height = image.size
    item_width = int(width / 3)  
    box_list = []
    # (left, upper, right, lower)
    for i in range(0,3):
        for j in range(0,3):
            #print((i*item_width,j*item_width,(i+1)*item_width,(j+1)*item_width))
            box = (j*item_width,i*item_width,(j+1)*item_width,(i+1)*item_width)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list

#保存
def save_images(image_list, save_path):
    index = 1
    for image in image_list:
        image.save(save_path + "/{}.png".format(index))
        index += 1

def get_image_cut(file_path, save_path):
    """获取切割后的文件地址"""
    image = Image.open(file_path)
    #image.show()
    #image_new = fill_image(image)
    image_list = cut_image(image)#获得了图像列表
    #将分割好的图片保存到对应的文件夹内
    save_images(image_list, save_path)
    #返回切割好的原图路径
    return get_images_path(save_path)

    