# ICASSP 2018: Nonnegative Tensor Factorization for Source Separation of Loops in Audio

This site contains instructions on how to generate the ground truth data related to our ICASSP 2018 publication, "Nonnegative Tensor Factorization for Source Separation of Loops in Audio" ([PDF](http://jblsmith.github.io/documents/smith2018-icassp-nonnegative_tensor_factorization.pdf)), [described in detail here](http://jblsmith.github.io/projects/nonnegative-tensor-factorization/).

	@inproceedings{smith2018nonnegative,
	Address = {Calgary, AB, Canada},
	Author = {Smith, Jordan B. L. and Goto, Masataka},
	Booktitle = {Proceedings of the {IEEE} International Conference on Acoustics, Speech and Signal Processing},
	Pages = {171--175},
	Title = {Nonnegative tensor factorization for source separation of loops in audio},
	Year = {2018}}

## Abstract

The prevalence of exact repetition in loop-based music makes it an opportune target for source separation. Nonnegative factorization approaches have been used to model the repetition of looped content, and kernel additive modeling has leveraged periodicity within a piece to separate looped background elements. We propose a novel method of leveraging periodicity in a factorization model: we treat the two-dimensional spectrogram as a three-dimensional tensor, and use nonnegative tensor factorization to estimate the component spectral templates, rhythms and loop recurrences in a single step. Testing our method on synthesized loop-based examples, we find that our algorithm mostly exceeds the performance of competing methods, with a reduction in execution cost. We discuss limitations of the algorithm as we demonstrate its potential to analyze larger and more complex songs.

## How to use

1. Download the [original dataset](https://www.audiolabs-erlangen.de/resources/MIR/2016-ISMIR-EMLoop), which is licensed under [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/).

2. Unzip the dataset and move the folder ("ISMIR16-EM-Patterns-Audio") to your working directory.

3. In terminal, run:

```
cd icassp2018
python audio_generation.py
```

## Source

The data we used to evaluate our algorithm were derived from "Towards Modeling and Decomposing Loop-based Electronic Music", by Patricio López-Serrano, Christian Dittmar, Jonathan Driedger and Meinard Müller. They provided a set of sample stems to create short electronic dance music (EDM) tracks.

1. [Link to original dataset](https://www.audiolabs-erlangen.de/resources/MIR/2016-ISMIR-EMLoop)
2. Citation:

		@inproceedings{lopez-serrano2016,
		Address = {New York, NY, USA},
		Author = {L{\'o}pez-Serrano, Patricio and Dittmar, Christian and Driedger, Jonathan and M{\"u}ller, Meinard},
		Booktitle = {Proceedings of the International Society for Music Information Retrieval Conference},
		Pages = {502--508},
		Title = {Towards Modeling and Decomposing Loop-based Electronic Music},
		Year = {2016}}
