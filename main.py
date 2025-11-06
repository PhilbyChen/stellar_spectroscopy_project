import sys
import os

# 设置路径
src_dir = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_dir)

from dataloader import read_spectrum
from visualizer import plot_spectrum
from physic_analyzer import surface_temperature
print(" 所有模块导入成功！")

def main():
    # 使用绝对路径
    data_file = r"D:\Documents\GitHub\stellar_spectroscopy_project\data\alpha_lyr_stis_011.fits"
    print(f"读取文件: {data_file}")

    wavelength, flux = read_spectrum(data_file)
    plot_spectrum(wavelength, flux, 'Vega Spectrum')
    # 检查数据范围
    print(f"通量范围: {flux.min():.2e} - {flux.max():.2e}")

    # 计算表面温度
    surface_temperature(wavelength,flux)

if __name__ == "__main__":
    main()