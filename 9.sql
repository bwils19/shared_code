SELECT a.name FROM people a
WHERE a.id in (
SELECT distinct b.person_id
FROM stars b
JOIN movies c
ON b.movie_id = c.id
WHERE c.year = 2004)
ORDER BY a.birth;