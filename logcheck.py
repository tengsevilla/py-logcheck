#! python3
import tarfile
import sys
import os
import time
import shutil #Remove folder 
import rmnt_log #RMNT Component

##########----Global declarations-------###########

log_1 = sys.argv[1] #because log 1 cannot be empty
#log_1 = 'E:\\Dump files\\October\\2V6-3599\\Iter2 Failed FWUpdate\\log.tar.gz'
#sys.argv[1] # command line argument.
#Example: log_1 = C:\Users\Raffy\Desktop\WFH\TEST_PYTHON\log.tar.gztest
try: log_2 = sys.argv[2]
except: log_2 = "empty"
try: log_3 = sys.argv[3]
except: log_3 = "empty"
try: log_4 = sys.argv[4]
except: log_4 = "empty"
try: log_5 = sys.argv[5]
except: log_5 = "empty"

logList = [log_1,log_2,log_3,log_4,log_5]

archList = ['WC3','WC4s']

componentList = ['RMNT','KSF','DCM']

##########---------FUNCTIONS------------###########
def archInput():
    arch = 0
    print('\n===============================')
    print('Select architecture:\n1 - WC3\n2 - WC4s')
    arch = int(input('Please enter the number: '))
    if arch == 1: return 0
    elif arch == 2: return 1
    else:
        print("Your input is invalid!!")

def componentInput():
    component = 0
    print('\n===============================')
    print('\nSelect component:\n1 - RMNT\n2 - KSF\n3 - DCM')
    component = int(input("Please enter the number: "))
    if component == 1: return 0
    elif component == 2: return 1
    elif component == 3: return 2
    else:
        print("Your input is invalid!!")


def main(dirLog,logFileName):
    summary = open(dirLog+'\\xx_'+logFileName+'.txt', 'w')
    summary.write('Extracting... '+ logFileName)
    print('Extracting... '+ logFileName)
    summary.close()

    #creating unique directory for the logfile
    newDir = dirLog+logFileName[:-2]

    if not os.path.exists(newDir): # if the directory does not exist
        os.mkdir(newDir) 
    else: # else overwrite file
        try:
            shutil.rmtree(newDir)
            time.sleep(.5) #delay
            os.mkdir(newDir)
        except:
            print('\n\n\n!!!!!!! ERROR !!!!!!!')
            print('Can not override the file when it is opened!!!')
            print('Close the file under '+ newDir +' to proceed')
            print('\nPlease try again.\n\n')
            raise
        
    #initial extraction of the log file
    tf = tarfile.open(logFile,"r:gz")
    tf.extractall(newDir) 

    print("Extraction Finish!")
    newDirLog = newDir+'\\log' #a new \log directory after initial extraction

    arch = archInput()

    if( int(archList.index('WC3')) == arch ):
        print("WC3")
        component = componentInput()

        if( int(componentList.index('RMNT')) == component ):
            print("WC3-RMNT")
            rmnt_log.exec(arch,dirLog,newDirLog,summary,logFileName)

        elif( int(componentList.index('KSF')) == component ):
            print("WC3-KSF")

        elif( int(componentList.index('DCM')) == component ):
            print("WC3-DCM")

        else:
            print("End")


    elif( int(archList.index('WC4s')) == arch ):
        print("WC4s")
        component = componentInput()

        if( int(componentList.index('RMNT')) == component ):
            print("WC4s-RMNT")
            rmnt_log.exec(arch,dirLog,newDirLog,summary,logFileName)

        elif( int(componentList.index('KSF')) == component ):
            print("WC4s-KSF")

        elif( int(componentList.index('DCM')) == component ):
            print("WC4s-DCM")

        else:
            print("End")


    else:
        print("End")

    summary.close()
    print('\n\nLogchecker done...')
    print('Created a .txt file. Open the file with the provided link below')
    print(dirLog+"xx_"+logFileName+'.txt'+'')
    
    print('\n\n')


##########-------MAIN EXECUTION---------###########

for logFile in logList:

    if(logFile != "empty"):
        dirLog = logFile[:logFile.rfind("\\")] + "\\"
        #Example: dirLog = C:\Users\Raffy\Desktop\WFH\TEST_PYTHON\

        logFileName = logFile[logFile.rfind("\\"):]
        logFileName = logFileName[1:]  #to remove \
        #Example: logFileName = \log.tar.gz

        main(dirLog,logFileName)

