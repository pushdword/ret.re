#!/bin/env python3
import os
def process_imap_folders(M,dir):
    for i in M.list()[1]:
        l = i.decode().split(' "/" ')
        rv, data = M.select(l[1])
        print(rv)
        print("DATA:")
        print(data)
        process_mailbox(M,dir)

def process_mailbox(M,dir):
    """
    Dump all emails in the folder to files in output directory.
    """
    
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    for num in data[0].split():
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message:"+str(num))
            return
        print("Writing message "+ str(num))
        if not os.path.exists(dir):
            os.makedirs(dir)
        f = open('%s/%s.eml' %(dir, str(num)), 'wb')
        f.write(data[0][1])
        f.close()