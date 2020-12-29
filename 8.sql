SELECT name FROM people a
JOIN stars b
ON a.id = b.person_id
JOIN movies c
ON b.movie_id = c.id
WHERE c.title = 'Toy Story';