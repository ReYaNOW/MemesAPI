[![Linter check](https://github.com/ReYaNOW/MemesAPI/actions/workflows/linter_check.yml/badge.svg)](https://github.com/ReYaNOW/MemesAPI/actions/workflows/linter_check.yml)
[![Run tests](https://github.com/ReYaNOW/MemesAPI/actions/workflows/run_tests.yml/badge.svg)](https://github.com/ReYaNOW/MemesAPI/actions/workflows/run_tests.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/f1c3173e996e7a7b12ef/maintainability)](https://codeclimate.com/github/ReYaNOW/MemesAPI/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/f1c3173e996e7a7b12ef/test_coverage)](https://codeclimate.com/github/ReYaNOW/MemesAPI/test_coverage)

## Описание
Тестовое задание для некой компании

Веб-приложение, которое предоставляет API для работы с коллекцией мемов.
Сервис взаимодействует с клиентом при помощи REST API.  

Используется S3-совместимое хранилище (MinIO)  
Присутствуют тесты, написанные при помощи Pytest
Реализована возможность запуска всего проекта в Docker Compose.  
Реализована валидация входных данных.


Стек: Python3.11, FastApi, SqlAlchemy, Alembic, Asyncpg, Pytest, Docker, Minio

## Документация
Открыть документацию можно по GGGGG[ссылке](https://test-task-avito-tech.onrender.com/docs)  
Там же можно поделать запросы к веб-приложению

# Использование


 - Открыть задеплоенный [тестовый вариант](https://avito-tech-test-task.onrender.com)
 - [Развернуть сервис с Docker](#Как-развернуть-сервис-с-Docker)  
 - [Развернуть сервис полностью в Docker](#Как-развернуть-полностьЮ-в-Docker)

![App previeффффффw](https://github.com/ReYaNOW/ReYaNOW/blob/main/Images/stats_preview_imgффффф.png?raw=true)

## Как развернуть сервис с Docker
Для этого необходим [Poetry](https://python-poetry.org/docs/#installing-with-pipx)  
  
1. Склонировать репозиторий

```
git clone https://github.com/ReYaNOW/MemesAPI.git
```

2. Перейти в директорию проекта и переименовать .env.example в .env
  
```
cd MemesAPI
mv .env.example .env
```
  
3. Собрать необходимые Docker образы, применить миграции к БД, запустив перед этим необходимые Docker контейнеры
  
```  
make compose-install
```  
  
4. Установить Python зависимости
  
```
poetry install
```

5. Запустить локальный сервер и открыть http://127.0.0.1:8080
  
```
make dev
```

Либо запустить сначала все необходимые контейнеры, если они были остановлены, а потом уже сам сервер  
  
```
make compose-dev
```
  

## Как развернуть полностью в Docker
1. Склонировать репозиторий

```
git clone https://github.com/ReYaNOW/MemesAPI.git
```

2. Перейти в директорию проекта и переименовать .env.example в .env
  
```
cd MemesAPI
mv .env.example .env
```

3. Собрать необходимые Docker образы, применить миграции к БД, запустив перед этим необходимые Docker контейнеры
  
```
make compose-install
```

4. запустить все контейнеры и открыть http://127.0.0.1:8080
  
```
make compose-full-start
```
