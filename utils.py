import math

def box_print(seq, title, space=4):
    seq = list(seq)
    width_box = 0
    
    for text in seq:
        if len(text) > width_box:
            width_box = len(text)
            
    bars = width_box + space * 2
    
    print("┏" + bars * "━" + "┓")
    
    pad = (width_box - len(title))/2
    lspace = math.ceil(pad) + space
    rspace = math.floor(pad) + space
        
    print("┃" + " "*lspace + title + " "*rspace + "┃")
    print("┣" + "━"*bars + "┫")
        
    for text in seq:
        rspace = width_box - len(text) - space
        rspace = math.floor(rspace) + 2 * space
        
        print("┃" + space * " " + text + rspace * " " + "┃")
        
    print("┗" + bars * "━" + "┛")

################################################################################

def box_print2D(seq, title, space=2):
    rows = len(seq)
    cols = len(seq[0])
    width_cols = []
    
    for col in range(cols):
        longest = 0
        
        for row in range(rows):
            text = f"{seq[row][col]}"
            
            if len(text) > longest:
                longest = len(text)
                
        width_cols.append(longest)
        
    bars = sum(width_cols) + 2 * space * cols + cols - 1
    pad = (bars - len(title)) / 2
    lpad = math.ceil(pad)
    rpad = math.floor(pad)
    
    print("┏" + bars * "━" + "┓")
    print("┃" + lpad * " " + title + rpad * " " + "┃")
        
    for row in range(rows):
        print("┣", end="")
            
        for col in range(cols):
            bars = width_cols[col] + 2 * space 
            print(bars * "━", end="")
            
            if col == cols - 1: #last column
                print(end="┫")
            
            elif row == 0: #first row
                print(end="┳")
                
            else:
                print(end="╋")
                
        print(end="\n┃")
            
        for col in range(cols):
            text = f"{seq[row][col]}"
            pad = width_cols[col] - len(text)
            rpad = pad  + space
            print(space * " " + text + rpad * " ", end="┃")
            
        print()
    
    print("┗", end="")
            
    for col in range(cols):
        bars = width_cols[col] + 2 * space 
        print(bars * "━", end="")
            
        if col == cols - 1: #last column
            print(end="┛")
            
        else:
            print(end="┻")
            
    print()

    