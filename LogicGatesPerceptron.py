import random

class LogicGatesPerceptron:
    logic_gates = {
        'AND' : ((0,0,0),(0,1,0),(1,0,0),(1,1,1)),
        'OR'  : ((0,0,0),(0,1,1),(1,0,1),(1,1,1)),
        'NAND': ((0,0,1),(0,1,1),(1,0,1),(1,1,0)),
        'NOR' : ((0,0,1),(0,1,0),(1,0,1),(1,1,0))
    }
    def __init__(self, gate='AND', N=100):
        self.logic_rules = self.logic_gates[gate]
        self.N = N
        self.W = [0,0,0]
        self.train()
        self.test()

    def sign(self, a):
        return 0 if a<0 else 1

    #training phase
    def train(self):
        for i in range(self.N):
            r = random.randint(0,3)

            x = [1]+list(self.logic_rules[r][0:2])
            y = self.logic_rules[r][2]

            if self.sign(self.W[0]*x[0] + self.W[1]*x[1] + self.W[2]*x[2]) != y:
                y2 = -1 if y==0 else 1
                x2 = map(lambda t: (t*y2), x)
                self.W = [sum(t) for t in zip(self.W,x2)]

    #testing phase
    def test(self):
        for i in range(4):
            x = list(self.logic_rules[i][0:2])
            x.insert(0,1)

            y = self.logic_rules[i][2]
            h = self.sign(self.W[0]*x[0] + self.W[1]*x[1] + self.W[2]*x[2])
            print('observed val:',h,'expected val:',y)

if __name__ == '__main__':
    try:
        gate = raw_input('Enter logic gate (AND/OR/NAND/NOR): ').upper()
        if gate not in ['AND','OR','NAND','NOR']: raise Exception
        N = input('Enter # training cases: ')
        classifier = LogicGatesPerceptron(gate, N)
    except Exception as e:
        print('invalid choice')