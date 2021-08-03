from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np

from solcore import material
from solcore.structure import Structure
from solcore.absorption_calculator import calculate_rat

# 波长，反射和吸收（不同角度）
E_eV = np.linspace(0.65, 4, 1000)   # λ = 1240/E_ev

def nk_convert(fname, energy):
    """ Designed to handle nk data files
    设计用于处理nk数据文件"""

    # Import data...E_n, n ??
    E_n, n, E_k, k = np.loadtxt(fname, delimiter=",", unpack=True)
    # print("File :: " + fname + " :: Imported Successfully!")

    # Interpolate data 插入数据...
    n_interp = interp1d(E_n, n, bounds_error=False, fill_value=(n[0], n[-1]))(energy)
    k_interp = interp1d(E_k, k, bounds_error=False, fill_value=(k[0], k[-1]))(energy)

    return (energy, n_interp, k_interp)


# Load nk data using nk_convert function...
alinp_nk = nk_convert("data/AlInP_nk.csv", energy=E_eV)
gainp_nk = nk_convert("data/GaInP_nk.csv", energy=E_eV)
mgf_nk = nk_convert("data/MgF_nk.csv", energy=E_eV)
sic_nk = nk_convert("data/SiCx_nk.csv", energy=E_eV)
zns_nk = nk_convert("data/ZnS_nk.csv", energy=E_eV)
# print(alinp_nk)
# Build the optical stack 建立光学堆栈...

wl = 1240 / E_eV
ml1 = material("MgF2", sopra=True)(T=300)
ml1_n = ml1.n(wl*1e-9)
ml1_k = ml1.k(wl*1e-9)

ml2 = material("SiC", sopra=True)(T=300)
ml2_n = ml2.n(wl*1e-9)
ml2_k = ml2.k(wl*1e-9)
ml3 = material("ZNSCUB", sopra=True)(T=300)
ml3_n = ml3.n(wl*1e-9)
ml3_k = ml3.k(wl*1e-9)

ml4=material("AlInP")(T=300,Al=1)
# ml4_1 = material("AlGaInP")(T=300,Al=1)

ml4_n = ml4.n(wl*1e-9)
ml4_k = ml4.k(wl*1e-9)

ml5 = material("GaInP")(T=300,In=0.5)
ml5_n = ml5.n(wl*1e-9)
ml5_k = ml5.k(wl*1e-9)

stack = Structure([
    [117, 1240 / E_eV, ml1_n, ml1_k],
    [80, 1240 / E_eV, sic_nk[1], sic_nk[2]],
    [61, 1240 / E_eV, ml3_n, ml3_k],
    [25, 1240 / E_eV, ml4_n,ml4_k],
    [350000, 1240 / E_eV,ml5_n,ml5_k]
])

angles = np.linspace(0, 80, 10) # 角度
RAT_angles = []

# ARC anti-reflection coating 防反射涂层
# print("Calculate RAT ::")     # reflected, absorbed, and transmitted 反射，吸收，传输
for theta in angles:
    # print("Calculating at angle :: %4.1f deg" % theta)
    # Calculate RAT data...
    rat_data = calculate_rat(stack, angle=theta, wavelength=1240 / E_eV)    # 层，角度，波长<<<

    RAT_angles.append((theta, rat_data["R"], rat_data["A"]))

print(len(RAT_angles))
colors = plt.cm.jet(np.linspace(1, 0, len(RAT_angles)))

fig, ax2 = plt.subplots(1, 1)

for i, RAT in enumerate(RAT_angles):
    ax2.plot(1240 / E_eV, RAT[1] * 100, ls="-", color=colors[i], label="%4.1f$^\circ$" % RAT[0])    # 反射曲线
    ax2.plot(1240 / E_eV, RAT[2] * 100, ls="--", color=colors[i])   # 吸收曲线

ax2.set_ylim([0, 100])
ax2.set_xlim([300, 1800])
ax2.set_xlabel("Wavelength (nm)")
ax2.set_ylabel("Reflection and Transmission (%)")
ax2.legend(loc=5)
ax2.text(0.05, 0.45, '(a)', transform=ax2.transAxes, fontsize=12)

plt.tight_layout(w_pad=4)
plt.show()
