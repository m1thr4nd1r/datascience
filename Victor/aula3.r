#library(shiny)
cat("\014")
load("~/Downloads/bancoufba.rData")

columns = names(banco.ufba)
#print(columns)
head = head(banco.ufba)
#print(head)
mediaPeso = mean(banco.ufba$peso)
#print(mediaPeso)
medianaPeso = median(banco.ufba$peso)
#print(medianaPeso)

moda = sort(table(banco.ufba$estado), decreasing=T)[1]
# Table faz contagem, sort ordena e [1] pega o ultimo
#print(moda)

#sumario = summary(banco.ufba$salario)
sumario = summary(banco.ufba) 
#print(sumario)

varianca = var(banco.ufba$peso)
#print(varianca)

desvioPadrao = sd(banco.ufba$peso)
#print(desvioPadrao)

graficoSalario = boxplot(banco.ufba$salario)
for (a in graficoSalario$out)
{
  line = which(banco.ufba$salario == a)
  #print(banco.ufba[line,])
}

lines = which(banco.ufba$salario%in%graficoSalario$out)
#print(lines)
#print('Outliers dos Salarios')
#print(banco.ufba[lines,])
#print(banco.ufba[-lines]) #removendo linhas de outliers
#boxplot(banco.ufba$salario[-lines])

#hist(banco.ufba$salario)
hist(banco.ufba$salario[-lines])

#volto dps
for (a in columns)
{
  #print(banco.ufba[a])
  #print(banco.ufba[1,'salario'])
  #print(banco.ufba$salario[1])
  #grafico = boxplot(banco.ufba$a)
  #print(grafico$out)
  lines = which(banco.ufba$a%in%grafico$out)
  #print(a)
  #print(lines)
  #print(banco.ufba[lines,])
}

par(mfrow=c(2,1))
temp = banco.ufba$salario
temp = temp[-which(is.na(temp))]
#print(temp)
temp2 = temp[-which[temp%in%graficoSalario$out]]
temp3 = (temp2-min(temp2)) / (max(temp2)-min(temp2))
plot(temp3)
temp4 = scale(temp2, center=T, scale=T)
plot(temp4, t="l")