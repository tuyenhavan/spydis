# spydis
A simple package for calculating drought indices based on time-series remote sensing and gridded datasets.
# Main features
This package focuses on calculating some commonly used drought indices from remote sensing and meteorological perspectives:
- **Remote sensing-based drought indices**
	- VCI: Vegetation condition index. VCI can range from 0 (0) to 1 (100) scale, which indicates extreme to non-drought, respectively. Details can be found [here](https://www.tandfonline.com/doi/abs/10.1080/01431169608949106)
	- TCI: Temperature condition index. The values range from 0 (0) to 1 (100) scale, which indicates extreme to non-drought. Details can be found [here](https://doi.org/10.1016/0273-1177(95)00079-T)
	- VHI: Vegetation health index. This index is based on VCI and TCI and its value ranges from 0 to 100, indicating extreme to non-drought condition. Details can be found [here](https://doi.org/10.1016/j.rse.2010.07.005)
	- VAI: Vegetation anomaly index. This index indicates the variations of vegetation of a certain time with long-term statistics. Details can be found [here](https://doi.org/10.3390/rs11151783)
- **Meteorological drought indices**
	- SPI: Standardized precipitation index
	- SPEI: Standardized precipitation evapotranspiration index
