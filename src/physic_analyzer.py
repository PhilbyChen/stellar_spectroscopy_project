import numpy as np

#1.维恩位移定律估算表面温度
# λmax*T=b
def surface_temperature(wavelength,flux):
    # 找出最长的波长
    λmax = wavelength[np.argmax(flux)]
    # 单位换算：埃——米,计算
    T = 0.0028977721 / (λmax * 1e-10)
    print("最大波长：",λmax)
    print("T:",T)
    return T