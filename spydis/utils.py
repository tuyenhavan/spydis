""" Helper functions for facilitating drought indices"""

import xarray as xr
import rioxarray as rx
from dateutil.relativedelta import relativedelta
import datetime as dt

def time_dimension(ds, start_date=None, freq=None,input_dim=None,out_dim=None):
    """ A helper function to add a time dimension to the DataArray.

        Args:
            ds (DataArray): A xarray DataArray.
            start_date (str|optional): A start date of acquired dataset. Default uses None.
            freq (str|optional): A time frequency such as day (d), month (m), or year (y). Default uses None.
            input_dim (str|optional): A dimension that should be time dimension. Default uses None.
            out_dim (str|optional): A desired time dimension name. Default uses None.

        Return:
            A dataset (DataArray): Added a new time dimension.
    """
    if not isinstance(ds,xr.core.dataarray.DataArray):
        print(f"Please ensure {ds} is xarray.DataArray")
    if not isinstance(start_date, (type(None),str)) or not isinstance(freq, (type(None),str)):
        print(f"Please ensure {start_date} and {freq} are string or None")
    if start_date is None:
        start_date=dt.datetime.strptime("2000-02-01","%Y-%m-%d")
    else:
        start_date=date_format(start_date)
        start_date=dt.datetime.strptime(f"{start_date}","%Y-%m-%d")
    if input_dim is None:
        input_dim="band"
    else:
        input_dim=f"{input_dim}"
    if out_dim is None:
        out_dim="time"
    else:
        out_dim =f"{out_dim}"

    if freq is None or freq.lower() in ["m","months","month"]:
        start_date=[start_date+relativedelta(months=i) for i in range(len(ds))]
    else:
        if freq.lower() in ["d","day","days"]:
            start_date=[start_date+relativedelta(days=i) for i in range(len(ds))]
        elif freq.lower() in ["y","year","years"]:
            start_date=[start_date+relativedelta(years=i) for i in range(len(ds))]
    if not input_dim.lower() in ds.dims:
        print(f"{input_dim} is not one of the dimensions in the DataArray")
        raise ValueError("Please check the desired dimension that wanted to convert into time dimension.")
    ds[input_dim]=start_date
    ds=ds.rename({input_dim:out_dim})
    return ds

def date_format(date_str):
    """ Format datet string.

        Args:
            date_str (str): Date in string format.
    """
    if isinstance(date_str,str):
        if "." in date_str:
            date_str="-".join([i.strip() for i in date_str.split(".") if i.isdigit()])
            return date_str
        elif "/" in date_str:
            date_str="-".join([i.strip() for i in date_str.split("/") if i.isdigit()])
            return date_str
        elif "-" in date_str:
            date_str="-".join([i.strip() for i in date_str.split("-") if i.isdigit()])
            return date_str
        else:
            print("Date string should be like 2000-10-20")
    else:
        raise TypeError ("Please provide date string")


def NDVI(red,nir):
    """ Calculte NDVI from Red and Near Infrared bands.

        Args:
            red (numpy|DataArray): Red band in
            nir (numpy|DataArray): Nir infreared band

        return:
            NDVI (DataArray|numpy)

        Reference: https://doi.org/10.1175/1520-0477(1995)076%3C0655:DOTLIT%3E2.0.CO;2
    """
    if isinstance(red,(xr.core.dataarray.DataArray,np.ndarray)) and isinstance(nir,(xr.core.dataarray.DataArray,np.ndarray)):
        if (red.shape==nir.shape) and (len(red.shape)==2 and len(nir.shape)==2):
            ndvi=(nir-red)/(nir+red)
            return ndvi
        else:
            raise ValueError ("Input data are not the same shape")
    else:
        raise TypeError ("Input data should be DataArray or numpy 2-D")

def SAVI(nir,red,scale=0.5):
    """ Calculate SAVI (Soil Adjusted Vegetation Index)

        Args:
            nir (numpy|DataArray): Nir infreared band
            red (numpy|DataArray): Red band in
            scale (float|optional): A scaling factor.

        return:
            SAVI (numpy|DataArray): A SAVI data

        Reference: https://doi.org/10.1016/0034-4257(88)90106-X
    """
    if isinstance(red,(xr.core.dataarray.DataArray,np.ndarray)) and isinstance(nir,(xr.core.dataarray.DataArray,np.ndarray)):
        if (red.shape==nir.shape) and (len(red.shape)==2 and len(nir.shape)==2):
            pass
        else:
            raise ValueError ("Datasets should have the same shape")
    else:
        raise TypeError("Datasets should be DataArray or numpy")
    if not isinstance(scale, float):
        raise TypeError ("scale should be float")
    savi=((nir-red)/(nir+red+scale))*(1+scale)
    return savi