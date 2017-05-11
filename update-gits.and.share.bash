#!/bin/bash


[ -z $BRANCH_HOME ] && echo 'ERROR: $BRANCH_HOME path not set'


# Update my own HOME dir first
repos=( genomics_scripts phylogenetics_scripts AR_Bank_scripts summarize_kraken_data scripts c-SSTAR )
for repo in "${repos[@]}"; do
    cd $HOME/$repo
    git pull git@github.com:chrisgulvik/$repo.git
done

# Update BRANCH share from HOME dir scripts
repos=( "${repos[@]/#/$HOME/}" )
shopt -s nullglob
repos=( "${repos[@]/%//*}" )
for f in ${repos[@]}; do
    if [[ -f $f && $f != *.md ]]; then
        b=$(basename $f)
        cp -fv $f $BRANCH_HOME/.bin/$b
    elif [[ -d $f ]]; then
        for j in $f/*; do
            if [[ -f $j ]]; then
                k=$(basename $j)
                cp -rfv $j $BRANCH_HOME/.lib/$k
                if [[ $k == *.gz ]]; then
                    gunzip -f $BRANCH_HOME/.lib/$k
                fi
            fi
        done
    fi
done

