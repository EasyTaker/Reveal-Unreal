drop database if exists databasefake; #only run if it already exists
create database databasefake;
use databasefake;


create table Content
( contentID int primary key not null auto_increment,
webSourceName varchar(100) );


create table Websource
( websourceID int primary key not null auto_increment,
webSourceName varchar(100) ,
websourceLink varchar(100));

create table Topic
(
topicID int primary key not null auto_increment,
topicName varchar(100) );

create table Users
(
	userId int primary key not null auto_increment,
    userName varchar(100),
    userPassword varchar(100),
    firstName varchar(100) not null,
    lastName varchar(100) not null,
    email varchar(100)
    
);



create table FakeArticle
(
	articleId int primary key not null auto_increment,
    contentID int,
    topicID int,
    websourceId int,
    argumentation varchar(100),
    foreign key (contentID) references Content(contentID),
    foreign key (topicId) references Topic(topicId),
    foreign key (websourceId) references Websource(websourceId)
    
);

create table FakeSpot
(
	spotId int primary key not null auto_increment,
	articleId int,
    spotFrom int,
    spotTo int,
    foreign key (articleId) references FakeArticle(articleId)
);