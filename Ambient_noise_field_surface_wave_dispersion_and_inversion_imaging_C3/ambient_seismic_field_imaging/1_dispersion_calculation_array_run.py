# ----------------------------------------------------------------------------------
# Importing libraries
# ----------------------------------------------------------------------------------
import os
import sys
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.dates as mdates
from scipy import signal, fftpack
from scipy.fftpack import fft, fftshift
import segyio
import torch
from torch import nn
import torch.nn.functional as F
import pandas as pd
import time



# ----------------------------------------------------------------------------------
# Loading functions
# ----------------------------------------------------------------------------------
def radon_transform_obs(seismo_v1, dt, x, vmin=100, vmax=1500, fmin=1, fmax=20, df=0.05):
    # Initial settings
    uxt = seismo_v1
    poinum, tranum = uxt.shape
    i = 1j #  imaginary unit
    pmin = 0.0000
    pmax = 0.01
    pmax1 = 1.0 / vmin
    np_val = vmax - vmin + 1
    if pmax1 > pmax:
        pmax = pmax1
     # Zero-padding
    uxt = uxt.T
    m = tranum
    nn0 = poinum



    ccn = int((1.0 / df / dt - 1 - nn0) + 1)
    zeros1 = np.zeros((m, ccn))
    uxt_m = uxt.shape[0]
    uxt_n = zeros1.shape[1] + uxt.shape[1]
    uxt_uxt = np.zeros((uxt_m, uxt_n))
    for k in range(m):
        for t in range(uxt_n):
            if t <= nn0-1:
                uxt_uxt[k, t] = uxt[k, t]
            if t > nn0-1:
                uxt_uxt[k, t] = zeros1[k, t - nn0-1]
    m = uxt_uxt.shape[0]
    n = uxt_uxt.shape[1]
    # Single trace Fourier transform
    d = np.zeros((m, n), dtype=complex)
    abs_d = np.zeros((m, n))
    for luoi in range(m):
        d[luoi, :] = np.fft.fft(uxt_uxt[luoi, :], n)
    # Initialize parameters
    lf = round(fmin / df) + 1
    nf = round(fmax / df) + 1
    nx = m
    dp = (pmax - pmin) / (np_val - 1)
    p = pmin + np.arange(np_val) * dp
    ll0 = i * 2 * np.pi * df * (np.outer(p, x))
    mm = np.zeros((np_val, n + 1), dtype=complex)
    l = np.zeros((np_val, nx), dtype=complex)
    for luoj in range(lf, nf):
        l = np.exp(ll0 * (luoj - 1))

        # print("Shape of l:", l.shape)
        # print("Shape of d[:, luoj]:", d[:, luoj].shape)

        # print("Frequency index low (lf):", lf)
        # print("Frequency index high (nf):", nf)
        # print("Expected shape of frequency data:", d.shape)
        # print("Actual shape of frequency data slice:", d[:, luoj].shape)

        mm[:, luoj] = np.dot(l, d[:, luoj])
    # Translate to frequency-velocity domain
    p1 = np.zeros(np_val)
    p1[0] = 1000000000
    p1[1:] = 1.0 / p[1:]
    p2 = np.arange(vmin, vmax + 1)
    ml = np.zeros((np_val, nf), dtype=complex)
    for luoi in range(lf, nf):
        ml[:, luoi] = np.interp(p2, p1[::-1], np.abs(mm[::-1, luoi]), left=0, right=0)
        ml[:, luoi] /= np.max(ml[:, luoi])
    ml = np.abs(ml[:, lf:nf])
    return ml


def get_file_list(basis_dir="./", begin="", end=""):
	path_list = os.listdir(basis_dir)
	list_final = []
	for partial in path_list:
		if begin:
			if partial[:len(begin)] == begin:
				list_final.append(partial)
		elif end:
			if partial[-len(end):] == end:
				list_final.append(partial)
		
		elif begin and end:
			if partial[:len(begin)] == begin and partial[-len(end):] == end:
				list_final.append(partial)
				
		else:
			list_final.append(partial)
		list_final.sort()	
	return list_final

