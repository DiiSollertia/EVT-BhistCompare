import pandas as pd
import PySimpleGUI as sg

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
    return df

def comparedf(csv, evt):
    csv, evt, batchID = filterbatch(csv, evt)
    bhist = csv['eventdescr'].array
    output = list()
    for ind, ele in enumerate(evt['PValue'].array):
        if ele not in bhist:
            output.append(ind)
        sg.OneLineProgressMeter('Comparing...', ind + 1, len(evt.index),  batchID, 'Comparing EVT and CSV event fields.')
    output = evt.iloc[output]
    if output.empty:
        output = "No differences found."
    return output, batchID

def filterbatch(csv, evt):
    batch = evt['BatchID'].iloc[0]
    csv = csv[csv['batchid']==batch]
    csv.reset_index()
    evt.reset_index()
    return csv, evt, batch

def savecsv(location, content):
    content.to_csv(location,sep=',', encoding='utf-8')