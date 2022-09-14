#! /bin/bash

if [[ "$#" -ne 1 ]]; then
	echo "This command need the log file as argument" >&2
	exit 1
fi

filename=$1
nb_lines=$(wc -l < $filename)
n=1
rm result.log

while read line; do
	code=$(echo $line | awk '{print $18}')
	arguments=$(echo $line | awk '{print $6" "$8" "$10" "$12" "$14" "$16" "$18}')

	echo -ne "$n/$nb_lines\t"

	./mfkey32v2 $arguments | sed -n 's/Found Key: \[\(.*\)\]/\1/ p' | tee --append result.log
	n=$((n+1))
done < $filename

sort -u result.log 
