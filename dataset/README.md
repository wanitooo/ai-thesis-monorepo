# To get the dataset run the following in a WSL instance

```
# marks .sh script as executable
chmod +x ./download_dataset.sh

# runs script
./download_dataset.sh
```

### The generated dataset should have this file structure

```
dataset/
├── MiniLibriMix/
│   └── metadata/
├── test/
│   ├── mix_clean/
│   ├── s1/
│   └── s2/
├── train/
│   ├── mix_both (NOT USED)
│   ├── mix_clean/
│   ├── noise/
│   ├── s1/
│   └── s2/
└── val/
    ├── mix_both (NOT USED)
    ├── mix_clean/
    ├── noise/
    ├── s1/
    └── s2/
```

### Breakdown of generated data

- _test/_ is from the first 250 mixtures of Libri2Mix
  - Transcript for the mixtures in the set are not yet collected.
- _train/_ and _val/_ are from MiniLibriMix
- Only mix_clean will be used as input for the models
