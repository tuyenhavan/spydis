"""A module for calculating common drought indices from remote sensing time-series data recommended by the International Meteorological Organization (IMO)"""

def VCI(data, dim=None, freq=None):
    """ Calculate VCI (Vegetation Condition Index) from time-series NDVI observations. This function can be extended to TCI.

        Args:
        data (DataArray): Time-series NDVI data
        dim (str|optional): A time dimension.
        frq (str|optional): A time frequency (e.g., day, month, year)

        Return:
            VCI (DataArray): Time-series VCI calculated from NDVI data.

        Reference: https://doi.org/10.1016/0273-1177(95)00079-T
    """

    if not isinstance(data, xr.core.dataarray.DataArray):
        raise TypeError ("Data should be xarray DataArray")
    if dim is None:
        dim=data.dims[0].strip()
    else:
        dim=dim
    if freq is None:
        freq="month"
    else:
        freq=freq
    if freq.lower() in ["month","months","m"]:
        ndvi_min=data.groupby(f"{dim}.month").min(f"{dim}")
        ndvi_max=data.groupby(f"{dim}.month").max(f"{dim}")
        max_min=ndvi_max-ndvi_min
        nominator=data.groupby(f"{dim}.month")-ndvi_min
        vci=nominator.groupby(f"{dim}.month")/max_min*100
        return vci
    elif freq.lower() in ["days","day","d"]:
        ndvi_min=data.groupby(f"{dim}.day").min(f"{dim}")
        ndvi_max=data.groupby(f"{dim}.day").max(f"{dim}")
        max_min=ndvi_max-ndvi_min
        nominator=data.groupby(f"{dim}.day")-ndvi_min
        vci=nominator.groupby(f"{dim}.day")/max_min*100
        return vci
    elif freq.lower() in ["years","year","y"]:
        ndvi_min=data.min(f"{dim}")
        ndvi_max=data.max(f"{dim}")
        max_min=ndvi_max-ndvi_min
        nominator=data-ndvi_min
        vci=nominator/max_min*100
        return vci
    else:
        print("This function only supports the calculation of monthly, daily and yearly VCI.")

def AVI(data, dim=None, freq=None):
    """ Calculate AVI (Anomaly Vegetation Index) from time-series NDVI observations.

        Args:
        data (DataArray): Time-series NDVI data
        dim (str|optional): A time dimension.
        frq (str|optional): A time frequency (e.g., day, month, year)

        Return:
            AVI (DataArray): Time-series AVI calculated from NDVI data.
    """

    if not isinstance(data, xr.core.dataarray.DataArray):
        raise TypeError ("Data should be xarray DataArray")
    if dim is None:
        dim=data.dims[0].strip()
    else:
        dim=dim
    if freq is None:
        freq="month"
    else:
        freq=freq
    if freq.lower() in ["month","months","m"]:
        ndvi_mean=data.groupby(f"{dim}.month").mean(f"{dim}")
        avi=data.groupby(f"{dim}.month")-ndvi_mean
        return avi
    elif freq.lower() in ["days","day","d"]:
        ndvi_mean=data.groupby(f"{dim}.day").mean(f"{dim}")
        avi=data.groupby(f"{dim}.day")-ndvi_mean
        return avi
    elif freq.lower() in ["years","year","y"]:
        ndvi_mean=data.mean(f"{dim}")
        avi=data-ndvi_mean
        return avi
    else:
        print("This function only supports the calculation of monthly, daily and yearly AVI.")

def VHI(vci,tci, scale=None):
    """ Calculate VHI (Vegetation Health Index) from time-series VCI and TCI observations.

        Args:
        vci (DataArray|numpy): Time-series VCI data
        tci (DataArray|numpy): Time-series TCI data.
        scale (float|optional): a scaling factor. Default to None.

        Return:
            VHI (DataArray): Time-series VHI calculated from VIC and TCI data.

        Reference: https://doi.org/10.1080/01431169008955102
    """

    if not isinstance(vci, (xr.core.dataarray.DataArray, ndarray)) and not isinstance(tci, (xr.core.dataarray.DataArray, ndarray)):
        raise TypeError ("Data should be xarray DataArray or numpy")
    if not isinstance(scale, float):
        raise TypeError ("Scale should be float point")
    if vci.shape==tci.shape:
        vhi=scale*vci+(1-scale)*tci
        return vhi
    else:
        raise ValueError ("VCI and TCI must have the same shapes")

def TCI(data, dim=None, freq=None):
    """ Calculate TCI from time-series LST observations.

        Args:
        data (DataArray): Time-series LST data
        dim (str|optional): A time dimension.
        frq (str|optional): A time frequency (e.g., day, month, year)

        Return:
            TCI (DataArray): Time-series TCI calculated from LST data.

        Reference: https://doi.org/10.1016/0273-1177(95)00079-T
    """

    if not isinstance(data, xr.core.dataarray.DataArray):
        raise TypeError ("Data should be xarray DataArray")
    if dim is None:
        dim=data.dims[0].strip()
    else:
        dim=dim
    if freq is None:
        freq="month"
    else:
        freq=freq
    if freq.lower() in ["month","months","m"]:
        lst_min=data.groupby(f"{dim}.month").min(f"{dim}")
        lst_max=data.groupby(f"{dim}.month").max(f"{dim}")
        max_min=lst_max-lst_min
        nominator=data.groupby(f"{dim}.month")-lst_min
        tci=nominator.groupby(f"{dim}.month")/max_min*100
        return tci
    elif freq.lower() in ["days","day","d"]:
        lst_min=data.groupby(f"{dim}.day").min(f"{dim}")
        lst_max=data.groupby(f"{dim}.day").max(f"{dim}")
        max_min=lst_max-lst_min
        nominator=data.groupby(f"{dim}.day")-lst_min
        tci=nominator.groupby(f"{dim}.day")/max_min*100
        return tci
    elif freq.lower() in ["years","year","y"]:
        lst_min=data.min(f"{dim}")
        lst_max=data.max(f"{dim}")
        max_min=lst_max-lst_min
        nominator=data-lst_min
        tci=nominator/max_min*100
        return tci
    else:
        print("This function only supports the calculation of monthly, daily and yearly TCI.")
