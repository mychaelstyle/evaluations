# Evaluationsについて

IPA()が作成・公開しているiCD(iコンピテンシディクショナリ）を見やすく使いやすく評価に利用できるようにするために開発しているオープンソースのツールです。
今のところ個人プロジェクトですが協力者は随時募集しております。

- https://www.ipa.go.jp/
- https://www.ipa.go.jp/jinzai/hrd/i_competency_dictionary/index.html

# ライセンス

# How to use

1. マイグレーションを作成しevaluations/setting.pyのデータベース接続情報を変更してからマイグレーションする

```
cd [プロジェクトフォルダ]
python manage.py migrate
```

2. iCDのExcelファイル3種をダウンロードしてインポートする

```
python manage.py import_icd --type task --file ~/Downloads/000068633.xlsx
python manage.py import_icd --type skill --file ~/Downloads/000068634.xlsx
python manage.py import_icd --type relation --file ~/Downloads/000068635.xlsx
```

検索用ドキュメントテーブルのデータを生成する

```
python manage.py makesearchdocuments
```

3. キャッシュテーブルとstaticファイル収集と言語ファイルコンパイル

```
python manage.py createcachetable
python manage.py collectstatic
python manage.py compilemessages
```

4. runserverで起動するかサーバーのアプリケーションサーバーに配備してください

4. 使い方

ToDo
