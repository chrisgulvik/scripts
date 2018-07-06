#!/usr/bin/env bash


[ -z $LAB_HOME ] && { echo 'ERROR: $LAB_HOME path not set'; exit 1; }


# Update my own HOME dir first
repos=( genomics_scripts phylogenetics_scripts AR_Bank_scripts summarize_kraken_data scripts c-SSTAR )
for repo in "${repos[@]}"; do
  cd $HOME/$repo
  git pull git@github.com:chrisgulvik/$repo.git
done

# Update LAB share from HOME dir scripts
repos=( "${repos[@]/#/$HOME/}" )
shopt -s nullglob
repos=( "${repos[@]/%//*}" )
for f in ${repos[@]}; do
  if [[ -f $f && $f != *.md ]]; then
    b=$(basename $f)
    cp -fv $f $LAB_HOME/.bin/$b
  elif [[ -d $f ]]; then
    for j in $f/*; do
      if [[ -f $j ]]; then
        k=$(basename $j)
        cp -rfv $j $LAB_HOME/.lib/$k
        if [[ $k == *.gz ]]; then
          gunzip -f $LAB_HOME/.lib/$k
        fi
      fi
    done
  fi
done

# Handle job scripts seperately
repo='UnivaGridEngine_UGE_cluster_scripts'
git pull git@github.com:chrisgulvik/$repo.git $HOME/$repo
for f in $HOME/$repo/*.uge-bash; do
  cp -fv $f $LAB_HOME/.job/`basename $f`
done
