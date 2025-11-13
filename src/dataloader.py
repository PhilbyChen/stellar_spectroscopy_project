from astropy.io import fits
import numpy as np

def read_vega_spectrum(data_file):
    with fits.open(data_file) as hdul:
        data = hdul[1].data
        wavelength = data["WAVELENGTH"]
        flux = data["FLUX"]
        instrument_FWHM = data["FWHM"]   # full width at half-maximum
        totexp = data["TOTEXP"]   # 曝光时间

        print(f"波长范围: {wavelength.min():.1f} - {wavelength.max():.1f} Å")
        print(f"通量范围: {flux.min():.2e} - {flux.max():.2e}")
        
        return wavelength, flux, instrument_FWHM, totexp
    
    
def normalize_flux(wavelength,flux):
    max_flux = np.max(flux)
    norm_flux = flux/max_flux

    return wavelength, norm_flux, max_flux