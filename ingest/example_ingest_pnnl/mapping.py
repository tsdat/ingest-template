import re

from typing import AnyStr, Dict
from utils import IngestSpec, expand
from . import CustomPipeline


mapping: Dict["AnyStr@compile", IngestSpec] = {
    # Mapping for Raw Data -> Ingest
    re.compile(r".*/data\.csv"): IngestSpec(
        pipeline=CustomPipeline,
        pipeline_config=expand(
            "config/pipeline_config_example_ingest_pnnl.yml", __file__
        ),
        storage_config=expand(
            "config/storage_config_example_ingest_pnnl.yml", __file__
        ),
        name="example_ingest_pnnl",
    ),
    # Mapping for Processed Data -> Ingest (so we can reprocess plots)
    re.compile(r".*/pnnl\.example_ingest\.b1\.\d{8}\.\d{6}\.nc"): IngestSpec(
        pipeline=CustomPipeline,
        pipeline_config=expand(
            "config/pipeline_config_example_ingest_pnnl.yml", __file__
        ),
        storage_config=expand(
            "config/storage_config_example_ingest_pnnl.yml", __file__
        ),
        name="plot_example_ingest_pnnl",
    ),
}
