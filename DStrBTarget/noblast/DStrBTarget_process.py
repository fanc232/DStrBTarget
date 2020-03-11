#!/usr/bin/python3
#input:(list,dataset) for ligand, target, blastfile, tanimotofile, LSalignfile; finally,bindaffinity file.
import sys

#parameters of the model,sys.argv[1] means w1, sys.argv[2] means w2.
para1=float(sys.argv[1])
para2=float(1-para1)
para3=float(sys.argv[2])

#files as input:
ligIDfile=sys.argv[3]
tani2Dfile=sys.argv[4]
LS3Dfile=sys.argv[5]

global scoreSet
scoreSet={}

def read_List(fn): #Read data in the form of list, such as molecule list, tanimoto, blast, blast, etc.
    Set=[]
    appendd=Set.append
    with open (fn) as fm:
        for line in fm.readlines():
            appendd(line.strip('\n'))
    return Set

def build_two_key_dictionary(key1, key2, value, Set): #for example, scoreSet[ligand][target]=score, or, bindSet[ligand][target]=binding_affinity 
    if key1 not in Set.keys():
        Set[key1]={}
    Set[key1][key2]=value
    return Set

def read_bindaff(fn,lSet):
#Read ligand-receptor binding affinity and reposit as bindSet[ligand][trget]=binding_affinity. The varient "Set" is different according to reference bindSet or bindSet
    Set={}
    with open (fn) as bindfile:
        for lbind in bindfile.readlines():
            llbind=lbind.split()
            if (llbind[1] in lSet) and (llbind[0] in targSet):
                index1=lSet.index(llbind[1])#ligand 
                index2=targSet.index(llbind[0])#target 
            build_two_key_dictionary(index1, index2, llbind[2], Set)
    return Set

def cal_ligsimi(set1, set2): #set1 and set2 must be strictly comparable, such as tanimoto and lsalign files
    ligsimi=list(map(lambda x,y: para1*float(x)+para2*float(y), set1, set2))
    return ligsimi     

def get_simi(i1, i2):
#Get the ligand-ligand similarity data, which is a combination of tanimoto and LSalign,but this is different, because this is a external-validation
    simi_index=9197*i1+i2
    return ligsimi[simi_index]

def append_score(lig, targ, score):
#Append all scores from a ligand to a target into the scoreSet(Remember that scoreSet is acclaimed as global varient at the beggining)
    if targ not in scoreSet.keys():
        scoreSet[targ]=[]
    appendd=scoreSet[targ].append
    appendd(score)
    return scoreSet

def add_12(sett,lig_simi,lig2i):
    for targi in sett:
        score12=lig_simi-para3*float(refbindSet[lig2i][targi])#2D+3D+bind score
        append_score(lig1i, targi, score12)#Integration of 2D+3D+bind score

def score12(lig1i):#Generating 2D+3D+bind score for the input ligand to each ref-target. Note that lig1i means index of lig1 in molSet.
    for lig2i in [ligSet.index(x) for x in ligSet]:
        lig_simi=get_simi(lig1i, lig2i)#2D+3D similarity score
        add_12(refbindSet[lig2i].keys(),lig_simi,lig2i)
    for targi in scoreSet.keys():#Convient of later integration of blast
        scoreSet[targi]=max(scoreSet[targi])
    return scoreSet
    
                         ###################### MAIN CODE ####################

if __name__== '__main__':
#read_data#
	ligIn=read_List(ligIDfile) #input ligand set
	ligSet=read_List('../database/clusterlig_MW.list')
	targSet=read_List('../database/clustMW_debug.targ')
	taniSet=read_List(tani2Dfile)
	LSSet=read_List(LS3Dfile)
	refbindSet=read_bindaff('../database/fact190510.bindaff1w',ligSet)
	print('Data read completed.')

	#calculate ligand similarity score#
	ligsimi=cal_ligsimi(taniSet, LSSet)

	for lig1i in [ligIn.index(lig1) for lig1 in ligIn]:
		scoreSet={}
		scoreSet=score12(lig1i)
		sortedSet=sorted(scoreSet.items(),key=lambda x:x[1],reverse=True)
		top10Set=sortedSet[0:10]
		resultfile=open(ligIn[lig1i]+'.result','a+')
		for x in sortedSet:
		#for x in top10Set:
			resultfile.write(targSet[x[0]]+' '+"{:3f}".format(x[1])+'\n')
		resultfile.close()


    



    

