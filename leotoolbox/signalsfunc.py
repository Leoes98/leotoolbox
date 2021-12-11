from scipy import signal
from scipy.fft import fft
from scipy.sparse import spdiags, linalg
import numpy as np
import matplotlib.pyplot as plt


def fourier(sig, fs, fig=True):
    """
    This method computes the Fast Fourier Transform.

    Parameters
    ----------
    sig : 1D array, signal vector.
    fs : INT, sample frequency.
    fig: BOOL, put True if you want the plot.

    Returns
    -------
    f : 1D array, frequencies vector.
    P1 : 1D array, power amplitude.

    """
    L = len(sig)
    fft_sig = fft(sig)
    P2 = abs(fft_sig / L)
    P1 = P2[0:np.int(L / 2 + 10)]
    P1[1:-1] = 2 * P1[1:-1]
    f = fs * np.arange(0, (L / 2 + 10)) / L
    if fig == True:
        plt.figure()
        plt.plot(f, P1)
        plt.xlabel('f(Hz)'), plt.ylabel('|P1(f)|'), plt.title('FFT')
    return f, P1


def get_peaks(sig, mpp=None, mpd=None):
    """
    This method computes the find peaks algorithm to return a matrix with
    the index in each peak and its value.

    Parameters
    ----------
    sig : 1D array, signal vector.
    mpp : FLOAT, minimum peak prominence. The default is None.
    mpd : FLOAT, minimum peak distance. The default is None.

    Returns
    -------
    picos : 2D array, matrix with index peak and peak value.

    """
    peaks, _ = signal.find_peaks(sig, prominence=mpp, distance=mpd)
    vpeaks = np.take(sig, peaks)  # peak value
    picos = np.array([peaks,
                      vpeaks]).T  # matrix with index peak and peak value
    return picos


def sliding_window(signal, fs, t_win, t_overlap):
    """
    This method computes the sliding window algorithm to return a matrix with
    the separated segments of the signal.

    Parameters
    ----------
    signal : 1D array, signal vector.
    fs : FLOAT, frequency sample.
    t_win : FLOAT, value for time of each window.
    t_overlap: FLOAT, value for time overlapping in each window.

    Returns
    -------
    sig_segments : 2D array, matrix with segmented signal.

    """
    win = int(t_win * fs)
    overlap = int(t_overlap * fs)
    L = len(signal)
    n_win = int((L - win) / overlap)
    sig_segments = np.zeros((win, n_win))

    for i in range(n_win):
        sig_segments[:, i] = signal[int(i * overlap):int(i * overlap + win)]
    return sig_segments


def find_nearest(array, value):
    """
    Method to find the index of the nearest value on an array.

    Parameters
    ----------
    array : A 1D array.
    value : A scalar value.

    Returns
    -------
    idx : An integer value corresponding to the index found.

    """
    idx = (np.abs(array - value)).argmin()
    return idx


def z_score(array):
    """
    Computes the Z-score of a given 1-D array.

    Parameters
    ----------
    array : A 1D array.

    Returns
    -------
    z : 1D array with the Z-score values.

    """
    z = (array - np.mean(array)) / np.std(array)
    return z


def rmv_artifact(array, thr=20000):
    """
    Method that removes artifacts from PPG signal given a certain threshold.
    It uses the Z-score to find the outliers/artifacts.

    Parameters
    ----------
    array : 1D array of a PPG signal.
    thr : Scalar value, threshold used. The default is 20000.

    Returns
    -------
    n_arr : New 1D array with the removed artifact.

    """
    n_arr = array.copy()
    if np.abs(np.max(array) - np.min(array)) > thr:
        z = z_score(array)
        n_arr[z > 1] = np.mean(np.median(array) - array[z > 1]) + array[z > 1]
    return n_arr
