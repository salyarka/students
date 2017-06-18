DROP TABLE IF EXISTS student, discipline, student_discipline;
CREATE TABLE student (
  id       	    serial PRIMARY KEY,
  name     	    varchar(40) NOT NULL
);
CREATE TABLE discipline (
  id            serial PRIMARY KEY,
  title         varchar(40) NOT NULL
);
CREATE TABLE student_discipline(
  student_id    integer NOT NULL,
  discipline_id integer NOT NULL,
  score         integer NOT NULL,
  id            serial,
  PRIMARY KEY (student_id, discipline_id, id),
  FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE,
  FOREIGN KEY (discipline_id) REFERENCES discipline(id) ON DELETE CASCADE
);
