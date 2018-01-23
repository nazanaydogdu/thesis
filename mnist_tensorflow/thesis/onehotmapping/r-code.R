#Digit Recognition on kaggle.com
#SCORE: 0.98300
library(stats)
library("e1071")
library("devtools")

trainingSet <- read.csv("char_df.csv")   #read data files
validationSet <- read.csv("test_char_df.csv")
set.seed(20140202)

trainingLabel <- trainingSet[, 1]          #read labels
trainingSet <- trainingSet[, -1]           #read data without labels


validationLabel <- validationSet[, 1]          #read labels
validationSet <- validationSet[, -1]           #read data without labels

prc <- proc.time()
principalComps <- prcomp( ~. , data = trainingSet)  #retrieve PCs
screeplot(principalComps, type="line", main="Principle Components")
num.of.comp.train = 50
pca.train.rotation <- principalComps$rotation
pca.train.rotation <- pca.train.rotation[,1:num.of.comp.train]
trainingPRC <- as.matrix(trainingSet) %*% pca.train.rotation  #apply PCs to training data
validationPRC <- as.matrix(validationSet) %*% pca.train.rotation  #apply PCs to validation data

train.model <- svm(trainingPRC, trainingLabel,  type = "C-classification", kernel = "radial", gamma=0.01, cost = 10)  #train SVM

svm.pred <- predict(train.model, validationPRC)  #predict labels for validation data
write.csv(as.matrix(svm.pred), file = "calculateddata/results.csv")  #write predictions into CVS file
print(proc.time() - prc)
sum(svm.pred == validationLabel)/length(validationLabel)