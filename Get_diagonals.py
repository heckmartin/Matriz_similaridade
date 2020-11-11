import numpy as np

def get_diag(sim_matrix, distance_max = 25, exclusion_zone = 25, tam_min = 215):
    diagonal = []
    num_row, num_col = np.shape(sim_matrix)
    for row in range(num_row):
        tam_max=0
        maior_diag = [None]
        for col in range(row,num_col):
            if sim_matrix[row][col]<distance_max: #parametro que define o limitante superior da distancia
                inicio = [row,col]
                tamanho = 0
                while (row+tamanho)<num_row and (col+tamanho)<num_col and sim_matrix[row+tamanho][col+tamanho]<distance_max:
                    tamanho+=1
                if tamanho>tam_max:
                    maior_diag = [inicio,tamanho]
                    tam_max = tamanho
        if(tam_max!=0): #verifica se existe ao menos um ponto 
            linha,coluna = maior_diag[0]
            #atribui infinito a diagonal e seus pontos vizinhos para prevenir valores repetidos ou de baixa informação
            for t in range(tam_max):
                sim_matrix[linha+t][coluna+t-exclusion_zone:coluna+t+exclusion_zone]= np.inf
            if(tam_max > tam_min): #guarda a diagonal somente se ela for de um tamanho satisfatório 
                diagonal.append(maior_diag)
    diagonal.sort(key=lambda x:x[1],reverse=True)#Ordena as diagonais pelo tamanho 
    return diagonal
