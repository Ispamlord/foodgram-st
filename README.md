Находясь в папке infra, скопируйте файл `.env.example` в `.env` и выполните
`docker-compose up`. Контейнер `frontend` соберёт статические файлы и
остановится. По адресу `http://localhost` будет доступен интерфейс, а
`http://localhost/api/docs/` откроет спецификацию API.

