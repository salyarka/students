DO
$$
DECLARE
  student TEXT ;
BEGIN
  student := 'student';
  FOR i IN 1..10 LOOP
    EXECUTE 'INSERT INTO student (name) values('
    	|| quote_literal(student)
    	|| quote_literal(i)
    	|| ');';
  END LOOP;
END;
$$