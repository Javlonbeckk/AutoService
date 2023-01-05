# AutoService

#INSTALLING POSTGRESQL + PGADMIN

Download PostgreSQL 14 or higher and install PGAdmin, link -  https://www.enterprisedb.com/downloads/postgres-postgresql-downloads (PGAdmin and PostgreSQL are both in one file)

Install PostgreSQL + PGAdmin 4 on your machine(Stack Builder is not necessary)

If you do not have, create database, superuser, and set password




#TO-DO LIST INSIDE PROJECT

Rename file "dotenv" to ".env" and enter all your data(name of database, pguser, pgpassword, ip, token of bot, id of admin in telegram)

To get id of user in Telegram you can use https://t.me/ShowJsonBot

If you are running bot on your own machine, then ip: localhost 

Install all packages from "requirements.txt"

You can see structure of database and list of all servises in 
pictures, which are in folder "graphs"




#DOCKER(but it is not mandatory)

To install Docker use https://golb.hplar.ch/2019/01/docker-on-windows10-home-scratch.html

To run docker-compose run terminal(or command prompt) in folder of project, then use commands:

$ docker-machine stop 

$ start_docker

$ docker-compose up

$ docker-machine ip

Open your web-brower and enter ip and port 8080.




#RUN BOT

To start bot run "app.py". If you want see all reservations
in web interface run "webapp.py"
 
