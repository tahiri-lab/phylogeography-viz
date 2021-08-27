import subprocess
import os
import re
import pandas as pd
from csv import writer
import shutil

# ATTENTION AUX NOMS DES FICHIERS AVEC LES _

bootstrap_threshold = 0
rf_threshold = 100
window_size = 5000
step_size = 100 
data_names = ["Précipitation_totale_sur_le_mois_mm_newick",
              "T_max_à_2m_C_newick"]
reference_gene_file = 'output/reference_gene.fasta'


#-----------------------------------------  
def prepareDirectory():
    path_output_windows = './output/windows'                            
    isExist = os.path.exists(path_output_windows)

    if isExist:
        for f in os.listdir(path_output_windows):
            os.remove(os.path.join(path_output_windows, f))
    else:
        os.makedirs(path_output_windows)

    # delete the results of last analysis, if we have    
    #delete_path = os.listdir('output')

    #for item in delete_path:
    #    if item.endswith("_gene"):
    #        shutil.rmtree('output'+'/'+item)

    delete_path2 = os.listdir()

    for item in delete_path2:
        if item == "output.csv" or item.startswith("RAxML_") or item.startswith("outtree"):
            os.remove(item)

prepareDirectory()



#-----------------------------------------  
#'2. Study specific genes of SARS-CoV-2'

genes_chosen = ["ORF1ab","ORF3a","ORF10"]

def displayGenesOption(window_size, step_size, bootstrap_threshold, rf_threshold, data_names,genes_chosen):

    #prepareDirectory()

    genes = {'ORF1ab': 'ATGGAGAGCC(.*)TAACAACTAA', 'S': 'ATGTTTGTTT(.*)TTACACATAA', 'ORF3a': 'ATGGATTTGT(.*)GCCTTTGTAA', 'ORF3b': 'ATGAGGCTTT(.*)GCCTTTGTAA',
            'E': 'ATGTACTCAT(.*)TCTGGTCTAA', 'M': 'ATG[GT]CAGATT(.*)TGTACAGTAA', 'ORF6': 'ATGTTTCATC(.*)GATTGA[CT]TAA', 'ORF7a': 'ATGAAAATTAT(.*)GACAGAATGA',
            'ORF7b': 'ATGATTGAACTTTCATTAATTGACTTCTATTTGTGCTTTTTAGCCTTTCTGCTATTCCTTGTTTTAATTATGCTTATTATCTTTTGGTTCTCACTTGAACTGCAAGATCATAATGAAACTTGTCACGCCTAA',
            'ORF8': 'ATGAAATTTCTTGTTTT(.*)TTT[TC]ATCTAA', 'N': 'ATGAAATTTCTTGTTTT(.*)TTT[TC]ATCTAA', 'ORF10': 'ATGGGCTATA(.*)TCTCACATAG'}
    for gene in genes_chosen:
        pattern = genes.get(gene)
        getGene(gene, pattern)
        #createPhylogeneticTree(gene, window_size, step_size, bootstrap_threshold, rf_threshold, data_names)
        #subprocess.call(["make", "clean"])
        break

def getGene(gene, pattern): 
    sequences_file = open("output/reference_gene.fasta", "r").read()
    list_of_sequences = sequences_file.split(">")
    s = pattern
    directory_name = gene + "_gene"
    file_name = gene + "_gene.fasta"
    path = os.path.join("output", directory_name, file_name)
    new_file = open(path, "w")
    for index in range(len(list_of_sequences)):
        if list_of_sequences[index] == "":
            continue
        name = list_of_sequences[index].split("\n")[0]
        gene_sequence = list_of_sequences[index].replace("\n", "")
        gene_sequence = (re.search(s, gene_sequence).group())
        new_file.writelines(">" + name + "\n")
        new_file.writelines(gene_sequence + "\n")

    new_file.close()

displayGenesOption(window_size, step_size, bootstrap_threshold, rf_threshold, data_names,genes_chosen)