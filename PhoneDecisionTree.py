from __future__ import division
import random, copy, collections
from math import log

#global variables
data = None
header = None
unique_attr = None
Noutcomes = None
tree = {}

def get_raw_data(file_path):
	global data, header
	fd = open(file_path,'r')
	data = [row.split(',') for row in fd.read().split('\n')]
	header, data = data[0],data[1:]
	fd.close()

def make_dict_list(header,rows):
	res = list()
	for row in rows:
		d = dict()
		for i, attr in enumerate(header):
			d[attr] = row[i]
		res.append(d)
	return res

def get_conditional_entropy(h_parent, n_parent, distro):
	for attr in distro:
		cprob = 0
		for cat in distro[attr]:
			cprob += (distro[attr][cat][0]/n_parent)*distro[attr][cat][1]
		distro[attr] = h_parent - cprob
	return distro

#discretize attributes & remove unnecessary cols
def get_clean_attributes(raw_data):
	data = copy.deepcopy(raw_data)
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
	return data

def get_distribution(data, unique_attr):
	res = {}
	for attr in unique_attr.keys():
		res[attr] = {}
		for i in range(unique_attr[attr]):
			res[attr][i+1] = [0]*Noutcomes
		for row in data:
			res[attr][row[attr]][row['Price']-1] += 1
	return res

def choose_attribute(h_parent, n_parent, distro):
	for attr in distro:
		for choice in distro[attr]:
			distro[attr][choice] = (sum(distro[attr][choice]),get_entropy(distro[attr][choice]))
	distro = get_conditional_entropy(h_parent, n_parent, distro)
	attr_entry = collections.OrderedDict(sorted(distro.items(), reverse = True, key = lambda x:x[1])).popitem(0)
	return attr_entry[0]

def get_cat_data(data, attr):
	cat_data = {}
	for i in range(unique_attr[attr]):
		cat_data[i+1] = []
	for row in data:
		cat_data[row[attr]].append(row)
	return cat_data

def get_entropy(distro):
	entropy = 0
	s = sum(distro)
	for i in distro:
		if i != 0:
			entropy += (i/s)*log((i/s),2)
	return -1*entropy

def create_decision_tree(data, attr, unique_attr, target_distro = None):
	tree = {}
	h_node = get_entropy(target_distro)
	n_node = sum(target_distro)
	
	distro = get_distribution(data, unique_attr)
	chozen_attr = choose_attribute(h_node, n_node, copy.deepcopy(distro))

	cat_data = get_cat_data(data,chozen_attr)
	for cdata in cat_data:
		distro = get_distribution(cat_data[cdata], unique_attr)
		if get_entropy(distro[chozen_attr][cdata]) == 0:
			if distro[chozen_attr][cdata][0] != 0:
				tree[cdata] = '1'
			elif distro[chozen_attr][cdata][1] != 0:
				tree[cdata] = '2'
			else: tree[cdata] = '3'
		else:
			dup_unique_attr = copy.deepcopy(unique_attr)
			del dup_unique_attr[chozen_attr]
			tree[cdata] = ( 
				create_decision_tree(
					cat_data[cdata], 
					chozen_attr, 
					dup_unique_attr, 
					target_distro = distro[chozen_attr][cdata]
				)
			)
	return (chozen_attr, tree)

get_raw_data('./data/phones.csv')
unique_attr = {'Memory':3,'Size':3,'Camera':3,'Cores':3,'Brand':5} #keeps track of the discrete values each attribute can take

data = make_dict_list(header, data)
data = get_clean_attributes(data)
Noutcomes = 3

decision_tree = create_decision_tree(data,'Price', copy.deepcopy(unique_attr), target_distro = (4, 4, 3))
print(decision_tree)