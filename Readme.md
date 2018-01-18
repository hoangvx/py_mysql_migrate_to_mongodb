# mysql migrate to mongodb

## Prepare

+ python (mysql.connector, pymongo, yaml, datetime)

+ docker

## Setting

### Database setting

```yml
# db.yml
mysql:
  host:127.0.0.1
  username: root
  password: abc1234
  database: sample

mongodb:
  host: 127.0.0.1
  database: sample
```

### Transaction

```yml
# tr.yml
prefectures:
  columns:
    name:
    prefecture_cd:
    latitude:
    longitude:
    center_latitude:
    center_longitude:

regions:
  embed:
    from: prefectures
    key: prefecture_cd
  columns:
    license_plate_chimei_cd:
    license_plate_chimei:
    prefecture_cd:
    is_valid:
```

`embed`: want to embed this collection to other collection. provide collection name and key

> Default translate datetime datatype to string

## Run

```bash
python migrate.py
```

# End