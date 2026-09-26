import math
def read_input():
    with open('input.txt',"r") as file: #open and read all of input.txt
        input_state = file.read()
        
    if not input_state: #make sure it actually got the input and the file actually contains a start state 
        return "Input start state is empty" #input was empty

    else: 
        input_state=input_state.strip()
        start_state = input_state.split(",") #make start state into an array seperated by the commas
        for i in range(4): #make the # of missionaries and cannibals an int
            start_state[i] = int(start_state[i])
    return start_state

#checks to make sure the state follows all of the rules
#not negative or greater than 3
#more cannibals than missionaries on one side
def is_valid(state):
    #extract each piece of the state array
    for i in state:
        m_left = state[0]
        c_left = state[1]
        m_right = state[2]
        c_right = state[3]
        boat = state[4]

    #checks for negative values or greater than 3
    if(m_left < 0 or c_left < 0 or m_right < 0 or c_right < 0 or m_left > 3 or c_left > 3 or m_right > 3 or c_right > 3):
        return False

    #checks for more cannibals than missionaries if m is not 0
    if(c_left > m_left and m_left != 0): #LEFT
        return False
    elif(c_right > m_right and m_right!= 0): #RIGHT
        return False    
    return True #if it makes it this far, it survived the checks

#creates the Node class for path traceback
class Node:
    def __init__(self, state, parent, cost, heuristic):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

#creates a priority queue to expand nodes based on lowest cost
#inserts nodes to the queue
def add_queue(queue, state):
    queue.append(state)

#removes the node at the top of the queue and returns it
def next_node(queue):
    #if the queue is empty, there is no next node
    if(len(queue) == 0):
        print("Queue empty.")
        return None
    #finds the first node in the queue with the lowest cost
    else:
        lowest = 0
        for i in range(len(queue)):
            if (queue[i].cost + queue[i].heuristic) < (queue[lowest].cost + queue[lowest].heuristic):
                lowest = i
        node = queue[lowest]
        del queue[lowest]
        return node

def get_valid_next_states(node):
    #extract each piece of the state array
    state = node.state
    for i in state:
        m_left = state[0]
        c_left = state[1]
        m_right = state[2]
        c_right = state[3]
        boat = state[4]

    potential_states=[]
    moves=[(0,1), (1,0), (1,1), (2,0), (0,2)] #all valid moves from one side to the other (M,C)

    for move_m, move_c in moves:
        if boat=='L':
            new_state=[m_left - move_m, c_left - move_c, m_right + move_m, c_right + move_c, 'R']
        elif boat=='R':
            new_state=[m_left + move_m, c_left + move_c, m_right - move_m, c_right - move_c, 'L']

        if is_valid(new_state):
            potential_states.append(new_state)
    
    return potential_states

def get_costA(state, new_state):
    #extract each piece of the state arrays
    for i in state:
        m_left = state[0]
        c_left = state[1]
        m_right = state[2]
        c_right = state[3]
        boat = state[4]
    
    for i in new_state:
        m_left_new = new_state[0]
        c_left_new = new_state[1]
        m_right_new = new_state[2]
        c_right_new = new_state[3]
        boat_new = new_state[4]

    #each missionary costs 2, each cannibal costs 1
    if boat == 'L':
        move_m = m_left - m_left_new
        move_c = c_left - c_left_new
    elif boat == 'R':
        move_m = m_right - m_right_new
        move_c = c_right - c_right_new
    return 2 * move_m + move_c

#expand the node, adding expansions to the queue
def expand_node(queue, node, heuristic_type): 
    #creates nodes for all new potential state and adds them to the priority queue
    potential_states = get_valid_next_states(node)
    for new_state in potential_states:
        for i in new_state:
            m_left_new = new_state[0]
            c_left_new = new_state[1]
            m_right_new = new_state[2]
            c_right_new = new_state[3]
            boat_new = new_state[4]
        if heuristic_type == "1":
            new_heuristic = 2 * m_left_new + c_left_new #h_1(s) = 2M_left + 1C_left
        elif heuristic_type == "2":
            new_heuristic = math.ceil((2 * m_left_new + c_left_new)/3) #h_2(s) = |(2M_left + 1C_left)/3|
        elif heuristic_type == "3":
            new_heuristic = 2 * m_left_new + c_left_new
            if boat_new == "R" and (m_left_new + c_left_new) > 0:
                new_heuristic += 1
        new_cost = get_costA(node.state, new_state)
        new_node = Node(state = new_state, parent = node, cost = node.cost + new_cost, heuristic = new_heuristic)
        add_queue(queue, new_node)
            
#traces the path back from the goal state to the start state, then reverses order for printing purposes
def get_path(node):
    path = []
    while node is not None:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path

def print_final_answer(name, path,cost, node_exp):
    print(f"The solution of {name} is:\nSolution Path:")
    for i in range(len(path)):
        if i<len(path)-1:
            print(f"{path[i]} ->")
        else:
            print(path[i])
            
    print(f"Total cost = {cost}\nNumber of node expansions = {node_exp}")

#core function, loops through queue until goal state is reached
def a_star_cost(queue, start_node, heuristic_type):
    add_queue(queue, start_node)
    visited = set()
    while queue:
        node = next_node(queue)

        if tuple(node.state) in visited:
            continue
        
    
        if node.state == [0, 0, 3, 3, 'R']:
            path = get_path(node)
            print_final_answer(f"Q3.1 (Heuristic {heuristic_type})", path, node.cost, len(visited))
            return
        visited.add(tuple(node.state)) #moved here so it doesnt count the goal state as expanded
        expand_node(queue, node, heuristic_type)

    print(f"No solution found with Heuristic {heuristic_type}.")

if __name__ == '__main__':
    queue = []
    start_state = read_input()
    for i in start_state:
        m_left = start_state[0]
        c_left = start_state[1]
        m_right = start_state[2]
        c_right = start_state[3]
        boat = start_state[4]

    start_node1 = Node(state = start_state, parent = None, cost = 0, heuristic = 2 * m_left + c_left) #h_1(s) = 2M_left + 1C_left
    start_node2 = Node(state = start_state, parent = None, cost = 0, heuristic = math.ceil((2 * m_left + c_left)/3)) #h_2(s) = |(2M_left + 1C_left)/3|

    #NEW HEURISTIC h3 - This one takes into account which side the boat is on, thats why the if statement decides how it starts
    start_h3 = 2 * m_left + c_left
    if boat=="R" and (m_left+c_left) > 0:
        start_h3 +=1

    start_node3 = Node(state=start_state, parent=None, cost=0, heuristic=start_h3)
    
    
    a_star_cost(queue, start_node1, "1")
    a_star_cost(queue, start_node2, "2")
    a_star_cost(queue, start_node3, "3")