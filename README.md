# Web-Server-Python3

Тестовое задание «MD5 light»

Необходимо написать небольшой веб-сервис, позволяющий посчитать MD5-хеш от файла, расположенного в сети Интернет.
Скачивание и расчет должны происходить в фоновом режиме. API данного сервиса следующий:

# POST
Запрос на /submit с параметрами url и email. На этот запрос сервис должен создать задачу с идентификатором, по которому пользователь может узнать о состоянии ее выполнения.
Email — опциональный параметр. Если он указан, то по окончанию выполнения задачи, необходимо прислать на этот адрес письмо в
котором будет указан url файла и его посчитанная MD5-хеш сумма. В качестве ответа на этот запрос необходимо выдать
пользователю идентификатор задачи.

# GET
Запрос на /check с параметром id. На этот запрос сервис должен вернуть пользователю состояние задачи по указанному
им id. Состояния — задачи не существует, задача в работе, задача завершена, задача завершилась неудачей. Если задача
завершена, то помимо этого необходимо указать в ответе url документа и его посчитанную MD5-хеш сумму. Статус код ответа
должен согласоваться с самим ответом (404, если задачи не существует и тд)


Пример использования данного сервиса:

> curl -X POST -d "email=user@example.com&url=https://www.google.com/robots.txt" http://localhost:8080/submit

{"id":"0e4fac17-f367-4807-8c28-8a059a2f82ac"}

> curl -X GET http://localhost:8080/check?id=0e4fac17-f367-4807-8c28-8a059a2f82ac

{"status":"running"}

> curl -X GET http://localhost:8080/check?id=0e4fac17-f367-4807-8c28-8a059a2f82ac

{"md5":"f4afe93ad799484b1d512cc20e93efd1","status":"done","url":"http://site.com/file.txt"}


#How to use it

Програма запускается в терминале №1:

python3 program.py --port=8080

Далее в терминале №2 пишутся запросы (как в примере). В этом же терминале мы получим ответ(при удачной компиляции и запуске), а в
терминале №1 мы увидим код завершения - 400 или код ошибки. 
