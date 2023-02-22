#!/usr/bin/env python

import PySimpleGUI as sg
import pandas as pd
import sys
import pdb

def main():
    while True:
        filters = initgui()
        evtfile = filters.pop(0)
        csvfile = filters.pop(1)
        filters = list(filter(filters.get, filters))
        dfevt = getdf(evtfile, filters, ftype='evt')
        batchid = dfevt['BatchID'].iloc[0]
        dfcsv = getdf(csvfile, filters, ftype='BHIST')
        dfcsv = dfcsv[dfcsv['batchid']==batchid]
        dfcsv.reset_index()
        dfevt.reset_index()
        diff = compare(dfcsv, dfevt, batchid)
        filtered = dfevt.iloc[diff]
        displaylog(filtered, batchid)

def initgui():
    file_frame =[
        [sg.T('Event File (.evt)')],
        [sg.I(disabled=True,expand_x=True),sg.FileBrowse(file_types=(('Windows Event','*.evt'),),key=None)],
        [sg.T('BHist Export (.csv)')],
        [sg.I(disabled=True,expand_x=True),sg.FileBrowse(file_types=(('Comma Separated Values','*.csv'),),key=None)],
    ]
    para_frame = [
        [sg.Checkbox('B_ARP_TEXT',key='B_ARP_TEXT'),sg.Checkbox('B_CRP_TEXT',key='B_CRP_TEXT'),sg.Checkbox('B_ERP_TEXT',key='B_ERP_TEXT'),sg.Checkbox('B_FRP_TEXT',key='B_FRP_TEXT')],
        [sg.Checkbox('B_GRP_TEXT',key='B_GRP_TEXT'),sg.Checkbox('B_PRP_TEXT',key='B_PRP_TEXT'),sg.Checkbox('B_RRP_TEXT',key='B_RRP_TEXT')],
    ]
    layout = [
        [sg.Frame('Select Files',file_frame,expand_x=True)],
        [sg.Frame('Report Parameters',para_frame,expand_x=True)],
        [sg.Submit()],
    ]
    window = sg.Window('Compare .evt and BHist', layout)
    while True:
        event, values = window.read()
        if event == 'Submit':
            if all(values) != '':
                del values['Browse']
                del values['Browse0']
                window.close()
                return values
        elif event == sg.WINDOW_CLOSED:
            sys.exit()

# buggy interaction with pd.read_csv
def getskiprows(csvfile, filters):
    skip = [0]
    with open(csvfile, 'r', encoding='UTF-8') as f:
        for i, l in enumerate(f):
            if any(para not in l for para in filters):
                skip.append(i)
    f.close()
    return skip

def getdf(f, filters, ftype = None):
    if ftype == 'BHIST':
        df = pd.read_csv(f, encoding='mbcs', dtype={'eventdescr':str},encoding_errors='replace')
        df = df[df['reportClass'].isin(filters)]
        df['eventdescr'] = df['eventdescr'].str.strip()
    elif ftype == 'evt':
        df = pd.read_csv(f, sep='\t', skipinitialspace=True, dtype={'PValue':str, 'BatchID':str}, encoding='utf-8',encoding_errors='replace')
        df = df[(df['Event'] == 'Report') & (df['Descript'].isin(filters)) & (df['PValue'] != ' ')]
        df['PValue'] = df['PValue'].str.strip()
        df = df.loc[pd.notnull(df['PValue'])]
    elif ftype == 'Bevent':
        title = ['Row','Batch_Id','Event_Type','Event_Desc','Time','Milliseconds','Area','Process_Cell','Unit','Phase_Module','Action','User_Name','Unknown','Description']
        df = pd.read_csv(f, delimiter=',', skipinitialspace=True, names=title, header=0)
        df = df[(df['Event_Type'] == 'Report') & (df['Event_Desc'].isin(filters))]
    return df

def compare(csv, evt, batchID):
    bhist = csv['eventdescr'].array
    output = list()
    for ind, ele in enumerate(evt['PValue'].array):
        if ele not in bhist:
            output.append(ind)
        sg.OneLineProgressMeter('Comparing...', ind + 1, len(evt.index),  batchID, 'Comparing EVT and CSV event fields.')
    return output

def displaylog(result, batchID):
    layout = [
        [sg.T('Batch:'), sg.I(batchID, disabled=True)],
        [sg.Multiline(result,size=(145,16),horizontal_scroll=True,key='-PRINT-')],
        [sg.I(disabled=True,expand_x=True, enable_events=True,key='-SAVE-'),sg.FileSaveAs(file_types=(('Comma Separated Value File','*.csv'),),key='-SAVE-')],
        [sg.Ok(key='-OK-')],
    ]
    window = sg.Window(batchID,layout)
    while True:
        event, values = window.read()
        if event == '-SAVE-':
            savecsv(values['-SAVE-'],result)
        elif event == '-OK-':
            window.close()
            return
        elif event == None:
            sys.exit()

def savecsv(location, content):
    content.to_csv(location,sep=',', encoding='utf-8')

if __name__ == '__main__':
    main()