def readdata(file, filepath = './', filetype = 'puniu',flag=1):
    if filetype=='puniu':
        info = np.fromfile(filepath+file, dtype = 'double', count=10)
        data = np.fromfile(filepath+file, dtype = 'float32', offset=80)
        dt = info[3]
        dx = info[1]
        nch = int(info[0])
        data = data.reshape(int(info[2]), int(info[0]))
        if flag == 1:
            print('from %s reading data. channel number: %d, npts: %d, dt: %fs, dx: %dm'%(file,int(info[0]), int(info[2]), info[3], int(info[1])))
    return data, dt, dx, nch

def mst(ax=[], label=[], xlabel="", ylabel="",title=[], xlim=[], ylim=[], style="Times", fontsize=10, width_line=1 ,legend=False, rotate=False, axis_width=1, half_axis=False):
	
	if not ax:
		ax = plt.gca()
		
	if style == "Times":
		font1 = {'family' : 'Times New Roman', 'size': fontsize,}
		font2 = {'family' : 'Times New Roman', 'size': fontsize*1.2,}
		plt.tick_params(labelsize=fontsize)
		labels = ax.get_xticklabels() + ax.get_yticklabels()
		[label.set_fontname('Times New Roman') for label in labels]
		
	elif style == "Arial":
		font1 = {'family' : 'Arial', 'size': fontsize,}
		font2 = {'family' : 'Arial', 'size': fontsize*1.2,}
		plt.tick_params(labelsize=fontsize)
		labels = ax.get_xticklabels() + ax.get_yticklabels()
		[label.set_fontname('Arial') for label in labels]
		
	else:
		font1 = {'size': fontsize,}
		font2 = {'size': fontsize*1.2,}
		plt.tick_params(labelsize=fontsize)
		
	if half_axis:
		for axis in ['bottom','left']:
			ax.spines[axis].set_linewidth(axis_width)
		for axis in ['top', 'right']:
			ax.spines[axis].set_linewidth(0)
	else:
		for axis in ['top','bottom','left','right']:
			ax.spines[axis].set_linewidth(axis_width)
	
	if title:
		ax.set_title(title,font2)

	if len(label) == 2:
		ax.set_xlabel(label[0],font2)
		ax.set_ylabel(label[1],font2)
	
	if xlabel:
		ax.set_xlabel(xlabel, font2)
	
	if ylabel:
		ax.set_ylabel(ylabel, font2)
	
	if legend:
		legend = ax.legend(prop=font1)
			
	if len(xlim) == 2:
		ax.set_xlim(xlim)

	if rotate:
		ax.set_xticklabels(ax.get_xticks(),rotation=45)
	
	if len(ylim) == 2:
		ax.set_ylim(ylim)
def x_bf(major, num=0, dot=1, ax=[]):
	if not ax:
		ax = plt.gca()
	
	if num <= 0:
		minor = major
			
	else:
		minor = major / num
			
	format_str = '%1.' + str(dot) + 'f'
	xmajorLocator   = MultipleLocator(major)
	xmajorFormatter = FormatStrFormatter(format_str)
	xminorLocator   = MultipleLocator(minor)
	ax.xaxis.set_major_locator(xmajorLocator)
	ax.xaxis.set_minor_locator(xminorLocator)
	ax.xaxis.set_major_formatter(xmajorFormatter)
def y_bf(major, num=0, dot=1, ax=[]):
	if not ax:
		ax = plt.gca()
	if num <= 0:
		minor = major	
	else:
		minor = major / num
	format_str = '%1.' + str(dot) + 'f'
	ymajorLocator   = MultipleLocator(major)
	ymajorFormatter = FormatStrFormatter(format_str)
	yminorLocator   = MultipleLocator(minor)
	ax.yaxis.set_major_locator(ymajorLocator)
	ax.yaxis.set_minor_locator(yminorLocator)
	ax.yaxis.set_major_formatter(ymajorFormatter)
