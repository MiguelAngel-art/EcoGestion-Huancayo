
-- ============================================
-- ECOGESTION HUANCAYO
-- Curso: Programacion Web
-- Base de datos: SQL Server Express
-- ============================================

-- Este archivo prepara la base de datos
-- necesaria para ejecutar nuestro sistema.

USE master;
GO

-- Crear la base de datos solamente
-- cuando todavia no existe.

IF DB_ID(N'EcoGestionHuancayo') IS NULL
BEGIN

    CREATE DATABASE EcoGestionHuancayo;

    PRINT 'Base de datos creada correctamente.';

END
ELSE
BEGIN

    PRINT 'La base de datos ya existe. No se modifico.';

END;
GO

-- Comprobar que la base de datos existe.

SELECT
    name AS Nombre_Base_Datos,
    state_desc AS Estado
FROM sys.databases
WHERE name = N'EcoGestionHuancayo';
GO

-- NOTA:
-- Las tablas se crean automaticamente
-- mediante SQLAlchemy al iniciar FastAPI.
--
-- Este archivo no elimina ni modifica
-- las tablas o registros existentes.
