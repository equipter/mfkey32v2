#!/bin/bash
echo "Cracking keys from .mfkey32.log"
IFS=$'\n'; for line in `awk '{print $6 " " $8 " " $10 " " $12 " " $14 " " $16" " $18}' mfkey32.log`; do echo ./mfkey32v2 $line >> temp.sh; chmod +x temp.sh; ./temp.sh | grep "Found Key" | tee found_keys.txt; rm temp.sh; done
echo "Cracking complete! Keys saved to found_keys.txt"
