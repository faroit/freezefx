# FreezeFX 

![screen shot 2016-09-21 at 15 30 05](https://cloud.githubusercontent.com/assets/72940/18712819/5680c540-8010-11e6-9003-f6d2bfa46485.png)

## How does it work

One of the most often used approaches for modeling audio signals utilizes an autoregressive process (AR) 

  ```x(n)= ∑a_k * x(n−k)```

with ```{a_1, a_2, ..., ap}``` being the AR coefficients. The AR coefficients can be identified by system identification al- gorithms like the Burg algorithm. The basic idea of extrapolating samples in time domain using the AR model is described in [2]. Basically to extrapolate `W` samples based on `ns` past known samples:

* Identify the AR coefficients by using the Burg algorithm
* Initialize the filter with `ns` past known samples just before the section to be extrapolated
* Feed zeros of length `W` into the filter

A more detailed description including audio demos can be found [in this ipython notebook.](http://nbviewer.jupyter.org/github/faroit/pyfreeze/blob/master/freeze_demo.ipynb)
![screen shot 2016-09-21 at 15 33 11](https://cloud.githubusercontent.com/assets/72940/18712915/d312ecd2-8010-11e6-909c-ca8c985de8d6.png)

## References

[1] S. Preihs, F.R. Stöter, and J. Ostermann, “Low delay error concealment for audio signals,” in Audio Engineering Society Conference: 46th International Conference: Audio Forensics, Jun 2012.

[2] I. Kauppinen and K. Roth, “Audio signal extrapolation - theory and applications,” Proc. of the 5th Int. Conference on Digital Audio Effects (DAFx- 02), 2002.
