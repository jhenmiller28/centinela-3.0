DROP TABLE IF EXISTS ataques; -- Borramos la vieja para actualizar
CREATE TABLE ataques (
    id SERIAL PRIMARY KEY,
    ip VARCHAR(50)UNIQUE ,            -- Antes era ip_origen
    intentos INT,              -- Columna nueva que pide tu script
    ultimo_ataque TIMESTAMP    -- Antes era fecha
);
