cat("\014Aprendizado probabilistico - Naive Bayes\n")

naiveBayes = function(data, test)
{
  cat("Entrada de teste:\n\n")
  print(test)
  cat("------------------\n")
  #probs = vector("numeric", nlevels(data[,length(data)]))
  probs = rep(1, nlevels(data[,length(data)]))
  names(probs) = levels(data[,length(data)])
  
  for (i in 1:length(probs))
  {
    lines = which(!data[,ncol(data)] %in% levels(data[,length(data)])[i])
    newData = data[-lines,]
    
    for (j in 1:(length(newData)-1))
    {
      lines = which(newData[,j]%in%test[,j])
      cat("\nP(",names(newData)[j],":", as.character(test[,j]),"|",names(newData)[length(newData)],":", names(probs)[i],") = ",(length(lines) / nrow(newData)),"\nProbs:")
      probs[i] = probs[i] * length(lines) / nrow(newData)
      print(probs[i])
    }
    
    probs[i] = probs[i] * nrow(newData) / nrow(data)
    cat("------------------\n")
  }
  
  print(probs)
  cat("\n",names(data)[j+1],":",names(probs)[which.max(probs)])
}

test = tennis[round(runif(1, min = 1, max = nrow(tennis))),-1]
test$play = NA
#test[] = c("Sunny", "Mild", "High", "Strong", NA)

#test = tennis[1,-1]
naiveBayes(tennis[,-1], test)