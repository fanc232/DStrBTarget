#!/usr/bin/python

def read_list(fn):
	with open (fn) as fn:
		Set=[]
		for line in fn.readlines():
			Set.append(line.strip('\n'))
	return Set

def dict_3D(): # a two-key dictionary 
	with open('../gen_files/ligIn.lsalign') as fn:
		dictt={}
		for line in fn.readlines():
			cont=line.split()
			if (len(cont)==10) and (cont[0]!='QEURY_NAME'):
				if cont[0] not in dictt.keys():
					dictt[cont[0]] = {}
				dictt[cont[0]][cont[1]] = cont[2].strip('\n')
	return dictt
			
                                    ############ MAIN CODE #############
queryLig=read_list('../gen_files/ligIn.names')
refLig=read_list('./seqiden50.lig')
LSfile=open('./extract.lsalign','a+')
dictt=dict_3D()
for qlig in queryLig:
	for reflig in refLig:
		LSfile.write(dictt[qlig][str(refLig.index(reflig))]+'\n')
LSfile.close()
