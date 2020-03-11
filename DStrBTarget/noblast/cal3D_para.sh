#!/bin/bash
lIst=$1
for i in $(cat $lIst);do
	echo $i
	for j in $(seq 0 9);do
		nohup ~/software/LSalign/LSalign -rf 1 ~/network/process/prepare/mol2s/${i}.mol2 ./prepare/proc${j}.mol2 >> ./ori_result/proc${j}.lsalign &
	done
	wait
done
