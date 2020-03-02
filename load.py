import sys
import json
import requests
import threading
import Tkinter as tk
from ttkHyperlinkLabel import HyperlinkLabel
import myNotebook as nb
from config import config

this = sys.modules[__name__]

def plugin_start(plugin_dir):
    """
    Load this plugin into EDMC
    """
    print "IDA-Distress-Call loaded! My plugin folder is {}".format(plugin_dir.encode("utf-8"))
    return "IDA-Distress-Call"

def plugin_stop():
    """
    EDMC is closing
    """
    print "Closing down"

def plugin_prefs(parent, cmdr, is_beta):
    """
    Return a TK Frame for adding to the EDMC settings dialog.
    """
    this.DCapikey = tk.StringVar(value=config.get("DCAPIkey"))
    this.DCactivated = tk.IntVar(value=config.getint("DCstatus"))

    frame = nb.Frame(parent)

    plugin_label = nb.Label(frame, text="IDA Distress Call plugin v0.12")
    plugin_label.grid(padx=10, row=0, column=0, sticky=tk.W)

    HyperlinkLabel(frame, text='Visit website', background=nb.Label().cget('background'), url='https://github.com/ZTiKnl/IDA-Distress-Call', underline=True).grid(padx=10, row=0, column=1, sticky=tk.W)

    empty_label = nb.Label(frame, text="")
    empty_label.grid(padx=10, row=1, column=0, columnspan=2, sticky=tk.W)

    apikey_label = nb.Label(frame, text="Enter your API key")
    apikey_label.grid(padx=10, row=2, column=0, sticky=tk.W)

    apikey_entry = nb.Entry(frame, textvariable=this.DCapikey)
    apikey_entry.grid(padx=10, row=2, column=1, sticky=tk.EW)

    activated_entry = nb.Checkbutton(frame, text=_('Activate by placing checkmark'), variable=this.DCactivated)
    activated_entry.grid(padx=10, row=5, column=0, columnspan=2, sticky=tk.EW)

    return frame

def prefs_changed(cmdr, is_beta):
    """
    Save settings.
    """
    config.set('DCAPIkey', this.DCapikey.get())
    config.set('DCstatus', this.DCactivated.get())

def plugin_app(parent):
    """
    Create a pair of TK widgets for the EDMC main window
    """
    label = tk.Label(parent, text="IDA DC:")
    this.status = tk.Label(parent, text="Idle")

    return (label, this.status)

def journal_entry(cmdr, is_beta, system, station, entry, state):
    """
    Evaluate data and transfer to http://distresscall.ztik.nl/api
    """
    this.DCactivated = tk.IntVar(value=config.getint("DCstatus"))

    if this.DCactivated.get() == 1 :
        if entry['event'] == 'Interdicted':
            if entry['IsPlayer'] == True:
                # interdicted
                this.DCapikey = tk.StringVar(value=config.get("DCAPIkey"))

                entry['key'] = this.DCapikey.get()
                entry['CMDR'] = cmdr

                this.status['text'] = "Sending Distress Call"
                url = "http://distresscall.ztik.nl/api"
                r = requests.post(url, json=entry)
                if r.status_code == 200:
                    sys.stderr.write("Status: 200\n")
                    this.status['text'] = "Distress Call sent"
                    t = threading.Timer(15.0, clearstatus)
                else:
                    data = json.loads(r.text)
                    sys.stderr.write("Status: " + str(r.status_code) + ": " + str(data['message']) + "\n")
                    sys.stderr.write("Error: " + str(data['error']) + "\n")
                    this.status['text'] = "Fail: " + str(r.status_code) + ": " + str(data['message'])
                    t = threading.Timer(15.0, clearstatus)
                t.start()

def clearstatus():
    this.status['text'] = "Idle"