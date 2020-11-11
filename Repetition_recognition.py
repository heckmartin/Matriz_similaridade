import plotly as py
import plotly.graph_objects as go
import argparse
import click
import itertools
import librosa
import numpy as np
import os
import sys
import argparse

import Simple_similarity
import Get_diagonals
import Visualization

parser = argparse.ArgumentParser()

y,sr = librosa.load(sys.argv[1])#loads the image
chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)#gets the chroma energy normalized

sim_matrix, mpindex = Simple_similarity.simpleself(chroma_cens, 215) # 215 ~ 5sec

diagonal = Get_diagonals.get_diag(sim_matrix)#runs through the similarity matrix saving the longest diagonals
Visualization.arc_plot(diagonal)#calculates the desired arc plot 
