import numpy as np
import scipy.io.wavfile
import scipy.signal
import modules.extern.fastburg as burg
import soundfile as sf
import argparse


def ar_filter_block(
    samples,
    pos,
    dur,
    n=200,  # AR order
    ns=200,  # number of samples to adapat on
    nd=1024,  # Buffer length in samples
):
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


def ar_filter_offline(
    samples,
    pos,
    dur,
    n=4000,  # AR order
    ns=4000,  # number of samples to adapat on
):
    # create buffer
    outBuffer = np.zeros(dur, np.float)

    # filter identification
    a = np.real(burg._arburg2(samples[pos - ns - 1:pos], n)[0])

    # compute initial filter states
    z = scipy.signal.lfiltic([1], a, samples[pos-(np.arange(1, n+1))])

    outBuffer, z = scipy.signal.lfilter(
        [1], a, np.zeros(dur, np.float), zi=z
    )

    return outBuffer


def extrapolate(
    signal,
    pos,
    dur,
    rate,
    n_signal=4000,
    ns_signal=4000,
):
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

    write_warped_wavs = False

    samples, rate = sf.read(args.input, always_2d=True)
    samples = np.squeeze(np.mean(samples, axis=1))

    xpos = args.x

    out = extrapolate(
        samples,
        pos=xpos,
        dur=args.d,
        n_signal=args.n,
        ns_signal=args.n,
        rate=rate,
    )
    sf.write(out, args.output, samplerate=rate)
