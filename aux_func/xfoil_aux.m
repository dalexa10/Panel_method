clc
clear all

addpath('C:\Users\dario\OneDrive - Escuela Politécnica Nacional\Matlab codes - Copy\Functions\Xfoil')

pol = xfoil(af_name,0,,Vc_ma,'MDES','FILT','EXEC',' ','PANE','oper iter 300','ppar N 300');