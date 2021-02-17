#! python3
import tarfile
import os
import io
import re
import json

##########----Global declarations-------###########
WC3  = 0
WC4s = 1
description = 'description'
items = 'items'
output = {
    '0x00000001': { description: 'Common error', items: [] },
    '0x00000002': { description: '[HTTP] invalid parameter.', items: [] },
    '0x00000003': { description: '[HTTP] out of resource.', items: [] },
    '0x00000004': { description: '[HTTP] communication error.', items: [] },
    '0x00000005': { description: '[HTTP] processing error.', items: [] },
    '0x00000006': { description: '[HTTP] XMPP login error.', items: [] },
    '0x00000007': { description: '[HTTP] internal error.', items: [] },
    '0x00000008': { description: '[HTTP] authentication error..', items: [] },
    '0x00000009': { description: '[HTTP] request error(HTTP error)..', items: [] },
    '0x00000010': { description: '[HTTP] server error (HTTP error)..', items: [] },
    '0x00000011': { description: '[HTTP] client error (HTTP error)..', items: [] },
    '0x00000012': { description: '[HTTP] aborted..', items: [] },
    '0x00000013': { description: '[HTTP] unknown error..', items: [] },
    '0x00000014': { description: '[XMPP] invalid parameter..', items: [] },
    '0x00000015': { description: '[XMPP] out of resource..', items: [] },
    '0x00000016': { description: '[XMPP] communication error..', items: [] },
    '0x00000017': { description: '[XMPP] XMPP login error..', items: [] },
    '0x00000018': { description: '[XMPP] internal error..', items: [] },
    '0x00000019': { description: '[XMPP] unknown error.', items: [] },
    '0x00000020': { description: '[Network] invalid parameter.', items: [] },
    '0x00000021': { description: '[Network] out of resource.', items: [] },
    '0x00000022': { description: '[Network] communication error.', items: [] },
    '0x00000023': { description: '[Network] processing error.', items: [] },
    '0x00000024': { description: '[Network] XMPP login error.', items: [] },
    '0x00000025': { description: '[Network] internal error.', items: [] },
    '0x00000026': { description: '[Network] client error (HTTP error).', items: [] },
    '0x00000027': { description: '[Device Internal] system menu open.so not use xmpp cmd.', items: [] },
    '0x00000028': { description: '[Device Internal] Maintenance mode in .so not use xmpp cmd.', items: [] },
    '0x00000029': { description: 'User Reject', items: [] },
    'others': { description: 'Unfiltered errors', items: [] },
    'fcall': { description: 'FCALL / Segmentation fault', items: [] },
    '0x000000A1': { description: '0xA3 NTC_HTTP_CLIENT_INVALID_PARAM', items: [] },
    '0x000000A2': { description: '0xA2 NTC_HTTP_CLIENT_OUT_OF_RESOURCE', items: [] },
    '0x000000A3': { description: '0xA3 NTC_HTTP_CLIENT_COMMUNICATION_ERROR', items: [] },
    '0x000000A4': { description: '0xA4 NTC_HTTP_CLIENT_PROCESSING', items: [] },
    '0x000000A5': { description: '0xA5 NTC_HTTP_CLIENT_XMPP_LOGIN', items: [] },
    '0x000000A6': { description: '0xA6 NTC_HTTP_CLIENT_INTERNAL_ERROR', items: [] },
    '0x000000A7': { description: '0xA7 NTC_HTTP_CLIENT_AUTHENTICATION_ERROR', items: [] },
    '0x000000A8': { description: '0xA8 NTC_HTTP_CLIENT_REQUEST_ERROR', items: [] },
    '0x000000A9': { description: '0xA9 NTC_HTTP_CLIENT_SERVER_ERROR', items: [] }

    #'0x00000020': { description: 'YourErrorHere', items: [] }
    
}
###########------------FUNCTIONS----------------############

def logging(summary, description):
    print(description)
    summary.write(description)
    
