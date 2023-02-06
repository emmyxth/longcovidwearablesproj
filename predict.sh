#!/bin/bash
#Will need to change addresses for sources of data

if [["$1" = "valid" ] && ["$2" = "hrstep" ]]; then #
	python3 predict.py --lin --src=./zh_en_data/train.zh --tgt=./zh_en_data/train.en --dev-src=./zh_en_data/dev.zh --dev-tgt=./zh_en_data/dev.en --vocab=vocab.json --cuda --lr=5e-4 --patience=1 --valid-niter=200 --batch-size=32 --dropout=.3
elif [["$1" = "test" ] && ["$2" = "hrstep" ]]; then
	python3 predict.py --lin --train-src=./zh_en_data/train.zh --train-tgt=./zh_en_data/train.en --dev-src=./zh_en_data/dev.zh --dev-tgt=./zh_en_data/dev.en --vocab=vocab.json --cuda --lr=5e-4 --patience=1 --valid-niter=200 --batch-size=32 --dropout=.3
elif [["$1" = "valid" ] && ["$2" = "appfit" ]]; then
	python3 predict.py --lin --train-src=./zh_en_data/train.zh --train-tgt=./zh_en_data/train.en --dev-src=./zh_en_data/dev.zh --dev-tgt=./zh_en_data/dev.en --vocab=vocab.json --cuda --lr=5e-4 --patience=1 --valid-niter=200 --batch-size=32 --dropout=.3
elif [["$1" = "test" ] && ["$2" = "appfit" ]]; then
	python3 predict.py --lin --train-src=./zh_en_data/train.zh --train-tgt=./zh_en_data/train.en --dev-src=./zh_en_data/dev.zh --dev-tgt=./zh_en_data/dev.en --vocab=vocab.json --cuda --lr=5e-4 --patience=1 --valid-niter=200 --batch-size=32 --dropout=.3
elif [[ "$1" = "valid" ] && [ "$2" = "maj" ]]; then #for using majority classifier
	python3 run.py --maj --train-src=./zh_en_data/train_debug.zh --train-tgt=./zh_en_data/train_debug.en --dev-src=./zh_en_data/dev.zh --dev-tgt=./zh_en_data/dev.en --vocab=vocab.json --lr=5e-4
elif [[ "$1" = "test" ] && [ "$2" = "maj" ]]; then #for using majority classifier
	python3 run.py --maj --train-src=./zh_en_data/train_debug.zh --train-tgt=./zh_en_data/train_debug.en --dev-src=./zh_en_data/dev.zh --dev-tgt=./zh_en_data/dev.en --vocab=vocab.json --lr=5e-4
else
	echo "Invalid Option Selected"
fi