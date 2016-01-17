# accuracy obtained = 53%

import random
import matplotlib.pyplot as plt

fd = open('./data/cricket.csv')
data = [row.split(',') for row in fd.read().split('\n')]
data.pop()
header,data = data[0],data[1:]
fd.close()

selected_points = []
rejected_points = []
W = [random.random(),random.random(),random.random()]
miss = 0
N = 30

#cleaning data
for row in data:
    row[1] = 0 if row[1]=='-1' else float(row[1])
    row[2] = 0 if row[2]=='-1' else float(row[2])
    if row[3] == 'Yes':
        row[3] = 1
        selected_points.append([row[1],row[2]])
    else:
        row[3] = 0
        rejected_points.append([row[1],row[2]])

data_points =[x[1:3] for x in data]

def sign(a):
    return 0 if a<0 else 1

#training phase
def train():
    global W
    for i in range(N):
        x = [1]+list(data[i][1:3])
        y = data[i][3]
        if sign(W[0]*x[0] + W[1]*x[1] + W[2]*x[2]) != y:
            x2 = map(lambda t: (t*y), x)
            W = [sum(t) for t in zip(W,x2)]

def test():
    global miss
    for i in range(N):
        x = [1]+list(data[i][1:3])
        y = data[i][3]
        if sign(W[0]*x[0] + W[1]*x[1] + W[2]*x[2]) != y: miss+=1

train()
m = -W[1]/W[2]
c = -W[0]/W[2]
x1 = (80, m*10+c)
x2 = (0, m*-10+c)

test()
accuracy = (N-miss)*100/N
print('accuracy: ',accuracy,'%')

selected_points = zip(*selected_points)
rejected_points = zip(*rejected_points)
plt.plot([x1[0],x2[0]],[x1[1],x2[1]])
plt.plot(selected_points[0], selected_points[1], linestyle=' ', marker='o', color='g')
plt.plot(rejected_points[0], rejected_points[1], linestyle=' ', marker='o', color='r')
plt.show()