#filter error codes
def output_summary(line, display):

    fcall = re.search('(Fcode)+', line) # Search for error.

    if(fcall != None):
        output['fcall'][items].append([display])
        return
    else:
        errorValue = re.findall('.x[A-Za-z0-9]{8}', line) #gets all matches
        if(len(errorValue) == 0): return
        
        for val in errorValue:
            tmp_val = "0x000000"+str(val[-2:])
            # try catch block for key error issue.
            try: output[tmp_val][items].append([display])
            except: pass
                

# Extract all tar.gz related to component
def extract(newDirLog,summary,tarList_RMNT):
    for (dirpath, dirnames, filenames) in os.walk(newDirLog):
        for file in filenames:
            if file.endswith('.gz'):
                for component_gz in tarList_RMNT:
                    if(file == component_gz):
                        logging(summary, '\nExtract OK: '+file)
                        tf = tarfile.open(dirpath+'\\'+file, "r:gz")
                        tf.extractall(dirpath+'\\RMNT_EXTRACTED\\'+file)
                        tf.close()

# Get all related files of RMNT component
def getfiles(newDirLog,summary,fileList_RMNT,listOfFiles):
    for (dirpath, dirnames, filenames) in os.walk(newDirLog):
        for file in filenames:
                if file.endswith('.log'):
                    for component_file in fileList_RMNT:
                        if(file == component_file):
                            logging(summary, '\nGet OK: '+ component_file)
                            listOfFiles.append(os.path.join(dirpath, file))

# Get all related files of RMNT component
def getME_TMMS_DATA(newDirLog,summary):
    for (dirpath, dirnames, filenames) in os.walk(newDirLog):
        for file in filenames:
                if file.endswith('.log'):
                                #WC4 log                                            #WC3 log
                    if(file == 'dbs_me_debug_status_member_svc_proc.log' or file == 'dbs_me_debug_status_member_sysbase_proc.log'):
                        logging(summary, 'dbs_me file found! \n')
                        with io.open(os.path.join(dirpath, file), 'r', encoding='ISO-8859-1') as f:
                            for num, line in enumerate(f, 1): # Line per line checking of code.
                                isTMMS = re.search('(TMMS)', line)
                                if(isTMMS != None):
                                    try:
                                        logging(summary, ''+line)
                                    except:
                                        # Encoding error, cant store its value in a .txt file
                                        pass
                        

# WC3 finding error
def findErrorWC3(fileName,num,line,summary):
    
    result = None
    hasError = False
    isFound = re.search('(usv_mnt|ifs_rmnt)\w|(process_down|Fcode)', line)
    
    if(isFound != None):
        result = re.search('(ERROR|ERR)|(process_down|Fcode)|(ret:?(\[?0x[A-Za-z0-9]{8}\]?))+', line) # Search for error.
        
        if(result != None):
            result = re.search('(ret):?(\[?0x00000000\])+',line)
            
            if(result == None):
                hasError = True
            else:
                hasError = False
    
    if(hasError == True):
        logging(summary, '\nline:['+ str(num+1) +'] '+ line)
        output_summary('>filename: '+ fileName +' line:['+ str(num) +']\n '+ line, '>filename: '+ fileName +' / line:['+ str(num) +']')
        return True
    else:
        return False

# WC4s finding error
def findErrorWC4(fileName,num,line,summary):

    isError = False
    isExistERR = None

    if( 'all.log' == fileName ):
        isExist_USV_MNT = re.search('MNT_APS', line)
        if(isExist_USV_MNT!=None): 
            isExistERR = re.search('ERR', line) # Search for error.

    elif( 'comm_wcl_debug.log' == fileName or 'comm_msg_debug.log' == fileName ):
        isExistRet = re.search('Ret', line)
        isExist_cmp_http_ret = re.search('cmp_http_ret', line)
        if( isExistRet!=None or isExist_cmp_http_ret!=None ): 
            retValue = line[line.rfind("["):]
            retValue = retValue[1:11]
            if(retValue != "0x00000000"): isError = True

    elif('rmnt_log_fcall.log' == fileName):
        isError = True  #output all since it contains the error info  //TODO: find rmnt_log_fcall.log that has contents         
            
    else: #for other files
        isExistERR = re.search('ERR', line)


    if( isExistERR != None or isError == True ): #If found store here
        logging(summary, '\nline:['+ str(num+1) +'] '+ line)
        output_summary('>filename: '+ fileName +' line:['+ str(num) +']\n '+ line, '>filename: '+ fileName +' / line:['+ str(num) +']')
        return True


