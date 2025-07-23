import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('gesture_data.csv')
data = data[4:]
df = pd.DataFrame()
col1 = []
col2 = []
col3 = []
col4 = []
c = 1
for i in data:
    print(i)
    """
    if c % 4 == 0:
        col1= col1.append(i)
    if c % 4 == 2:
        col2.append(i)
    if c % 4 == 3:
        col3.append(i)
    if c % 4 == 4:
        col4.append(i)
    c+=1
    """
print(len(data))
print(data)
df = pd.DataFrame({'x1':col1, 'x2':col2, 'x3':col3, 'x4':col4})
#plt.hist(1000* col1)
#plt.show()
