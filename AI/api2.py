import json
import requests
import base64

# 使用get函数调用api接口获取数据
def get(url_):
    response = requests.get(url=url_)
    resp = json.loads(response.text)  # 从内存中加载字符串，并转换成字典类型
    return resp


# 使用post函数提交答案并返回测试结果
# url_:测试网址  uuid:题目编号  operations:操作序列  swap（列表）:交换的图片
def post(url_, uuid, operations, swap):
    # url = url_
    data = {"uuid":uuid,
            "answer":{
                "operations":operations,
                "swap":swap
            }}
    response = requests.post(url=url_, json=data)
    resp = json.loads(response.text)
    return resp


# 获取赛题，以列表方式展示所有的赛题
def get_question(url_):
    response = requests.get(url=url_)
    resp = json.loads(response.text)
    return resp
    
# 获取还未通过的题目，展示当前队伍还未挑战或通过的题目（不包括自己出的）
def get_problem(url_):
    response = requests.get(url=url_)
    resp = json.loads(response.text)
    return resp

# 获取赛题的解题记录，返回所有解出这题的队伍的纪录（列表）
# 按rank先后来排序，owner为队伍id
def get_record(url_):
    response = requests.get(url=url_)
    resp = json.loads(response.text)
    return resp


# 创建赛题，用token作为权限验证，提供队伍的teamid和赛题数据data。创建成功返回赛题标识符uuid。
# data中letter表示赛题的对应字母、exclude表示当前哪个位置的图片被删去作为空格，challenge为游戏地图，
# step为强制交换的步数（0<=X<=20），swap为强制交换的图片（从左到右从上到下编号1-9）

# { # 示例
#     "teamid": 6,
#     "data": {
#         "letter": "a",
#         "exclude": 5,
#         "challenge": [
#             [1, 2, 3],
#             [0, 4, 6],
#             [7, 8, 9]
#         ],
#         "step": 20,
#         "swap": [1,2]
#     },
#     "token": "xxxx"
# }

def post_create(url_, teamid, letter, exclude, challenge, step, swap, token):
    url = url_
    question = {"teamid": teamid,
                "data": {
                    "letter": letter,
                    "exclude": exclude,
                    "challenge": challenge,
                    "step": step,
                    "swap": swap
                },
                "token": token}
    response = requests.post(url=url_, json=question)
    resp = json.loads(response.text)
    return resp


# 挑战赛题的接口
def post_challenge(url_, teamid, token):
    # url = url_
    data = {"teamid": teamid,
            "token": token
            }
    response = requests.post(url=url_, json=data)
    resp = json.loads(response.text)
    head_img = resp['data']['img']
    head_step = resp['data']['step']
    head_swap = resp['data']['swap']
    head_uuid = resp['uuid']
    head = base64.b64decode(head_img)
    f=open("question/picture_q.png",'wb')#将图片保存在本地
    f.write(head)
    f.close()
    if(resp["success"]):
        print("success")
    
    return head_step,head_swap,head_uuid


# 提交赛题答案的接口
def post_submit(url_, uuid, teamid, token, operations, swap):
    # url = url_
    data = {"uuid": uuid,
            "teamid": teamid,
            "token": token,
            "answer": {
                "operations": operations,
                "swap": swap
            }
            }
    response = requests.post(url=url_, json=data)
    resp = json.loads(response.text)
    return resp


# 从高到低返回排行榜，展示每个队伍的获得的分数score、以及rank总分排名
def get_rank(url_):
    response = requests.get(url=url_)
    resp = json.loads(response.text)
    return resp


# 获取指定队伍的信息，展示当前队伍的分数score、rank总分排名、还有解出的题success列表
def get_teamdetail(url_):
    response = requests.get(url=url_)
    resp = json.loads(response.text)
    return resp


def create_question(C):
    """用于创建题目的函数"""
    
    teamid = 66
    letter = 'g'
    exclude = 1
    challenge = [[2,3,6],[0,5,8],[4,9,7]]
    step = 13
    swap = [2,6]
    token = "9ead8382-50db-4d3d-8a6d-fef755eb1c2a"
    txt = post_create(C, teamid, letter, exclude, challenge, step, swap, token)
    print(txt)

    