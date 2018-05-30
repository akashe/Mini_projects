import math
import csv
from collections import Counter

## build a bayes classifier and also learn to sample data from a distribution
## somepoint later implement a SVM

# Steps:
# 1) calculate pixel wise probs
# 2) calculate class wise probs
# 2.5) number of time same inputs maps to the same class
# 3) save all this info
# 4) calculate accuracy on test set

# TODO how to implement with string

# TODO current accuracy 0! Move to log!!

#Assumptions that prob of each pixel remains the same

## Load csv's
def load_csv(f):
    lines = csv.reader(open("data/"+f+".csv","r"))
    data = list(lines)
    label = []
    for i in range(len(data)):
        if i is not 0:
            label.append(data[i][0])
            data[i]= [float(x) for x in data[i][1:]]

    return data[1:] ,label


train_data,train_label = load_csv("train")
test_data,test_label = load_csv("test")

# caluculating pixel wise probs

num_of_pixels = len(train_data[0])

def mean(l):
    sum = 0
    for i in l:
        sum+=i
    return sum/float(len(l))

def standard_deviation(l,mean):
    sum_ = sum([pow(i-mean,2) for i in l]) # not using len(l) -1 for time being
    variance = sum_/ float(len(l) - 1)
    return math.sqrt(variance)

def distribution_probability(l,mean,sd):
    # return (math.exp(-math.pow(l - mean, 2) / (2 * math.pow(sd, 2))) / float(sd * math.sqrt(2 * math.pi)))
    # return [(pow(-1*pow(x-mean,2)/(2*pow(sd,2)),math.e)/(sd*math.sqrt(2*math.pi))) for x in l]
    # The existing terms return very low values.. moving to logs instead after removing constant terms
    return (float(-math.log(sd)/2)-float((-math.pow(l-mean,2)*sd)/2))

# pixel_wise_distribution = []

pixel_wise_mean_sd = []


# for i in range(0,num_of_pixels):
#     t = train_data[:,i]
#     t_mean = mean(t)
#     t_sd = standard_deviation(t,mean)
#     # pixel_wise_distribution.append(distribution_probability(t,t_mean,t_sd))
#     pixel_wise_mean_sd.append(t_mean,t_sd)

def seperate_by_class(data,label):
    seperated_data = {}
    for d,l in zip(data,label):
        if l not in seperated_data:
            seperated_data[l]=[]
        seperated_data[l].append(d)
    return seperated_data

def mean_sd_for_each_class_for_each_pixel(data):
    class_pixel_wise_mean_sd ={}
    for i in data:
        d = data[i]
        pixel_wise_mean_sd =[]
        for j in range(0,num_of_pixels):
            t = d[:][j]
            t_mean = mean(t)
            t_sd = standard_deviation(t, t_mean)
            # pixel_wise_distribution.append(distribution_probability(t,t_mean,t_sd))
            pixel_wise_mean_sd.append((t_mean, t_sd))
        class_pixel_wise_mean_sd[i]=pixel_wise_mean_sd
    return class_pixel_wise_mean_sd

# class probabilities - Most proabably they are same but writing for future use
# num_of_classes = len(Counter(x for x in train_label))
# class_mean = mean(train_label)
# class_stddev = standard_deviation(train_label,class_mean)
# TODO clarify distribution problem

# Prepare_data
analysis = mean_sd_for_each_class_for_each_pixel(seperate_by_class(train_data,train_label))

#Preidictions
pred = []
for i in range(0,len(test_data)):
    maxprob= -1.0
    for j in analysis:
        for k,d in enumerate(test_data[i]):
            a = distribution_probability(d,analysis[j][k][0],analysis[j][k][1])
            if k==0:
                class_prob = a
            else:
                class_prob+=a
        if class_prob>maxprob:
            best_class = j
        class_prob =None
    pred.append(j)

#Accuracy
correct = 0
for i,j in zip(pred,test_label):
    if i == j:
        correct+=1

print("Accuracy {}".format(correct/float(len(test_label))))

print("Akash")


