#!/bin/bash
set -eu  # Exit on error

storage_dir=./Dataset # put back to $1
librispeech_dir=$storage_dir/LibriSpeech
wham_dir=$storage_dir/wham_noise
librimix_outdir=$storage_dir/

# LibriSpeech_dev_clean &
# LibriSpeech_test_clean &
# LibriSpeech_clean100 &
# LibriSpeech_clean360 &
# wham &

# wait

# Path to python

python_path=./venv/bin/python

# If you wish to rerun" this script in the future please comment this line out.
# $python_path scripts/augment_train_noise.py --wham_dir $wham_dir

# CHANGE TO TWO SPEAKER ONLY
# Mix Clean only
for n_src in 2; do
  metadata_dir=metadata/Libri$n_src"Mix"
  $python_path scripts/create_librimix_from_metadata2.py --librispeech_dir $librispeech_dir \
    --metadata_dir $metadata_dir \
    --librimix_outdir $librimix_outdir \
    --n_src $n_src \
    --freqs 8k \
    --modes min max \
    --types mix_clean
done
