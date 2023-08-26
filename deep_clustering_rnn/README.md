## Deep Clustering for Speech Separation

Deep clustering in the field of speech separation implemented by pytorch

Demo Pages: [Results of pure speech separation model](https://www.likai.show/Pure-Audio/index.html)

> Hershey J R, Chen Z, Le Roux J, et al. Deep clustering: Discriminative embeddings for segmentation and separation[C]//2016 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2016: 31-35.

## Code writing log

- August 26, 2023 version - attempt at GPU-able repository. Confirmed to be working with CPU.

## Requirement

Install these in your WSL instance.

```
sudo apt-get update
sudo apt install libcairo2-dev pkg-config python3-dev libdbus-1-3 libdbus-1-dev libcups2-dev
```

Install requirements and dependencies in a virtual environment (any name will do). This is to avoid possible dependency versioning conflicts.

```
virtualenv dcdrnn
source dcdrnn/bin/activate
pip install -r requirements.txt
```

## Training steps

1. First, you can use the create_scp script to generate training and test data scp files.

```shell
python3 create_scp.py
```

2. Then, in order to reduce the mismatch of training and test environments. Therefore, you need to run the util script to generate a feature normalization file (CMVN).

```shell
python3 ./utils/util.py
```

3. Finally, use the following command to train the network.

```shell
python3 train.py --opt ./config/train.yml
```

## Inference steps

- Not yet tried.

1. Use the following command to start testing the model

```shell
python3 test.py -scp 1.scp -opt ./option/train.yml -save_file ./result
```

2. You can use the [this code](https://github.com/JusperLee/Calculate-SNR-SDR "this code") to calculate the SNR scores.

## Thanks

1. [Pytorch Template](https://github.com/victoresque/pytorch-template "Pytorch Template")
