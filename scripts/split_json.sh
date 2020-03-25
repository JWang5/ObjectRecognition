#!/bin/bash

# Split a JSON into multiple files. Uses jq.

# Usage
# ./split_json.sh /path/to/json/file

path="$1"
file="$2"

#jq -cr 'keys[] as $k | "\($k)\t\(.[$k])"' "$file"  | awk -F\\t '{ file=$1".json"; print $2 > file; close(file); }'

for f in `cat $path/$file | jq -r 'keys[]'` ; do
  name=`jq -r '.['$f'] | .filename' $path/$file`
  name="${name%.png}"
printf "%s\n" $name
  cat $path/$file | jq ".[$f]" > $path/$name.json
done
