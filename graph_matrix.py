import numpy as np

class Stack:
    '''
    Klasa reprezentująca stos
    '''
    def __init__(self):
        self.items = []
    def is_empty(self):
        return self.items == []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            pass
    def peek(self):
        if not self.is_empty():
            return self.items[len(self.items)-1]
        else:
            return None
    def size(self):
        return len(self.items)
    def __str__(self):
        if not self.is_empty():
            return str(self.items)
        else:
            return "pusty"

class QueueBaE(object):
  """
  Klasa implementująca kolejkę za pomocą pythonowej listy tak,
  że początek kolejki jest przechowywany na końcu listy.
  """
  
  def __init__(self):
    self.list_of_items = []
    
  def enqueue(self, item):
    self.list_of_items.insert(0, item)
    
  def dequeue(self):
    if not self.is_empty():
      return self.list_of_items.pop()
    else:
      raise IndexError("Nie można usunąć elementu z pustej listy")
  
  def is_empty(self):
    return self.list_of_items == []
    
  def size(self):
    return len(self.list_of_items)



class Graph:
    """
    Klasa reprezentująca graf.
    """
    def __init__(self):
        self.matrix = np.zeros((1,1), dtype = int)
        self.vertices = []
        self.size = 0
        self.edges = []
        self.dfs_stack = Stack()
        self.dfs_list = []
        self.bfs_queue = QueueBaE()
        self.bfs_list = []

    def add_vertex(self, ver_key):
        if ver_key not in self.vertices:
            if self.size == 0:
                self.vertices.append(ver_key)
                self.size += 1
            else:
                self.vertices.append(ver_key)
                self.size += 1
                self.matrix = np.append(self.matrix, np.zeros((self.size - 1, 1), dtype = int), axis = 1)
                self.matrix = np.append(self.matrix, np.zeros((1, self.size), dtype = int), axis = 0)
        else:
            raise ValueError("Vertex already in graph")

    def add_edge(self, start, end, weight = 1):
        if (start in self.vertices and end in self.vertices):
            start_ind = self.vertices.index(start)
            end_ind = self.vertices.index(end)
            self.matrix[start_ind, end_ind] = weight
            self.matrix[end_ind, start_ind] = (-1) * weight
            self.edges.append((start, end, weight))
        elif start in self.vertices:
            self.add_vertex(end)
            self.add_edge(start, end, weight)
        elif end in self.vertices:
            self.add_vertex(start)
            self.add_edge(start, end, weight)
        else:
            self.add_vertex(start)
            self.add_vertex(end)
            self.add_edge(start, end)

    def get_vertices(self):
        return self.vertices
        
    def get_edges(self):
        edges = []
        for i in range (1, self.size):
            for j in range(i):
                if self.matrix[i, j] != 0:
                    if self.matrix[i, j] > 0:
                        edges.append((self.vertices[i], self.vertices[j], self.matrix[i, j]))
                    else:
                        edges.append((self.vertices[j], self.vertices[i], (-1) * self.matrix[i, j]))
        return edges

    def dot_code(self):
        edges_list = self.get_edges()
        dot_str = 'digraph G {'
        for i in edges_list:
            dot_str += '"' + i[0] + '"' + " -> " + '"' + i[1] + '"' + ' '
        dot_str += '}'
        return dot_str

    def dfs(self, start_vert, arr, ver_list):
        arr[arr < 0] = 0
        arr[arr > 0] = 1
        if not np.array_equal(arr[:,:], np.zeros((self.size, self.size), dtype = int)[:,:]):
            if start_vert in self.vertices:
                vert_ind = self.vertices.index(start_vert)
                if not np.array_equal(arr[vert_ind, :], np.zeros((self.size, self.size), dtype = int)[0, :]):
                    self.dfs_stack.push(start_vert)
                    if not start_vert in ver_list:
                        ver_list.append(start_vert)
                    current_row = list(arr[vert_ind, :])
                    next_row = current_row.index(1)
                    arr[vert_ind, next_row] = 0
                    return self.dfs(self.vertices[next_row], arr, ver_list)
                else:
                    if not start_vert in ver_list:
                        ver_list.append(start_vert)
                    if not self.dfs_stack.is_empty():
                        next_vertex = self.dfs_stack.pop()
                        return self.dfs(next_vertex, arr, ver_list)
                    else:
                        return ver_list
            else:
                raise ValueError("No such a vertex in the graph")
        else:
            return ver_list

    def bfs(self, start_vert, arr, ver_list):
        arr[arr < 0] = 0
        arr[arr > 0] = 1
        print(arr)
        if ver_list in self.vertices:
            ver_list.append
            if not np.array_equal(arr[:,:], np.zeros((self.size, self.size), dtype = int)[:,:]):
                vert_ind = self.vertices.index(start_vert)
                current_row = arr[vert_ind, :]
                if not np.array_equal(current_row[:,:], np.zeros((self.size, self.size), dtype = int)[0, :]):
                    current_row = list(current_row)
                    while 1 in current_row:
                        crossing = current_row.index(1)
                        self.bfs_queue.enqueue(self.vertices[crossing])
                        current_row[crossing] = 0
                        arr[vert_ind, crossing] = 0
                    return self.bfs()
                        
        else:
            raise ValueError("No such a vertex in the graph")
            
    def __contains__(self, vert_key):
        return vert_key in self.vertices

    def __repr__(self):
        return self.matrix


    def dfs(self, start_vert, arr, ver_list, root_list, leaves_list):
        arr[arr < 0] = 0
        arr[arr > 0] = 1
        vert_ind = self.vertices.index(start_vert)
        if not start_vert in ver_list:
            if not start_vert in root_list:
                if not start_vert in leaves_list:
                    ver_list.append(start_vert)
        elif (start_vert in ver_list and np.array_equal(arr[:, vert_ind], np.zeros((self.size, self.size), dtype = int)[:, vert_ind])):
                ver_list.remove(start_vert)
                ver_list.append(start_vert)
        if not np.array_equal(arr[:,:], np.zeros((self.size, self.size), dtype = int)[:,:]):
            if start_vert in self.vertices:
                if not np.array_equal(arr[vert_ind, :], np.zeros((self.size, self.size), dtype = int)[0, :]):
                    self.dfs_stack.push(start_vert)
                    current_row = list(arr[vert_ind, :])
                    next_row = current_row.index(1)
                    arr[vert_ind, next_row] = 0
                    return self.dfs(self.vertices[next_row], arr, ver_list, root_list, leaves_list)
                else:
                    if not start_vert in ver_list:
                        if not start_vert in root_list:
                            if not start_vert in leaves_list:
                                ver_list.append(start_vert)
                    if not self.dfs_stack.is_empty():
                        next_vertex = self.dfs_stack.pop()
                        return self.dfs(next_vertex, arr, ver_list, root_list, leaves_list)
                    else:
                        return ver_list
            else:
                raise ValueError("No such a vertex in the graph")
        else:
            return ver_list

    def dfs_searching(self, start_vert, arr, ver_list, some_list, other_list):
        root_ver_list = self.get_roots(arr, some_list)
        leaves_ver_list = self.get_leaves(arr, other_list)
        final = []
        if len(root_ver_list) == 1:
            return root_ver_list + self.dfs(start_vert, arr, ver_list, root_ver_list, leaves_ver_list) + leaves_ver_list
        final = []
        for i in root_ver_list:
            final += self.dfs(i, arr, ver_list, root_ver_list, leaves_ver_list)
        for j in range(1, len(final) - 1):
            if final[j-1] == final[j]:
                del final[j-1]
        return root_ver_list + final + leaves_ver_list

    def dfs(self, start_vert, arr, ver_list):
        arr[arr < 0] = 0
        arr[arr > 0] = 1
        try:
            vert_ind = self.vertices.index(start_vert)
        except:
            raise ValueError("No such a vertex in a graph")
        if not start_vert in ver_list:
            if np.array_equal(arr[:, vert_ind], np.zeros((self.size, self.size), dtype = int)[:, 0]):
                ver_list.append(start_vert)
        if not np.array_equal(arr[vert_ind, :], np.zeros((self.size, self.size), dtype = int)[0, :]):
            self.dfs_stack.push(start_vert)
            current_row = list(arr[vert_ind, :])
            next_row = current_row.index(1)
            arr[vert_ind, next_row] = 0
            return self.dfs(self.vertices[next_row], arr, ver_list)
        else:
            if not self.dfs_stack.is_empty():
                next_vertex = self.dfs_stack.pop()
                return self.dfs(next_vertex, arr, ver_list)
            else:
                if not np.array_equal(arr[:, :], np.zeros((self.size, self.size), dtype = int)[:, :]):
                    for i in range(0, self.size):
                        if np.array_equal(arr[:, i], np.zeros((self.size, self.size), dtype = int)[:, 0]):
                            next_vert = self.vertices[i]
                            if next_vert not in ver_list:
                                return self.dfs(next_vert, arr, ver_list)
                else:
                    return ver_list


