#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interactive VirtualBox Launcher

"""

from libvbox import Vbox




def getOption():
    while True:
        try:
            opt = raw_input(">> ")

            if opt == '-':
                return opt

            return int(opt)

        except (KeyboardInterrupt, ValueError):
            pass

def selectMachine():
    idx= 1

    print "Choose a Virtual Machine\n- To cancel"

    for v, u in Vbox.getvms():
        print "%d\t%s\t%s" % (idx, v, u)
        idx +=1

    vms = Vbox.getvms()

    while True:
        try:
            opt = raw_input(">> ")

            if opt == '-':
                return None

            idx = int(opt)
            return vms[idx-1]

        except (KeyboardInterrupt, ValueError):
            pass





from subprocess import Popen

import os
import sys

name, uuid =Vbox.getvms()[0]
VM = Vbox(uuid)


options = [ 'Select a Virtual Machine',
            'Show Virtual Machine Summary',
            'Start',
            'Start Headless',
            'Stop (Save State)',
            'Shutdown - Poweroff',
            'Take Snapshot',
            'Revert to Snapshot',
            'Take Screenshot',
            'Remote Desktop',
            'Show Virtual Machines',
            'Show Running Machines',
            'Ipython Shell - Variable VM',
            'Exit\t[-]']

#print options

while True:


    print "\tVIRTUALBOX SHORTCUT"
    print "\t--------------------"

    for i, o in enumerate(options, start=1):
        print "%d\t%s" % (i, o)

    opt = getOption()

    if opt == '-':
        sys.exit(0)

    if opt == 1:
        name, uuid = selectMachine()
        VM = Vbox(uuid)
        #print VM

    elif opt ==  2:
        print VM

        print "\nCurrent Snapshot"
        print VM.currentSnapshot()
        print "\nVirtual Machine address"
        print VM.getIp()

    elif opt == 3:
        print VM.start()

    elif opt == 4:
        print VM.start('vrdp')

    elif opt == 5:
        print VM.stop()

    elif opt == 6:
        print VM.poweroff()

    elif opt == 7:



        snapshot = raw_input("Snapshot Name >> ")
        desc = raw_input("Description >> ")
        VM.takeSnapshot(snapshot, desc)

    elif opt == 8:

        current, uuid = VM.currentSnapshot()
        print "Current Snapshot: %s - %s\n" % (current, uuid)

        idx =1

        s= VM.getSnapshots()

        for snapshot, uuid, desc in s:
            print "%d %s\t%s\n%s\n" % (idx, snapshot, uuid, desc)
            idx+=1

        print "Revert to previous snapshot n-no/y-yes ?"
        q = raw_input(">> ")
        q = q.strip()
        if q == 'y':
            while True:
                try:
                    n = raw_input("Choose the corresponding snapshot number, -  to cancel\n>> ")
                    n = int(n)
                    break
                except (KeyboardInterrupt, ValueError):
                    pass

            try:
                name, uuid, desc = s[n-1]
                print "Reverting Virtual Machine to Snapshot:"
                print name, uuid
                VM.restoreSnapshot(uuid)
            except (IndexError, ValueError) as err:
                print err

    elif opt == 9:
        print VM.screenshot()

    elif opt == 10:
        print "Remote Desktop"
        cmd = "rdesktop  -z %s &" % VM.getIp()
        Popen(cmd, shell=True)

    elif opt == 13:
        print "Ipython Shell"
        import IPython ;  IPython.embed()

    raw_input("Hit return to continue")
        #p = call("",shell=True)


# msg= "Choose a Machine\nEnter exit to quit\n\n"
# d = getVMStates()
# m = choose_menu(d.iteritems(), msg=msg)
#
# print m