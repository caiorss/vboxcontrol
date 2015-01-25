# vi /etc/init.d/vboxservice.sh

#!/bin/bash


# Windows 7 Virtual Machine UUID
MACHINE=88196687-12d0-4442-a2a2-56626c7047ae
MACHINE_HOSTNAME=192.168.56.2

start()
{
	
	vboxmanage startvm  $MACHINE --type headless
	sleep 60

}
 
stop()
{	
	

	VBoxManage controlvm $MACHINE savestate
	
}


 
status()
{
	 vboxmanage  showvminfo  $MACHINE | grep State:

	
}

mount(){
	sudo mount -t cifs //$MACHINE_HOSTNAME/Users     /home/tux/mnt/windows -o user=oc,pass=windows,uid=1000,gid=1000,file_mode=0640,dir_mode=0750,sec=ntlm
	sudo mount -t cifs //$MACHINE_HOSTNAME/Python27  /home/tux/mnt/python  -o username=oc,password=windows,uid=1000,gid=1000,file_mode=0640,dir_mode=0750

}



umount(){
	sudo umount /home/tux/mnt/windows
	sudo umount /home/tux/mnt/python
}
 
case "$1" in
	start)
		start;;
	stop)
		stop;;
	status)
		status;;
	mount)
		mount;;
	umount)
		umount;;
		
	
	*)
		echo "Start/Stop Windows Virtual Machines"
		echo "More info: cat /etc/init.d/vboxservice.sh"
		echo "Format: /etc/init.d/vboxservice.sh {start|stop|status|mount|umount}"
		exit 1
esac
exit 0
