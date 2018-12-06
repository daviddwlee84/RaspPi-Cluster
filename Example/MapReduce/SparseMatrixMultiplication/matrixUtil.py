import numpy as np

def toSparseMat(mat):
    mat = np.mat(mat)
    rows, cols = mat.shape
    sparseMat = []
    for row in range(rows):
        for col in range(cols):
            val = mat[row, col]
            if val != 0:
                sparseMat.append([row, col, val])
    return sparseMat, mat.shape
            
def toMatrix(sparseMat, shape=None):
    if not shape:
        shape = (sparseMat[-1][0]+1, sparseMat[-1][1]+1)
    print(shape)
    
    matrix = np.zeros(shape)
    for item in sparseMat:
        row, col, val = item
        matrix[row, col] = val
    matrix = list(matrix)
    return list(map(lambda x: list(x), matrix))

def main():
    from pprint import pprint
    matA = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10, 11, 12]
    ]

    matB = [
        [10, 15],
        [0, 2],
        [11, 9]
    ]


    print('Original')
    pprint(matA)
    pprint(matB)

    print('\ntoSparseMat')
    pprint(toSparseMat(matA)[0])
    pprint(toSparseMat(matB)[0])

    print('\ntoMatrix')
    pprint(toMatrix(toSparseMat(matA)[0]))
    pprint(toMatrix(toSparseMat(matB)[0]))


if __name__ == "__main__":
    main()