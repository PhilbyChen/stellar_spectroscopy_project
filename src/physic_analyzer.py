import numpy as np

'''1.维恩位移定律估算表面温度'''
# λmax*T=b
def surface_temperature(wavelength,flux):

    λmax = wavelength[np.argmax(flux)]
    T = 0.0028977721 / (λmax * 1e-10)
    print("最大波长：",λmax)
    print("T:",T)

    return T

'''2.巴尔末跳跃'''
def locate_balmer_jump(wavelength,flux):
    search_region = (wavelength > 2000) & (wavelength < 5000)
    wl_search = wavelength[search_region]
    flux_search = flux[search_region]
    # 找到梯度最大点
    max_gradient_index = np.argmax(np.diff(flux_search))
    balmer_jump_wavelength = wl_search[max_gradient_index + 1] # +1 因为diff使数组缩短了一位
    print(f"巴尔末跳跃位置: {balmer_jump_wavelength:.1f} Å")

    return balmer_jump_wavelength

'''3.普朗克黑体辐射拟合'''
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
    from physic_analyzer import locate_balmer_jump
    balmer_jump_wavelength = locate_balmer_jump(wavelength,flux)
    long_wavelength_region = (wavelength > balmer_jump_wavelength) & (wavelength < 25000)
    wavelength_fit = wavelength[long_wavelength_region]
    flux_fit = flux[long_wavelength_region]
    
    # 缩放因子初始为1.0，让拟合算法自动调整
    initial_guess = [10000, 1.0]
    # 执行拟合: 找到使理论曲线最接近观测数据的参数
    popt, _ = curve_fit(planck_law, wavelength_fit, flux_fit, p0=initial_guess)
    
    # 提取拟合结果
    temperature, scale_factor = popt
    
    # 用最佳参数生成完整的拟合曲线
    fitted_curve = planck_law(wavelength, temperature, scale_factor)
    
    return temperature, fitted_curve


'''4.氢巴尔末谱线-等值宽度'''
#测量四条氢谱线等值宽度与半高全宽
def balmerlines(wavelength,flux):
    balmer_lines = {'Hα': 6562.8, 'Hβ': 4861.3, 'Hγ': 4340.5, 'Hδ': 4101.7}

    results = {}

    for name,center in balmer_lines.items():
        
        #吸收谱线
        line_region = (wavelength > center - 15) & (wavelength < center + 15)
        #两侧连续谱
        left_continuum = (wavelength > center - 50) & (wavelength < center - 25)
        right_continuum = (wavelength > center + 25) & (wavelength < center + 50)

        #计算平均连续谱Fc
        left_flux = np.mean(flux[left_continuum])  # ***[***] :布尔索引，提取left_continuum里为True的flux值
        right_flux = np.mean(flux[right_continuum])
        Fc = (left_flux + right_flux) / 2

        ### 计算等值宽度
        line_wl = wavelength[line_region]
        Fλ = flux[line_region]
        depth = (Fc - Fλ) / Fc
        # 深度在步长上积分
        # W = ∫(Fc − Fλ) / Fc dλ
        W = np.trapz(depth, line_wl)
        results[name] = W
        
        # f"{name}: {W:.2f} Å" 是f-string格式化字符串
        print(f"'等值宽度,'{name}: {W:.4f} Å")
    
    return results


'''5.测量半高全宽'''
def measure_fwhm(wavelength,norm_flux,center,instrument_FWHM):
    
    line_region = (wavelength > center - 15) & (wavelength < center + 15)
    line_wl = wavelength[line_region]
    line_flux = norm_flux[line_region]

    # Another measure of the width of a spectral line is the change in wavelength from one side of the line to the other, 
    #   where its depth (Fc − Fλ)/(Fc − Fλ0) = 1/2; this is called the full width at half-maximum and will be denoted by (3λ)1/2.

    # “半高” 部分
    line_depth = 1 - np.min(line_flux)
    # 半高位置 = 连续谱水平 - 半深度 = 1 - line_depth/2
    half_level = 1.0 - line_depth / 2.0
    # "全宽" 部分
    # 数组位置索引
    below_positions = np.where(line_flux < half_level)[0]
    left_position = below_positions[0]  #第一个低于半高水平的点
    right_position = below_positions[-1]  # 最后一个

    observed_fwhm = line_wl[right_position] - line_wl[left_position]
 
    # 修正仪器展宽
    intrinsic_fwhm_squared = observed_fwhm**2 - instrument_FWHM**2
    
    if (intrinsic_fwhm_squared > 0).all():
        intrinsic_fwhm = np.sqrt(intrinsic_fwhm_squared)
    else:
        intrinsic_fwhm = 0.0
    
    return intrinsic_fwhm



'''测量压力展宽'''
def pressure_broadening(wavelength, norm_flux, instrument_FWHM):

    test_lines = {
        'Hγ': 4340.5,
        'Fe_I_4383': 4383.5
    }
    results = {}
    for name,center in test_lines.items():
        fwhm = measure_fwhm(wavelength,norm_flux,center,instrument_FWHM)
        results[name] = fwhm

    H_width = results['Hγ']
    Fe_width = results['Fe_I_4383']
    width_difference = H_width - Fe_width
    print("H_width:",H_width,
          "Fe_width:",Fe_width,
          "width_difference:",width_difference)
    if width_difference > 3.0:
            print("主序星范围，光度V")
    else:
            print("巨星范围")
    return results