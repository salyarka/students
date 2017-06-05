DROP TABLE IF EXISTS student, discipline, student_discipline;
CREATE TABLE student (
	id       	  serial PRIMARY KEY,
	name     	  varchar(40) NOT NULL
);
CREATE TABLE discipline (
	id            serial PRIMARY KEY,
	title         varchar(40) NOT NULL
);
CREATE TABLE student_discipline(
	student_id    integer REFERENCES student ON DELETE CASCADE,
	discipline_id integer REFERENCES discipline ON DELETE CASCADE,
	score         integer NOT NULL,
	id            serial PRIMARY KEY
);
