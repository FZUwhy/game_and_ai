import json
import requests
import base64

#使用get函数调用api接口获取数据
def get(url_):
    response = requests.get(url_)
    response_dict = response.json()
    head_img = response_dict['img']
    head_step = response_dict['step']
    head_swap = response_dict['swap']
    head_uuid = response_dict['uuid']
    head = base64.b64decode(head_img)#
    f=open("question/picture_q.png",'wb')#将图片保存在本地
    f.write(head)
    f.close()
    return head_step,head_swap,head_uuid


def post(url_, head_uuid, operations, head_swap):
    data = {"uuid":head_uuid,
            "answer":{
                "operations":operations,
                "swap":head_swap
            }}
    res = requests.post(url=url_, json=data)


if __name__ == "__main__":
    #url_ = "http://47.102.118.1:8089/api/problem?stuid=031802230"
    #get(url_)
    url_ = "http://47.102.118.1:8089/api/answer"
    post(url_)
