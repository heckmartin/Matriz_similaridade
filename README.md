# SiMPle-Musical-repetition-recognition

### Dependecy:
 - **Plotly** (Required for the arc plot)
 - **Librosa** (Required for similarity matrix calculation)
 - **Numpy** (Required for the similarity matrix and for the repetition recognition)
 - **Jupyter notebook** (Optional, but recomended)

### Usage:
To generate the similarity matrix used to compute the repetition you will need to provide the path to an audio file.

Run ```Python Repetition_recognition.py <path to the desired track>```

However it is recomended to use the provided notebook file for testing.

### Example: 
In this example we calculate the similarity matrix for the music Gymnopédie No.1 from Erik Satie using the SiMPle algorithm.
![alt text](https://github.com/heckmartin/SiMPle-Musical-repetition-recognition/blob/master/Examples/Sim_matrixes/gymnop%C3%A9die_sim.png?raw=true)
From it we can calculate the diagonals found in the similarity matrix (here we use the maximum distance as 25, the exclusion zone also as 25 and the minimum size of the diagonal as 215).

With the proper diagonals, we can make the visualization. On the visualization, each node references a time (in seconds) on the music, each arc is one fo the repetitions found, and the size of the arc is the duration (in seconds) of the repetition. The Jupyter Notebook is again recomended here. 
