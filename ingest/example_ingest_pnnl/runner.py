from ingest.example_ingest_pnnl import CustomPipeline
from utils import expand, set_env


if __name__ == "__main__":
    set_env()
    pipeline = CustomPipeline(
        expand("config/pipeline_config_example_ingest_pnnl.yml", __file__),
        expand("config/storage_config_example_ingest_pnnl.yml", __file__),
    )
    pipeline.run(expand("tests/data/input/data.csv", __file__))
