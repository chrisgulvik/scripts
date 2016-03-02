#!/bin/bash
# changes extensions
# Usage:  change-ext.sh ext1 ext2

for f in *$1; do
    [ -f "$f" ] && mv -v "$f" "${f%$1}$2"
done
