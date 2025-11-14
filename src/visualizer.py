import matplotlib.pyplot as plt
import numpy as np

'''波长-通量图'''
def plot_spectrum(wavelength, flux, title="Spectrum"):
    plt.figure(figsize=(10, 5))
    plt.plot(wavelength, flux, 'b-', linewidth=1)
    plt.xlabel('Wavelength')
    plt.ylabel('Flux')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 25000)

    # 主要波长区域标注
    plt.axvspan(1000, 4000, alpha=0.1, color='purple', label='UV')
    plt.axvspan(4000, 7000, alpha=0.1, color='blue', label='Optical')
    plt.axvspan(7000, 25000, alpha=0.1, color='red', label='IR')
    plt.legend()

    # 标记巴尔末系限
    from physic_analyzer import locate_balmer_jump
    jump_location = locate_balmer_jump(wavelength, flux)

    plt.axvline(x=jump_location, color='red', linestyle='--', linewidth=3, 
                label=f'Detected Balmer Jump ({jump_location:.0f} Å)')
    plt.axvline(x=3646, color='black', linestyle=':', linewidth=2, 
                label='Theoretical (3646 Å)')
    
    plt.legend()

    plt.tight_layout()
    plt.show()