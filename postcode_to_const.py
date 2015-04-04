import os
try:
    import cPickle as pickle
except:
    import pickle

'''
How to implement and links from:
http://data.gov.uk/forum/general-discussion/mp-postcode-csv-file
search:
https://geoportal.statistics.gov.uk/geoportal/catalog/main/home.page
for:
code history database & ONSPD

Then, from code history database, want Equivalents.csv and from ONSPD, want Data/ONSPD.csv

'''

def parse_onspd(onspd_file):
	res_dict = {}
	with open(onspd_file, 'r') as fi:
		for line in fi:
			if not line.startswith('p'):
				split_line = line.split(',')
				pc = split_line[0].strip('"')
				pcon = split_line[17].strip('"')
				res_dict[pc] = pcon
	with open('/Users/flashton/pc_to_pcon.pick', 'wb') as fo:
		pickle.dump(res_dict, fo, -1)
	return res_dict

def parse_chd(chd_file):
	res_dict = {}
	with open(chd_file) as fi:
		for line in fi:
			if not line.startswith('\"GEOGCD\",\"GEOGNM\"'):
				if not line.split(',')[1] == '':
					pcon = line.split(',')[0].strip('"')
					const = line.split(',')[1].strip('"')
					res_dict[pcon] = const
	with open('/Users/flashton/pcon_to_constituency.pick', 'wb') as fo:
		pickle.dump(res_dict, fo, -1)
	return res_dict

def write_lookup(pc_to_pcon, pcon_to_constituency):
	for pc in pc_to_pcon:
		try:
			print pc + '\t' + pc_to_pcon[pc] + '\t' + pcon_to_constituency[pc_to_pcon[pc]]
		except KeyError:
			pass

onspd_file = '/Users/flashton/Downloads/ONSPD_NOV_2014_csv/Data/ONSPD_NOV_2014_UK.csv'
chd_file = '/Users/flashton/Downloads/Code_History_Database_Dec_2014/Equivalents.csv'


if os.path.exists('/Users/flashton/pcon_to_constituency.pick'):
	if os.path.exists('/Users/flashton/pc_to_pcon.pick'):
		pcon_to_constituency = pickle.load(open('/Users/flashton/pcon_to_constituency.pick', 'rb'))
		pc_to_pcon = pickle.load(open('/Users/flashton/pc_to_pcon.pick', 'rb'))
		# print len(pc_to_pcon)
		write_lookup(pc_to_pcon, pcon_to_constituency)
else:
	pc_to_pcon = parse_onspd(onspd_file)
	pcon_to_constituency = parse_chd(chd_file)
	write_lookup(pc_to_pcon, pcon_to_constituency)





#md = pc_to_pcon['ME141EX']
#print pcon_to_constituency[md]



