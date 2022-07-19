<a id="anchor"></a>
# Проект Foodgram "Продуктовый помощник"
![example workflow](https://github.com/ase77/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
## Описание:
На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
## Используемые технологии:
![https://www.python.org/](https://camo.githubusercontent.com/55e471c50835a4e4b084eafa9a82fd49aa1288bd148ae4c3e276e405db6a7f75/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d507974686f6e2d3436343634363f7374796c653d666c6174266c6f676f3d507974686f6e266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://www.djangoproject.com/](https://camo.githubusercontent.com/7192b5cd049ca04bd028774695bcf790c850e6f3b8fcfd4022daa79d0f183daf/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d446a616e676f2d3436343634363f7374796c653d666c6174266c6f676f3d446a616e676f266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://www.postgresql.org/](https://camo.githubusercontent.com/35940080ac4c53d288ec41ca11367e98b56e34fb1007ec9e8178c0e032407d88/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d506f737467726553514c2d3436343634363f7374796c653d666c6174266c6f676f3d506f737467726553514c266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://nginx.org/ru/](https://camo.githubusercontent.com/6ebc0f3d416cdfd5e6af91c8003745f8b49c3f30741bb5303abe11bc1f93cf27/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d4e47494e582d3436343634363f7374796c653d666c6174266c6f676f3d4e47494e58266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://gunicorn.org/](https://camo.githubusercontent.com/d637e79276a56dfb4531ddc67429ff52af04becc78052d88a6a14ccc08c1c5cd/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d67756e69636f726e2d3436343634363f7374796c653d666c6174266c6f676f3d67756e69636f726e266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://www.docker.com/](https://camo.githubusercontent.com/6e928d8c13895b010c64a37fcc6a1adfa0d5e774146eae485cf8df28abc03093/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d446f636b65722d3436343634363f7374796c653d666c6174266c6f676f3d446f636b6572266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://github.com/features/actions](https://camo.githubusercontent.com/d9698cafacdfcb0e1d80d16ecdbcdc8c58c6fb59914d3cbf5e439f0881157814/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d476974487562253230416374696f6e732d3436343634363f7374796c653d666c6174266c6f676f3d476974487562253230616374696f6e73266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)
![https://cloud.yandex.ru/](https://camo.githubusercontent.com/a571043856303345577ffa9977e04a90df121767ecff17fd6d080bb304d9854d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d59616e6465782e436c6f75642d3436343634363f7374796c653d666c6174266c6f676f3d59616e6465782e436c6f7564266c6f676f436f6c6f723d35364330433026636f6c6f723d303038303830)

## Workflow:
  * `tests` - проверка кода на соответствие стандарту PEP8;
  * `build_and_push_to_docker_hub` - сборка и доставка докер-образа для контейнера web на Docker Hub;
  * `deploy` - автоматический деплой проекта на боевой сервер;
  * `send_message` - отправка уведомления в Telegram о том, что процесс деплоя успешно завершился.
## Подготовьте сервер:
1. Войдите на свой удаленный сервер в облаке.
2. Остановите службу `nginx`:
```
sudo systemctl stop nginx 
```
3. Установите `docker`:
```
sudo apt install docker.io 
```
4. Установите docker-compose, с этим вам поможет официальная [документация](https://docs.docker.com/compose/install/).
5. Скопируйте файлы `docker-compose.yaml` и `nginx.conf` из вашего проекта на сервер 
в `home/<ваш_username>/docker-compose.yaml` и `home/<ваш_username>/nginx.conf` соответственно:
```
scp docker-compose.yaml <username>@<host>:/home/<username>/
scp default.conf <username>@<host>:/home/<username>/
```
6. В репозитории на Гитхабе добавьте данные в `Settings -> Secrets -> Actions -> New repository secret`:
```
DOCKER_USERNAME - ваш username на dockerhub
DOCKER_PASSWORD - ваш пароль на dockerhub
USER - имя пользователя для подключения к серверу
HOST - IP-адрес вашего сервера
SSH_KEY - скопируйте приватный ключ с компьютера, имеющего доступ к боевому серверу (cat ~/.ssh/id_rsa)
PASSPHRASE - если при создании ssh-ключа вы использовали фразу-пароль, то сохраните её в эту переменную
DB_ENGINE - django.db.backends.postgresql
DB_NAME - postgres
POSTGRES_USER - postgres
POSTGRES_PASSWORD - postgres
DB_HOST - db
DB_PORT - 5432
TELEGRAM_TO - ID своего телеграм-аккаунта (узнать свой ID можно у бота @userinfobot)
TELEGRAM_TOKEN - токен вашего бота (получить токен можно у бота @BotFather)
```
## После деплоя:
1. Выполните миграции в контейнере `backend`:
```
docker-compose exec backend python manage.py migrate
```
2. Создайте суперпользователя в контейнере `backend`:
```
docker-compose exec backend python manage.py createsuperuser
```
3. Соберите статику в контейнере `backend`:
```
docker-compose exec backend python manage.py collectstatic --noinput
```
4. Загрузите начальные данные из файлов `csv` в базу данных:
```
docker-compose exec backend python manage.py load_csv
```
___

## Сайт

Сайт доступен по ссылке: http://foodgramproject.hopto.org/

Админка доступка по ссылке: http://foodgramproject.hopto.org/admin/

Документация доступка по ссылке: http://foodgramproject.hopto.org/api/docs/

| user  | email           | password  | token | superuser |
 :----- | :-------------- | :-------- | :---: | :-------: |
| admin | super@user.ru   | admin     |   v   |     v     |
| user1 | normal@user1.ru | foodgram1 |   v   |     х     |
| user2 | normal@user2.ru | foodgram2 |   х   |     х     |


## Список доступных роутов
| Method | Route                                  | Description                      |
| :----: | :------------------------------------- | :------------------------------- |
|  GET   | `/api/users/`                          | Список пользователей             |
|  POST  | `/api/users/`                          | Регистрация пользователя         |
|  GET   | `/api/users/<id>/`                     | Профиль пользователя             |
|  GET   | `/api/users/me/`                       | Текущий пользователь             |
|  POST  | `/api/users/set_password/`             | Изменение пароля                 |
|  POST  | `/api/auth/token/login/`               | Получить токен авторизации       |
|  POST  | `/api/auth/token/logout/`              | Удаление токена                  |
|  GET   | `/api/tags/`                           | Cписок тегов                     |
|  GET   | `/api/tags/<id>/`                      | Получение тега                   |
|  GET   | `/api/recipe/`                         | Список рецептов                  |
|  POST  | `/api/recipe/`                         | Создание рецепта                 |
|  GET   | `/api/recipe/<id>/`                    | Получение рецепта                |
| PATCH  | `/api/recipe/<id>/`                    | Обновление рецепта               |
| DELETE | `/api/recipe/<id>/`                    | Удаление рецепта                 |
|  GET   | `/api/recipes/download_shopping_cart/` | Скачать список покупок           |
|  POST  | `/api/recipes/<id>/shopping_cart/`     | Добавить рецепт в список покупок |
|  POST  | `/api/recipes/<id>/shopping_cart/`     | Удалить рецепт из списка покупок |
|  POST  | `/api/recipes/<id>/favorite/`          | Добавить рецепт в избранное      |
| DELETE | `/api/recipes/<id>/favorite/`          | Удалить рецепт из избранного     |
|  GET   | `/api/users/subscriptions/`            | Мои подписки                     |
|  POST  | `/api/users/<id>/subscribe/`           | Подписаться на пользователя      |
| DELETE | `/api/users/<id>/subscribe/`           | Отписаться от пользователя       |
|  GET   | `/api/ingredients/`                    | Список ингредиентов              |
|  GET   | `/api/ingredients/<id>`                | Получение ингредиента            |

[__В начало__](#anchor) :point_up:
