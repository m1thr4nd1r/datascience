# Referencia 
#http://web.tecnico.ulisboa.pt/ana.freitas/bioinformatics.ath.cx/bioinformatics.ath.cx/indexf23d.html?id
#https://raw.githubusercontent.com/sjwhitworth/golearn/master/examples/datasets/tennis.csv
#https://raw.githubusercontent.com/petehunt/c4.5-compiler/master/example/tennis.csv
#-----

cat("\014Árvores de decisão - ID3\n")
levelsCount = function(data)
{
  v = vector("integer", nlevels(data[,length(data)]))
  names(v) = levels(data[,length(data)])
  for (i in data[,length(data)])
    v[i] = v[i] + 1;
  print(v);
  return(v);
}

entropy = function(data)
{
  levelsAmount = levelsCount(data)
  s = 0
  for (i in levelsAmount)
    s = s - i/nrow(data) * log2(i/nrow(data))
  
  print(s)
  if (is.nan(s))
    return(0)
  return(s)
}

gain = function(data)
{
  cat("Exemplo de Entrada\n\n")
  print(data[1,])
  cat("\nEntropia do Conjunto\n")
  s = entropy(data)
  
  if (s == 0)
  {
    lvl = levelsCount(data)
    lvl = sort(lvl, decreasing = T)
    return(names(lvl)[1])
  }
  
  attrib = names(data)
  gains = vector("numeric", length(data)-1)
  names(gains) = names(data[,-length(data)])
  
  for (j in 1:length(gains))
  {
    label = levels(data[,j])
    cat("\nGanho do",attrib[j],"\n")
    partialGain = 0
    for (i in levels(data[,j]))
    {
      lines = which(!data[,j]%in%i)
      newData = data[-lines,]
      cat("--Entropia de",i,"\n")
      partialGain = partialGain - entropy(newData) * nrow(newData) / nrow(data)
    }
    
    gains[j] = s + partialGain
    cat("Ganho do",attrib[j],gains[j],"\n---------------")
  }
  
  gains = sort.int(gains, decreasing = T, index.return = T)
  cat("||||||||||\nMaior Ganho:", gains$x[1],"(",attrib[gains$ix[1]],")\n")
  
  l = vector("list", nlevels(data[,gains$ix[1]])+1)
  print(nlevels(data[,gains$ix[1]]))
  names(l) = c("Name",levels(data[,gains$ix[1]]))
  l["Name"] = attrib[gains$ix[1]]
  
  for (i in levels(data[,gains$ix[1]]))
  {
    lines = which(!data[,gains$ix[1]]%in%i)
    newData = data[-lines,-gains$ix[1]]
    cat("---------------||||||||||\nSubconjunto de", attrib[gains$ix[1]],"com classe", i,"\n")
    l[i] = list(gain(newData))
  }
  return(l)
}

evaluate = function(model, data)
{
  #print(model)
  value = paste(unlist(data[model$Name]))
  #print(model[[1]]$Name)
  model = model[value]
  print(value)
  #print(unlist(model, use.names = T))
  #model = unlist(model, use.names = T)
  #print(model[Name])
  #print(getElement(model,"Name"))
  #print(model[[1]]$Name)
  value = paste(unlist(data[model[[1]]$Name]))
  print(value)
  print(model[[1]])
  
  while (F)
  {
    value = paste(unlist(data[model$Name]))
    model = model[value]
  }
  
}

#Pre-processamento
data = tennis[,-1]
#----
l = gain(data)
#cat("--------------------------- MODELO ---------------------------\n")
#print(l)
cat("--------------------------- TESTE ---------------------------\n")
test = tennis[1,]
evaluate(l, test)