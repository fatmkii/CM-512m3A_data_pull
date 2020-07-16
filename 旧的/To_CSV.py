import pandas as pd

title = ['L25', 'L45', 'L75', 'a25', 'a45', 'a75', 'b25', 'b45', 'b75']
table = pd.DataFrame([[1, 2, 3, 4, 5, 6, 7, 8, 9]], index=[0], columns=title)
data_add = pd.DataFrame([[3, 4, 3, 4, 5, 6, 7, 8, 9]], index=[2],columns=title)

table = table.append(pd.DataFrame([[3, 4, 3, 4, 5, 6, 7, 8, 9]], index=[2], columns=title))

print(data_add.to_csv())