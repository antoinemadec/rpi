#!/bin/bash

file=$1
effect_name=$2
params_str=$3

echo "$0:"
echo "  effect_name = $effect_name"
echo "  params_str = $params_str"

file_tmp="$file.tmp"

while read line
do
  if echo "$line" | grep -q "; *$effect_name *;"
  then
    line=$(echo "$line" | sed "s/; $effect_name[^;]*;.*/; $effect_name $params_str/")
  fi
  echo "$line" >> $file_tmp
done < $file

mv $file_tmp $file
