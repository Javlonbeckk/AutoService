# AutoService
Download PostgreSQL 14 or higher and install PGAdmin(you can download them from https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
Install PostgreSQL + PGAdmin on your machine
Create database, superuser, and set password


Rename file "dotenv" to ".env" and enter all your data(database, token, pguser, password, ip)
If you are running bot on your local machine, then ip: localhost 
Install all packages from "requirements.txt"


You can see structure of database and list of all servises in 
pictures, which are in folder "graphs"


To run docker-compose use commands:

$ docker-machine stop 

$ start_docker

$ docker-compose up

$ docker-machine ip

Open your web-brower and enter ip and port 8080.



To start bot run "app.py". If you want see all reservations
in web interface run "webapp.py"
 
