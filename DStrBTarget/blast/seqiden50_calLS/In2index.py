#!/usr/bin/python
'''transfer input rankID to ligSet index'''
import sys

def read_list(fn):
       	Set=[]
	appendd=Set.append
	with open(fn) as fn:
		for line in fn.readlines():
			appendd(line.strip('\n'))
	return Set
#idef read_dict(fn, Set):
#	Set=Set
#	indexx=Set.index
#	Dict={}
#	with open(fn) as fn:
#		for line in fn.readlines():
#			line=line.strip('\n')
#			content=line.split()
#			Dict[content[1]]=indexx(content[0]) #link 'rank'ID to ligSet index
#	return Dict

#######
if __name__== '__main__':
	rank2index=open('In2index.map','a+')
	ligSet=read_list('./seqiden50.lig') #This is strictly the same order as in 9197
	#keyDict=read_dict('./rank.map', ligSet)
	for lig in ligSet:
		rank2index.write(lig+' '+str(ligSet.index(lig))+'\n')
	rank2index.close()




					
