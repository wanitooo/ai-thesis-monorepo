# Dual-path-RNN-Pytorch

## Requirement

Install requirements and dependencies in a virtual environment (any name will do). This is to avoid possible dependency versioning conflicts.

```
virtualenv dptasnet
source dptasnet/bin/activate
pip install -r requirements.txt
```

# Training

Skip mo muna yung Conv-TasNet instructions drin, and go straight to Dual Path RNN instructions. I think the Conv-Tasnet model part is integrated in the Dual Path model na based sa code but it's not explicitly stated (could be wrong). Also in both train.py and train_rnn.py, nauuna yung validation sa logs, even though una yung training dapat sa code. Though after some iterations lalabas narin yung train (dapat). See log/conv_Tasnet/conv-tasnet.log

## Training for Conv-TasNet model

1. First, you need to generate the scp file using the following command. The content of the scp file is "filename && path".
   Change filepath to correct directories if needed

```shell
python3 create_scp.py
```

2. Then you can modify the training and model parameters through "[config/Conv_Tasnet/train.yml](https://github.com/JusperLee/Dual-Path-RNN-Pytorch/tree/master/config/Conv_Tasnet)".

```shell
cd config/Conv-Tasnet
vim train.yml
```

3. Then use the following command in the root directory to train the model.

```shell
python3 train_Tasnet.py --opt config/Conv_Tasnet/train.yml
```

## Training for Dual Path RNN model

1. First, you need to generate the scp file using the following command. The content of the scp file is "filename && path".

```shell
python3 create_scp.py
```

2. Then you can modify the training and model parameters through "[config/Dual_RNN/train.yml](https://github.com/JusperLee/Dual-Path-RNN-Pytorch/tree/master/config/Dual_RNN "config / Dual_RNN / train.yml")".

```shell
cd config/Dual_RNN
vim train_rnn.yml
```

3. Then use the following command in the root directory to train the model.

```shell
python3 train_rnn.py --opt config/Dual_RNN/train_rnn.yml
```

# Inference

- Have not attempted to run this code at all (Sept 3, 2023)

## Conv-TasNet

You need to modify the default parameters in the test_tasnet.py file, including test files, test models, etc.

### For multi-audio

```shell
python3 test_tasnet.py
```

### For single-audio

```shell
python3 test_tasnet_wav.py
```

## Dual-Path-RNN

You need to modify the default parameters in the test_dualrnn.py file, including test files, test models, etc.

### For multi-audio

```shell
python test_dualrnn.py
```

### For single-audio

```shell
python test_dualrnn_wav.py
```

# Pretrain Model

- [Conv-TasNet model](https://drive.google.com/open?id=1MRe4jiwgtAFZErjz-LWuuyEG8VGSU0YS "Google Driver")

- [Dual-Path-RNN model](https://drive.google.com/open?id=1TInJB-idggkKJ5YkNvnrTopum_HgX3_o "Google Driver")

# Result

## Conv-TasNet

![](https://github.com/JusperLee/Dual-Path-RNN-Pytorch/blob/master/log/Conv_Tasnet/loss.png)

Final Results: **15.8690** is 0.56 higher than **15.3** in the paper.

## Dual-Path-RNN

Final Results: **18.98** is 0.1 higher than **18.8** in the paper.

# Reference

1. Luo Y, Chen Z, Yoshioka T. Dual-path RNN: efficient long sequence modeling for time-domain single-channel speech separation[J]. arXiv preprint arXiv:1910.06379, 2019.
2. [Conv-TasNet code](https://github.com/JusperLee/Conv-TasNet "Conv-TasNet code") && [Dual-RNN code](https://github.com/yluo42/TAC/blob/master/utility/models.py "Dual-RNN code")
