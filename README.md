# Notes Generator
## Desc
どちらかというとコンバータ(英弱で気づかなかった)

## Tree

```
.
├── Generator.py
├── README.md
├── json
│   └── sam.json
└── output
    └── sam.json

```

## How2Use

### 1. jsonフォルダに変換前のjsonファイルを入れる
(例) hogehoge.json

```
.
└── json
    └── hogehoge.json
```

### 2. 実行

```
python3 Generator.py hogehoge.py
```

### 3. 変換される

```
.
└── output
    └── hogehoge.json
```