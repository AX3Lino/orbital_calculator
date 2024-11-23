import pandas
import pandas as pd




files  = pandas.read_csv("atmo_0_to_1000.txt", sep=r"\s+", engine="python")
# files[["Heit(km)", "air(gm/cm3)"]] *=1000
# print(files["air(gm/cm3)"])
# for i in files:
#     print(i)
print(files["Heit(m)"][1000])
print(files[["Heit(m)"]])
# files.to_csv("atmo_0_to_1000.txt", index=True, sep='\t')