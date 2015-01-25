#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

def execute(command):
    from subprocess import Popen, PIPE

    p = Popen(command, shell=True, stderr=PIPE, stdout=PIPE, stdin=PIPE)
    out, err = p.communicate()
    return out, err



#  VBoxManage controlvm UUID keyboardputscancode aa
#
#  sudo mount -t vboxsf folder-name /media/windows-share
#
#
#  VBoxManage unregistervm Debian
#
#  /usr/bin/VBoxManage modifyvm Debian5 --nic1 bridged --cableconnected1 on --bridgeadapter1 eth0
#
#  sudo mount -t cifs //192.168.1.10/scripts  ~/mnt/windows/  -o username=oc,password=windows,domain=WORKGROUP
#
#

class Vbox:

    def __init__(self, uuid=None):
        self.vmname = ""
        self.uuid = uuid
        self.data = ""

        self.username = ""
        self.password = ""

    def __str__(self):
        import re
        import os

        info = self.vminfo()

        NAME = re.findall('Name:\s+(.*)', info)[0]
        OS = re.findall('Guest OS:\s+(.*)', info)[0]
        STATE = re.findall('State:\s+(\w+\s\w*)', info)[0]
        UUID = re.findall('UUID:\s+(.*)', info)[0]
        VRAM = re.findall('VRAM size:\s+(.*)MB', info)[0]
        RAM  = re.findall('Memory size:\s+(.*)MB', info)[0]
        VMDIR = re.findall('Memory size:\s+(.*)MB', info)[0]

        path=re.findall("Log folder:\s+(.*)", info)[0]
        path = os.path.split(path)[0]

        nic = re.findall("NIC 1:\s+(.*)" , info)[0]
        nic = nic.split(',')

        txt ="VIRTUAL MACHINE SUMMARY\n\n"
        txt += "Name:\t" + NAME + '\nState:\t' + STATE + '\nOS:\t' + OS  + '\nUUID:\t' + UUID

        txt += "\n\nSettings\n"
        txt += "RAM:\t%s\tMB" % RAM + "\nVRAM:\t%s\tMB" % VRAM
        txt += "\nPATH:\t%s" % path

        txt += "\n\nNetwork Card\n\t"
        txt += "\n\t".join(nic)

        return txt

    def __repr__(self):
        return self.__str__()

    def vminfo(self):
        out, err = execute('vboxmanage showvminfo "%s"' % self.uuid)
        return out

    def hdinfo(self):
        import re
        info = self.vminfo()
        hduuid = re.findall("SATA.*\(UUID:(.*)\)", info)[0]
        #print hduuid
        out, err = execute("vboxmanage showhdinfo %s" % hduuid)
        return out

    def guestinfo(self):
        cmd = "vboxmanage guestproperty enumerate %s" % self.uuid
        out, err = execute(cmd)
        return out

    def getIp(self):
        """
        Returns guest IP address

        Requires Virtualbox guest addition installed in the guest OS
        and guest operating in bridge mode
        """
        # VBoxManage guestproperty get  88196687-12d0-4442-a2a2-56626c7047ae   "/VirtualBox/GuestInfo/Net/0/V4/IP"
        import re
        cmd = 'VBoxManage guestproperty get %s "/VirtualBox/GuestInfo/Net/0/V4/IP"' % self.uuid
        out, err = execute(cmd)

        ip = re.findall('Value:\s*(.*)', out)
        if ip!=[]:
            return ip[0]
        else:
            return ""

    def state(self):
        import re
        info = self.vminfo()
        state = re.findall("State:\s+(.*)", info)[0]
        state = state.split()[0]
        return state

    def start(self, gui=""):
        """
        Start virtual Machine

        @param gui: GUI type
        @type gui: str

        gui:
            ""       Empty string [default] Start VM without GUI
            gui      Simple GUI without controls in the background execute command:
            sdl      Start VM using a simple GUI
            seamless Start VM in seamless mode
            vrdp
            headless Start With no GUI
        """
        if gui !="":
            _gui = "--type %s" % gui
        else:
            _gui = ""

        out, err =  execute("vboxmanage startvm %s %s" %  (self.uuid, _gui))
        print out, err

    def start_headless(self, vncport=None, passw=None):

        if vncport is not None:
            vnc = "--vnc --vncport %s --vncpass %s" % (vncport, passw)
        else:
            vnc = ""

        out, err = execute("VBoxManage startvm %s --type headless " % self.uuid + vnc)
        print out, err

    #   out, err = execute("VBoxHeadless --startvm Crunchbang --vnc --vncport 5901 --vncpass passw")

    def stop(self):
        """
        Do the same as self.savestate(),
        it is an alias to savestate(),

        Save VM satate and shutdown()
        """
        # VBoxManage controlvm "slackware" savestate
        out, err =  execute("vboxmanage controlvm %s savestate" %  self.uuid)
        print out, err


    def pause(self):
        # VBoxManage controlvm "slackware" pause
        out, err =  execute("vboxmanage controlvm %s pause" %  self.uuid)
        print out, err


    def resume(self):
        # VBoxManage controlvm "slackware" pause
        out, err =  execute("vboxmanage controlvm %s resume" %  self.uuid)
        print out, err


    def savestate(self):
        self.stop()

    def poweroff(self):
        #VBoxManage controlvm "CentOS" poweroff soft
        # Safe shutdown virtual machine
        out, err = execute("vboxmanage controlvm %s poweroff" % self.uuid)

    def reset(self):
        # VBoxManage controlvm "Ubuntu 11.04 Server" reset
        out, err = execute("vboxmanage controlvm %s reset" % self.uuid)
        print out, err


    def removevm(self):
        """
        WARNING: Completely removes the virtual machine
        """
        # VBoxManage unregistervm "<vmname/uuid>" --delete
        out, err = execute("vboxmanage unregistervm %s --delete" % self.uuid)
        print out, err

    def attachUSB(self, deviceUuid):
        """
        Attach the usb-device:
        """
        out, err = execute("vboxmanage controlvm %s usbattach %s" % ( self.uuid, deviceUuid))
        print out, err

    def detachUSB(self, deviceUuid):
        """
        detach the usb-device:

        """
        out, err = execute("vboxmanage controlvm %s usbdetach %s" % ( self.uuid, deviceUuid))
        print out, err

    def attachDVD(self, isofile):
    # VBoxManage controlvm "<vmname/uuid>" dvdattach "<filename>"
        out, err = execute("vboxmanage controlvm %s dvdattach %s" % ( self.uuid, isofile))
        print out, err

    def dettachDVD(self):
        out, err = execute("VBoxManage modifyvm %s --dvd none" % self.uuid)
        print out, err

    def screenshot(self, path="screenshot.png"):
        """
        path - path to image

        Take screenshot of virtual machine and save to *.png image.

        """
        out, err = execute("VBoxManage controlvm %s screenshotpng %s" % (self.uuid, path))
        print out, err

    def addFolder(self, name, path):
        """
        Add shared folder to the guest OS

        """
        # VBoxManage sharedfolder add MediaServer --name UserData --hostpath /media/UserData
        cmd = "VBoxManage sharedfolder add %s --name %s --hostpath %s" % (self.uuid, name, path)
        out, err = execute(cmd)
        print out + '\n' + err

    def takeSnapshot(self, name, description="backup snapshot"):
        # VBoxManage snapshot "CentOS" take snap1-stable-system
        #
        #  VBoxManage snapshot <guest> take <name> [-desc <description>]
        #
        cmd = 'VBoxManage snapshot %s take %s -desc "%s"' % (self.uuid, name, description)
        out, err = execute(cmd)
        print out + '\n' + err


    def infoSnapshot(self):
        cmd = " vboxmanage snapshot %s list" % self.uuid
        out, err = execute(cmd)
        return  out + '\n' + err

    def getSnapshots(self):
        """
        Return snapshot data in the following way:

        Returns:
            [(name1, uuid1, desc1), (name2, uuid2, desc2), .... ]
             [ (str, str, str) ... ]

        """
        import re

        txt = self.infoSnapshot()

        names= re.findall('Name:\s+(.*)\(', txt)
        desc = re.findall('Description:\n(.*)', txt)
        uuids = re.findall('UUID:(.*)\)', txt)

        return zip(names, uuids, desc)

    def currentSnapshot(self):
        """
        Returns the current state snapshot

        """
        import re
        txt = self.infoSnapshot()
        return re.findall('Name:\s+(.*)\s+\(UUID:\s+(.*)\)\s+\*', txt)[0]


    def restoreSnapshot(self, uuid):
        """
        Restore snapshot

        @param uuid: Snapshot uuid
        @type  uuid: str
        """
        # VBoxManage snapshot vm04-zca8 restore snap1-before-upgrade
        cmd = "VBoxManage snapshot %s restore %s" % (self.uuid, uuid)
        out, err= execute(cmd)
        return out + '\n' + err

    def deleteSnapshot(self, uuid):
        """
        Delete snapshot

        @param uuid: Snapshot uuid
        @type  uuid: str
        """
        cmd = "VBoxManage snapshot %s delete %s" % (self.uuid, uuid)
        out, err= execute(cmd)
        return out + '\n' + err

    def modifyMemory(self, size):
        """
        Set RAM memory size in MB
        """
        #VBoxManage modifyvm "LinuxMint -memory "1024MB"
        out, err = execute('VBoxManage modifyvm %s --memory "%d"' % (self.uuid, size))
        print out, err

    def modifyName(self, name):
        """
        Modify Virtual Machine Name

        """
        #VBoxManage modifyvm "LinuxMint -memory "1024MB"
        out, err = execute('VBoxManage modifyvm %s --name "%s"' % (self.uuid, name))
        print out, err


    def vrpdOn(self):
        cmd = "VBoxManage modifyvm %s --vrde off" % self.uuid
        execute(cmd)

    def vrpdOff(self):
        cmd = "VBoxManage modifyvm %s --vrde off" % self.uuid
        execute(cmd)


    def command(self, gcommand, username="oc", password="windows"):
        #VBoxManage guestcontrol WindowsXP exec --image c:\\program\ files\\Internet\ Explorer\\IEXPLORE.EXE --username owner --password password

        cmd = "VBoxManage guestcontrol %s exec --image %s --username %s --password %s "  % (self.uuid, gcommand, username, password)
        print cmd
        out, err = execute(cmd)
        return out, err

    def listsmb(self):
        """
        List shared smb volumes

        """
        ip = self.getIp()
        cmd = "smbclient -L %s -U %s%%%s" % (ip, self.username, self.password)
        out, err = execute(cmd)
        return out

    def mountsmb(self, share, mountpoint):
        ip = self.getIp()
        cmd = "sudo mount -t cifs -o rw -o iocharset=utf8  //%s/%s  %s -o username=%s,password=%s,domain=workgroup," \
              "file_mode=0775,dir_mode=0775,uid=1000,gid=1000"
        cmd = cmd %  (ip, share, mountpoint, self.username, self.password)
        print cmd
        out, err = execute(cmd)
        return out+'\n'+err


    def export(self, outptut, vsys=0, **kwargs):
        """
        Export Virtual Machine

        Argumenst
            output=<ovf,ova>
            [product=<product_name>]
            [vendor=<vendor_name>]
            [version=<version_name>]
            [description=<description>]


        e.g:
            self.export(output="/home/t1/appliance.ova", vsys='v', product="Windows7", description="desc")

        """
        from subprocess import call

        arguments = ""
        for key, value in kwargs.iteritems():
            arguments += " --%s '%s'" % (key, value)

        cmd = "vboxmanage export %s --output %s --vsys %s %s" % (self.uuid, outptut, vsys,  arguments)

        print "\nExporting Virutal Machine -- Executing \n%s" % cmd
        call(cmd, shell=True)
        #out, err = execute(cmd)
        #print out + '\n' + err



    @classmethod
    def getvms(cls):
        import re
        out, err = execute("vboxmanage list vms")
        vms = re.findall('\"(.*)\"' ,out)
        uuids = re.findall("\{(.*)\}", out)

        VMS = zip(vms, uuids)

        return VMS

    @classmethod
    def runningvms(cls):
        out, err = execute("vboxmanage list runningvms")
        return out

    @classmethod
    def listbridges(cls):
        """
        List Bridge Adapters

        """
        out, err = execute("VBoxManage list bridgedifs")
        return out

    @classmethod
    def listhosts(cls):
        """
        List Host Adapters
        """
        out, err = execute("VBoxManage list hostonlyifs")
        return out

    @classmethod
    def listdvds(cls):
        out, err = execute("vboxmanage list dvds")
        return out

    @classmethod
    def registervm(cls, vboxfile):
        """
        Register Virtual Machine given the configuration file

        VBoxManage registervm <full path - xml filename.vbox>
        """
        out, err = execute("vboxmanage registervm %s" % vboxfile)
        return out

    @classmethod
    def gui(cls):
        #from subprocess import call
        execute("virtualbox &")

#print getvms()
#Vbox.getVMS
# print Vbox.getvms()
#
# print Vbox.listbridges()
#
# v = Vbox('88196687-12d0-4442-a2a2-56626c7047ae')
# v.username = 'oc'
# v.password = 'windows'
