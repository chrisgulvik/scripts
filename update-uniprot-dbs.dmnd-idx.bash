#!/usr/bin/env bash


source $HOME/.bashrc
[ -z $LAB_HOME ] && { echo 'ERROR: $LAB_HOME path not set'; exit 1; }
# FTP blocked on Aspen but rule exception exists for Uniprot on biolinux
[ ${HOSTNAME%%.*} != 'biolinux' ] && { echo 'ERROR: must be on biolinux'; exit 1; }

UNIPROT='ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete'
SWISSPROT="${UNIPROT}/uniprot_sprot.fasta.gz"  #84 MB size
TREMBL="${UNIPROT}/uniprot_trembl.fasta.gz"  #27 GB size

source /etc/profile.d/modules.sh
module load diamond/0.9.10
cd "$LAB_HOME"/.lib
for DB in $SWISSPROT $TREMBL ; do
  MD5_before=$( md5sum "$DB" 2> /dev/null )
  wget --timestamping "$DB"
  MD5_after=$( md5sum "$DB" 2> /dev/null )
  if [ "$MD5_before" != "$MD5_after" ]; then
    diamond makedb --in "$LAB_HOME"/.lib/`basename $DB` \
     --db "$LAB_HOME"/.lib/`basename $DB .fasta.gz`.dmnd
  fi
done
module unload diamond/0.9.10
