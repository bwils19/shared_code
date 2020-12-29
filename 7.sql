SELECT a.title, b.rating 
FROM movies a
JOIN ratings b
ON a.id = b.movie_id
WHERE a.year = '2010'
ORDER BY b.rating DESC, a.title ASC;