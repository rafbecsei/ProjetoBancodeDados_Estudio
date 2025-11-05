--Listar todos os filmes com nome, gênero e ano de lançamento.
SELECT nome, genero, ano_lancamento
FROM filme
  
--Mostrar todos os atores que participaram de um determinado filme.
SELECT a.nome as ator, f.nome
FROM ator a
INNER JOIN elenco e
  ON a.id = e.id_ator
INNER JOIN filme f
  ON e.id_filme = f.id
WHERE e.id_filme = '174'
  
--Contar quantos filmes cada ator participou.
SELECT a.nome, COUNT(e.id_filme) AS "Num"
FROM ator AS a
INNER JOIN elenco AS e ON e.id_ator = a.id
GROUP BY a.id, a.nome
ORDER BY "Num" DESC;

--Listar todos os filmes dirigidos por um diretor específico.
SELECT f.nome AS filme, d.nome
FROM filme f
INNER JOIN diretor d
  ON f.id_diretor = d.id
WHERE f.id_diretor = 'DR216'
  
--Mostrar os filmes com duração superior a determinado tempo.
SELECT f.nome AS filme
FROM filme f
WHERE cast(f.tempo as int) >= 200
  
--Contar a quantidade de filmes por gênero.
SELECT genero, count(genero) AS qtde
FROM filme
GROUP BY genero
  
--Mostrar os roteiristas que escreveram mais de um filme.
SELECT r.id AS id_roteirista, r.nome AS nome, count(f.id_roteirista) AS qtde_filmes
FROM roteirista r 
INNER JOIN filme f
  ON f.id_roteirista = r.id
GROUP BY r.id
HAVING count(id_roteirista) > 1

--Listar os atores do sexo feminino com menos de 30 anos.
SELECT nome, sexo, idade
FROM ator
WHERE sexo = 'feminino' AND cast(idade as int) < 30 

--Listar os filmes com mais de 5 atores no elenco
SELECT f.nome AS filme, count(e.id_ator) AS qtde_atores
FROM filme f
INNER JOIN elenco e
  ON f.id = e.id_filme
GROUP BY f.id
HAVING count(id_ator) > 5
  
--Listar todos os filmes de um determinado gênero lançados em um intervalo de anos.
SELECT f.nome AS filme
FROM filme f
WHERE cast(f.ano_lancamento as int) <= 2020 AND cast(f.ano_lancamento as int) >= 2010 and f.genero = 'Documentário'
