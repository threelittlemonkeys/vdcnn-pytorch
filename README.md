# VDCNNs in PyTorch

A PyTorch implementation of Very Deep Convolutional Networks (VDCNNs) for text classification.

## Usage

Training data should be formatted as below:
```
sentence \t label
sentence \t label
...
```

To prepare data:
```
python prepare.py training_data
```

To train:
```
python train.py model word_to_idx tag_to_idx training_data.csv num_epoch
```

To predict:
```
python predict.py model.epochN word_to_idx tag_to_idx test_data
```

To evaluate:
```
python evaluate.py model.epochN word_to_idx tag_to_idx test_data
```

## References

Alexis Conneau, Holger Schwenk, Loïc Barrault, Yann Lecun. 2017. [Very Deep Convolutional Networks for Text Classification.](https://arxiv.org/abs/1606.01781) arXiv:1606.01781.
