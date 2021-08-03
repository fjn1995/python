import pandas as pd
import numpy as np
from solcore.absorption_calculator import sopra_db
import os

class ML_DB():
    """n——K的材料类"""
    def __init__(self):
        self.sopra_data_path = sopra_db.SOPRA_PATH
        self.sopra_data = np.genfromtxt(os.path.join(self.sopra_data_path, "SOPRA_DB_Updated.csv"), delimiter=",", dtype=str)
        self.sopra_composition_data = np.genfromtxt(os.path.join('solcore_datas', "sopra_composition.csv"), delimiter=",", dtype=str)

    def ml_nk_data(self):
        """材料的n—k数据"""
        self.fnames = []
        self.symbols = []
        self.symbol_name = []

        self.ranges_old = []
        self.ranges = []
        self.infos = []

        for fname, symbol, range, info in self.sopra_data[2:127,:]:
            self.fnames.append(fname)
            self.symbols.append(symbol)
            range = " —— ".join(range.split())
            self.ranges.append(range)
            self.infos.append(info)

            a = f'{symbol}({fname})'
            self.symbol_name.append(a)

        return self.symbol_name,self.ranges,self.infos,self.fnames

    def ml_nk_T_data(self):
        """与温度相关的材料的折射率，消光系数"""
        self.fnames_T = []
        self.symbols_T = []
        self.ranges_T = []
        self.infos_T = []
        self.symbols_T_unique = []
        for fname, symbol, range, info in self.sopra_data[130:187,:]:
            self.fnames_T.append(fname)
            self.symbols_T.append(symbol)
            range = " —— ".join(range.split())
            self.ranges_T.append(range)
            self.infos_T.append(info)

        for i in self.symbols_T:
            if i not in self.symbols_T_unique:
                self.symbols_T_unique.append(i)

        return self.symbols_T_unique,self.ranges_T,self.infos_T,self.symbols_T,self.fnames_T

    def ml_nk_composition_data(self):
        """材料成分比例不同的折射率，消光系数"""
        self.fnames_composition = []
        self.symbols_composition = []
        self.ranges_composition = []
        self.infos_composition = []
        self.compos = []
        for fname, symbol, range, info,compos in self.sopra_composition_data[1:,:]:
            self.fnames_composition.append(fname)
            self.symbols_composition.append(symbol)
            self.ranges_composition.append(range)
            self.infos_composition.append(info)
            self.compos.append(compos)
        return self.fnames_composition,self.symbols_composition,self.ranges_composition,self.infos_composition,self.compos

def ml_data():
    """材料的n—k数据"""
    material_data = pd.read_csv("solcore_datas/material_nk_data.csv")
    material_data = material_data.iloc[0:,0:1]
    list =material_data.values.tolist()
    material_datas = []
    for i in range(len(list)):
        material_datas.append(list[i][0])
    return material_datas

