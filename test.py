# from.e_plot import *
from Bonds.pendemic_bonds.e_plot import *

pixel_ratio = 1
date = "2020-03-12"
data = pd.read_excel("Bonds/pendemic_bonds/data/疫情债券3117.xlsx")
data = data[data['发行起始日期↑']<=date]

p = plot_all(data)
p.render("page.html")


