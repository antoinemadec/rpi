#!/bin/bash

config_file="config.txt"
instrument_name=instru_$1
shift
effect_value_string=$@

if grep -q "$instrument_name " $config_file
then
  sed -i "s/$instrument_name .*/$instrument_name $effect_value_string/" $config_file
else
  echo $instrument_name $effect_value_string >> $config_file
fi
