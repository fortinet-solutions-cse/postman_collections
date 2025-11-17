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

if [ -f /fabric.env ]; then
    . /fabric.env
fi

fab_ver() {
  fgt_password=$(grep 'fgt_password:' /fabric/autodeploy/tenants/shared/.secrets.yaml | awk '{print $2}')  
  for d in FGT11 FGT12 FGT21 FGT1H1 FGT1H2 FGT2H1
  do
    sshpass -p $fgt_password ssh $d 'get system status' 2>/dev/null | grep -E "Version:|Status:"
    echo
  done
}

fab_upgrade() {

  [ $# -eq 1 ] || { echo "Usage: $0 <image.out>"; return; }

  fgt_password=$(grep 'fgt_password:' /fabric/autodeploy/tenants/shared/.secrets.yaml | awk '{print $2}')  
  for d in FGT11 FGT12 FGT21 FGT1H1 FGT1H2 FGT2H1
  do
    sshpass -p $fgt_password scp -O $1 ${d}:fgt-image &
  done
}

fab_deploy() {

  [ $# -eq 1 ] || { echo "Usage: $0 <src_dir>"; return; }

  fgt_password=$(grep 'fgt_password:' /fabric/autodeploy/tenants/shared/.secrets.yaml | awk '{print $2}')  
  for d in FGT11 FGT12 FGT21 FGT1H1 FGT1H2 FGT2H1
  do
    [[ -z $1 ]] && dir=. || dir=$1
    file=$dir/site${d:3:1}-${d:4}
    [[ -f $file ]] && sshpass -p $fgt_password ssh $d < $file
  done
}

fab_backup() {

  [ $# -eq 1 ] || { echo "Usage: $0 <target_dir>"; return; }

  fgt_password=$(grep 'fgt_password:' /fabric/autodeploy/tenants/shared/.secrets.yaml | awk '{print $2}')  
  for d in FGT11 FGT12 FGT21 FGT1H1 FGT1H2 FGT2H1
  do
    [[ -z $1 ]] && dir=. || dir=$1
    file=$dir/site${d:3:1}-${d:4}
    sshpass -p $fgt_password scp -O ${d}:fgt-config $file
  done
}

fab_restore() {

  [ $# -eq 1 ] || { echo "Usage: $0 <src_dir>"; return; }

  fgt_password=$(grep 'fgt_password:' /fabric/autodeploy/tenants/shared/.secrets.yaml | awk '{print $2}')  
  for d in FGT11 FGT12 FGT21 FGT1H1 FGT1H2 FGT2H1
  do
    [[ -z $1 ]] && dir=. || dir=$1
    file=$dir/site${d:3:1}-${d:4}
    [[ -f $file ]] && sshpass -p $fgt_password scp -O $file ${d}:fgt-restore-config
  done
}

fab_exec() {

  [ $# -eq 1 ] || { echo "Usage: $0 <command_file>"; return; }

  fgt_password=$(grep 'fgt_password:' /fabric/autodeploy/tenants/shared/.secrets.yaml | awk '{print $2}')  
  for d in FGT11 FGT12 FGT21 FGT1H1 FGT1H2 FGT2H1
  do
    sshpass -p $fgt_password ssh $d < $1
  done
}

fab_auth() {

  [ $# -eq 1 ] || { echo "Usage: $0 <ssh_key_file.pub>"; return; }

  sshkey="$(< $1)"
  fgt_password=$(grep 'fgt_password:' /fabric/autodeploy/tenants/shared/.secrets.yaml | awk '{print $2}')  
  for d in FGT11 FGT12 FGT21 FGT1H1 FGT1H2 FGT2H1 
  do
    sshpass -p $fgt_password ssh $d <<- EOF
      config system admin
        edit "admin"
          set ssh-public-key1 "$sshkey"
        next
      end
EOF
  done

  for d in C11 C12 C21 C1H1 C1H2 C2H1
  do
    sshpass -p $fgt_password ssh $d "grep -qxF \"$sshkey\" ~/.ssh/authorized_keys || echo $sshkey >> ~/.ssh/authorized_keys"
  done

}
