from pandas import read_excel

dfs = read_excel("GlassFibreData.xlsx", sheet_name="Sheet1")

gf_data = {"prop":[], "avg":[], "std":[]}
for i in range(3,10):
    gf_data["prop"].append(dfs.iloc[i, 1])
    gf_data["avg"].append(dfs.iloc[i, 9])
    gf_data["std"].append(dfs.iloc[i, 10])

print(gf_data)

