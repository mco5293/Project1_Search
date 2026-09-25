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

class Node:
    def __init__(self, state, parent, cost):
        self.state = state
        self.parent = parent
        self.cost = cost

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
    else:
        lowest = 0
        for i in range(len(queue)):
            if queue[i].cost < queue[lowest].cost:
                lowest = i
        node = queue[lowest]
        del queue[lowest]
        return node

#expand the node, adding expansions to the queue
def expand_node(queue, node):
    #checks if state is valid before attempting to expand
    if(is_valid(state)):
        #extract each piece of the state array
        for i in state:
            m_left = state[0]
            c_left = state[1]
            m_right = state[2]
            c_right = state[3]
            boat = state[4]

if __name__=='__main__':
    queue = []
    start_state = read_input
    start_node = Node(state = start_state, parent = None, cost = 0)

    ucs_costA(queue, start_node)
    ucs_costB(queue, start_node)