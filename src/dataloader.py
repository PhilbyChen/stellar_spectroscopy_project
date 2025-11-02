#读取fits光谱数据
from astropy.io import fits


#格式说明：来自http://vizier.nao.ac.jp/ftp/J/AJ/146/68/ReadMe
# Byte-by-byte Description of file: table2[6789].dat
#--------------------------------------------------------------------------------
#   Bytes Format   Units      Label     Explanations
#--------------------------------------------------------------------------------
#   1-  9  F9.2    0.1nm      lambda    [900/] Wavelength {lambda} in {AA}
#  11- 23  E13.7   cW/m2/nm   Flux      Flux; in erg/s/cm^2^/A

def read_vega_spectrum(datapath):
    with fits.open(datapath) as hdul:   #用with打开可以自动打开和关闭文件；hdul是包含hits文件中所有数据单元Header/Data Units的列表
        for hdu in hdul:
            data = hdu.data
            wavelength = data[:, 0]  # 所有行的第0列
            flux = data[:, 1]        # 所有行的第1列
            return wavelength,flux
        
def read_spectrum(file_path):
    with fits.open(file_path) as hdul:
        # 获取第一个数据表（通常是hdul[1]）
        data = hdul[1].data
        
        # 提取列名
        col_names = data.dtype.names
        
        # 假设第一列是波长，第二列是通量
        wavelength = data[col_names[0]]
        flux = data[col_names[1]]
        
        return wavelength, flux