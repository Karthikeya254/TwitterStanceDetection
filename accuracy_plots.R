library(data.table)
library(ggplot2)

train = as.data.frame(fread("train.csv"))
test = as.data.frame(fread("test.csv"))
train$Stance
targets = unique(train$Target)
boxplot(Stance ~ interaction(Target), data = train)
stripchart(train$Stance ~ train$Target, vertical = TRUE, method = "jitter"
           , jitter = 0.1)

stripchart(d$TOTAL.NUMBER.OF.CLAIMS ~ d$YEAR, vertical = TRUE, method = "jitter"
           , jitter = 0.1, pch = 1:length(unique(d$Year)), col = 1:length(unique(d$YEAR)))

barplot(train$Target)

ggplot(data, aes(fill=condition, y=value, x=specie)) + 
  geom_bar(position="dodge", stat="identity")

ggplot(train, aes(x=Target, fill=Stance)) + 
  geom_bar() +
  scale_x_discrete(labels = c("Climate Change is a Real Concern" = "Climate Change"))

ggplot(train, aes(x=Target, fill=Stance)) + 
  geom_bar() +
  scale_x_discrete(labels = function(x) lapply(strwrap(x, width = 20, simplify = FALSE), paste, collapse="\n"))

ggplot(test, aes(x=Target, fill=Stance)) + 
  geom_bar() +
  scale_x_discrete(labels = function(x) lapply(strwrap(x, width = 20, simplify = FALSE), paste, collapse="\n"))
######################################################################

acc_bow_all = c(66.36, 32.45, 32.63, 49.83, 40.35)
acc_bow_filter = c(69.09, 34.91, 58.94, 44.06, 36.07)
acc_bow_tuned = c(75, 73.37, 64.21, 64.06, 67.85)
acc_mpqa = c(72.73, 72.78, 63.87, 58.98, 67.5)
acc_ngram = c(75.54, 46.15, 55.87, 62.71, 69.28)
acc_dep_trop = c(72.72, 20.92, 63.22, 58.64, 67.36)
acc_head_chain = c(72.72, 20.92, 15.47, 58.64, 67.37)
acc_rf = c(68.8,64.91,72.04,65.1,61.77)


Accuracy = c(acc_bow_filter,acc_bow_tuned,acc_mpqa,acc_ngram,acc_dep_trop,acc_rf)
Model = rep(c("BOW", "BOW Tuned", "BOW+MPQA", "BOW+MPQA+n-gram",
            "Dependency Triplets","Random Forest"), each = 5)
Target = rep(c("Atheism", "Climate", "Feminism", "Hillary", "Abortion"), 6)

d = data.frame(Accuracy, Model,Target)

ggplot(d, aes(fill=Model, y=Accuracy, x=Target)) + 
  geom_bar(position="dodge", stat="identity")+ theme(legend.position="bottom")

ggplot(d, aes(fill=Model, y=Accuracy, x=Target)) + 
  geom_bar(position="dodge", stat="identity") + 
  theme(legend.position="bottom", legend.box = "horizontal")
