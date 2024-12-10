#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Test Weather App
"""
import weather_app as App


def main():
    """
Execution of user functions for Weather App
"""
    # begin gathering and processing data
    App.initiate()
    print('-'*99)
    # calculate the hottest city from provided zip codes in zip_codes.txt
    App.calculate_hottest_city()
    print('-'*99)
    # calculate the coldest city from provided zip codes in zip_codes.txt
    App.calculate_coldest_city()
    print('-'*99)


if __name__ == '__main__':
    main()
