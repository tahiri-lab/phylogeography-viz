import subprocess
import pandas as pd
import os
from pipeline_test import getDissimilaritiesMatrix

file_name = "donnees.csv"
#number_trees = 5  #"Number of trees to create
specimen = 'Nom du specimen'   #"Please enter the name of the colum containing the specimens names: "

names = ['Nom du specimen','T min à 2m (C)','T max à 2m (C)',
        'Humidité relative à 2m(%)','Précipitation totale sur le mois (mm)','Pression en surface (kPa)']



def create_tree(file_name, names):
    for i in range(1, len(names)):
        getDissimilaritiesMatrix(file_name, names[0], names[i], "infile") 
        # liste a la position 0 contient les noms des specimens
        os.system("./exec/neighbor < input_files/neighbor_input.txt")
        subprocess.call(["mv", "outtree", "intree"])
        subprocess.call(["rm", "infile", "outfile"])
        os.system("./exec/consense < input_files/input.txt" )
        newick_file = names[i] + "_newick"
        subprocess.call(["rm", "outfile"])
        subprocess.call(["mv", "outtree", newick_file])


'''
if __name__ == '__main__':
    try:
        create_tree(file_name, names)
    except:
        print("An error has occured.")
    else:
        subprocess.call(["rm", "intree"])
'''

create_tree(file_name, names)

