#To generate the comparison, call:
# > run_comparison(nf_data)
# Here nf_data is a dictionary containing properties names, averages and standard deviations of the following form:
# {'prop': ['Density [kg/m^3]', 'Stiffness [GPa]', 'T Strength [MPa]', 'T Toughness [MJ/m^3]', 'C Strength  [MPa]', 'C Toughness [MJ/m^2]', 'Shear Stress [MPa]'], 'avg': [1.54128, 1.904075, 0.5605114999999999, 0.8056942924071532, 2.778185, 2.4849885259125193, 0.47233333333333327], 'std': [0.3234226955549038, 0.921262904929964, 0.4521726894627759, 0.8782348297332258, 1.0396229420323453, 2.574659308365211, 0.3790033714303287]}

from pandas import read_excel
from RadarPlot import radar_plot

def fetch_data(file):
    dfs = read_excel(file, sheet_name="Sheet1")

    data = {"prop":[], "avg":[], "std":[]}
    for i in range(3,10):
        data["prop"].append(dfs.iloc[i, 1])
        data["avg"].append(dfs.iloc[i, 9])
        data["std"].append(dfs.iloc[i, 10])

    return data

def run_comparison(nf_data):
    data = fetch_data("GlassFibreData.xlsx")
    data["nf_avg"] = nf_data["avg"]
    data["nf_std"] = nf_data["std"]

    sp_data = {"prop":data['prop'].copy(), "avg":[], "std":[], "nf_avg":[], "nf_std":[]}
    #Calculate Specific Data
    for k in range(len(sp_data['prop'])):
        for key in data.keys():
            if key !="prop":
                sp_data[key].append(data[key][k]/data[key][0])

    def fractions(idata):
        frac_data = {"prop": idata['prop'].copy(), "avg": [], "std": [], "nf_avg": [], "nf_std": []}
        for l in range(len(frac_data['prop'])):
            frac_data['avg'].append(1)
            frac_data['std'].append(0)
            frac_data["nf_avg"].append(idata['nf_avg'][l] / idata['avg'][l])
            frac_data["nf_std"].append(0)
            gf = frac_data['prop'][l].partition(" [")
            frac_data["prop"][l] = gf[0]
        return frac_data

    fdata = fractions(data)
    sp_fdata = fractions(sp_data)

    def normalise(ndata):
        for j in range(len(ndata['avg'])):
            n = 0
            while max(ndata['avg'][j]+ndata['std'][j], ndata['nf_avg'][j]+ndata['nf_std'][j]) >= 10:
                for key in ndata.keys():
                    if key != "prop":
                        ndata[key][j] /= 10
                n += 1
            while max(ndata['avg'][j]+ndata['std'][j], ndata['nf_avg'][j]+ndata['nf_std'][j]) <= 1:
                for key in ndata.keys():
                    if key != "prop":
                        ndata[key][j] *= 10
                n -= 1
            gf = ndata['prop'][j].partition(" [")
            if n != 0:
                ndata['prop'][j] = gf[0] + '\n[e' + str(n) + ' ' + gf[-1]
            else:
                ndata['prop'][j] = gf[0] + '\n[' + gf[-1]

    normalise(data)
    normalise(sp_data)


    final_data = [
        [data["prop"], sp_data["prop"], fdata['prop'], sp_fdata['prop']],
        ('Absolute Properties', [
        [data["avg"], data["std"]],
        [data["nf_avg"], data["nf_std"]]]),
        ('Specific Properties', [
        [sp_data["avg"], sp_data["std"]],
        [sp_data["nf_avg"], sp_data["nf_std"]]]),
        ('Absolute Fraction', [
            [fdata["avg"], fdata["std"]],
            [fdata["nf_avg"], fdata["nf_std"]]]),
        ('Specific Fraction', [
            [sp_fdata["avg"], sp_fdata["std"]],
            [sp_fdata["nf_avg"], sp_fdata["nf_std"]]])
    ]

    radar_plot(final_data)


nf_data = fetch_data("GlassFibreData.xlsx")
for i in range(len(nf_data["avg"])):
    if i == 0:
        r = 0.8
    else:
        r=0.5
    nf_data["avg"][i] = nf_data["avg"][i]*r

run_comparison(nf_data)