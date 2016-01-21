from __future__ import division
import random
from math import log

def make_dict_list(header,rows):
	res = list()
	for row in rows:
		d = dict()
		for i, attr in enumerate(header):
			d[attr] = row[i]
		res.append(d)
	return res

def get_conditional_entropy(e_root, e_children, total):
	pass

def get_entropy(t):
	entropy = 0
	s = sum(t)
	for i in t:
		print(i)
		if i != 0:
			entropy += (i/s)*log((i/s),2)
	return -1*entropy

fd = open('./data/phones.csv','r')
data = [row.split(',') for row in fd.read().split('\n')]
header, data = data[0],data[1:]
fd.close()

N = {}
data = make_dict_list(header, data)

#keeps track of the discrete values each attribute can take
unique_attr = {'Memory':3,'Size':3,'Camera':3,'Cores':3,'Brand':5,'Price':3}

#discretize attributes
for row in data:
	if float(row['Memory']) <=8: row['Memory'] = 1
	elif float(row['Memory']) <=16: row['Memory'] = 2
	else: row['Memory'] = 3

	if float(row['Size']) < 5: row['Size'] = 1
	elif float(row['Size']) < 5.3: row['Size'] = 2
	else: row['Size'] = 3

	if float(row['Camera']) <=8: row['Camera'] = 1
	elif float(row['Camera']) <=13: row['Camera'] = 2
	else: row['Camera'] = 3

	if float(row['Cores']) == 2: row['Cores'] = 1
	elif float(row['Cores']) == 4: row['Cores'] = 2
	elif float(row['Cores']) == 8: row['Cores'] = 3

	if row['Brand'] == 'Apple': row['Brand'] = 1
	elif row['Brand'] == 'Samsung': row['Brand'] = 2
	elif row['Brand'] == 'Micromax': row['Brand'] = 3
	elif row['Brand'] == 'Motorola': row['Brand'] = 4
	elif row['Brand'] == 'Google': row['Brand'] = 5

	if float(row['Price']) < 20000: row['Price'] = 1
	elif float(row['Price']) < 40000: row['Price'] = 2
	else: row['Price'] = 3

	row['SNo'] = int(row['SNo'])
	del row['SNo']
	del row['Product']

def get_distribution(header, data):
	res = {}
	for attr in unique_attr.keys():
		print(attr)
		res[attr] = {}
		for i in range(unique_attr[attr]):
			res[attr][i+1] = [0]*unique_attr[attr]
		for row in data:
			print(res[attr])
			print(res[attr][row[attr]])
			res[attr][row[attr]][row['Price']-1] += 1
	return res

print(data)
# for i in ((3,0,0),(1,4,),())
# print(get_entropy((1,4,0)))
print(get_distribution(header,data))