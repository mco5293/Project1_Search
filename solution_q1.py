#reads input.txt which is the start state
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
    if(m_left<0 or c_left<0 or m_right<0 or c_right<0 or m_left>3 or c_left>3 or m_right >3 or c_right>3):
        return False
    #checks for more cannibals than missionaries if m is not 0
    if(c_left>m_left and m_left != 0): #LEFT
        return False;
    elif(c_right>m_right and m_right!= 0): #RIGHT
        return False;     
    return True; #if it makes it this far, it survived the checks

#finds every possible next state that can happen at the current state
def get_valid_next_states(state):
    #extract each piece of the state array
    for i in state:
        m_left = state[0]
        c_left = state[1]
        m_right = state[2]
        c_right = state[3]
        boat = state[4]

    potential_states=[]
    moves=[(1,0),(0,1),(2,0),(0,2),(1,1)] #all valid moves from one side to the other (M,C)

    for move_m, move_c in moves:
        if boat=='L':
            new_state=[m_left-move_m,c_left-move_c,m_right+move_m,c_right+move_c,'R']
        elif boat=='R':
            new_state=[m_left+move_m,c_left+move_c,m_right-move_m,c_right-move_c,'L']

        if is_valid(new_state):
            potential_states.append(new_state)
    
    return potential_states

def print_final_answer(name, path,cost, node_exp):
    print(f"The solution of {name} is:\nSolution Path:")
    for i in range(len(path)):
        if i<len(path)-1:
            print(f"{path[i]} ->")
        else:
            print(path[i])
            
    print(f"Total cost = {cost}\nNumber of node expansions = {node_exp}")

def bfs(start_state):
    GOAL_STATE = [0,0,3,3,"R"]
    path=[start_state]
    queue = [(start_state, path)] #(current state, path to get to tht state)
    visited = [] #states that have been expanded
    node_exp = 0 #node expansions counter

    while queue:#FIFO
        current_state, path = queue.pop(0)#take current state out of queue
        if current_state in visited:#make sure it isnt a dupe
            continue
        if current_state==GOAL_STATE:#check if we made to the goal state
            cost = len(path)-1
            return path, cost, node_exp

        visited.append(current_state)#not at goal state so add this one to visited and lets expand
        node_exp+=1
        next_states = get_valid_next_states(current_state)#find the next valid states so we can add those to queue

        for state in next_states:#^add them to the queue^
            new_path= path + [state]
            queue.append((state,new_path))

    return None, None, node_exp #path, cost, node_exp NO SOLUTION, so its null/none

def dfs(start_state):
    GOAL_STATE=[0,0,3,3,'R']
    path=[start_state]
    stack = [(start_state, path)] #(current state, path to get to tht state)
    visited = [] #states that have been expanded
    node_exp = 0 #node expansions counter
    while stack:
        current_state,path=stack.pop() #removes the latest item so LIFO
        if current_state in visited:
            continue
        if current_state==GOAL_STATE:
            cost=len(path)-1
            return path,cost,node_exp

        visited.append(current_state)
        node_exp+=1
        next_states= get_valid_next_states(current_state)
        for state in next_states:
            new_path=path+[state]
            stack.append((state,new_path))

    return None,None,node_exp

start_state = read_input()#read the input.txt
dfs_p,dfs_c,dfs_n = dfs(start_state)
print_final_answer("Q1.1.a (DFS)", dfs_p,dfs_c,dfs_n)#print that in the right format
bfs_p, bfs_c, bfs_n = bfs(start_state)#run bfs, output: path, cost, node expansions
print_final_answer("Q1.1.b (BFS)", bfs_p,bfs_c,bfs_n)#print that in the right format
