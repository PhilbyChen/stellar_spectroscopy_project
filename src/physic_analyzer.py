import numpy as np

'''1.维恩位移定律估算表面温度'''
# λmax*T=b
def surface_temperature(wavelength,flux):

    λmax = wavelength[np.argmax(flux)]
    T = 0.0028977721 / (λmax * 1e-10)
    print("最大波长：",λmax)
    print("T:",T)

    return T

'''2.普朗克黑体辐射拟合'''
def fit_blackbody(wavelength,flux):
    from scipy.optimize import curve_fit
    def planck_law(wl,temperature,scale):
        # wl：波长
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


'''3.氢巴尔末谱线'''
#测量四条氢谱线等值宽度与半高全宽
def balmerlines(wavelength,flux):
    balmer_lines = {
    'Hα': 6562.8,
    'Hβ': 4861.3,
    'Hγ': 4340.5,
    'Hδ': 4101.7
    }

    results = {} # 初始化空字典存储等值宽度

    for name,center in balmer_lines.items():
        
        #吸收谱线
        line_region = (wavelength > center - 5) & (wavelength < center - 5)
        #两侧连续谱
        left_continuum = (wavelength > center - 20) & (wavelength < center - 10)
        right_continuum = (wavelength > center + 10) & (wavelength < center + 20)

        #计算平均连续谱Fc
        left_flux = np.mean(flux[left_continuum])  # ***[***] :布尔索引，提取left_continuum里为True的flux值
        right_flux = np.mean(flux[right_continuum])
        Fc = (left_flux + right_flux) / 2

        ### 计算等值宽度

        line_wl = wavelength[line_region]
        Fλ = flux[line_region]
        depth = (Fc - Fλ) / Fc
        # 计算波长步长：相邻波长点之间的平均间隔
        # np.diff(wavelength) 计算相邻元素的差值
        wl_step = np.diff(wavelength).mean()
        # 深度在步长上积分
        # W = ∫(Fc − Fλ) / Fc dλ
        W = np.sum(depth) * wl_step
        results[name] = W
        
        # f"{name}: {W:.2f} Å" 是f-string格式化字符串
        print(f"  {name}: {W:.2f} Å")
    
    return results