import images_match as im
import cut
import api
import copy
import api2
import sys
# 输出状态
def PrintState(state):
    for i in state: print(i)


# 复制状态
def CopyState(state):
    s = []
    for i in state:
        s.append(i[:])
    return s


# 获取空格的位置
def GetSpace(state):
    for y in range(len(state)):
        for x in range(len(state[y])):
            if state[y][x] == 0:
                return y, x


# 获取空格上移后的状态，不改变原状态
def MoveUp(state):
    s = CopyState(state)
    y, x = GetSpace(s)
    s[y][x], s[y - 1][x] = s[y - 1][x], s[y][x]
    return s


# 获取空格下移后的状态，不改变原状态
def MoveDown(state):
    s = CopyState(state)
    y, x = GetSpace(s)
    s[y][x], s[y + 1][x] = s[y + 1][x], s[y][x]
    return s


# 获取空格左移后的状态，不改变原状态
def MoveLeft(state):
    s = CopyState(state)
    y, x = GetSpace(s)
    s[y][x], s[y][x - 1] = s[y][x - 1], s[y][x]
    return s


# 获取空格右移后的状态，不改变原状态
def MoveRight(state):
    s = CopyState(state)
    y, x = GetSpace(s)
    s[y][x], s[y][x + 1] = s[y][x + 1], s[y][x]
    return s


# 获取两个状态之间的启发距离
def GetDistance(src, dest):
    dic, d = goal_dic, 0
    for i in range(len(src)):
        for j in range(len(src[i])):
            pos = dic[src[i][j]]
            y, x= pos[0], pos[1]
            d += abs(y - i) + abs(x - j)
    return d


# 获取指定状态下的操作
def GetActions(state):
    acts = []
    y, x = GetSpace(state)
    if x > 0:acts.append(MoveLeft)
    if y > 0:acts.append(MoveUp)
    if x < len(state[0]) - 1:acts.append(MoveRight)
    if y < len(state[0]) - 1: acts.append(MoveDown)
    return acts


# 用于统一操作序列的函数
def Start(state):
    return


# 边缘队列中的节点类
class Node:
    state = None   # 状态
    value = -1     # 启发值
    step = 0       # 初始状态到当前状态的距离（步数）
    action = Start  # 到达此节点所进行的操作
    parent = None,  # 父节点
    # 用状态和步数构造节点对象
    def __init__(self, state, step, action, parent):
        self.state = state
        self.step = step
        self.action = action
        self.parent = parent
        # 计算估计距离 = 当前状态与目标态的启发距离 + 移动当前状态花费的代价(步数)
        self.value = GetDistance(state, goal_state) + step


# 获取拥有最小启发值的元素索引
def GetMinIndex(queue):
    index = 0
    for i in range(len(queue)):
        node = queue[i]
        if node.value < queue[index].value:
            index = i
    return index


# 将状态转换为整数
def toInt(state):
    value = 0
    for i in state:
        for j in i:
            value = value * 10 + j
    return value

def inverse_number(num_list):
    """计算除0外的逆序数"""
    ans = 0
    for i in range(len(num_list)):
        for j in range(i):
            if num_list[i] != 0 and num_list[j] > num_list[i]:
                ans += 1
    return ans

def judge(init):
    """判断是否可解，即两个状态的奇偶性是否一致"""
    init_list = [i for item in init for i in item]
    if inverse_number(init_list) % 2 == 0: 
        return True
    else:
        return False


