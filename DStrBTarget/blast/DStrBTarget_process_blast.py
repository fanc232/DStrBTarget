#!/usr/bin/python3
#Expand the range of predicted target to seqiden to 50%,using the reference targ of 40%. and consider target seqiden > 50% as sharing the same ligand. 
import sys

para1=float(sys.argv[1])
para2=float(1-para1)
para3=float(sys.argv[2])

#files as input:
ligIDfile=sys.argv[3]
tani2Dfile=sys.argv[4]
LS3Dfile=sys.argv[5]

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
#Read ligand-receptor binding affinity and reposit as bindSet[ligand][trget]=binding_affinity
    Set={}
    with open (fn) as bindfile:
        for lbind in bindfile.readlines():
            llbind=lbind.split()
            if (llbind[1] in lSet) and (llbind[0] in molSet):
                index1=lSet.index(llbind[1])
                index2=molSet.index(llbind[0])
            build_two_key_dictionary(index1, index2, llbind[2], Set)
    return Set

def dict_blast(fn):#blast was added as level.
    blastDict={}
    with open (fn) as fm:
        for line in fm.readlines():
            cont=line.split()
            if float(cont[2])<=1E-2 and cont[0] in molSet and cont[1] in molSet:
                index1=molSet.index(cont[0])
                index2=molSet.index(cont[1])
                blastDict[(index1,index2)]=float(cont[2])
    return blastDict

def append_score(lig, targ, score):
#Append all scores from a ligand to a target into the scoreSet(Remember that scoreSet is acclaimed as global varient at the beggining)
    if targ not in scoreSet.keys():
        scoreSet[targ]=[]
    scoreSet[targ].append(score)
    return scoreSet

def cal_ligsimi(set1, set2): #set1 and set2 must be strictly comparable, such as tanimoto and lsalign files
    ligsimi=[]
    appendd=ligsimi.append
    ligsimi=list(map(lambda x,y: 0.7*float(x)+0.3*float(y), set1, set2))
    return ligsimi

def get_simi(i1, i2):
#Get the ligand-ligand similarity data, such as tanimoto and lsalign
    simi_index=10192*i1+i2
    return ligsimi[simi_index]

def get_targhomo(targ):
    targhomo=set([x[1] for x in blastDict.keys() if x[0]==targ])
    return targhomo

def dict_mostHomo():
    homoDict={}
    for targ in set([x[0] for x in blastDict.keys()]):
        homolist1=list(get_targhomo(targ))
        homolist=homolist1[:]
        for targg in [x for x in homolist1 if x!= targ]:
            homolist.extend(get_targhomo(targg))
        while targ in homolist:
            homolist.remove(targ)
	#for x in [x for x in homolist if homolist.count(x)==1]:
	#	homolist.remove(x)
        if homolist==[]:
            continue
        else:
            homoNum=list(map(lambda x: (x,homolist.count(x)),homolist1))
            homoNum.sort(key=lambda x: x[1],reverse=True)
            topNum=homoNum[0][1]
            homoEvalue=list(map(lambda x:(x,blastDict[(targ,x)]),[x[0] for x in homoNum if x[1]==topNum]))
            homoEvalue.sort(key=lambda x:x[1])
            homoDict[targ]=homoEvalue[0][0]
	#for targ in [x for x in range(tel+trl) if x not in homoDict.keys()]:
	#	homoDict[targ]=[]
    return homoDict

def add_12(sett,lig_simi,lig2i):
    for targi in sett:
        score12=lig_simi-0.1*float(refbindSet[lig2i][targi])#2D+3D+bind score
        append_score(lig1i, targi, score12)#Integration of 2D+3D+bind score

def score12(lig1i):#Generating 2D+3D+bind score for the input ligand to each ref-target. Note that lig1i means index of lig1 in molSet.
    for lig2i in range(0,10192):
        lig_simi=get_simi(lig1i, lig2i)#2D+3D similarity score
        add_12(refbindSet[lig2i].keys(),lig_simi,lig2i)
    for targi in scoreSet.keys():#Convient of later integration of blast
        scoreSet[targi]=max(scoreSet[targi])
    return scoreSet

def score123(lig1i):#Generating 2D+3D+bind+blast score for the input ligand to each ref-target.Note that lig1i means index of lig1 in molSet.
    for targ in [x for x in range(10192,len(molSet)) if x in scoreSet.keys()]:
        if targ in homoDict.keys() and homoDict[targ] in scoreSet.keys():
	#scoreSet2[targ]=w*scoreSet[targ]+(1-w)*scoreSet[homoDict[targ]] #Here you can add a parameter!
            scoreSet2[targ]=(scoreSet[targ]+scoreSet[homoDict[targ]])
	#elif targ not in homoDict.keys() or homoDict[targ] not in scoreSet.keys():
        else:
            scoreSet2[targ]=scoreSet[targ]
    for targ in [x for x in range(10192,len(molSet)) if x not in scoreSet.keys()]:
        if targ in homoDict.keys() and homoDict[targ] in scoreSet.keys():
            scoreSet2[targ]=scoreSet[homoDict[targ]] 
        else:
            scoreSet2[targ]=0
    return scoreSet2

	   ########## MAIN CODE ########

if __name__== '__main__':
	
    ligIn=read_List(ligIDfile)
    ligSet=read_List('./seqiden50.lig')
    targSet=read_List('./seqiden50.targ')
    molSet=ligSet[:]
    molSet.extend(targSet)
    ligSet=[]
    targSet=[]

    taniSet=read_List(tani2Dfile)
    LSSet=read_List(LS3Dfile)

    refbindSet=read_bindaff('./seqiden50.bindaff1w',molSet)
    blastDict=dict_blast('./extract_totaltarg190709.Evalue')
   
    homoDict=dict_mostHomo()
    ligsimi=cal_ligsimi(taniSet, LSSet)

    for lig1i in [ligIn.index(x) for x in ligIn]:
	#for lig1i in [0]:
        scoreSet={}
        scoreSet=score12(lig1i)
        #print (scoreSet)
        scoreSet2={}
        scoreSet2=score123(lig1i)
        sortedSet=sorted(scoreSet2.items(), key=lambda x:x[1], reverse=True)
        top10Set=sortedSet[0:10]
        resultfile=open(ligIn[lig1i]+'.result','a+')
        for x in top10Set:
            resultfile.write(molSet[x[0]]+' '+"{:3f}".format(x[1])+'\n')
        resultfile.close()