def taper(x,p):
    if p <= 0.0:
        return x
    else:
        f0 = 0.5
        f1 = 0.5
        n  = len(x)
        nw = int(p*n)

        if nw > 0:
            ow = np.pi/nw

            w = np.ones( n )
            for i in range( nw ):
                w[i] = f0 - f1 * np.cos(ow*i)

            for i in range( n-nw,n ):
                w[i] = 1.0 - w[i-n+nw]

            return x * w
        elif nw == 0:
            return x
def preprocessing(data, dt, fmin, fmax, norm_method='bpnorm'):
    f1 = fmin*0.5
    f2 = fmin
    f3 = fmax
    f4 = fmax*1.2
    itwin = int(1/dt*0.1)
    fwin = .1
    nch = data.shape[1]
    data0 = data.copy()
    for i in range(nch):
        dat_in = data[:,i]
        dat_in = filter_szh(dat_in, dt, fmin, fmax) # filter 
        dat = dat_in - np.mean((dat_in))
        if norm_method == 'bpnorm':
            dat_tn = bpnorm(dat, fmin, fmax, dt, itwin)
        elif norm_method == '1bit':
            dat_tn = np.sign(dat)
            dat_tn = np.float32(dat_tn)
        data0[:,i] = whtnd(f1, f2, f3, f4, dt, dat_tn, fwin)
    return data0
def hanning(N):
    window = np.array([0.5 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) for n in range(N)])
    return window
def whtnd(f1,f2,f3,f4,dt,d1n,fwin):
    dlen = len(d1n)
    df = 1/(dlen*dt)
    d1 = int(round(f1/df))
    d2 = int(round(f2/df))
    d3 = int(round(f3/df))
    d4 = int(round(f4/df))
    # print(d2-d1,d4-d3)
    tpr = hanning(int(2*(d2-d1)+1))
    tpr1 = tpr[:d2-d1+1]
    tpr = hanning(int(2*(d4-d3)+1))
    tpr2 = tpr[d4-d3:]
    if (np.mod(dlen,2)== 0.0):
        tprp= np.hstack([np.zeros(d1),tpr1,np.ones(d3-d2-1),tpr2,np.zeros(int(dlen/2)-d4-1)])
        tprf = np.hstack([0,np.flip(tprp[1:]),tprp])
    else:
        tprp= np.hstack([np.zeros(d1),tpr1,np.ones(d3-d2-1),tpr2,np.zeros(int((dlen+1)/2)-d4-1)])
        tprf = np.hstack([np.flip(tprp[1:]),tprp])
    smln = int(round(fwin*dlen*dt))   
    d1nff = fftpack.fftshift(fftpack.fft(d1n))
    d1nffs = convsm(abs(d1nff),smln)
    d1nw = np.real(fftpack.ifft(fftpack.ifftshift((d1nff/d1nffs+np.spacing(1)*np.mean(abs(d1nff)))*tprf)))
    return d1nw
def bpnorm(dat0,f0,f1,dt,itwin):
    fs = 1/dt/2
    b, a = signal.butter(2, [f0/fs,f1/fs], 'bandpass')
    dat1 = signal.filtfilt(b, a, dat0)
#    itwin = int(np.floor(itwin/dt));
    if(np.mod(itwin,2) == 0.0):
        itwin = itwin+1
    dat2= smooth(abs(dat1),itwin)
    dat3 = dat0/(dat2)
    return dat3
def filter_szh(data,dt,fmin,fmax):
    band = np.array([fmin, fmax])
    Wn = band * 2 * dt
    b, a = signal.butter(2, Wn, 'bandpass') 
    pp2 = signal.filtfilt(b, a, data.T)    
    return pp2.T
def bandpass_bp(dat0, f0, f1, dt):
    fs = 1/dt/2
    b, a = signal.butter(2, [f0/fs,f1/fs], 'bandpass')
    dat1 = signal.filtfilt(b, a, dat0)
    return dat1
