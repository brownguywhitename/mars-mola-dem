import os
from osgeo import gdal, osr

# Enable GDAL exceptions for better error messages
gdal.UseExceptions()

# Directory with your files
directory = r"C:\Users\4ourfuture\Documents\UCL PhD\Topology Files"

# .lbl files (open these – GDAL needs the label for correct metadata)
lbl_files = [
    "megt90n000gb.lbl",  # Northern west
    "megt90n180gb.lbl",  # Northern east
    "megt00n000gb.lbl",  # Southern west
    "megt00n180gb.lbl",  # Southern east
]

lbl_paths = [os.path.join(directory, f) for f in lbl_files]

# Output files
vrt_output = os.path.join(directory, "mars_mola_global.vrt")
tif_output = os.path.join(directory, "mars_mola_global_463m.tif")

# Important: Apply the half-pixel offset correction required for MOLA MEGDR files
# This is done via GDAL config options (standard method for PDS driver)
gdal.SetConfigOption("PDS_SampleProjOffset_Shift", "-0.5")
gdal.SetConfigOption("PDS_LineProjOffset_Shift", "-0.5")

# Step 1: Build virtual mosaic (VRT)
vrt_options = gdal.BuildVRTOptions(
    resampleAlg="cubic",      # Good for continuous data like elevation
    addAlpha=False,
    srcNodata=None,
    VRTNodata=None
)

vrt_ds = gdal.BuildVRT(vrt_output, lbl_paths, options=vrt_options)
if vrt_ds is None:
    raise RuntimeError("Failed to build VRT – check that the .lbl files are readable.")

# Ensure proper Mars simple cylindrical projection (optional but recommended)
srs = osr.SpatialReference()
srs.ImportFromEPSG(4326)  # Equirectangular on WGS84 sphere – very close to Mars IAU sphere
vrt_ds.SetProjection(srs.ExportToWkt())

vrt_ds.FlushCache()
vrt_ds = None
print(f"Virtual mosaic created: {vrt_output}")
print("   You can open this VRT directly in QGIS/ArcGIS/etc. Elevations auto-unscale to meters.")

# Step 2: Materialize to compressed GeoTIFF (real meters, Float32)
translate_options = gdal.TranslateOptions(
    format="GTiff",
    creationOptions=["COMPRESS=DEFLATE", "PREDICTOR=2", "ZLEVEL=9", "TILED=YES", "BIGTIFF=YES"],
    noData=None,
    unscale=True  # Essential: converts scaled Int16 → real elevation in meters
)

print("Materializing to GeoTIFF (expect ~500–600 MB)...")
tif_ds = gdal.Translate(tif_output, vrt_output, options=translate_options)
if tif_ds is None:
    raise RuntimeError("Failed to create GeoTIFF.")

tif_ds.FlushCache()
tif_ds = None
print(f"Global Mars MOLA DEM created: {tif_output}")
print("   Float32, units: meters relative to Mars areoid.")

# Optional: Add overviews for faster display in GIS software
print("Adding overviews (this may take a few minutes)...")
os.system(f"gdaladdo -ro --config COMPRESS_OVERVIEW DEFLATE --config PREDICTOR_OVERVIEW 2 {tif_output} 2 4 8 16 32 64")

print("All done!")