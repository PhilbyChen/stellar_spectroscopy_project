import numpy as np

#1.维恩位移定律估算表面温度
# λmax*T=b
def surface_temperature(wavelength,flux):

    λmax = wavelength[np.argmax(flux)]
    T = 0.0028977721 / (λmax * 1e-10)
    print("最大波长：",λmax)
    print("T:",T)

    return T

#2.普朗克黑体辐射拟合
def fit_blackbody(wavelength,flux):
    from scipy.optimize import curve_fit
    def planck_law(wl,temperature,scale):
        # lamda wl：波长
        # Tem: 温度
        # scale: 匹配因子

        h = 6.62607015e-34
        c = 3.0e8
        k = 1.380649e-23

        wl_m = wl * 1e-10  # 波长从埃转换为米
        
        # 普朗克黑体辐射公式 B(λ,T) = (2h·c² / λ⁵) · [1 / (e^(h·c/(λ·k·T)) - 1)]
        numerator = 2 * h * c**2
        exponent = (h * c) / (wl_m * k * temperature)
        denominator = (wl_m**5) * (np.exp(exponent) - 1)
        theoretical_flux = numerator / denominator
        scaled_flux = scale * theoretical_flux
        
        return scaled_flux
  

    # ==================== 执行曲线拟合 ====================
    # 使用非线性最小二乘法找到最佳的黑体参数
    # 初始猜测值: [温度, 缩放因子]
    # 织女星是A型星，温度约9600K，所以用10000K作为初始值
    # 缩放因子初始为1.0，让拟合算法自动调整
    initial_guess = [10000, 1.0]
    
    # 执行拟合: 找到使理论曲线最接近观测数据的参数
    popt, _ = curve_fit(planck_law, wavelength, flux, p0=initial_guess)
    
    # 提取拟合结果
    temperature, scale_factor = popt
    
    # 用最佳参数生成完整的拟合曲线
    fitted_curve = planck_law(wavelength, temperature, scale_factor)
    
    return temperature, fitted_curve