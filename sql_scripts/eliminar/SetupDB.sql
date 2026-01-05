select * from resultados r;
select * from observaciones_videos ov;
create table fases(
id int primary key auto_increment,
nombre varchar(100)
);

drop table fases;

create table acciones(
id int primary key auto_increment,
nombre varchar(100)
);

alter table acciones modify column nombre varchar(100) unique;

create table fases_acciones(
id int primary key auto_increment,
idfase int,
idaccion int,
constraint unique key (idfase,idaccion),
constraint foreign key(idfase) references fases(id),
constraint foreign key(idaccion) references acciones(id)
);

insert into fases(nombre) values('Habituación'),('Moldeamiento'),('Mantenimiento'),('Refuerzo'), ('Habituación'),('Extinción');
select * from fases;
insert into acciones(nombre) values('Palanqueo'),('Levantamiento'),('Acercamiento'),('Entrega Pellet'),('Consumo Pellet'),('Comedero'),('Aproximación'),('Tocar Palanca');
select * from acciones;


insert into acciones(nombre) values('Palanqueo Reforzado'),('Palanqueo No Reforzado');

select * from fases_acciones;

insert into fases_acciones(idfase,idaccion) values(1,1),(1,2),(1,3),(1,4),(1,5);
insert into fases_acciones(idfase,idaccion) values(2,6),(2,7),(2,8),(2,1);
insert into fases_acciones(idfase,idaccion) values(3,1),(3,2),(3,3);
insert into fases_acciones(idfase,idaccion) values(4,9),(4,10);
insert into fases_acciones(idfase,idaccion) values(5,1),(5,2),(5,3);



update fases set nombre = 'Habituación' where id=1;
delete from fases where id=6;
