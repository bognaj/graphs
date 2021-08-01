# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 20:18:49 2019

@author: Bogna Jaszczak
"""

from graph_matrix import Graph as gr

def is_valid(mis_num, can_num):
    '''
    Funkcja sprawdzająca, czy dany stan spełnia założenia zadania
    i może być dodany do grafu. 
    '''
    if (mis_num < 4 and mis_num >= 0):
        if (can_num < 4 and can_num >= 0):
            if (mis_num, can_num) not in [(1,2), (1,3), (2,0), (2,1)]:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def states(graph, key):
    '''
    Funkcja sprawdzająca wszystkie możliwe działania. 
    Jeżeli stan spełnia założenia zadania, zostaje dodany do grafu. 
    Stan ma postać krotki reprezentującej stan początkowego brzegu:
    (misjonarze, kanibale, gdzie jest łódka, krok)
    '''
    added = []
    if key[2] == 1:
        if is_valid(key[0] - 1, key[1]):
            new_key = (key[0] - 1, key[1], 0, key[3] + 1)
            graph.add_edge(key, new_key)
            added.append(new_key)
        if is_valid(key[0] - 2, key[1]):
            new_key = (key[0] - 2, key[1], 0, key[3] + 1)
            graph.add_edge(key, new_key)
            added.append(new_key)
        if is_valid(key[0], key[1] - 1):
            new_key = (key[0], key[1] - 1, 0, key[3] + 1)
            graph.add_edge(key, new_key)
            added.append(new_key)
        if is_valid(key[0], key[1] - 2):
            new_key = (key[0], key[1] - 2, 0, key[3] + 1 )
            graph.add_edge(key, new_key)
            added.append(new_key)
        if is_valid(key[0] - 1, key[1] - 1):
            new_key = (key[0] - 1, key[1] - 1, 0, key[3] + 1)
            graph.add_edge(key, new_key)
            added.append(new_key)
    elif key[2] == 0:
        if is_valid(key[0] + 1, key[1]):
            new_key = (key[0] + 1, key[1], 1, key[3] + 1)
            graph.add_edge(key, new_key)
            added.append(new_key)
        if is_valid(key[0] + 2, key[1]):
            new_key = (key[0] + 2, key[1], 1, key[3] + 1)
            graph.add_edge(key, new_key)
            added.append(new_key)
        if is_valid(key[0], key[1] + 1):
            new_key = (key[0], key[1] + 1, 1, key[3] + 1)
            graph.add_edge(key, new_key)
            added.append(new_key)
        if is_valid(key[0], key[1] + 2):
            new_key = (key[0], key[1] + 2, 1, key[3] + 1)
            graph.add_edge(key, new_key)
            added.append(new_key)
        if is_valid(key[0] + 1, key[1] + 1):
            new_key = (key[0] + 1, key[1] + 1, 1, key[3] + 1)
            graph.add_edge(key, new_key)
            added.append(new_key)
    return added

def solved(states_list):
    '''
    Funkcja sprawdza, czy zostało już znalezione rozwiązanie. 
    '''
    solved = False
    finish = None
    for i in states_list:
        if i[0] == 0:
            if i[1] == 0:
                if i[2] == 0:
                    solved = True
                    finish = i
    return (solved, finish)
           
def solution(graph):
    '''
    Funkcja rozwiązująca problem. Zwraca reprezentację grafu 
    do wklejenia w webgraphviz oraz stan wierzchołka z rozwiązaniem. 
    '''
    current_verts = [(3,3,1,0)]
    future_verts = []
    while not solved(current_verts)[0]:
        for i in current_verts:
            future_verts.extend(states(graph, i))
        future_verts = list(dict.fromkeys(future_verts))
        current_verts, future_verts = future_verts, []
    return graph.dot_code(), solved(current_verts)[1]

def find_1(graph, column_ind):
    '''
    Funkcja wyszukująca wartosci 1 w zadanej kolumnie.
    W praktyce oznacza to znajdowanie "rodzica" wierzchołka, 
    któremu odpowiada kolumna. 
    '''
    column = list(graph.matrix[:, column_ind])
    row = column.index(1)
    return row
    
def recreate_path(graph, start, end):
    '''
    Funkcja odczytująca z grafu drogę od stanu początkowego 
    do rozwiązania. 
    '''
    path = []
    current = end
    while current != start:
        path.append(current)
        ind = graph.get_vert(current)
        current = graph.vertices[find_1(graph, ind)]
    path.append(start)
    return list(reversed(path))

def draw(path_list):
    '''
    Funkcja przestawiająca rozwiązanie w postaci "graficznej".
    '''
    for i in range(len(path_list) - 1):
        situation = path_list[i]
        x_part = situation[0]
        x_spaces = 3 - x_part
        o_part = situation[1]
        o_spaces = 3 - o_part
        boat_side = situation[2]
        step = situation[3]
        mis_diff = path_list[i][0] - path_list[i+1][0]
        can_diff = path_list[i][1] - path_list[i+1][1]
        if mis_diff in [-2, 2]:
            boat = r'\xx/'
        elif can_diff in [-2, 2]:
            boat = r'\oo/'
        elif (mis_diff in [-1,1] and can_diff in [-1, 1]):
            boat = r'\xo/'
        elif mis_diff in [-1, 1]:
            boat = r'\x /'
        elif can_diff in [-1, 1]:
            boat = r'\ o/'
        if boat_side == 0:
            print(str(step) + '.' + '______________')
            print(x_part * 'x' + x_spaces * ' ' + '|    \__/|' + x_spaces * 'x' + x_part * ' ')
            print(o_part * 'o' + o_spaces * ' ' + '|        |' + o_spaces * 'o' + o_part * ' ')
            print('________________')
            print(str(step) + '-->' + str(step +1))
            print('<--' + boat)
            print('________________')
        else:
            print(str(step) + '.' + '______________')
            print(x_part * 'x' + x_spaces * ' ' + '|\__/    |' + x_spaces * 'x' + x_part * ' ')
            print(o_part * 'o' + o_spaces * ' ' + '|        |' + o_spaces * 'o' + o_part * ' ')
            print('________________')
            print(str(step) + '-->' + str(step +1))
            print(boat + '-->')
            print('________________')
    i = path_list[-1]
    x_part = i[0]
    x_spaces = 3 - x_part
    o_part = i[1]
    o_spaces = 3 - o_part
    boat_side = i[2]
    step = i[3]
    if boat_side == 0:
        print(str(step) + '.' + '______________')
        print(x_part * 'x' + x_spaces * ' ' + '|    \__/|' + x_spaces * 'x' + x_part * ' ')
        print(o_part * 'o' + o_spaces * ' ' + '|        |' + o_spaces * 'o' + o_part * ' ')
        print('________________')

    else:
        print(str(step) + '.' + '______________')
        print(x_part * 'x' + x_spaces * ' ' + '|\__/    |' + x_spaces * 'x' + x_part * ' ')
        print(o_part * 'o' + o_spaces * ' ' + '|        |' + o_spaces * 'o' + o_part * ' ')
        print('________________')

        
if __name__ == "__main__":
    # rozwiązanie 
    my_graph = gr()
    dot_code, end_point = solution(my_graph)
    draw(recreate_path(my_graph, (3,3,1,0), end_point))


