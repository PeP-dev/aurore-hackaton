CREATE SCHEMA 'aurore';

CREATE TABLE `aurore`.`heberges` (
  `id` INT NOT NULL,
  `nom` VARCHAR(45) NULL,
  `prenom` VARCHAR(45) NULL,
  `tel` BIGINT(10) NULL,
  `mail` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `aurore`.`admin` (
  `id` INT NOT NULL,
  `login` VARCHAR(45),
  `password` VARCHAR(45),
  PRIMARY KEY (`id`));

CREATE TABLE `aurore`.`hebergeurs` (
  `id` INT NOT NULL,
  `login` VARCHAR(45),
  `password` VARCHAR(45),
  `nom` VARCHAR(45)
  PRIMARY KEY (`id`));

CREATE TABLE `aurore`.`logements` (
  `id` INT NOT NULL,
  `debut` VARCHAR(45),
  `fin` VARCHAR(45),
  `adresse` VARCHAR(45),
  `tel` BIGINT(10),
  `mail` VARCHAR(45),
  PRIMARY KEY (`id`));

CREATE TABLE `aurore`.`conditions` (
  `id` INT NOT NULL,
  `libelle` VARCHAR(45),
  PRIMARY KEY (`id`));