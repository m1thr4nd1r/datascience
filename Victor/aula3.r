cat("\014IBL - KNN\n")
# Calculo de Distancia
euclidian = function(a,b) {
  sqrt(sum(a-b)^2)
}

distance = function(a,b,p) {
  #manhathan -> p = 1
  #euclidian -> p = 2
  (sum(abs(a-b))^ p) ^ 1/p
}
#---------------------------
#Normalize
normalize = function(x)
{
  return ((x- min(x)) / (max(x) - min(x)))
}
#---------------------------
# KNN (Uma função de classificação e uma de regressão)
KNN = function(data, y, k) {
### Entradas (Teste)
#data = iris #data = Iris, ou Vector3(x,y,label)
#y = data[1,] 
#k = 3
### Normalizando
for (i in 1:(ncol(data)-1))
  data[,i] = ((data[,i]- min(data[,i])) / (max(data[,i]) - min(data[,i]))) 
### Calcular Distancias
  #print(cleanData[1,])
  #print(cleanData[2,])
  #print(cleanData[1,] - cleanData[2,])
  #print(euclidian(cleanData[1,], cleanData[2,]))
yDist = vector("numeric", nrow(data))
for (i in 1:nrow(data))
  yDist[i] = euclidian(y[-ncol(y)], data[i,-ncol(data)])
#yDist = rank(yDist)
yDist = sort.int(yDist, decreasing = F, index.return = T)
  #print(yDist$x[2])
### Classificar
cat("Dado de Teste:\n")
print(y[,-ncol(y)])
cat(k ,"Vizinhos:",yDist$ix[1:k],"\n")
  #print(data$Species[tail(yDist,k)])
votes = vector("integer",length(levels(data$Species)))
names(votes) = levels(data$Species)
j = 0
for (i in data$Species[yDist$ix[1:k]])
{
  j = j + 1
#  votes[i] = votes[i] + 1 # Votação Simples
  votes[i] = votes[i] + k + 1 - j # Votação com Peso
}
votes = sort(votes, decreasing = T)
y$Species = names(votes)[1]
cat("Novo dado classificado como:",names(votes)[1],"\n")
print(y)
### Adicionar caso de teste a base
  #print(nrow(data))
data[nrow(data)+1,] = y
  #print(nrow(data))
}

teste = vector("list", 5)
#teste = array(data = c(runif(4,0,1), NA), dim = 1, dimnames = names(iris))
names(teste) = names(iris)
teste[] = c(runif(4,0,1), NA)
print(typeof(teste))
print(ncol(teste))

teste = iris[1,]
#print(typeof(teste))

KNN(data = iris, k = 3, y = teste)