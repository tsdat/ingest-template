from pathlib import Path
from typing import Any, Dict
import typer
from cookiecutter.main import cookiecutter
from slugify import slugify  # type: ignore


app = typer.Typer(add_completion=False)


@app.command()
def ingest(
    ingest_name: str = typer.Option(
        ...,
        help="A name to give the ingest. This will be used as a title in the ingest's"
        " README file and in the metadata produced by the pipeline.",
        prompt="What name do you want to give this ingest?\n",
    ),
    ingest_location: str = typer.Option(
        ...,
        help="A label for the location where the data are measured.",
        prompt="What label should be used for the location of the ingest? (E.g., PNNL,"
        " San Francisco, etc.)\n",
    ),
    ingest_description: str = typer.Option(
        ...,
        help="A brief description of the ingest that will be used in the ingest's"
        " README file and in the metadata produced by the pipeline.",
        prompt="Briefly describe the ingest\n",
    ),
    use_custom_data_reader: bool = typer.Option(
        False,
        help="Flag to generate boilerplate code for handling inputs stored in a data"
        " format not supported by tsdat out-of-the-box. To see a complete list of"
        " built-in data readers visit"
        " https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/readers",
        prompt="Do you want to use a custom DataReader?\n",
    ),
    use_custom_data_converter: bool = typer.Option(
        False,
        help="Flag to generate boilerplate code to apply custom convertions or other"
        " preprocessing actions to the raw data before it enters the data pipeline. Use"
        " this if the built-in data converters are not sufficient. To see a complete"
        " list of built-in DataConverters visit"
        " https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/converters",
        prompt="Do you want to use a custom DataConverter?\n",
    ),
    use_custom_qc: bool = typer.Option(
        False,
        help="Flag to generate boilerplate code for applying custom quality checks or"
        " corrections to the data. Use this if the built-in QualityCheckers or"
        " QualityHandlers are not sufficient. To see a complete list of "
        " list of built-in QualityCheckers and QualityHandlers visit"
        " https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/qc",
        prompt="Do you want to use a custom QualityChecker or QualityHandler?\n",
    ),
):
    """Ingest cookiecutter wrapper that adds validation and better dynamic defaults."""

    module = slugify(ingest_name, separator="_")
    classname = module.replace("_", " ").title().replace(" ", "")
    location_id = slugify(ingest_location, separator="_")

    if not typer.confirm(
        f"'{module}' will be the module name (the folder created under 'pipelines/') Is"
        " this OK?\n",
        default=True,
    ):
        module = typer.prompt("What would you like to rename the module to?\n")

    if not typer.confirm(
        f"'{classname}' will be the name of your IngestPipeline class (the python class"
        " containing your custom python code hooks). Is this OK?\n",
        default=True,
    ):
        classname = typer.prompt(
            "What would you like to rename the pipeline class to?\n"
        )

    if not typer.confirm(
        f"'{location_id}' will be the short label used to represent the location where"
        " the data are collected. Is this OK?\n",
        default=True,
    ):
        location_id = typer.prompt(
            "What would you like to rename the location identifier to?\n"
        )

    cookiedough: Dict[str, Any] = {
        "ingest_name": ingest_name,
        "ingest_location": ingest_location,
        "ingest_description": ingest_description,
        "use_custom_data_reader": use_custom_data_reader,
        "use_custom_data_converter": use_custom_data_converter,
        "use_custom_qc": use_custom_qc,
        "module": module,
        "classname": classname,
        "location_id": location_id,
    }

    typer.echo(
        "\nGenerating templates/ingest cookiecutter with the following answers:\n"
        f" {cookiedough}\n"
    )

    cookiecutter(
        "templates/ingest",
        no_input=True,
        output_dir="pipelines/",
        extra_context={**cookiedough},
    )

    output_dir = Path("pipelines") / module
    typer.echo(f"Created new ingest pipeline in {output_dir.as_posix()}")


@app.callback()
def callback():
    pass


if __name__ == "__main__":
    app()
