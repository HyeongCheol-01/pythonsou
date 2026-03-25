import requests
from bs4 import BeautifulSoup
import time
import sys
import urllib
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import MySQLdb
from sqlalchemy import create_engine
import seaborn as sns

df = pd.read_csv('sales_data.csv')
pt = df.pivot_table(index='날짜', columns='제품', values='판매수량', aggfunc='sum')
print(pt)