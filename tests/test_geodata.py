import utils.geodata as geo
import pytest


data = geo.geo_data.us('Birmingham','AL')
data2 = geo.geo_data("Rome","Italy")

def test_geodata_lat():
    assert data.lat == 33.5206824

def test_geodata_lon():
    assert data.lon == -86.8024326

def test_geodata_international():
    assert data2.lat == 41.8933203