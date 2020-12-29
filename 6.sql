SELECT avg(rating) FROM ratings a
JOIN movies b
ON a.movie_id = b.id
WHERE b.year  = 2012; 