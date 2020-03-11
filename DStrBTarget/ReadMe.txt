Now only noblast mode of DStruBTarget can be directly used.

It should be used in linux 64-bit system.

When using it, please go into the folder "./DStrBTarget/noblast" first.

Then run "DStrBTarget_noblast.sh <your file>".

Here <your file> means the .mol2 file containing all of your query ligands.

Note that in the section for each ligand, the ligand name under the header "@<TRIPOS>MOLECULE" must be correct, because it is exactly the basename of the output file.For example, if your hand in two query ligands whose names under the header "@<TRIPOS>MOLECULE" are "A" and "B" respectively, then their top15 predicted targets are recorded in the separate files, "A.result" and "B.result", respectively, in the path of "./DStrBTarget/gen_files/".

Another importent notice is that each time your run DStrBTarget_noblast.sh, please DO REMEMBER to clear the folder "./DStrBTarget/gen_files/" first of all.

A pre-test input file is in "./DStrBTarget/test/test_pipline.mol2"

I'm sorry if you feel any un-convinence using DStrBTarget. I'm trying to develop a Web Service version of DStruBTarget.
