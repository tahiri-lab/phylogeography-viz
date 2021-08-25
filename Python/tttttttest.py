import subprocess
import pandas as pd
import os
import pathlib

def prepareDirectory():
    # delete the results of last analysis, if we have    ???
    with open("intree", "w"):
        pass
    # remove old newick files
    delete_path = os.listdir()

    for item in delete_path:
        if item.endswith("_newick"):
            os.remove(item)

prepareDirectory()

