
import csv
import sys

cohort_size = int(sys.argv[1])
lines = []
out = open("cohorts_final.csv","w")

with open('cohorts_init.csv', mode ='r') as file:
    for line in csv.reader(file):
        lines.append(line[0])

n= int(cohort_size/len(lines))

for i in range(1,n+1):
    for cohort in lines:
        out.write(cohort+f'{i:05d}'+'\n')

out.close()