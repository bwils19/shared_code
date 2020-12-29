SELECT a.name FROM people a
WHERE a.id in (
SELECT distinct b.person_id
FROM directors b
JOIN movies c
ON b.movie_id = c.id
JOIN ratings d
ON c.id = d.movie_id
WHERE rating >= 9.0);
