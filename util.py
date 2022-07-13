
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

to_csv(ss, "spearman_rank_correlation.csv")



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
