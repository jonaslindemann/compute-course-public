# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 11:37:54 2018

@author: Jonas Lindemann
"""

from datetime import datetime

import requests

import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates


class SMHI:
    """Class for extracting a weather forecast"""

    def __init__(self, longitude="16", latitude="58"):
        """Class constructor"""

        self.url = "https://opendata-download-metfcst.smhi.se"
        self.api_template = "/api/category/{}/version/{}/geotype/point/lon/{}/lat/{}/data.json"
        self.param_template = "/api/category/{}/version/{}/parameter.json"
        self.category = "snow1g"
        self.version = "1"
        self.longitude = longitude
        self.latitude = latitude
        self.request_parameters()
        self.request_forecast()

    def request_parameters(self):
        """Request parameter descriptions (units, missing values) from SMHI"""

        param_string = self.param_template.format(self.category, self.version)

        smhi_info = requests.get(self.url + param_string)
        smhi_info.raise_for_status()

        self.parameters = {}

        for param in smhi_info.json()["parameter"]:
            self.parameters[param["name"]] = param

    def request_forecast(self):
        """Request data from SMHI"""

        api_string = self.api_template.format(self.category,
                                              self.version,
                                              self.longitude,
                                              self.latitude)

        smhi_info = requests.get(self.url + api_string)
        smhi_info.raise_for_status()

        self.forecast = smhi_info.json()

    def parameter_names(self):
        """Return a dict with available parameter names and their units"""

        names = {}

        for item in self.forecast["timeSeries"]:
            for name in item["data"]:
                if not name in names:
                    if name in self.parameters:
                        names[name] = self.parameters[name]["unit"]
                    else:
                        names[name] = ""

        return names

    def parameter_values(self, name):
        """Extract specific values from data"""

        missing_value = None
        if name in self.parameters:
            missing_value = self.parameters[name]["missingValue"]

        date_times = []
        values = []

        for item in self.forecast["timeSeries"]:
            data = item["data"]
            if name in data and data[name] != missing_value:
                values.append(float(data[name]))
                date_times.append(datetime.fromisoformat(item["time"].replace("Z", "+00:00")))

        return date_times, values


if __name__ == '__main__':

    smhi = SMHI()
    params = smhi.parameter_names()
    date_times, values = smhi.parameter_values("air_temperature")

    #print(params)
    #print(date_times)
    #print(values)

    plt.plot(date_times, values, "r-")
    ax = plt.gca()

    ax.xaxis.set_major_formatter(mpl_dates.DateFormatter("%m-%d %H:%M"))
    plt.gcf().autofmt_xdate()

    plt.show()
