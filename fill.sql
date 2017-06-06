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
  student_id    integer REFERENCES student ON DELETE CASCADE,
  discipline_id integer REFERENCES discipline ON DELETE CASCADE,
  score         integer NOT NULL,
  id            serial PRIMARY KEY
);
DO
$$
DECLARE
  student varchar(7);
  discipline varchar(10);
  number_of_students INTEGER;
  number_of_discipline INTEGER;
  lower_score INTEGER;
  higher_score INTEGER;
BEGIN
  student := 'student';
  discipline := 'discipline';
  number_of_students := 50000;
  number_of_discipline := 20;
  FOR i IN 1..number_of_students LOOP
    EXECUTE 'INSERT INTO student (name) values('
      || quote_literal(student)
      || quote_literal(i)
      || ');';
  END LOOP;
  FOR i IN 1..number_of_discipline LOOP
    EXECUTE 'INSERT INTO discipline (title) values('
      || quote_literal(discipline)
      || quote_literal(i)
      || ');';
  END LOOP;
  FOR i IN 1..number_of_students LOOP
    FOR j IN 1..number_of_discipline LOOP
      EXECUTE 'INSERT INTO student_discipline (student_id, discipline_id, score) values('
        || quote_literal(i)
        || ', '
        || quote_literal(j)
        || ', '
        || quote_literal(floor(random()*(5-1+1))+1)
        || ');';
    END LOOP;
  END LOOP;
END
$$