# Filter all files for errors related to component
def findError(listOfFiles,summary,arch):
    for file in listOfFiles:
        logging(summary, '\nSearching filename: '+ file)
        #get only the file name
        fileName = file[file.rfind("\\"):]
        fileName = fileName[1:]

        isErrorFound = False

        with io.open(file, 'r', encoding='ISO-8859-1') as f:
            for num, line in enumerate(f, 1): # Line per line checking of code.
                if( WC3 == arch ):
                    isFound = findErrorWC3(fileName,num,line,summary)
                    if( isFound == True ): isErrorFound = True #Always True once error is recorded

                elif(WC4s == arch):
                    isFound = findErrorWC4(fileName,num,line,summary)
                    if( isFound == True ): isErrorFound = True #Always True once error is recorded       
                else:
                    print("Do Nothing")    
        
        if( isErrorFound == False ):
            logging(summary, '****No Errors Found****\n\n')  
        else:
            logging(summary, '\n\n')
            


###########----------MAIN EXECUTION---------------#############
def exec(arch,dirLog,newDirLog,summary,logFileName):
    
    summary = open(dirLog+'\\xx_'+logFileName+'.txt', 'a')
    summary.write('Checking log: '+ newDirLog)

    #Setting tarList for RMNT logs
    if( WC3 == arch ):
        tarList_RMNT = [
            'usv_mnt_tmms.tar.gz', 
            'ifs_rmnt_log.tar.gz'
            ]
        fileList_RMNT = [
            'all.log', 
            'stacktrace.svc_proc.log',
            'ifs_rmnt.log',
            'usv_mnt.log', 
            'usv_mnt_tmms_comm.log', 
            'usv_mnt_tmms_exec.log'
            ]
        
    elif( WC4s == arch ):
        tarList_RMNT = [
            'rmnt_log.tar.gz'
            ] 
        fileList_RMNT = [
            'all.log',
            'comm_wcl_debug.log',
            'comm_msg_debug.log',
            'rmnt_log_comm.log',
            'rmnt_log_dv_exec.log',
            'rmnt_log_exec.log',
            'rmnt_log_fcall.log',
            #rebooting log rearding import/export function
            'BeforeRestart_RMNT.log',
            #FW Updating log
            'mnt_app_fwupdate.log'
            ]

    else:
        print("Do Nothing")
   
    #Extract all tar.gz related to component
    logging(summary, '\n\nExtracting files...')
    extract(newDirLog,summary,tarList_RMNT)
    logging(summary, '\nExtracted to -> files\debug_log\RMNT_EXTRACTED')

    # Get TMMS Data
    logging(summary, '\n\nGetting TMMS ME Data...\n')
    getME_TMMS_DATA(newDirLog, summary)
    
    # Get all related files of RMNT component
    listOfFiles = list() #container
    logging(summary, '\n\nGetting all related files of the component...')
    getfiles(newDirLog,summary,fileList_RMNT,listOfFiles)

    # Filter all files for errors related to component
    logging(summary, '\n\nSearching for errors...')
    findError(listOfFiles,summary,arch)

    logging(summary, '*********************** LOG SUMMARY ***********************')
    for i in output:

        if len(output[i][items]) != 0:
            logging(summary, '\n==============================================\n')
            logging(summary, ''+i+ ': '+str(output[i][description]) + '\n')
            for item in output[i][items]:
                logging(summary, str(item[0])+'\n')
    logging(summary, '\n*********************** END LOG SUMMARY ***********************')
