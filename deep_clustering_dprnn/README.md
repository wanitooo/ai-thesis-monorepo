# Combining both Dual Path RNN and Deep Clustering

Scaffold for architecting / building the model. The code is not runnable. The added code are for reference/editing later. Attempts at making the DPCL-DPRNN model are at model/initial_dpcl_dprnn.

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

- Terrible naming in the model_rnn.py file
- the Dual_RNN_Block class corresponds to `B)` in the original paper.
- Dual_Path_RNN class corresponds to `A)`, `B)`, `C)` altogether combined, the segmentation and overlap add are only found here.
- the shaping and reshaping of the input tensors require contiguous() which allocates a contiguous chunk of memory in the hardware
-

# Generally

-

# Resources

- [Luo's implementation](https://github.com/yluo42/TAC/blob/master/utility/models.py)
- [Asteroid](https://github.com/asteroid-team/asteroid/blob/68c26692da9bfc545e8cae0a9a650296dce34c60/asteroid/models/dprnn_tasnet.py)
- [SpeechBrain](https://github.com/speechbrain/speechbrain/)
- [Jusper](https://github.com/JusperLee/Dual-Path-RNN-Pytorch)
- [Karpathy (ChatGPT researcher) making a model from scratch](https://www.youtube.com/watch?v=kCc8FmEb1nY)

# Sanity check notes

- [Excalidraw notes](https://excalidraw.com/#room=7506e0242b69ba2cd0c1,C82QAUx-XFqGQ5HC_57x6A)
