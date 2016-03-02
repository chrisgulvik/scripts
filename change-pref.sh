#!/bin/bash
# changes prefixes
# Usage:  change-pref.sh pref1 pref2

for f in $1*; do
    [ -f "$f" ] && mv -v "$f" "$2${f#$1}"
done