def smooth(a,WSZ):
    out0 = np.convolve(a,np.ones(WSZ,dtype=int),'valid')/WSZ    
    r = np.arange(1,WSZ-1,2)
    start = np.cumsum(a[:WSZ-1])[::2]/r
    stop = (np.cumsum(a[:-WSZ:-1])[::2]/r)[::-1]
    return np.concatenate((  start , out0, stop  ))
def convsm(A,nx):
    Nx = len(A)
    Ap = np.zeros((Nx+2*nx))
    Ap[nx:nx+Nx] = A.copy()
    Ap[:nx] = Ap[np.arange(nx*2,nx,-1)].copy()
    Ap[nx+Nx:] = Ap[np.arange(nx+Nx-2,Nx-2,-1)]
    Nxp = Nx+2*nx
    Ktx = np.zeros((Nxp))
    kx = np.arange(1,Nxp+1)
    eps = 2.2204e-16
    if (np.mod(Nx,2)==0):
        Ktx = 1/(2*nx+1)*np.sin(0.5*(2*nx+1)*(kx-((Nxp+2)/2)+eps)*((2*np.pi)/Nxp))/np.sin\
            (0.5*(kx-((Nxp+2)/2)+eps)*((2*np.pi)/Nxp))
    else:
        Ktx = 1/(2*nx+1)*np.sin(0.5*(2*nx+1)*(kx-((Nxp+1)/2)+eps)*((2*np.pi)/Nxp))/np.sin\
            (0.5*(kx-((Nxp+1)/2)+eps)*((2*np.pi)/Nxp))
    Ap = np.real(fftpack.ifftn(fftpack.ifftshift(fftpack.fftshift(fftpack.fftn(Ap))*Ktx)))
    Asm = np.zeros(Nx)
    Asm = Ap[nx:nx+Nx]
    return Asm
def xcorr(a,b,mode ='coef'):
    fa = np.fft.fft(a,n=len(a)*2-1)
    fb = np.fft.fft(b,n=len(a)*2-1)
    xx = fa*np.conj(fb)
    if b.ndim>1:
        xcc = np.fft.fftshift(np.fft.ifft(xx),1)
    else:
        xcc = np.fft.fftshift(np.fft.ifft(xx))
    if mode == 'coef':
        aa = fa*np.conj(fa)
        xaa = np.fft.fftshift(np.fft.ifft(aa))
        bb = fb*np.conj(fb)
        xbb = np.fft.fftshift(np.fft.ifft(bb))
        xcc = xcc/np.sqrt(xaa[len(a)-1]*xbb[len(b)-1])
    return np.real(xcc)
def readdata_simple(file,filepath='./'):
    info = np.fromfile(filepath+file, dtype='double', count=10)
    data = np.fromfile(filepath+file, dtype='float32', offset=80)
    data = data.reshape(int(info[2]),int(info[0]))
    print('from %s reading data. channel number: %d, npts: %d, dt:%fs, dx:%fm'%(file,info[0],info[2],info[3],info[1]))
    return data

def masw_fc_trans(data, dt, dist, f1, f2, c1, c2, nc=201):
    data = data.T
    m, n = data.shape
    fs = 1 / dt
    fn1 = int(f1 * n / fs)
    fn2 = int(f2 * n / fs)
    c = np.linspace(c1, c2, nc)
    f = np.arange(n) * fs / (n - 1)
    df = f[1] - f[0]
    w = 2 * np.pi * f
    fft_d = np.zeros((m, n), dtype=np.complex128)
    for i in range(m):
        fft_d[i] = np.fft.fft(data[i])
    fft_d = fft_d / abs(fft_d)
    fft_d[np.isnan(fft_d)] = 0
    fc = np.zeros((len(c), len(w[fn1:fn2 + 1])))
    for ci, cc in enumerate(c):
        for fi in range(fn1, fn2 + 1):
            fc[ci, fi - fn1] = abs(
                sum(np.exp(1j * w[fi] / cc * dist) * fft_d[:, fi]))
    return fc / abs(fc).max(), f[fn1:fn2 + 1], c

