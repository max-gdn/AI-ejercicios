
START = (3, 0)
FINISH = (3, 11)
ACTION = {
    "N" :(-1, 0),   
    "E" : (0,1), 
    "S" : (1,0), 
    "W" : (0, -1)
}

N_ROW = 4
N_COLUMN = 12
 
def is_cliff(case) : 
    row, column = case
    return row == 3 and 1<=column<=10

def is_out(case) : 
    row, column = case
    return row < 0 or row > 3 or column > 11 or column < 0

def step(case , action) :

    dr, dc = ACTION[action]

    new_state = (case[0] +dr, case[1] + dc)

    if(is_cliff(new_state)): 
        return START, -100, False
    
    if(is_out(new_state)):
        return case, -1, False

    if(new_state == FINISH) : 
        return FINISH, -1, True

    return new_state, -1, False

if __name__=="__main__" : 
    assert step(START, "N") == ((2, 0), -1, False)
    print("Assert: start direction north works")
    assert step(START, "E") == (START, -100, False)
    print("Assert: start direction East works")
    assert step((2, 11), "S") == (FINISH, -1, True)
    print("Assert: (2, 11) direction South works")
 
    # Cas supplémentaires
    assert step(START, "W") == (START, -1, False)      # mur à gauche
    assert step(START, "S") == (START, -1, False)      # mur en bas
    assert step((2, 5), "S") == (START, -100, False)   # chute au milieu
    assert step((2, 0), "S") == (START, -1, False)     # retour sur S, pas une chute
 
    print("All the assert work")


