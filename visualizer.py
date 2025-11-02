import matplotlib.pyplot as plt

def plot_spectrum(wavelength, flux, title="Spectrum"):
    """绘制光谱图"""
    plt.figure(figsize=(10, 5))
    plt.plot(wavelength, flux, 'b-', linewidth=1)
    plt.xlabel('Wavelength')
    plt.ylabel('Flux')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()