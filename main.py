import sys
import os
import numpy as np

# 设置路径
src_dir = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_dir)

from dataloader import read_vega_spectrum
from visualizer import plot_spectrum
from physic_analyzer import surface_temperature
print(" 所有模块导入成功！")

def main():

    data_file = r"D:\Documents\GitHub\stellar_spectroscopy_project\data\alpha_lyr_stis_011.fits"
    print(f"读取文件: {data_file}")

    wavelength, flux, instrument_FWHM, totexp= read_vega_spectrum(data_file)
    plot_spectrum(wavelength, flux, 'Vega Spectrum')
    # 检查数据范围
    print(f"通量范围: {flux.min():.2e} - {flux.max():.2e}")

    # 简单估算表面温度
    surface_temperature(wavelength,flux)

    # ====================普朗克黑体辐射拟合====================
    # 归一化处理
    from dataloader import normalize_flux
    wl_norm, flux_norm, max_flux = normalize_flux(wavelength, flux)
    
    # 黑体拟合
    from physic_analyzer import fit_blackbody
    temperature, fitted_curve = fit_blackbody(wl_norm, flux_norm)
    
    print(f"黑体拟合温度: {temperature:.0f} K")


    # ====================氢巴尔末谱线====================
    from dataloader import normalize_flux
    wl_norm, flux_norm, max_flux = normalize_flux(wavelength, flux) 

    from physic_analyzer import balmerlines
    W = balmerlines(wl_norm, flux_norm)


if __name__ == "__main__":
    main()