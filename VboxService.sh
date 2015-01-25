#! /bin/sh
# /etc/init.d/StartVM
#

#Edit these variables!

VMUSER=tux

# Machine: Debian
# Machine UUID
VMNAME="caa453ca-9aaa-4a87-a15e-d1297e2b8ff2"

LOCKFILE=/tmp/$VMNAME.lock

case "$1" in
  start)
    echo "Starting VirtualBox VM..."
    sudo -H -b -u $VMUSER  /usr/bin/VBoxManage startvm "$VMNAME" --type headless 
    touch $LOCKFILE
    
    exit 0
    ;;
  stop)
    echo "Saving state of Virtualbox VM..."
    sudo -H -u  $VMUSER /usr/bin/VBoxManage controlvm "$VMNAME" savestate
    rm -rf $LOCKFILE
    exit 0
    ;;
   status)
   vmstatus=$(sudo -H -u  $VMUSER /usr/bin/VBoxManage showvminfo  --machinereadable "$VMNAME" | grep -E "VMState=")
   echo $vmstatus 
   
   if [ -e "$LOCKFILE" ]
   then
   	exit 0
   else
        exit 1
   fi


   ;; 
  *)
    echo "Usage: /etc/init.d/VboxService {start|stop|status}"
    exit 1
    ;;
esac

exit 0
