create table users(id int primary key auto_increment,
                    name varchar(32) not null,
                    password varchar(128) not null);

create table history_record(id int primary key auto_increment,
                            username varchar(32) not null,
                            time timestamp default current_timestamp(),
                            word varchar(32) not null);