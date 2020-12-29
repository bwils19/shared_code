SELECT a.title FROM movies a
JOIN ratings b
ON a.id = b.movie_id
WHERE id IN
(SELECT movie_id FROM stars c
WHERE c.person_id =
(SELECT d.id FROM people d
WHERE d.name ="Chadwick Boseman"))
ORDER BY b.rating DESC LIMIT 5




