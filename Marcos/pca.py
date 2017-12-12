'''

PCA (Principal Component Analysis)

Principais aplicações:

- Redução de dimensionalidade
- Redução de redundância
- Filtragem de ruído
- Compressão de dados

'''
import pandas as pd
import numpy as np

dados = np.matrix('2.5, .5, 2.2, 1.9, 3.1, 2.3, 2, 1, 1.5, 1.1; 2.4, .7, 2.9, 2.2, 3, 2.7, 1.6, 1.1, 1.6, .9')
print(dados)

'''
mean_vec = np.mean(dados, axis=0) # usado na normalizacao
cov_mat = (dados - mean_vec).T.dot((dados - mean_vec)) / (dados.shape[0]-1)
print('Covariance matrix \n%s' % cov_mat)
'''
dados[0] -= np.mean(dados[0])
dados[1] -= np.mean(dados[1])

cov = np.cov(dados)
print('Covariance \n%s' % cov)

eig_vals, eig_vecs = np.linalg.eig(cov)
print('Eigenvectors \n%s' % eig_vecs)
print('\nEigenvalues \n%s' % eig_vals)
