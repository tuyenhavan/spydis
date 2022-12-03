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
        if check_date(start_date):
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

def check_date(date_str):
    """ Check if date is in a required format.

        Args:
            date_str (str): Date in string format.
    """
    fmts="%Y-%m-%d"
    try:
        _date=dt.datetime.strptime(date_str,fmts)
        return True
    except Exception:
        raise Exception

