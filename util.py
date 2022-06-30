


def to_csv(data, output):
    data = data.replace("\n", "!")
    data = data.split()
    data = ",".join(data)
    data = data.replace("!", "\n")

    with open(output, "w") as f:
        f.write(data)

ss = """
 Bird   Typical  Odd
 A     -0.255   -0.324
 B     -0.213   -0.185
 C     -0.190   -0.299
 D     -0.185   -0.144
 E     -0.045   -0.027
 F     -0.025   -0.039
 G     -0.015   -0.264
 H      0.003   -0.077
 I      0.015   -0.017
 J      0.020   -0.169
 K      0.023   -0.096
 L      0.040   -0.330
 M      0.040   -0.346
 N      0.050   -0.191
 O      0.055   -0.128
 P      0.058   -0.182  
"""

to_csv(ss, "two_sample_t_test.csv")