def forced_xchg(image_sequence, head_swap):
    """强制交换列表中的两个元素"""
    #先转换为列表下标
    head_swap[0] -= 1
    head_swap[1] -= 1
    a = [head_swap[0]//3, head_swap[0] % 3]
    b = [head_swap[1]//3, head_swap[1] % 3]
    #交换二维列表中的a,b位置的值
    image_sequence[a[0]][a[1]], image_sequence[b[0]][b[1]] = image_sequence[b[0]][b[1]], image_sequence[a[0]][a[1]]
    #若可解，直接返回列表；若不可解，寻找最优的交换方式，即曼哈顿距离最短的状态
    if judge(image_sequence):
        return image_sequence, a, b
    else:
        min_cost = 9999
        for i in range(8):
            for j in range(i+1, 9):
                #先获得一份列表的深拷贝
                temp = copy.deepcopy(image_sequence)
                a = [i//3, i % 3]
                b = [j//3, j % 3]
                temp[a[0]][a[1]], temp[b[0]][b[1]] = temp[b[0]][b[1]], temp[a[0]][a[1]]
                #若此状态可解，则计算曼哈顿距离
                if judge(temp):
                    cost = GetDistance(temp, goal_state)
                    if min_cost > cost:
                        min_cost = cost
                        min_a = list(a)
                        min_b = list(b)
        #根据最小代价交换列表下标
        image_sequence[min_a[0]][min_a[1]], image_sequence[min_b[0]][min_b[1]] = image_sequence[min_b[0]][min_b[1]], image_sequence[min_a[0]][min_a[1]]
        #返回交换后的列表和自由交换的列表下标
        return image_sequence,min_a,min_b

    

def AStar(init, goal, head_step):
    """A*算法寻找初始状态到目标状态的路径"""
    # 边缘队列初始已有源状态节点
    queue = [Node(init, 0, Start, None)]
    visit = {}  # 访问过的状态表
    count = 0   # 循环次数
    # 队列没有元素则查找失败
    while queue:
        # 获取拥有最小估计距离的节点索引
        index = GetMinIndex(queue)
        node = queue[index]
        #访问过的结点放在visit列表中
        visit[toInt(node.state)] = True
        #print("搜索的状态为:")
        #print(node.state)
        count += 1
        #找到目标状态，返回此结点
        if node.state == goal:
            return node, count
        del queue[index]
        # 扩展当前节点
        for act in GetActions(node.state):
            # 获取此操作下到达的状态节点并将其加入边缘队列中
            near = Node(act(node.state), node.step + 1, act, node)
            #print(near.step)
            #不在visit表中的结点加入到边缘队列中
            if toInt(near.state) not in visit:
                queue.append(near)
    return None, count


# 将链表倒序，返回链头和链尾
def reverse(node):
    #print("倒转一个结点")
    if node.parent == None:
        return node, node
    head, rear = reverse(node.parent)
    rear.parent, node.parent = node, None
    return head, node


def init_state(blank_num):
    # 目标状态
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    for i in range(3):
        for j in range(3):
            if goal_state[i][j] == blank_num:
                goal_state[i][j] = 0
    # 目标状态 值-位置表
    goal_dic = {
        1:(0,0), 2:(0,1), 3:(0,2),
        4:(1,0), 5:(1,1), 6:(1,2),
        7:(2,0), 8:(2,1), 9:(2,2)
    }
    goal_dic[0]=goal_dic[blank_num]
    del goal_dic[blank_num]
    return goal_state, goal_dic

def random_move(init_list, head_step):
    operations = ""
    step = head_step
    while step > 0:
        y, x = GetSpace(init_list)
        if x > 0:
            init_list = MoveLeft(init_list)
            operations += 'a'
        elif y > 0:
            init_list = MoveUp(init_list)
            operations += 'w'
        elif x < len(init_list[0]) - 1:
            init_list = MoveRight(init_list)
            operations += 'd'
        elif y < len(init_list[0]) - 1:
            init_list = MoveDown(init_list)
            operations += 's'
        step -= 1
    init_list,min_a,min_b = forced_xchg(init_list, head_swap)
    return init_list, min_a, min_b, operations


if __name__ == '__main__':
    url = "http://47.102.118.1:8089/"
    L = url+"/api/challenge/list"  # 获取赛题
    teamid = 66
    R = url+"/api/challenge/record/"  # 获取赛题的解题记录（R+赛题的uuid）
    C = url+"/api/challenge/create"  # 创建赛题
    ST = url+"/api/challenge/start/"  # 挑战赛题（ST+赛题的uuid）
    SU = url+"/api/challenge/submit"  # 提交赛题答案
    RA = url+"/api/rank"  # 排行榜
    T = url+"/api/teamdetail/"  # 获取指定队伍的信息（T+teamid）
    P = url+"/api/team/problem/"  # 获取还未通过的题目（P+teamid）
    token = "9ead8382-50db-4d3d-8a6d-fef755eb1c2a"
    #api2.create_question(C)
    score = api2.get_teamdetail(T+str(66))
    print(score["rank"])
    sys.exit()
    questions = api2.get_problem(P+str(teamid))
    print(questions)
    for i in questions:
        if i["author"] != 66:
            uuid = i["uuid"]
            #api2.create_question()
            
            head_step,head_swap,uuid = api2.post_challenge(ST+uuid, teamid, token)
            #head_step,head_swap,head_uuid = api.get(url_)
            operations = ""
            x,y = head_swap[0],head_swap[1]
            picture_q = "question/picture_q.png"
            picture_o_list = cut.get_images_path("images")
            for picture_o in picture_o_list:
                v,image_sequence = im.compare("images/"+picture_o, picture_q)
                if v:
                    break
            tmp = [i for item in image_sequence for i in item]
            blank_num = 0
            for item in tmp:
                blank_num += 1
                if blank_num not in tmp:
                    break
            goal_state, goal_dic = init_state(blank_num)
            xchged = False
            judge_flag = judge(image_sequence)
            if not judge_flag:
                #nodes = list()
                #notsolve_cnt = -1
                image_sequence, min_a, min_b, operations = random_move(image_sequence, head_step)
                x = min_a[0]*3+min_a[1]+1
                y = min_b[0]*3+min_b[1]+1
                xchged = True
            node, count = AStar(image_sequence, goal_state, head_step)
            
            if node is None:
                print("找不到任何结点，请检查你的输入!!")
            else:
                node, rear = reverse(node)
                count = -1
                while node:
                    # 启发值包括从起点到此节点的距离
                    if node.action.__name__ == 'MoveDown':
                        operations += 's'
                    elif node.action.__name__ == 'MoveUp':
                        operations += 'w'
                    elif node.action.__name__ == 'MoveLeft':
                        operations += 'a'
                    elif node.action.__name__ == 'MoveRight':
                        operations += 'd'
                    #PrintState(node.state)
                    if count + 1 == head_step and not xchged:#强制交换后重新将当前状态通过A*算法寻找到达目标状态的路径
                        xchged = True
                        image_sequence,min_a,min_b = forced_xchg(node.state, head_swap)
                        node, count = AStar(image_sequence, goal_state, head_swap)
                        node, rear = reverse(node)
                        count = -2
                        x = min_a[0]*3+min_a[1]+1
                        y = min_b[0]*3+min_b[1]+1
                    else:
                        node = node.parent
                    count += 1
            #url_ = "http://47.102.118.1:8089/api/answer"
            free_swap = [x,y]
            #api.post(url_, head_uuid, operations, free_swap)
            result = api2.post_submit(SU, uuid, teamid, token, operations, free_swap)
            print(result)