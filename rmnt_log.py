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
    '0x210600A1': { description: 'NTC_HTTP_CLIENT_INVALID_PARAM', items: [] },
    '0x210600A2': { description: 'NTC_HTTP_CLIENT_OUT_OF_RESOURCE', items: [] },
    '0x210600A3': { description: 'NTC_HTTP_CLIENT_COMMUNICATION_ERROR', items: [] },
    '0x210600A4': { description: 'NTC_HTTP_CLIENT_PROCESSING', items: [] },
    '0x210600A5': { description: 'NTC_HTTP_CLIENT_XMPP_LOGIN', items: [] },
    '0x210600A6': { description: 'NTC_HTTP_CLIENT_INTERNAL_ERROR', items: [] },
    '0x210600A7': { description: 'NTC_HTTP_CLIENT_AUTHENTICATION_ERROR', items: [] },
    '0x210600A8': { description: 'NTC_HTTP_CLIENT_REQUEST_ERROR', items: [] },
    '0x210600A9': { description: 'NTC_HTTP_CLIENT_SERVER_ERROR', items: [] }

    #'0x00000020': { description: 'YourErrorHere', items: [] }
    
}
###########------------FUNCTIONS----------------############

#output summary
def output_summary(line, display):

    try:
        errorValue = re.findall('.x[A-Za-z0-9]{8}|.x[A-Za-z0-9]{4}', line)
    except:
        errorValue = ''; #Set to null or do nothing
    
    for val in errorValue:
        try:
            output[val][items].append([display])
        except: 
            fcall = re.search('(Fcode)+', line) # Search for error.
            if(fcall != None):
                output['fcall'][items].append([display])
    


# Extract all tar.gz related to component
def extract(newDirLog,summary,tarList_RMNT):
    for (dirpath, dirnames, filenames) in os.walk(newDirLog):
        for file in filenames:
            if file.endswith('.gz'):
                for component_gz in tarList_RMNT:
                    if(file == component_gz):
                        summary.write('\nExtract OK: '+file)
                        print('Extract OK: '+file)
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
                            summary.write('\nGet OK: '+ component_file)
                            print('Get OK: '+ component_file)
                            listOfFiles.append(os.path.join(dirpath, file))

# WC3 finding error
def findErrorWC3(fileName,num,line,summary):
    
    result = None
    hasError = False
    isFound = re.search('(usv_mnt|ifs_rmnt)\w|(process_down|Fcode)', line)
    
    if(isFound != None):
        result = re.search('(ERROR|ERR)|(process_down|Fcode)|(ret:?(\[?0x[A-Za-z0-9]{8}\]?))+', line) # Search for error.
        #print('found match [result]: '+ str(result) +'\n')
        
        if(result != None):
            result = re.search('(ret):?(\[?0x00000000\])+',line)
            
            if(result == None):
                hasError = True
            else:
                hasError = False
            #print('Line: '+ line +'\n')
            #print('found match [result]: '+ str(isError) +'\n')
        
    
    if(hasError == True):
        print('LINE:['+ str(num+1) +']\n'+ line)
        output_summary('>filename: '+ fileName +' line:['+ str(num+1) +']\n '+ line, '>filename: '+ fileName +' / line:['+ str(num+1) +']')
        summary.write('\nLINE:['+ str(num+1) +']\n'+ line)
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
        summary.write('\nLINE:['+ str(num+1) +']\n'+ line)
        print('LINE:['+ str(num+1) +']\n'+ line)
        return True


# Filter all files for errors related to component
def findError(listOfFiles,summary,arch):
    for file in listOfFiles:
        summary.write('\nSearching filename: '+ file)
        print('Searching filename: '+ file)

        #get only the file name
        fileName = file[file.rfind("\\"):]
        fileName = fileName[1:]

        isErrorFound = False

        with io.open(file, 'r', encoding='ISO-8859-1') as f:
            text = f.readline()
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
            print("****No Errors Found****\n\n")
            summary.write("****No Errors Found****\n\n")        
        else:
            print("\n\n")
            summary.write("\n\n")
            


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
            'rmnt_log_fcall.log'
            ]

    else:
        print("Do Nothing")
   
    #Extract all tar.gz related to component
    summary.write('\n\nExtracting files...')
    print('\n\nExtracting files...')
    extract(newDirLog,summary,tarList_RMNT)
    summary.write('\nExtracted to -> files\debug_log\RMNT_EXTRACTED')
    print('Extracted to -> files\debug_log\RMNT_EXTRACTED')

    # Get all related files of RMNT component
    listOfFiles = list() #container
    summary.write('\n\nGetting all related files of the component...')
    print('\n\nGetting all related files of the component...')
    getfiles(newDirLog,summary,fileList_RMNT,listOfFiles)

    # Filter all files for errors related to component
    summary.write('\n\nSearching for errors...')
    print('\n\nSearching for errors...')
    findError(listOfFiles,summary,arch)

    print('*********************** LOG SUMMARY ***********************\n')
    for i in output:

        if len(output[i][items]) != 0:
            print('==============================================')
            print(''+i+ ': '+str(output[i][description]) + '\n')
            for item in output[i][items]: 
                print(str(item[0]))

    print('*********************** END LOG SUMMARY ***********************')
