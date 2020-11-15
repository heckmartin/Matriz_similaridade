import plotly as py
import plotly.graph_objects as go
import argparse
import click
import itertools
import librosa
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

import Simple_similarity
import Get_diagonals
import Visualization

y,sr = librosa.load(sys.argv[1])# loads the music
chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)#gets the chroma energy normalized

sim_matrix, _ = Simple_similarity.simpleself(chroma_cens, 215) # 215 ~ 5sec

diagonal = Get_diagonals.get_diag(sim_matrix, distance_max=25, exclusion_zone=25, tam_min=215)# runs through the similarity matrix saving the longest diagonals
num_row, num_col = np.shape(sim_matrix)
img_diag = np.zeros((num_row,num_col))
for k in range(len(diagonal)):
    x,y = diagonal[k][0]
    for i in range(diagonal[k][1]):
        img_diag[x+i][y+i] = 255

Visualization.arc_plot(diagonal,cut = 43, arc_num = 20,arc_size = 0.1)# calculates the desired arc plot and saves it
