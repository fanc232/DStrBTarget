#!/usr/bin/python

def read_list(fn):
	with open (fn) as fn:
		Set=[]
		for line in fn.readlines():
			Set.append(line.strip('\n'))
	return Set

def tani_dict(lig):
	with open('../gen_files/ligIn.tanimoto') as fn:
		dictt={}
		for line in fn.readlines():
			cont=line.split()
                        if cont[0]==lig:
			    dictt[cont[1]]=cont[2].strip('\n')
	return dictt
			
                                    ############ MAIN CODE #############
queryLig=read_list('../gen_files/ligIn.names')
refLig=read_list('../database/clusterlig_MW.list')
tanifile=open('../gen_files/extract.tanimoto','a+')
for qlig in queryLig:
	dictt=tani_dict(qlig)
	for reflig in refLig:
		tanifile.write(dictt[reflig]+'\n')
tanifile.close()
