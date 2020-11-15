import os
import numpy as np

def read_txt(af_name, main_path):
    """
    This function reads the .txt files that contains the airfoil geometry
    :param af_name = Name of the airfoil:
    :return:
    """
    try:
        af_path = os.path.join(main_path, 'Resources', '/', af_name, '.dat')
        #airfoil = af_path + "/" + af_name + '.dat'
        if os.path.exists(af_path):
            print('Nice! We have that airfoil in our database')
            with open(af_path, 'r') as af_file:
                x, y = np.loadtxt(af_file, dtype=float, delimiter='\t', unpack=True)

        else:
            print('This airfoil does not exist')

    except TypeError:
        print('Something went wrong, try again')
        pass
    return x,y


