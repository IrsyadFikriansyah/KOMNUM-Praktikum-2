import numpy as np
import math 

# tested function
def f(x):
    return math.sin(x)

# function for getting Numerical Integration with Composite Trapezoidal Rule (CTR)
def CTR(points: np.ndarray) -> float:
    h = points[1] - points[0]
    if(points.size < 2): 
        return -1
    else:
        temp = 0
        for i in range(1, points.size - 1):
            temp += f(points[i])
        return h / 2 * (f(points[0]) + 2 * temp + f(points[points.size - 1]))

# function for getting Numerical Integration with romberg
# a and b are boundaries
def romberg(a, b, iter):
    # matrix for store the romberg value
    matrix = [] 
    # making empty 4 by 4 matrix
    for _ in range(0, iter): 
        matrix.append([None for _ in range(0, iter)])
    
    section = 1 # the number of section for CTR
    iteration = 0 # iteration of the while loop
    while (section < 2**iter):
        points = np.linspace(a, b, section + 1) # getting the evenly spread points
        matrix[iteration][0] = CTR(points) 

        # increment the section by times 2 and iteration by 1
        section *= 2
        iteration += 1

    # calculating Romberg Integration 
    for i in range(1, iter):
        for j in range(1, iter):
            if (i < j):
                continue

            # Romberg formula
            temp = (4**(j) * matrix[i][j - 1] - matrix[i - 1][j - 1]) / (4**(j) - 1)
            matrix[i][j] = temp

    ## printing the Romberg Integration every iteration (matrix)
    # for i in range(0, iter):
    #     for j in range(0, iter):
    #         if (i < j):
    #             continue
    #         print("{},\t".format(matrix[i][j]), end='')
    #     print()

    return matrix[iter - 1][iter - 1]
    
def main():
    a = 0       # lower boundary
    b = math.pi # upper boundary
    iter = 4    # number of iteration

    result = romberg(a, b, iter)
    print("R({},{}) = {}".format(iter, iter, result))

if __name__ == "__main__":
    main()