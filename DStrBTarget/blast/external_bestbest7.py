#!/usr/bin/python3
import sys

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
    simi_index=10978*i1+i2
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
        #    homolist.remove(x)
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
    #    homoDict[targ]=[]
    return homoDict

def add_12(sett,lig_simi,lig2i):
    for targi in sett:
        score12=lig_simi-0.1*float(refbindSet[lig2i][targi])#2D+3D+bind score
        append_score(lig1i, targi, score12)#Integration of 2D+3D+bind score

def score12(lig1i):#Generating 2D+3D+bind score for the input ligand to each ref-target. Note that lig1i means index of lig1 in molSet.
    for lig2i in [molSet.index(x) for x in ligSet]:
        lig_simi=get_simi(lig1i, lig2i)#2D+3D similarity score
        add_12(refbindSet[lig2i].keys(),lig_simi,lig2i)
    for targi in scoreSet.keys():#Convient of later integration of blast
        scoreSet[targi]=max(scoreSet[targi])
    return scoreSet

def score123(lig1i):#Generating 2D+3D+bind+blast score for the input ligand to each ref-target.Note that lig1i means index of lig1 in molSet.
    for targ in [molSet.index(x) for x in targSet if molSet.index(x) in scoreSet.keys()]:
        if targ in homoDict.keys() and homoDict[targ] in scoreSet.keys():
            #scoreSet2[targ]=w*scoreSet[targ]+(1-w)*scoreSet[homoDict[targ]] #Here you can add a parameter!
            scoreSet2[targ]=(scoreSet[targ]+scoreSet[homoDict[targ]])
        #elif targ not in homoDict.keys() or homoDict[targ] not in scoreSet.keys():
        else:
            scoreSet2[targ]=scoreSet[targ]
    for targ in [molSet.index(x) for x in targSet if molSet.index(x) not in scoreSet.keys()]:
        if targ in homoDict.keys() and homoDict[targ] in scoreSet.keys():
            scoreSet2[targ]=scoreSet[homoDict[targ]] 
        else:
            scoreSet2[targ]=0
    return scoreSet2

                   ########## MAIN CODE ########

if __name__== '__main__':
    
    ligIn=read_List(sys.argv[1])
    ligSet=read_List('../../process_add3/extract/3Dresult/after_add3.lig')
    targSet=read_List('../../process_add3/after_add3.targ')
    #ligsimiSet=read_List('./dataSet/fold'+str(gn)+'.ligsimi')
    molSet=ligSet[:]
    molSet.extend(targSet)
    ligSet==[]
    targSet==[]

    taniSet=read_List('../../process_add3/extract/tanimoto/afteradd3_extract.tanimoto')
    LSSet=read_List('../../process_add3/extract/3Dresult/afteradd3_extract.lsalign')

    bindSet=read_bindaff('../../process_add3/chembl2.bind',ligIn)
    refbindSet=read_bindaff('../../external_add3_blast/fact190605_afteradd3.bindaff1w',molSet)
    blastDict=dict_blast('../../external_add3_blast/extract_afteradd3.Evalue')
   
    homoDict=dict_mostHomo()
    ligsimi=cal_ligsimi(taniSet, LSSet)
    
    for lig1i in [ligIn.index(x) for x in ligIn]:
    #for lig1i in [0]:
        scoreSet={}
        scoreSet=score12(lig1i)
        scoreSet2={}
        scoreSet2=score123(lig1i)
        sortedSet=sorted(scoreSet2.items(), key=lambda x:x[1], reverse=True)
        for targ in [x for x in bindSet[lig1i].keys() if x in scoreSet2.keys()]:
            targrank=[sortedSet.index(x) for x in sortedSet if x[0]==targ]
            targrank=targrank[0]
            print(ligIn[lig1i]+' '+molSet[targ]+' '+str(scoreSet[targ])+' '+str(targrank))
        for targ in [x for x in bindSet[lig1i].keys() if x not in scoreSet2.keys()]:
            #targrank=[sortedSet.index(x) for x in sortedSet if x[0]==targ]
            #targrank=targrank[0]
            print(ligIn[lig1i]+' '+molSet[targ]+' NoScore 1111  ')
