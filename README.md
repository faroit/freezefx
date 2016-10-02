# Python, Freeze!

##### [View ipython notebook (includes audio demos)](http://nbviewer.jupyter.org/github/faroit/pyfreeze/blob/master/freeze_demo.ipynb)

This is a python implementation of an audio extrapolation method that is very well suited to freeze time domain audio signals. The idea of audio freezing is to being able to infinitely sustain a given signal. Audio extrapolation is a challenging task because the quality of the extrapolation highly depends on the input signal. E.g. sustaining a predominently harmonic sound (violin, trumpet) can be different to a noise like ride/cymbal.
Extrapolation/Freezing is closely related to [error concealment](https://en.wikipedia.org/wiki/Error_concealment) and [time scale modification](https://en.wikipedia.org/wiki/Audio_time-scale/pitch_modification).

![screen shot 2016-09-21 at 15 30 05](https://cloud.githubusercontent.com/assets/72940/18712819/5680c540-8010-11e6-9003-f6d2bfa46485.png)

The plots shows the spectrogram of a trumpet signal where the task is to extrapolate/freeze the signal, given a freeze time position (black arrow), a the number of samples being extrapolated (green).

## How does it work

Simpler methods, both in time and frequency domain, to extrapolate audio signals are based on  

  * repeating the previous time domain signal in an overlap+add fashion (OLA)
  * Using phase vocoder in the frequency domain

Both methods are simple to compute but fail to produce natural sounds. They often sound static or looped and contain artifacts. Also it is difficult to transition between the original signal and the extrapolated signal without long cross-fade windows.

### Extrapolation using AR modeling

Another approach for modeling audio signals, utilizes  autoregressive processes (AR), where each time domain signal is modeled by

  ```x(n)= ∑a_k * x(n−k)```

with ```{a_1, a_2, ..., ap}``` being the AR coefficients. The AR coefficients can be identified by system identification algorithms like the Burg algorithm. The basic idea of extrapolating samples in time domain using the AR model is described in [1]. Basically to extrapolate `W` samples based on `ns` past known samples:

* Identify the AR coefficients by using the Burg algorithm
* Initialize the filter with `ns` past known samples just before the section to be extrapolated
* Feed zeros of length `W` into the filter

![screen shot 2016-09-21 at 15 33 11](https://cloud.githubusercontent.com/assets/72940/18712915/d312ecd2-8010-11e6-909c-ca8c985de8d6.png)

The plots shows the spectrogram of the trumpet signal being extrapolated using the AR model. The blue/purple area indicates the number of past known samples `ns` being used to fit the AR model.

## Installation

Assuming, you already have python and pip installed, you can then install the requirements by

```
  pip install -r requirements.txt
```

## Usage

To use apply the freeze effect from the command line just run:

```c
python freeze.py input.wav output.wav -x 44100 -d 441000 -n 4000
```

where

* `-x` is the freeze position in samples
* `-d` are the number of samples to extrapolate
* `-n` is the AR model filter order (defaults to 4000)

## License


## References

[1] I. Kauppinen and K. Roth, “Audio signal extrapolation - theory and applications,” Proc. of the 5th Int. Conference on Digital Audio Effects (DAFx- 02), 2002.
