# ~/.bashrc: executed by bash(1) for non-login shells.

# Note: PS1 and umask are already set in /etc/profile. You should not
# need this unless you want different defaults for root.
# PS1='${debian_chroot:+($debian_chroot)}\h:\w\$ '
# umask 022

# You may uncomment the following lines if you want `ls' to be colorized:
# export LS_OPTIONS='--color=auto'
# eval "$(dircolors)"
# alias ls='ls $LS_OPTIONS'
# alias ll='ls $LS_OPTIONS -l'
# alias l='ls $LS_OPTIONS -lA'
#
# Some more alias to avoid making mistakes:
# alias rm='rm -i'
# alias cp='cp -i'
# alias mv='mv -i'

fpoc_ver() {
  for d in FGT11 FGT12 FGT21 FGT1H1 FGT1H2 FGT2H1
  do
    sshpass -p fortinet ssh $d 'get system status' 2>/dev/null | grep -E "Version:|Status:"
    echo
  done
}

fpoc_upgrade() {
  for d in FGT11 FGT12 FGT21 FGT1H1 FGT1H2 FGT2H1
  do
    sshpass -p fortinet scp -O $1 ${d}:fgt-image &
  done
}

fpoc_deploy() {
  for d in FGT11 FGT12 FGT21 FGT1H1 FGT1H2 FGT2H1
  do
    [[ -z $1 ]] && dir=. || dir=$1
    file=$dir/site${d:3:1}-${d:4}
    [[ -f $file ]] && sshpass -p fortinet ssh $d < $file
  done
}

fpoc_backup() {
  for d in FGT11 FGT12 FGT21 FGT1H1 FGT1H2 FGT2H1
  do
    [[ -z $1 ]] && dir=. || dir=$1
    file=$dir/site${d:3:1}-${d:4}
    sshpass -p fortinet scp -O ${d}:fgt-config $file
  done
}

fpoc_restore() {
  for d in FGT11 FGT12 FGT21 FGT1H1 FGT1H2 FGT2H1
  do
    [[ -z $1 ]] && dir=. || dir=$1
    file=$dir/site${d:3:1}-${d:4}
    [[ -f $file ]] && sshpass -p fortinet scp -O $file ${d}:fgt-restore-config
  done
}

fpoc_exec() {
  for d in FGT11 FGT12 FGT21 FGT1H1 FGT1H2 FGT2H1
  do
    sshpass -p fortinet ssh $d < $1
  done
}

