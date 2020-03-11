#!/bin/bash

#grap out query ligands' name, which will be used in TLBTarget_process.py
lig_str_file=$1
w1=$2
w2=$3

grep -A 1 '@<TRIPOS>MOLECULE' $lig_str_file|awk '{if ((NR+1)%3==0) print}' > ../gen_files/ligIn.names

#transfer to fpt for 2D similarity
obabel -imol2 $lig_str_file -ofpt -O ../gen_files/lig.fpt -m
cat ../gen_files/lig*.fpt >> ../gen_files/ligIn.fpt

#calculate 2D similarity
~/softwares/calTanimoto/calTanimoto ../gen_files/ligIn.fpt ../database/clusterlig_MW.fpt > ../gen_files/ligIn.tanimoto

#calculate 3D similarity in parallel
nohup ~/softwares/LSalign/LSalign -rf 1 $lig_str_file ../database/proc10/proc0.mol2 > ../gen_files/proc0.lsalign
#for j in $(seq 0 4);do
#	nohup ~/softwares/LSalign/LSalign -rf 1 $lig_str_file ../database/proc10/proc${j}.mol2 > ../gen_files/proc${j}.lsalign &
#done
#	wait
#for j in $(seq 5 9);do
#    nohup ~/softwares/LSalign/LSalign -rf 1 $lig_str_file ../database/proc10/proc${j}.mol2 > ../gen_files/proc${j}.lsalign &
#done
#	wait
#cat ../gen_files/proc*.lsalign >> ../gen_files/ligIn.lsalign

#extract 2D/3D similarity result
#./extract_tani.py
#./extract_3D.py

#process and output
#./DStrBTarget_process.py $w1 $w2 ../gen_files/ligIn.names ./extract.tanimoto ./extract.lsalign

#restart everything!!!
#rm -f ../gen_files/* -r
