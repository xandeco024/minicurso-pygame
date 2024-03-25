def drawTriangle(size):
    '''if size % 2 == 0:
        for i in range(size):
            if i == size / 2 - 1 or i == size / 2 + 1:
                print("*", end="")
            else:
                print(" ", end="")

    else:
        for i in range(size):
            print("*") '''
    
    for x in range(size):
        for y in range(size):
            print("*", end="")
        print()


drawTriangle(10)