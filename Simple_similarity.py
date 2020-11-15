import plotly as py
import plotly.graph_objects as go
import argparse
import click
import itertools
import librosa
import numpy as np
import os
import sys


_EPS = 1e-14

def simpleself(seq, subseq_len):
    
    # prerequisites
    exclusion_zone = int(np.round(subseq_len/2));
    ndim = seq.shape[0]
    seq_len = seq.shape[1]
    matrix_profile_len = seq_len - subseq_len + 1;
    
    # windowed cumulative sum of the sequence
    seq_cum_sum2 = np.insert(np.sum(np.cumsum(np.square(seq),1),0), 0, 0)
    seq_cum_sum2 = seq_cum_sum2[subseq_len:]-seq_cum_sum2[0:seq_len - subseq_len + 1]
    
    # first distance profile
    first_subseq = np.flip(seq[:,0:subseq_len],1)    
    dist_profile = seq_cum_sum2 + seq_cum_sum2[0]
    
    prods = np.full([ndim,seq_len+subseq_len-1], np.inf)
    for i_dim in range(0,ndim):
        prods[i_dim,:] = np.convolve(first_subseq[i_dim,:],seq[i_dim,:])
        dist_profile -= (2 * prods[i_dim,subseq_len-1:seq_len])
    prods = prods[:, subseq_len-1:seq_len] # only the interesting products
    prods_inv = np.copy(prods)
    
    dist_profile[0:exclusion_zone] = np.inf
    
    matrix_profile = np.ndarray((matrix_profile_len,matrix_profile_len))
    matrix_profile[0] = dist_profile[:]

    mp_index = -np.ones((matrix_profile_len), dtype=int)
    mp_index[0] = np.argmin(dist_profile)

    # for all the other values of the profile
    for i_subseq in range(1,matrix_profile_len):
        
        sub_value = seq[:,i_subseq-1, np.newaxis] * seq[:,0:prods.shape[1]-1]
        add_value = seq[:,i_subseq+subseq_len-1, np.newaxis] * seq[:, subseq_len:subseq_len+prods.shape[1]-1]

        prods[:,1:] = prods[:,0:prods.shape[1]-1] - sub_value + add_value
        prods[:,0] = prods_inv[:,i_subseq]
        
        # dist_profile = seq^2 + subseq^2 - 2 * seq.subseq
        subseq_cum_sum2 = seq_cum_sum2[i_subseq]
        dist_profile = seq_cum_sum2 + subseq_cum_sum2 - 2 * np.sum(prods,0)
        
        # excluding trivial matches
        dist_profile[max(0,i_subseq-exclusion_zone+1):min(matrix_profile_len,i_subseq+exclusion_zone)] = np.inf
        
        matrix_profile[i_subseq] = dist_profile[:]
        mp_index[i_subseq] = np.argmin(dist_profile)
        
    return matrix_profile, mp_index

