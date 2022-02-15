import os
import numpy as np
from bs4 import BeautifulSoup  # Import the BeautifulSoup library
import re  # Import regular expressions


def af_web(af, main_path):
    try:  # Import urllib
        import urllib.request as urllib2
    except ImportError:
        import urllib2

    # Base filepath for the UIUC airfoil website (used for accessing .dat files)
    baseFlpth = "https://m-selig.ae.illinois.edu/ads/"  # Base filepath for saving

    # Open the webpage and create the soup
    html_page = urllib2.urlopen("https://m-selig.ae.illinois.edu/ads/coord_database.html")  # Open the URL
    soup = BeautifulSoup(html_page, 'lxml')  # Create the soup

    for link in soup.find_all('a', attrs={'href': re.compile(af + '\.dat', re.IGNORECASE)}):
        af_name = link.get('href').rsplit('/', 1)[-1]
        print(af_name)
        fullfilename = os.path.join(main_path, 'Resources', af_name)
        urllib2.urlretrieve(baseFlpth + link.get('href'), fullfilename)
        print("Saving file")  # Indicate the link that we are currently saving

    return

def check_af(af_name, main_path):
    """
    Check if an airfoil.dat file exist in the path in question

    :param af_name:
    :param main_path:
    :return:
    """
    try:
        af_path = os.path.join(main_path, 'Resources', af_name + '.dat')
        if os.path.exists(af_path):
            i = True
            print('Nice! We have that airfoil in our database')
        else:
            print('This airfoil does not exist in our database. Lets try to download it')
            af_web(af_name, main_path)
            i = True

    except TypeError:
        print('Something went wrong, try again')

    return i

def read_txt(af_name, main_path):
    """
    This function reads the .txt files that contains the airfoil geometry
    :param af_name = Name of the airfoil:
    :return:
    """
    try:
        af_path = os.path.join(main_path, 'Resources', af_name + '.dat')
        with open(af_path, 'r') as af_file:
            x, y = np.loadtxt(af_file, dtype=float, unpack=True, skiprows=1)

    except TypeError:
        print('Something went wrong, try again')
        pass
    return x, y

def read_xfoil(filename, main_path):
    """
    Read xfoil data saved in a .data file
    :param filename:
    :param main_path:
    :return:
    """
    try:
        xfoil_data_path = os.path.join(main_path, 'xfoil_exp', filename + '.dat')
        with open(xfoil_data_path, 'r') as data_file:
            x, y, Cp = np.loadtxt(data_file, dtype=float, unpack=True, skiprows=1)

    except TypeError:
        print('Something went wrong, try again')
        pass
    return [x, y, Cp]

def read_exp(filename, main_path):
    """
    Read xfoil data saved in a .data file
    :param filename:
    :param main_path:
    :return:
    """
    try:
        exp_data_path = os.path.join(main_path, 'xfoil_exp', filename + '.dat')
        with open(exp_data_path, 'r') as data_file:
            x, Cp = np.loadtxt(data_file, dtype=float, unpack=True, skiprows=0)

    except TypeError:
        print('Something went wrong, try again')
        pass
    return [x, Cp]