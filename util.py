


def to_csv(data, output):
    data = data.replace("\n", "!")
    data = data.split()
    data = ",".join(data)
    data = data.replace("!", "\n")

    with open(output, "w") as f:
        f.write(data)

ss = """
 Bird    Feather   Length
 A       Typical   -0.255
 B       Typical   -0.213
 C       Typical   -0.19
 D       Typical   -0.185
 E       Typical   -0.045
 F       Typical   -0.025
 G       Typical   -0.015
 H       Typical    0.003
 I       Typical    0.015
 J       Typical    0.02
 K       Typical    0.023
 L       Typical    0.04
 M       Typical    0.04
 N       Typical    0.05
 O       Typical    0.055
 P       Typical    0.058
 A       Odd       -0.324
 B       Odd       -0.185
 C       Odd       -0.299
 D       Odd       -0.144
 E       Odd       -0.027
 F       Odd       -0.039
 G       Odd       -0.264
 H       Odd       -0.077
 I       Odd       -0.017
 J       Odd       -0.169
 K       Odd       -0.096
 L       Odd       -0.33
 M       Odd       -0.346
 N       Odd       -0.191
 O       Odd       -0.128
 P       Odd       -0.182
"""

to_csv(ss, "repeated_anova.csv")