def muting(seis,nshot,v1,v2,dx,dt,taper=10,tt=20,tlag=1):
    nt = seis.shape[0]
    ng = seis.shape[1]
    aa=hanning(int(2*taper))
    seis_mute = seis.copy()
    for k in range(ng):
        t1=int((dx*np.abs(k-nshot)/v1)/dt)+tlag
        t2=int((dx*np.abs(k-nshot)/v2)/dt)+tt+tlag
        damping1=np.zeros(int(nt+2*taper))
        damping2=np.zeros(nt)
        if t2>nt:
            t2=nt
        damping1[t1+taper:t2+taper]=1
        damping1[t1+1:t1+taper]=aa[1:taper]
        damping1[t2+taper:t2+taper*2-1]=aa[taper+1:taper*2]
        damping2=damping1[taper:taper+nt]
        seis_mute[:,k]=seis[:,k]*damping2
    return seis_mute

def denoising(data, dx, dt, iter0=5, mutev1=[], mutev2=[], source_tlag=0):
    nt, ng, ns = data.shape
    
    if ns == 1:
        print('ns=1, skip denoising')
        return data
    
    # Normalizing data
    for its in range(ns):
        dd1 = data[:, :, its]
        norms = np.linalg.norm(dd1, axis=0)
        non_zero_norms = norms > 0
        dd1[:, non_zero_norms] = dd1[:, non_zero_norms] / norms[non_zero_norms]
        data[:, :, its] = dd1
    
    data0 = data.copy()
    
    
    if not mutev1:
        data1 = data0
    else:
        data1 = np.zeros((nt, ng, ns))
        for i in range(ns):
            temp = data0[:, :, i]
            temp2 = muting(temp, i, mutev2, mutev1, dx, dt)
            data1[:, :, i] = temp2

    w = np.arange(1, nt * 2 + 1) / dt / (nt * 2)
    p_c = np.exp(-1j * w * source_tlag * dt * 2 * np.pi)
    
    data_f = np.zeros((nt, ng, ns, iter0))
    data = data1.copy()
    
    for kk in range(iter0):
        data_pad = np.zeros((nt * 2, ng, ns))
        data_pad[:nt, :, :] = data
        data_w = np.fft.fft(data_pad, axis=0)

        dd = np.zeros((nt, ng, ns))

        for its in range(ns):
            dd1 = data_w[:, :, its]
            for ig in range(ng):
                dd2 = data_w[:, ig, :]
                temp = np.zeros(nt * 2, dtype=complex)
                
                if ig >= its:
                    for igg in range(ng):
                        tr1 = dd1[:, igg]
                        tr2 = dd2[:, igg]
                        
                        if igg <= its and igg <= ig:
                            tr3 = np.conj(tr1) * tr2 * np.conj(p_c)
                        elif igg >= its and igg >= ig:
                            tr3 = tr1 * np.conj(tr2) * np.conj(p_c)
                        else:
                            tr3 = tr1 * tr2 * p_c
                        
                        temp += tr3
                    
                    temp /= np.sqrt(np.abs(temp))
                    temp = np.real(np.fft.ifft(temp))
                    dd[:, ig, its] = temp[:nt] / np.linalg.norm(temp[:nt])
                else:
                    for igg in range(ng):
                        tr1 = dd1[:, igg]
                        tr2 = dd2[:, igg]
                        
                        if igg <= its and igg <= ig:
                            tr3 = np.conj(np.conj(tr1) * tr2 * p_c)
                        elif igg >= its and igg >= ig:
                            tr3 = np.conj(tr1 * np.conj(tr2) * p_c)
                        else:
                            tr3 = tr1 * tr2 * p_c
                        
                        temp += tr3
                    
                    temp /= np.sqrt(np.abs(temp))
                    temp = np.real(np.fft.ifft(temp))
                    dd[:, ig, its] = temp[:nt] / np.linalg.norm(temp[:nt])
        
        data = dd
        data_f[:, :, :, kk] = dd
    return data



