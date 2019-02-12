-- Set SRID to WGS84
SELECT UpdateGeometrySRID('world_countries_2017','geom',4326);

-- GiST Index on geom column
CREATE INDEX "GiST_Index"
    ON public.world_countries_2017 USING gist
    (geom)
    TABLESPACE pg_default;

-- Set geom column to not null to allow clustering
ALTER TABLE world_countries_2017 ALTER COLUMN geom SET not null;

-- Cluster to further increase performance 
ALTER TABLE public.world_countries_2017 CLUSTER ON "GiST_Index";

-- Update execution analyzer
VACUUM(FULL, ANALYZE) world_countries_2017;
