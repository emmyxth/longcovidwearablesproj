#!/bin/bash
echo "ran"

if [ "$1" = "rhr" ]; then #
    python3 plot_data.py rhr --src=./zh_en_data/train.zh --tgt=./zh_en_data/train.en --dev-src=./zh_en_data/dev.zh --dev-tgt=./zh_en_data/dev.en --vocab=vocab.json --cuda --lr=5e-4 --patience=1 --valid-niter=200 --batch-size=32 --dropout=.3
elif [ "$1" = "dc" ]; then #data count
    echo "okay"
    python3 plot_data.py data_count /labs/mpsnyder/long-covid-study-data/processed_features/test_data_count.csv
elif [ "$1" = "dl" ]; then #device length
    python3 predict.py --lin --train-src=./zh_en_data/train.zh --train-tgt=./zh_en_data/train.en --dev-src=./zh_en_data/dev.zh --dev-tgt=./zh_en_data/dev.en --vocab=vocab.json --cuda --lr=5e-4 --patience=1 --valid-niter=200 --batch-size=32 --dropout=.3
elif [ "$1" = "gap" ]; then #gaps
    python3 predict.py --lin --train-src=./zh_en_data/train.zh --train-tgt=./zh_en_data/train.en --dev-src=./zh_en_data/dev.zh --dev-tgt=./zh_en_data/dev.en --vocab=vocab.json --cuda --lr=5e-4 --patience=1 --valid-niter=200 --batch-size=32 --dropout=.3
else
    echo "Invalid Option Selected"
fi