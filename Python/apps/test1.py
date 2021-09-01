import os
from Bio import AlignIO, SeqIO, Phylo
from ete3 import Tree
import re


import dash
from dash.dependencies import Input, Output
import dash_bio as dashbio
import dash_html_components as html



#--------------
app = dash.Dash(__name__)

#-----------------


gene = "ORF6"
position_ASM = "8400_8700"
tree_phylogeo = "Pression_en_surface_kPa_newick"


directory_name = gene + '_gene'
align_file_name = position_ASM
theGene_fileFasta = directory_name + '.fasta'
tree_output_file = position_ASM + '_' + tree_phylogeo + '_tree'

#align_path = os.path.join('../output',directory_name,align_file_name)

align_chart_path = os.path.join('../output',directory_name,theGene_fileFasta)
tree_path = os.path.join('../output',directory_name,tree_output_file)


#make a tree
#https://biopython.org/wiki/Phylo

#tree = Phylo.read(tree_path, "newick")
#print(tree)
#Phylo.draw(tree)
#Phylo.draw_ascii(tree)
#with open('../assets/phylo_tree.txt', 'w') as fh:
#     Phylo.draw_ascii(tree, file = fh)


#Phylo.convert(tree_path, "nexus","example.nhx", "newick")


#newick = '(DCGC-50693:0.00000100000050002909,(((RJ-LNN0011:0.00000100000050002909,TX-DSHS-52:0.00000100000050002909):0.00000100000050002909[0],((IMR_125063:0.00000100000050002909,NB-NML-300:0.00000100000050002909):0.00000100000050002909[0],(TRE23196_1:0.00000100000050002909,(NSW4490:0.00000100000050002909,(PAIS-D0094:0.00000100000050002909,(GJ-GBRC560:0.00000100000050002909,(LOND-128A7:0.00000100000050002909,(ON-E76b:0.00000100000050002909,(S38:0.00000100000050002909,(S21D474:0.00000100000050002909,OR-OSPHL00:0.00000100000050002909):0.00000100000050002909[20]):0.00000100000050002909[10]):0.00000100000050002909[10]):0.00000100000050002909[10]):0.00000100000050002909[10]):0.00000100000050002909[10]):0.00000100000050002909[10]):0.00000100000050002909[10]):0.00000100000050002909[0]):0.00000100000050002909[0],(AP8:0.00334389054503755022,(CMX-INER-I:0.00334622096930954887,ON-S2383:0.00334622068033279228):0.00000100000050002909[0]):0.00000100000050002909[0]):0.00000100000050002909[10],CAM-TIGEM-:0.00000100000050002909);'
#nw = re.sub(":(\d+\.\d+)\[(\d+)\]", ":\\1[&&NHX:support=\\2]", open
#(tree_path).read())

#print(nw)
#t = Tree(nw)
#t.render("mytree.png", w=183, units="mm")



#read the files
'''
alignment = AlignIO.read(open(align_path), "phylip")
print("Alignment length %i" % alignment.get_alignment_length())
for record in alignment:
    print(record.id)
'''


# convert from phylip to clustal
'''
records = SeqIO.parse(align_path, "phylip")
clustal_file_path = align_path +'.clustal'
SeqIO.write(records, clustal_file_path, "clustal")
'''

#alignment Chart
'''
# prepare dataset

with open(align_chart_path, encoding='utf-8') as data_file:
    data = data_file.read()
    #print(data)


#---------------------------------
app.layout = html.Div([

    dashbio.AlignmentChart(
        id='my-alignment-viewer',
        data=data
    ),
    html.Div(id='alignment-viewer-output')
])

#----------------------------------------
@app.callback(
    Output('alignment-viewer-output', 'children'),
    Input('my-alignment-viewer', 'eventDatum')
)
def update_output(value):
    if value is None:
        return 'No data.'
    return str(value)


if __name__ == '__main__':
    app.run_server(debug=True)
'''

#---------------------------------
with open ("../assets/phylo_tree.txt", "r") as f:
    tree_txt = f.read()

print(tree_txt)
app.layout = html.Div([
    html.Div(tree_txt, style={'whiteSpace': 'pre-line'}),
    
])

#----------------------------------------


if __name__ == '__main__':
    app.run_server(debug=True)