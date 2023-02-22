import sys
import PySimpleGUI as sg
import handledf

def getfiles():
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
        try:
            event, values = window.read()
        except:
            continue
        if event == 'Submit':
            if all(values) != '':
                del values['Browse']
                del values['Browse0']
                window.close()
                return values
        elif event == sg.WINDOW_CLOSED:
            sys.exit()

def displaylog(result, batchID='N/A'):
    layout = [
        [sg.T('Batch:'), sg.I(batchID, disabled=True)],
        [sg.Multiline(result,size=(145,16),horizontal_scroll=True,key='-PRINT-')],
        [sg.I(disabled=True,expand_x=True, enable_events=True,key='-SAVE-'),sg.FileSaveAs(file_types=(('Comma Separated Value File','*.csv'),),key='-SAVE-')],
        [sg.Ok(key='-OK-')],
    ]
    window = sg.Window('Differences Found',layout)
    while True:
        event, values = window.read()
        if event == '-SAVE-':
            handledf.savecsv(values['-SAVE-'],result)
        elif event == '-OK-':
            window.close()
            return
        elif event == None:
            sys.exit()