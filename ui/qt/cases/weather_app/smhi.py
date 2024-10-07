# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 11:37:54 2018

@author: Jonas Lindemann
"""

import json
import requests

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
import matplotlib.ticker as mticker


class SMHI:
    """Class for extracting a weather forecast"""

    def __init__(self, longitude="16", latitude="58"):
        """Class constructor"""

        self.url = "https://opendata-download-metfcst.smhi.se"
        self.api_template = "/api/category/{}/version/{}/geotype/point/lon/{}/lat/{}/data.json"
        self.category = "pmp3g"
        self.version = "2"
        self.longitude = longitude
        self.latitude = latitude
        self.request_forecast()

    def request_forecast(self):
        """Request data from SMHI"""

        api_string = self.api_template.format(self.category,
                                              self.version,
                                              self.longitude,
                                              self.latitude)

        smhi_info = requests.get(self.url + api_string)

        self.forecast = json.loads(smhi_info.text)

    def parameter_names(self):
        """Return a list with available param_names"""

        names = {}

        for item in self.forecast["timeSeries"]:
            params = item["parameters"]
            for param in params:
                if not param["name"] in names:
                    names[param["name"]] = param["unit"]

        return names

    def parameter_values(self, name):
        """Extract specific values from data"""

        date_times = []
        values = []

        for item in self.forecast["timeSeries"]:
            params = item["parameters"]
            for param in params:
                if param["name"] == name:
                    values.append(float(param["values"][0]))
                    date_times.append(item["validTime"])

        return date_times, values


if __name__ == '__main__':

    smhi = SMHI()
    params = smhi.parameter_names()
    date_times, values = smhi.parameter_values("t")

    # print(params)
    #print(date_times)
    #print(values)

    plt.plot_date(date_times, values, xdate=True, fmt="r-")
    ax = plt.gca()

    my_locator = mticker.MultipleLocator(8)
    ax.xaxis.set_major_locator(my_locator)
    plt.gcf().autofmt_xdate()

    plt.show()
