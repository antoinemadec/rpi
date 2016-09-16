#!/bin/bash

file="config.txt"
instrument_name=instru_$1
effect_value_string=$2

sed -i "s/$instrument_name\( *\);.*/$instrument_name\1;$effect_value_string/" $file
