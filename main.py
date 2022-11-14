from copy import deepcopy as dp
from importlib.abc import ResourceLoader
from importlib.resources import path
from math import dist
import pygame 
pygame.init()
plot=pygame.display.set_mode((800,800))
run = True
listpos = []
edge_dict={}
conc_dict = []
dict = {}
cou = 0
gotnumbers = False
drawedge = False
Nodes = 0
main_dict ={}
sel_len = 2
se_sel =False
gotselect =False
sle_node=[]
selected=[]
edges_list = []
edge_num = 1
two_nodes=[]
letter = ''
result = {}
lettercount = 0
state = 'run'
first_start = 0
sum_to_path = 0
path_determiner = []
last_sol=[]
start_coloring=False
concadlist = []

def next_node(result,start,end):
    res={}
    for i,j in result.items():
        if type(j) == int and j != 0:
            res[i] = j 
    if end in res.keys():
        res.pop(end)
    if len(res) == 0:
        return 
    else:
        a = min(res.values())
        b = min(zip(res.values(),res.keys()))[1]
        return (b,a)

def condition(res):
    r={}
    for i, j in res.items():
        if type(j) == int and j != 0 :
            r[i] = j
    b = min(zip(r.values(),r.keys()))[1]
    return b 

def find_path(start,end):
    global result,path_determiner
    last_sol.append(end)
    path_determiner = path_determiner[::-1]
    try:
        for i in range(len(path_determiner)):
            s_val = path_determiner
            first = s_val[i][end]
            if s_val[i+1][end] != first:
                cost = condition(s_val[i+1])
                last_sol.append(cost)
                end = cost
    except IndexError:
        last_sol.append(first_start)
    print(last_sol[::-1])
    return last_sol[::-1]



def mainalg(start,end,state):
    global first_start , result ,sum_to_path ,path_determiner,path_take


    if state == 'run':
        first_start = start
        state = 'stop'
    result[start]= 'v'
    result_copy = dp(result)
    for i in main_dict[start]:
        if result[i] != 'v' and (result[i] > (sum_to_path + main_dict[start][i]) or result[i] == 0):
                result_copy[i] = sum_to_path + main_dict[start][i]
    path_determiner.append(result_copy)
    result = dp(result_copy)
    func_value = next_node(result,start,end)
    if func_value == None:
        path_take = find_path(start,end)
        print(path_take)
    else:
        start = func_value[0]
        sum_to_path = func_value[1]
        mainalg(start,end,state)

def distance(pos):
    minimum = dist(pos,listpos[0][0])
    minimum_pos = listpos[0][0]
    index_num = listpos[0][1]
    for i in listpos:
        near = dist(pos,i[0])
        if minimum>near:
            minimum = near
            minimum_pos = i[0]
            index_num = i[1]
    return (minimum_pos,index_num)

        

font = pygame.font.SysFont("Times New Roman",18)
while run:
    plot.fill((0,0,0))

    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                for i in edge_dict.values():
                    main_dict[i[0]][i[1]] = i[2]
                    main_dict[i[1]][i[0]] = i[2]
                print(main_dict)
                for i in main_dict.keys():
                    result[i] = 0
                start = int(input('enter the starting node'))
                end = int(input('enter the ending node'))
                mainalg(start,end,state)
                start_coloring = True 

        if len(listpos) < int(Nodes):
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                listpos.append((pos,cou))
                cou += 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                drawedge = True 

        if not gotnumbers:
            if event.type == pygame.KEYDOWN:
                Nodes = pygame.key.name(event.key)
                print(Nodes)
                gotnumbers = True
        
        if gotselect and len(selected)==2:
            if event.type == pygame.KEYDOWN:
                lettercount += 1
                letter += pygame.key.name(event.key)
                if event.key == pygame.K_RETURN:
                    sle_node = [i[0] for i in selected] 
                    two_nodes = [i[1] for i in selected]
                    edge_weight = int(letter[:lettercount-1])
                    sle_node.append(edge_weight)
                    edges_list.append(sle_node)
                    two_nodes.append(int(edge_weight))
                    edge_dict[edge_num] = two_nodes
                    newtup = tuple(sle_node)+tuple(two_nodes)
                    concadlist.append(list(newtup))
                    edge_num += 1
                    selected = []
                    lettercount=0
                    letter = ''

        # if drawedge:
        #     if len(selected) <=sel_len:
        #         if event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_BACKSPACE:
        #                 selected.pop(-1)


                

        if drawedge:
            if len(selected) < sel_len:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pose = pygame.mouse.get_pos()
                    near_node = distance(pose)
                    if near_node not in selected:
                        selected.append(near_node)
                        gotselect = True
    if gotselect and len(selected) == 2:
        dispw = font.render('enter the weight of the edge',1,(225,225,225))
        plot.blit(dispw,(20,20))
        
    if not gotnumbers:
        disp = font.render('enter the number of nodes', 1,(225,225,225))
        plot.blit(disp,(20,20))
    

    if not drawedge and gotnumbers:
        if len(listpos) == int(Nodes):
            dispe = font.render('click spacebar to draw the edges', 1,(225,225,225))
            plot.blit(dispe,(20,20))
 
    if gotnumbers:
        for i in listpos:
            pygame.draw.circle(plot,(225,0,0),i[0],5)
            num = font.render(str(i[1]), 1,(225,225,225))
            new_pos = (i[0][0]-2,i[0][1]+5)
            main_dict[i[1]]={}
            plot.blit(num,new_pos)
            
    if gotselect and gotnumbers and drawedge:
                for i in selected:
                    pygame.draw.circle(plot,(224,224,224),i[0],7,1)
    
    for i in edges_list:
        pygame.draw.line(plot,(225,225,0),tuple(i[0]),tuple(i[1]))
        middle = ((i[0][0]+i[1][0])//2+5,(i[0][1]+i[1][1])//2+5)
        edge_weig = font.render(str(i[2]), 1,(0,225,225))
        plot.blit(edge_weig,middle)
    if start_coloring:
        for i in range(len(path_take)-1):
            for j in concadlist:
                if path_take[i] in j[3:5] and path_take[i+1] in j[3:5]:
                    conc_dict.append(j[0:2])
    
    for i in conc_dict:
        pygame.draw.line(plot,(225,225,225),i[0],i[1],2)

    pygame.display.update()




