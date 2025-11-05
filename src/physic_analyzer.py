import numpy as np

#1.维恩位移定律估算表面温度
# λmax*T=b
def surface_temperature(wavelength,flux):
    # 找出最长的波长
    λmax = wavelength[np.argmax(flux)]
    # 单位换算：埃——米,计算
    T = 0.002897 / (λmax * 1e-10)
    print("最大波长：",λmax)
    print("T:",T)
    return T   # 此计算结果温度为7199K，而真实计算温度为9600K左右，可能是数据集紫外波段受消光影响所致