-- fases_conductas_view
CREATE OR REPLACE VIEW fases_conductas_view AS
SELECT 
    fc.`id` AS `id`,
    fc.`idfase` AS `idfase`,
    fc.`idconducta` AS `idconducta`,
    f.`nombre` AS `fase`,
    c.`nombre` AS `conducta`
FROM fases_conductas fc
JOIN fases f ON fc.idfase = f.id
JOIN conductas c ON fc.idconducta = c.id
ORDER BY fc.idfase;

-- videos_conductas_view
CREATE OR REPLACE VIEW videos_conductas_view AS
SELECT 
    vc.id AS id,
    vc.idvideo AS idvideo,
    vc.inicio AS inicio,
    vc.fin AS fin,
    c.nombre AS nombre,
    vc.cantidad AS cantidad
FROM videos_conductas vc
JOIN fases_conductas fc ON fc.id = vc.idfaseconducta
JOIN conductas c ON c.id = fc.idconducta;