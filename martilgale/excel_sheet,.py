excel_sheet = [[0, 1, 2, 3, 4, 4, 3, 2, 1, 1, 0], [1, 0, 1, 3, 4, 4, 4, 3, 2, 1, 0], [2, 1, 0, 2, 3, 4, 5, 4, 3, 2, 0], [3, 3, 2, 0, 2, 4, 5, 6, 5, 3, 1], [4, 4, 3, 2, 0, 2, 5, 7, 7, 5, 2], [4, 4, 4, 4, 2, 0, 3, 7, 9, 8, 4], [3, 4, 5, 5, 5, 3, 0, 5, 9, 11, 8], [2, 3, 4, 6, 7, 7, 5, 0, 8, 15, 15],
               [1, 2, 3, 5, 7, 9, 9, 8, 0, 15, 30], [1, 1, 2, 3, 5, 8, 11, 15, 15, 0, 61], [0, 0, 0, 1, 2, 4, 8, 15, 30, 61, 0]]
for i in range(10):
    for j in range(i+1, 11):
        a = excel_sheet[i][j]
        excel_sheet[i][j] = a+100
print(excel_sheet)