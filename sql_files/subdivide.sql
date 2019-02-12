-- Drop primary key constraint to allow multiple entries for the same country
ALTER TABLE world_countries_2017 DROP CONSTRAINT world_countries_2017_pkey

-- Subdivide complex geometries, North America countries only
with complex_areas_to_subdivide as (
    delete from world_countries_2017
    where cntry_name='United States' or cntry_name='Canada' or cntry_name='Mexico'
    returning gid, objectid, cntry_name, cntry_code, bpl_code, geom
)
insert into world_countries_2017 (gid, objectid, cntry_name, cntry_code, bpl_code, geom)
    select
        gid, objectid, cntry_name, cntry_code, bpl_code, ST_Multi(ST_Subdivide(geom, 255)) as geom
    from complex_areas_to_subdivide;
