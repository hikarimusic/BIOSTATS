import pandas as pd

def to_csv(data, output):
    data = data.replace("\n", "!")
    data = data.split()
    data = ",".join(data)
    data = data.replace("!", "\n")

    with open(output, "w") as f:
        f.write(data)

ss = """
Volume   Pitch
 1760    529
 2040    566
 2440    473
 2550    461
 2730    465
 2740    532
 3010    484
 3080    527
 3370    488
 3740    485
 4910    478
 5090    434
 5090    468
 5380    449
 5850    425
 6730    389
 6990    421
 7960    416
"""

#to_csv(ss, "spearman_rank_correlation.csv")



'''
ss = "ID,Treatment,Result\n"

for i in range(1,22):
    ss += "{},control,fail\n".format(str(i))
for i in range(22,31):
    ss += "{},control,fail\n".format(str(i))
for i in range(31,33):
    ss += "{},control,pass\n".format(str(i))
for i in range(33,45):
    ss += "{},control,pass\n".format(str(i))

for i in range(1,22):
    ss += "{},test,fail\n".format(str(i))
for i in range(22,31):
    ss += "{},test,pass\n".format(str(i))
for i in range(31,33):
    ss += "{},test,fail\n".format(str(i))
for i in range(33,45):
    ss += "{},test,pass\n".format(str(i))



to_csv(ss, "mcnemars_exact_test.csv")
'''

ss = """
"State","Murder","Assault","UrbanPop","Rape"
"Alabama",13.2,236,58,21.2
"Alaska",10,263,48,44.5
"Arizona",8.1,294,80,31
"Arkansas",8.8,190,50,19.5
"California",9,276,91,40.6
"Colorado",7.9,204,78,38.7
"Connecticut",3.3,110,77,11.1
"Delaware",5.9,238,72,15.8
"Florida",15.4,335,80,31.9
"Georgia",17.4,211,60,25.8
"Hawaii",5.3,46,83,20.2
"Idaho",2.6,120,54,14.2
"Illinois",10.4,249,83,24
"Indiana",7.2,113,65,21
"Iowa",2.2,56,57,11.3
"Kansas",6,115,66,18
"Kentucky",9.7,109,52,16.3
"Louisiana",15.4,249,66,22.2
"Maine",2.1,83,51,7.8
"Maryland",11.3,300,67,27.8
"Massachusetts",4.4,149,85,16.3
"Michigan",12.1,255,74,35.1
"Minnesota",2.7,72,66,14.9
"Mississippi",16.1,259,44,17.1
"Missouri",9,178,70,28.2
"Montana",6,109,53,16.4
"Nebraska",4.3,102,62,16.5
"Nevada",12.2,252,81,46
"New Hampshire",2.1,57,56,9.5
"New Jersey",7.4,159,89,18.8
"New Mexico",11.4,285,70,32.1
"New York",11.1,254,86,26.1
"North Carolina",13,337,45,16.1
"North Dakota",0.8,45,44,7.3
"Ohio",7.3,120,75,21.4
"Oklahoma",6.6,151,68,20
"Oregon",4.9,159,67,29.3
"Pennsylvania",6.3,106,72,14.9
"Rhode Island",3.4,174,87,8.3
"South Carolina",14.4,279,48,22.5
"South Dakota",3.8,86,45,12.8
"Tennessee",13.2,188,59,26.9
"Texas",12.7,201,80,25.5
"Utah",3.2,120,80,22.9
"Vermont",2.2,48,32,11.2
"Virginia",8.5,156,63,20.7
"Washington",4,145,73,26.2
"West Virginia",5.7,81,39,9.3
"Wisconsin",2.6,53,66,10.8
"Wyoming",6.8,161,60,15.6
"""

ss = ss.replace('"', "")

with open("principal_component_analysis.csv", "w") as f:
    f.write(ss)