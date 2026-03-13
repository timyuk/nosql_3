# 1. Запуск шардинга
## Инициализация конфиг-сервер
```docker exec -it configsvr mongosh --port 27019 --eval 'rs.initiate({  _id: "configReplSet", configsvr: true, members: [{ _id: 0, host: "configsvr:27019" }]})'```

## Инициализация первого шарда
```docker exec -it shard1 mongosh --port 27018 --eval 'rs.initiate({  _id: "shard1", members: [{ _id: 0, host: "shard1:27018" }]})'```

## Инициализация второго шарда
```docker exec -it shard2 mongosh --port 27020 --eval 'rs.initiate({  _id: "shard2", members: [{ _id: 0, host: "shard2:27020" }]})'```

## Дальше надо зайти в mongos и настроить шардирование
```docker exec -it mongos mongosh --port 27017```

```
sh.addShard("shard1/shard1:27018")
sh.addShard("shard2/shard2:27020")

sh.enableSharding("university")

sh.shardCollection("university.grades", { student_id: 1 })
```

# 2. Запуск интерфейса и нагрузочного тестирования

## Интерфейс
```
docker compose run interface
```

## Нагрузочное тестирование
```
docker compose run load_test
```
