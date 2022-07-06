


def to_csv(data, output):
    data = data.replace("\n", "!")
    data = data.split()
    data = ",".join(data)
    data = data.replace("!", "\n")

    with open(output, "w") as f:
        f.write(data)

ss = """
Species   Temp   Pulse
 ex       20.8   67.9
 ex       20.8   65.1
 ex       24     77.3
 ex       24     78.7
 ex       24     79.4
 ex       24     80.4
 ex       26.2   85.8
 ex       26.2   86.6
 ex       26.2   87.5
 ex       26.2   89.1
 ex       28.4   98.6
 ex       29    100.8
 ex       30.4   99.3
 ex       30.4  101.7
 niv      17.2   44.3
 niv      18.3   47.2
 niv      18.3   47.6
 niv      18.3   49.6
 niv      18.9   50.3
 niv      18.9   51.8
 niv      20.4   60
 niv      21     58.5
 niv      21     58.9
 niv      22.1   60.7
 niv      23.5   69.8
 niv      24.2   70.9
 niv      25.9   76.2
 niv      26.5   76.1
 niv      26.5   77
 niv      26.5   77.7
 niv      28.6   84.7
 fake     17.2   74.3
 fake     18.3   77.2
 fake     18.3   77.6
 fake     18.3   79.6
 fake     18.9   80.3
 fake     18.9   81.8
 fake     20.4   90
 fake     21     88.5
 fake     21     88.9
 fake     22.1   90.7
 fake     23.5   99.8
 fake     24.2   100.9
 fake     25.9   106.2
 fake     26.5   106.1
 fake     26.5   107
 fake     26.5   107.7
 fake     28.6   114.7
"""

to_csv(ss, "ancova.csv")