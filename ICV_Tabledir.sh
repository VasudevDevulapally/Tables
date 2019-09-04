#!/bin/bash

 
#find sub1/* -type f -printf "%f\n" | paste -s -d , > data.csv

 
 


  eval "dirs=($(ls -v --quoting-style=shell-always))"
  headers_done=false
  for dir in "${dirs[@]}"; do
    eval "files=($(
      ls -vd --quoting-style=shell-always -- "$dir"/LABEL_*.txt))"
    if ! "$headers_done"; then
      printf SubjectID
      printf ',%s' "${files[@]}"
      printf '\n'
      headers_done=true
    fi
    printf %s, "$dir"
    tail -q -n 1 -- "${files[@]}" | paste -sd , -
  done > Output_volumes.csv







	
 

 #echo "SubjectID" > temp 
 #find . -type d -iname "subject*" | sed 's/^.*\///' >> temp 
# eval "dirs=($(ls -v --quoting-style=shell-always))"
#for dir in "${dirs[@]}"; do
 # eval "files=($(
  #  ls -vd --quoting-style=shell-always -- "$dir"/t1/regional_vol*.txt))"
  #tail -q -n 1 -- "${files[@]}" | paste -sd , -
#done > data.csv

#paste -d, <(ls -1v "$dir"/t1/regional_vol*.txt ) > data.csv
# paste  -d , temp <(sed '/^\s*$/d' data.csv)
 # mv  data.csv temp.csv
#x,regional_vol_GM_atlas1.txt,regional_vol_GM_atlas2.txt
#sub1,1 1,2 2
#sub2,3 3,4 4