######## działające bfs sprzed modyfikacji związanej z najkrótszą ścieżką
    def old_bfs(self, start_vert, arr, ver_list):
        arr[arr < 0] = 0
        arr[arr > 0] = 1
        vert_ind = self.vertices.index(start_vert)
        if start_vert in self.vertices:
            if not start_vert in ver_list:
                ver_list.append(start_vert)
            elif (start_vert in ver_list and np.array_equal(arr[vert_ind, :], np.zeros((self.size, self.size), dtype = int)[0, :])):
                ver_list.remove(start_vert)
                ver_list.append(start_vert)
            if not np.array_equal(arr[vert_ind, :], np.zeros((self.size, self.size), dtype = int)[0, :]):
                current_row = list(arr[vert_ind, :])
                while 1 in current_row:
                    ind = current_row.index(1)
                    self.bfs_queue.enqueue(self.vertices[ind])
                    arr[vert_ind, ind] = 0
                    current_row[ind] = 0
                next_vert = self.bfs_queue.dequeue()
                return self.old_bfs(next_vert, arr, ver_list)
            else:
                if not self.bfs_queue.is_empty():
                    next_vertex = self.bfs_queue.dequeue()
                    return self.old_bfs(next_vertex, arr, ver_list)
                else:
                    return ver_list
        else:
            raise ValueError("No such a vertex in the graph")
