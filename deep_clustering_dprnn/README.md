# Combining both Dual Path RNN and Deep Clustering

Scaffold for architecting / building the model. The code is not runnable. The added code are for reference/editing later.

## Notes

- Utility, training, and testing code should be based on the latest iteration that we have (Dual path repo)
-

# Considerations for building / architecting DP DCPL

## These are observations of the code:

### In /deep_clustering_rnn

- model.py does not provide the logic for separating the speaker mixtures into audio files
- trainer.py also does not separate speaker mixtures into audio files
- it measures separation success by the calculation of loss, which is independent of the audio separation of mixtures
- instead the difference/accuracy is calculated with the representations of the mixtures in number/tensor form as seen in loss.py.
- speakers are only separated in test.py.

### In /dprnn_tasnet

-

# Resources

- [Luo's implementation](https://github.com/yluo42/TAC/blob/master/utility/models.py)
- [Asteroid](https://www.example.com)
- [SpeechBrain](https://github.com/speechbrain/speechbrain/)
- [Jusper](https://github.com/JusperLee/Dual-Path-RNN-Pytorch)
