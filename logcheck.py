#! python3
import os
import tarfile
import io
import re
import sys

# Global declarations
#dirLog = sys.argv[1] # command line argument.
dirLog = 'C:\\Users\\Anthony S\\Documents\\WFH\\V7A6400539_202004071341\\log'
dirLogExtracted = dirLog+'\\files\\debug_log\\RMNT_EXTRACTED'

# Customize for RMNT checking.
tarList_RMNT = [ 'usv_mnt_tmms.tar.gz', 'ifs_rmnt_log.tar.gz']
fileList_RMNT = ['all.log', 'stacktrace.svc_proc.log','ifs_rmnt.log' 'usv_mnt.log', 'usv_mnt_tmms_comm.log', 'usv_mnt_tmms_exec.log']
listOfFiles = list()

summary = open(dirLog+'\\LOG_CHECKER.txt', 'w')
summary.write('Checking log: '+ dirLog)
summary.close()

# Extract all tar.gz related to component
summary = open(dirLog+'\\LOG_CHECKER.txt', 'a')
summary.write('\n\nExtracting files...')
print('\n\nExtracting files...')
for (dirpath, dirnames, filenames) in os.walk(dirLog):
    for file in filenames:
        if file.endswith('.gz'):
            for component_gz in tarList_RMNT:
                if(file == component_gz):
                    summary.write('\nExtract OK: '+file)
                    print('Extract OK: '+file)
                    tf = tarfile.open(dirpath+'\\'+file, "r:gz")
                    tf.extractall(dirpath+'\\RMNT_EXTRACTED\\'+file)
                    tf.close()
summary.write('\nExtracted to -> files\debug_log\RMNT_EXTRACTED')
print('Extracted to -> files\debug_log\RMNT_EXTRACTED')


# Get all related files of RMNT component
summary.write('\n\nGetting all related files of the component...')
print('\n\nGetting all related files of the component...')
for (dirpath, dirnames, filenames) in os.walk(dirLog):
    for file in filenames:
            if file.endswith('.log'):
                for component_file in fileList_RMNT:
                    if(file == component_file):
                        summary.write('\nGet OK: '+ component_file)
                        print('Get OK: '+ component_file)
                        listOfFiles.append(os.path.join(dirpath, file))
                        #listOfFiles += [os.path.join(dirpath, file) for file in filenames]    

# Filter all files for errors related to component
summary.write('\n\nSearching for errors...')
print('\n\nSearching for errors...')
for file in listOfFiles:
    summary.write('\nSearching filename: '+ file)
    print('Searching filename: '+ file)
    with io.open(file, 'r', encoding='utf8') as f:
        text = f.readline()
        for num, line in enumerate(f, 1): # Line per line checking of code.
            isExist = re.search('USV_MNT', line) #Check for USV_MNT
            if(isExist != None):
                # Modify to complex error checking conditions
                
                isExist = re.search('ERR', line) # Search for error.
                

                # END Modify
                if(isExist != None): #If found store here
                    summary.write('\nLINE:['+ str(num+1) +']\n'+ line)
                    print('LINE:['+ str(num+1) +']\n'+ line)
                
summary.close()
print('\n\n\nCheck done!\n')
print(dirLog+'\\LOG_CHECKER.txt created for summary')
#for (dirpath, dirnames, filenames) in os.walk(dirLogExtracted):
    #listOfFiles += [os.path.join(dirpath, file) for file in filenames]
