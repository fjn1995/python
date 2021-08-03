import numpy as np
import matplotlib.pyplot as plt

from solcore.light_source import LightSource


class L_S_Plot():
    """光源类绘图"""
    def __init__(self):
        wl = np.linspace(300, 2000, 50)

        # Now different types of light sources can be defined
        self.gauss = LightSource(source_type='laser', x=wl, center=800, linewidth=50, power=200)
        self.bb = LightSource(source_type='black body', x=wl, T=5800, entendue='Sun')
        self.am15g = LightSource(source_type='standard', x=wl, version='AM1.5g')
        self.am0 = LightSource(source_type='standard', x=wl, version='AM0')  # 大气层外接收的太阳光谱，适用于人造卫星或宇宙飞船
        self.spectral = LightSource(source_type='SPECTRAL2', x=wl)  # 光谱


    def gauss_plot(self):
        plt.plot(*self.gauss.spectrum(), label='Gauss')
        self.plt_plot('gauss')

    def bb_plot(self):
        plt.plot(*self.bb.spectrum(), label='Black body')
        self.plt_plot('bb')
    def am15g_plot(self):
        plt.plot(*self.am15g.spectrum(),label = 'AM1.5g')
        self.plt_plot('am15g')
    def am0_plot(self):
        plt.plot(*self.am0.spectrum(), label='AM0')
        self.plt_plot('am0')
    def spectral_plot(self):
        plt.plot(*self.spectral.spectrum(), label='SPECTRAL2')
        self.plt_plot('spectral')
    def all_plot(self):
        plt.plot(*self.gauss.spectrum(), label='Gauss')
        plt.plot(*self.bb.spectrum(), label='Black body')
        plt.plot(*self.am15g.spectrum(),label = 'AM1.5g')
        plt.plot(*self.am0.spectrum(), label='AM0')
        plt.plot(*self.spectral.spectrum(), label='SPECTRAL2')
        self.plt_plot('all')

    def plt_plot(self,Light_Source_Type):
        plt.xlim(300, 3000)
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Power density (Wm$^{-2}$nm$^{-1}$)')
        plt.title("不同光谱的功率密度")
        plt.tight_layout()
        plt.legend(frameon=False)

        plt.savefig('light_plot/{}.png'.format(Light_Source_Type))
        plt.close()

    # def smarts_plot(self):
    #     try:
    #         smarts = LightSource(source_type='SMARTS', x=wl)
    #         plt.plot(*smarts.spectrum(), label='SMARTS')
    #     except TypeError:
    #         pass
    #
    #     try:
    #         # Plot comparing the spectra calculated with SMARTS at different hours of the day
    #         for h in range(8, 20):
    #             plt.plot(*smarts.spectrum(HOUR=h), label='{} h'.format(h))
    #     plt.xlim(300, 3000)
    #     plt.xlabel('Wavelength (nm)')
    #     plt.ylabel('Power density (Wm$^{-2}$nm$^{-1}$)')
    #     plt.tight_layout()
    #     plt.legend()
    #     except TypeError:
    #         pass