# Function to convert SEGY data to numpy
def sgy2numpy(filename, ch1=0, ch2=0):
    with segyio.open(filename, ignore_geometry=True) as segyfile:
        if ch2 == 0:
            data = np.array(segyfile.trace.raw[:])
        else:
            data = np.array(segyfile.trace.raw[ch1:ch2])
    return data.T

# Cross-correlation function for all channels
def cc_all(data):
    a, b = data.shape
    base = torch.cat([torch.zeros_like(data), data, torch.zeros_like(data)], axis=1)
    data = data.repeat((a, 1)).view(a, a, -1).permute((1, 0, 2))
    re = cal_cc(base, data)
    return re

# Calculate cross-correlation
def cal_cc(data, tmp, step=1):
    tmf_num = tmp.shape[0]
    groups = tmp.shape[1]
    tmp = tmp.permute(1, 0, 2).reshape(-1, 1, tmp.shape[-1])
    ans = F.conv1d(data.view(1, -1, data.shape[-1]), tmp, groups=groups, stride=step)
    return ans.reshape(data.shape[0], tmf_num, -1).permute(2, 1, 0)

# Cross-correlation using FFT
def xcorr_torch(a, b):
    fa = torch.fft.fft(a, n=len(a) * 2 - 1)
    fb = torch.fft.fft(b, n=len(a) * 2 - 1)
    xx = fa * torch.conj(fb)
    if b.ndim > 1:
        xcc = torch.fft.fftshift(torch.fft.ifft(xx), 1)
    else:
        xcc = torch.fft.fftshift(torch.fft.ifft(xx))
    return np.real(xcc)

# ----------------------------------------------------------------------------------
# Setting the parameters
# ----------------------------------------------------------------------------------

font_path = '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'
matplotlib.font_manager.fontManager.addfont(font_path)
matplotlib.pyplot.rcParams['font.family'] = 'Arial'
matplotlib.pyplot.rcParams['font.size'] = 8

start = time.time()
path = sys.argv[1]
lst = get_file_list(path, end='sgy')

jpg_outputfolder_path = sys.argv[2]
spacing = float(sys.argv[4])
ch1 = int(sys.argv[5])
ch2 = int(sys.argv[6])

start_file_number = str(sys.argv[7])
end_file_number = str(sys.argv[8])
start_file_number_int = sys.argv[7]
end_file_number_int = sys.argv[8]

CCFs_C2_dir = sys.argv[10]
CCFs_C3_compute_dir = sys.argv[11]
CCFs_C3_plot_dir = sys.argv[12]
CCFs_ccfj_dir = sys.argv[13]
spectrum_C2_dir = sys.argv[14]
spectrum_C3_dir = sys.argv[15]
spectrum_ccfj_dir = sys.argv[16]
curve_C2_dir = sys.argv[17]
curve_C3_dir = sys.argv[18]
curve_ccfj_dir = sys.argv[19]

path_folder_name = os.path.basename(os.path.dirname(path))
filename = f'{path_folder_name}-{start_file_number_int}-{end_file_number_int}-{ch1}-{ch2}'

start_file_number = eval(start_file_number.replace('x', '*'))
end_file_number = eval(end_file_number.replace('x', '*'))
lst = lst[start_file_number:end_file_number]
fmin = 1
fmax = 50
df = 0.1
vmin = 100
vmax = 600

tbegin = 0
tend = 60
dt = 1 / 250
dt_ = 1 / 500

maxshift = 0.5
twin = maxshift * 3

# ----------------------------------------------------------------------------------
# Calculating the cross-correlation function
# ----------------------------------------------------------------------------------

