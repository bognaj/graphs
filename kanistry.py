from graph_matrix import Graph as gr

def states(graph, key, A_size, B_size, desired):
    '''
    Funkcja sprawdzająca wszystkie możliwe do osiągnięcia stany. 
    '''
    added = []
    if key[0] == 0:
        new_key = (A_size, key[1], key[2] + 1)
        graph.add_edge(key, new_key)
        added.append(new_key)
    if key[1] == 0:
        new_key = (key[0], B_size, key[2] + 1)
        graph.add_edge(key, new_key)
        added.append(new_key)
    if key[0] > 0:
        new_key = (0, key[1], key[2] + 1)
        graph.add_edge(key, new_key)
        added.append(new_key)
    if key[1] > 0:
        new_key = (key[0], 0, key[2] + 1)
        graph.add_edge(key, new_key)
        added.append(new_key)
    if key[0] + key[1] <= A_size:
        new_key = (key[0] + key[1], 0, key[2] + 1)
        graph.add_edge(key, new_key)
        added.append(new_key)
    if key[1] + key[0] <= B_size:
        new_key = (0, key[1] + key[0], key[2] + 1)
        graph.add_edge(key, new_key)
        added.append(new_key)
    if A_size - key[0] < key[1]:
        new_key = (A_size, key[1] - A_size + key[0], key[2] + 1)
        graph.add_edge(key, new_key)
        added.append(new_key)
    if B_size - key[1] < key[0]:
        new_key = (key[0] - B_size + key[1], B_size, key[2] + 1)
        graph.add_edge(key, new_key)
        added.append(new_key)
    return added

def solved(states_list, desired):
    '''
    Funkcja sprawdzająca, czy znaleziono już rozwiązanie. 
    '''
    solved = False
    finish = None
    for i in states_list:
        if (i[0] == 0 and i[1] == desired):
            solved = True
            finish = i
        elif (i[0] == desired and i[1] == 0):
            solved = True
            finish = i
        elif i[0] + i[1] == desired:
            solved = True
            finish = i
    return (solved, finish)

def solution(graph, beginning_point, A_size, B_size, desired):
    '''
    Funkcja rozwiązująca problem. Zwraca reprezentację grafu 
    do wklejenia w webgraphviz oraz stan z rozwiązaniem. 
    '''
    current_verts = [beginning_point]
    future_verts = []
    while not solved(current_verts, desired)[0]:
        for i in current_verts:
            future_verts.extend(states(graph, i, A_size, B_size, desired))
        future_verts = list(dict.fromkeys(future_verts))
        current_verts, future_verts = future_verts, []
    return graph.dot_code(), solved(current_verts, desired)[1]

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

def write(path_list, A_size, B_size, desired):
    '''
    Funkcja opisująca kolejne kroki, które trzeba wykonać. 
    '''
    print("Kanister A ma pojemnosc " + str(A_size) + ' ,a kanister B ma pojemnosc ' + str(B_size))
    print("Kolejne kroki do odmierzenia " + str(desired) + ":")
    for i in range(0, len(path_list) - 1):
        before = path_list[i]
        after = path_list[i + 1]
        if before[0] == after[0]:
            diff = after[1] - before[1]
            if diff == B_size:
                print(str(after[2]) + '.' + " Napełnij kanister B")
            elif diff == (-1) * B_size:
                print(str(after[2]) + '.' + " Opróżnij kanister B")
        elif before[1] == after[1]:
            diff = after[0] - before[0]
            if diff in list(range(0, A_size + 1)):
                print(str(after[2]) + '.' + " Napełnij kanister A")
            else:
                print(str(after[2]) + '.' + " Opróżnij kanister A")
        elif (before[0] > after[0] and before[1] < after[1]):
            diff = before[0] - after[0]
            print(str(after[2]) + '.' + " Przelej " + str(diff) + " l z kanistra A do kanistra B")
        elif (before[0] < after[0] and before[1] > after[1]):
            diff = after[0] - before[0]
            print(str(after[2]) + '.' + " Przelej " + str(diff) + " l z kanistra B do kanistra A")
        
    

if __name__ == "__main__":
    graph = gr()
    # program działa dla różnych wielkosci kanistrow i szukanych objetosci
    A_bucket_size = 4
    B_bucket_size = 3
    desired = 2
    dot_code, end_point = solution(graph, (0,0,0), A_bucket_size, B_bucket_size, desired)
    solution_path = recreate_path(graph, (0,0,0), end_point)
    write(solution_path, A_bucket_size, B_bucket_size, desired)
    
    
        