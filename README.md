# pythonAGI
Need to have UserDetail table

create table UserDetail (
id int not null PRIMARY KEY,
userID varchar(30),
location varchar(200)
FOREIGN KEY (userID) REFERENCES ps_auths(ID)
);

Insert data for location for useres in asterisk.

insert python script in /var/lib/asterisk/agi-bin/ 
add permision on file.
Change config file for your database. 
And run your asterisk =))

