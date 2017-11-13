#Pre Processamento
cat("\014Pre-Processamento\n")
dados=matrix(nrow=10,ncol=2)
dados[,1] = c(2.5, .5, 2.2, 1.9, 3.1, 2.3, 2, 1, 1.5, 1.1)
dados[,2] = c(2.4, .7, 2.9, 2.2, 3, 2.7, 1.6, 1.1, 1.6, .9)

dados2=matrix(nrow=10,ncol=2)
dados2[,1] = dados[,1] - mean(dados[,1])
dados2[,2] = dados[,2] - mean(dados[,2])

# Consertar
#conv = (1 / nrow(dados)) * ( t(dados)%*%(dados) )
#print(conv)
####### Fazer covariança na mão (e passo a passo no R)
conv = cov(dados2)
#print(conv)

autovec = eigen(conv)$vector

comps = t(t(autovec)%*%t(dados))

data = iris[,1:4]
#head(data)

resultado = princomp(data)

resultado2 = prcomp(data)

#print(autovec)
#print(comps)

#print(paste(sqrt(var(comps[,1])),
#            sqrt(var(comps[,2])),  sep="  |  "))
#cat(sqrt(var(comps[,1])),
#    "\n",
#    sqrt(var(comps[,2])))

print(summary(resultado))
print(summary(resultado2))

par(mfrow=c(2,1))
#plot(dados)
#plot(dados2)
#plot(conv)
#plot(comps)
#plot(resultado$scores)
#plot(resultado2$x)
biplot(resultado)
biplot(resultado2)

cat("\nValidação\n")