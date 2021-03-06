import numpy as np
import scipy.io.wavfile
import scipy.signal
import fastburg as burg
import soundfile as sf
import argparse


def ar_filter_offline(
    samples,
    pos,
    dur,
    n=4000,  # AR order
    ns=4000,  # number of samples to adapat on
):
    """`Freezes` signal using AR model and IIR filtering.

    Parameters
    ----------
    signal : ndarray, shape (nb_samples,)
        input signal of `ndim = 1`. Typically a mono audio signal
    pos : int
        Freeze position in samples
    dur : int
        Number of samples to extrapolate
    n : int, optional
        AR model order, defaults to 4000
    ns : int, optional
        Number of samples `[pos - ns]` that are used to identify the AR model,
        defaults to 4000

    Returns
    -------
    ndarray, shape=(nb_samples,)
        Extrapolated samples

    """
    # create buffer
    outBuffer = np.zeros(dur, np.float)

    # filter identification
    a = np.real(
        burg._arburg2(samples[pos - ns - 1:pos], n)[0]
    )

    # compute initial filter states
    z = scipy.signal.lfiltic([1.0], a, samples[pos-(np.arange(1, n+1))])

    outBuffer, z = scipy.signal.lfilter(
        [1.0], a, np.zeros(dur, np.float), zi=z
    )

    return outBuffer


def ar_filter_block(
    samples,
    pos,
    dur,
    n=200,
    ns=200,
    nd=1024,
):
    """`Freezes` signal using AR model and IIR filtering.

    Filtering is realised in a block wise fashion which might reduce
    computational complexity.

    Parameters
    ----------
    signal : ndarray, shape (nb_samples,)
        input signal of `ndim = 1`. Typically a mono audio signal
    pos : int
        Freeze position in samples
    dur : int
        Number of samples to extrapolate
    n : int, optional
        AR model order, defaults to 200
    ns : int, optional
        Number of samples `[pos - ns]` that are used to identify the AR model,
        defaults to 200
    nd: int, optional
        Block size in samples, defaults to 1024

    Returns
    -------
    ndarray, shape=(nb_samples,)
        Extrapolated samples

    """
    # Number of extrapolation blocks in nl * nd
    nl = dur / nd

    # create buffer
    outBuffer = np.zeros(nd * nl, np.float)

    # filter identification
    a = np.real(burg._arburg2(samples[pos - ns - 1:pos], n)[0])

    # compute initial filter states
    z = scipy.signal.lfiltic([1], a, samples[pos-(np.arange(1, n+1))])

    for x in range(nl):
        y, z = scipy.signal.lfilter(
            [1], a, np.zeros(nd, np.float), zi=z
        )
        outBuffer[x*nd:(x+1)*nd] = y

    return outBuffer


def extrapolate(
    signal,
    pos,
    dur,
    n_signal=4000,
    ns_signal=4000,
):
    """`Freezes` signal using AR model and IIR filtering.
    Appends extrapolation to signal. Uses offline computation

    Parameters
    ----------
    signal : ndarray, shape (nb_samples,)
        input signal of `ndim = 1`. Typically a mono audio signal
    pos : int
        Freeze position in samples
    dur : int
        Number of samples to extrapolate
    n_signal : int, optional
        AR model order, defaults to 4000
    ns_signal : int, optional
        Number of samples `[pos - ns]` that are used to identify the AR model,
        defaults to 4000

    Returns
    -------
    ndarray, shape=(nb_samples,)
        Signal with extrapolated samples concatenated

    """

    concealed = ar_filter_offline(signal, pos, dur, n=n_signal, ns=ns_signal)

    return np.concatenate((signal[:pos], concealed))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Freeze Audio')

    parser.add_argument(
        'input', help='input file', type=str
    )

    parser.add_argument(
        'output', help='output file', type=str
    )

    parser.add_argument(
        '-n', '--n', type=int, default=4000,
        help='Filter order')

    parser.add_argument(
        '-x', '--x', type=int, default=44100,
        help='Extrapolation start sample')

    parser.add_argument(
        '-d', '--d', type=int, default=441000,
        help='Duration of extrapolation in samples')

    args = parser.parse_args()

    samples, rate = sf.read(args.input, always_2d=True)
    samples = np.squeeze(np.mean(samples, axis=1))

    out = extrapolate(
        samples,
        pos=args.x,
        dur=args.d,
        n_signal=args.n,
        ns_signal=args.n,
    )
    sf.write(args.output, out, samplerate=rate)
