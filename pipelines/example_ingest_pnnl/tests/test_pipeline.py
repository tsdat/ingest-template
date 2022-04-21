import os
import xarray as xr
from utils import expand, set_env
from pipelines.example_ingest_pnnl import CustomPipeline

parent = os.path.dirname(__file__)


def test_example_ingest_pnnl_pipeline():
    set_env()
    pipeline = CustomPipeline(
        expand("config/pipeline_config_example_ingest_pnnl.yml", parent),
        expand("config/storage_config_example_ingest_pnnl.yml", parent),
    )
    output = pipeline.run(expand("tests/data/input/data.csv", parent))
    expected = xr.open_dataset(
        expand("tests/data/expected/pnnl.example_ingest.b1.20211114.000000.nc", parent)
    )
    xr.testing.assert_allclose(output, expected)
