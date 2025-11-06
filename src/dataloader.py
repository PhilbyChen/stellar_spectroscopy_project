#读取fits光谱数据
from astropy.io import fits


#格式说明：来自http://vizier.nao.ac.jp/ftp/J/AJ/146/68/ReadMe
# Byte-by-byte Description of file: table2[6789].dat
#--------------------------------------------------------------------------------
#   Bytes Format   Units      Label     Explanations
#--------------------------------------------------------------------------------
#   1-  9  F9.2    0.1nm      lambda    [900/] Wavelength {lambda} in {AA}
#  11- 23  E13.7   cW/m2/nm   Flux      Flux; in erg/s/cm^2^/A


def read_vega_spectrum(data_file):
    with fits.open(data_file) as hdul:
        for hdu in hdul:
            # 只处理有数据的HDU
            if hasattr(hdu, 'data') and hdu.data is not None:
                data = hdu.data
                wavelength = data[:, 0]  # 所有行的第0列
                flux = data[:, 1]        # 所有行的第1列
              
                print(f"波长范围: {wavelength.min():.1f} - {wavelength.max():.1f} Å")
                print(f"通量范围: {flux.min():.2e} - {flux.max():.2e} FLAM")
              
                return wavelength, flux
        raise ValueError("没有找到包含数据的HDU")