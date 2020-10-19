from PIL import Image, ImageDraw
import sys
import os
import random

os.chdir(sys.path[0])

def cut_image(image):
    """切割图片"""
    width, height = image.size
    item_width = int(width / 3)  #因为朋友圈一行放3张图。
    box_list = []
    # (left, upper, right, lower)
    for i in range(0,3):
        for j in range(0,3):
            box = (j*item_width,i*item_width,(j+1)*item_width,(i+1)*item_width)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list

def save_images(image_list):
    """保存图片"""
    index = 1
    for image in image_list:
        drawLine(image, 1, 1)
        image.save("images_cut/{}.png".format(index))
        index += 1

def get_image_list(file_path):
    """完成切割并保存切割好的图片"""
    image = Image.open(file_path)
    image_list = cut_image(image)#获得了图像列表
    #将分割好的图片顺序打乱
    save_images(image_list)

def drawLine(im, width, height):
    '''
    在图片上绘制矩形图
    :param im: 图片
    :param width: 矩形宽占比
    :param height: 矩形高占比
    :return:
    '''
    draw = ImageDraw.Draw(im)
    image_width = im.size[0]
    image_height = im.size[1]
    line_width = im.size[0] * width
    line_height = im.size[1] * height
    draw.line(
        ((image_width - line_width) / 2, (image_height - line_height) / 2,
         (image_width + line_width) / 2, (image_height - line_height) / 2),
        fill=(255, 255, 255))
    draw.line(
        ((image_width - line_width) / 2, (image_height - line_height) / 2,
         (image_width - line_width) / 2, (image_height + line_height) / 2),
        fill=(255, 255, 255))
    draw.line(
        ((image_width + line_width) / 2, (image_height - line_height) / 2,
         (image_width + line_width) / 2, (image_height + line_height) / 2),
        fill=(255, 255, 255))
    draw.line(
        ((image_width - line_width) / 2, (image_height + line_height) / 2,
         (image_width + line_width) / 2, (image_height + line_height) / 2),
        fill=(255, 255, 255))
    del draw