fs = 1 / dt
channel = np.linspace(ch1, ch2, ch2 - ch1 + 1, dtype='int')
nch = len(channel)
itwin = int(twin * fs)
wpm = int(maxshift * fs)
nwin = int((tend - tbegin) / twin) * 2 - 1
ccf = np.zeros((2 * wpm + 1, len(channel), len(channel)))
ccf = torch.from_numpy(ccf).to('cuda')

for ifile in lst:
    data = sgy2numpy(path + ifile, ch1, ch2 + 1)
    ifactor = int(dt / dt_)
    dat0_ = np.zeros((int((tend - tbegin) / dt), nch))
    for j in range(nch):
        if ifactor > 1:
            dat0_[:, j] = signal.decimate(data[:, j], ifactor, ftype='fir')
        else:
            dat0_[:, j] = data[:, j]
    dat = preprocessing(dat0_, dt, fmin, fmax)
    dat = torch.from_numpy(dat).to('cuda')
    for kk in range(nwin):
        ind0 = int(kk * itwin / 2)
        ind1 = int(ind0 + itwin)
        torchdata = dat[ind0:ind1, :].T
        cc = cc_all(torchdata)
        tmp = cc[itwin - wpm:itwin + wpm + 1, :, :]
        max_abs = torch.max(torch.abs(tmp), axis=0)[0]
        tmp = tmp / max_abs
        ccf += tmp / len(lst)

ccf = np.array(ccf.cpu())
tvec = np.linspace(-maxshift, maxshift, ccf.shape[0])

# ----------------------------------------------------------------------------------
# Plotting the result: normal C2 method
# ----------------------------------------------------------------------------------

matplotlib.use('Agg')
plt.figure(figsize=(12, 6), dpi=500)

plt.subplot(241)
for i in range(len(channel)):
    plt.plot(tvec, ccf[:, i, 0] / np.max(ccf[:, i, 0]) * 2 + i, 'k', lw=0.5)
plt.title("CCFs_C2")
plt.xlabel('Time (s)')
plt.ylabel('Channel')
plt.tight_layout()

plt.subplot(242)
ncf222 = ccf[::-1, :, :] + ccf
compute_dimension_size = int(ncf222.shape[0] / 2)
ncf222 = ncf222[compute_dimension_size:, :, :]

np.savez_compressed(os.path.join(CCFs_C2_dir, filename + '.npz'), data=ncf222[:, :, 0])
spec = radon_transform_obs(ncf222[:, :, 0], dt, np.arange(ch2 - ch1 + 1) * spacing, vmin, vmax, fmin, fmax, df)
np.savez_compressed(os.path.join(spectrum_C2_dir, filename + '.npz'), data=spec)
plt.imshow(spec**5, aspect='auto', extent=[fmin, fmax, vmin, vmax], origin='lower')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase velocity (m/s)')
plt.title('spectrum_C2')
plt.tight_layout()

c = np.arange(vmax - vmin) + vmin
f = np.arange(int((fmax - 1) / df)) * df + 1
indices = np.argmax(spec, 0)
indices = np.clip(indices, 0, len(c) - 1)
disp = c[indices]
step = 10
curve_C2_save = pd.DataFrame({
    'Frequency': f,
    'Velocity': disp
})
curve_C2_save_reduced = curve_C2_save.iloc[::step]
plt.scatter(curve_C2_save_reduced['Frequency'], curve_C2_save_reduced['Velocity'], edgecolors='r', facecolors='none', s=5)
plt.grid(True, linestyle='--')
plt.tight_layout()
curve_C2_save.to_csv(os.path.join(curve_C2_dir, filename + '.txt'), index=False, header=False)

plt.subplot(246)
plt.imshow(spec**5, aspect='auto', extent=[fmin, fmax, vmin, vmax], origin='lower')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase velocity (m/s)')
plt.title('spectrum_C3')
plt.tight_layout()

plt.savefig(os.path.join(jpg_outputfolder_path, f'{filename}.jpg'))
