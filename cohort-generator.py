
import csv

lines = []

out = open("cohorts_full.csv","w")


with open('cohorts.csv', mode ='r') as file:
    for line in csv.reader(file):
        lines.append(line[0])

n= int(51000/20)

for i in range(1,n+1):
    for cohort in lines:
        out.write(cohort+f'{i:05d}'+'\n')

out.close()