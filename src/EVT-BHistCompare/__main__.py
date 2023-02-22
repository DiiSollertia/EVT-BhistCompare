#!/usr/bin/env python

import gui
import handledf

def main():
    filters = gui.getfiles()
    evtfile = filters.pop(0)
    csvfile = filters.pop(1)
    filters = list(filter(filters.get, filters))
    dfevt = handledf.getdf(evtfile, filters, ftype='evt')
    dfcsv = handledf.getdf(csvfile, filters, ftype='BHIST')
    diff, batchid = handledf.comparedf(dfcsv, dfevt)
    gui.displaylog(diff, batchid)

if __name__ == '__main__':
    while True:
        main()