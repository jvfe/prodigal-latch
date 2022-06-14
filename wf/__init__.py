"""
Predict protein-coding genes with prodigal
"""

import subprocess
from pathlib import Path
from typing import Annotated

from flytekit.core.annotation import FlyteAnnotation
from latch import small_task, workflow
from latch.types import LatchDir, LatchFile


@small_task
def predict_genes(fasta: LatchFile, sample_name: str, output_format: str) -> LatchDir:

    # A reference to our output.
    output_dir = Path("prodigal/{sample_name}/").resolve()

    output_file = output_dir.joinpath(f"{sample_name}.{output_format}")
    output_proteins = output_dir.joinpath(f"{sample_name}.faa")
    output_genes = output_dir.joinpath(f"{sample_name}.fna")
    output_scores = output_dir.joinpath(f"{sample_name}.cds")

    _prodigal_cmd = [
        "/root/prodigal",
        "-i",
        fasta.local_path,
        "-o",
        str(output_file),
        "-a",
        str(output_proteins),
        "-d",
        str(output_genes),
        "-s",
        str(output_scores),
    ]

    subprocess.run(_prodigal_cmd)

    return LatchDir(str(output_dir), f"latch:///{output_dir}")


@workflow
def assemble_and_sort(
    fasta: LatchFile,
    sample_name: str = "prodigal_sample",
    output_format: Annotated[
        str,
        FlyteAnnotation(
            {
                "rules": [
                    {
                        "regex": "(gbk|gff|sco)$",
                        "message": "Only gbk, gff or sco extensions are valid",
                    }
                ]
            }
        ),
    ] = "gbk",
) -> LatchFile:
    """Predict protein-coding genes with Prodigal

    Prodigal
    ----

    __metadata__:
        display_name: Prodigal (Gene prediction software)
        author:
            name: João Vitor Cavalcante
            email:
            github: https://github.com/jvfe/
        repository: https://github.com/jvfe/prodigal-latch
        license:
            id: GPL-3.0

    Args:

        sample_name:
          Sample name (will define output file names).

          __metadata__:
            display_name: Sample name

        fasta:
          Single/multiple FASTA input sequence.

          __metadata__:
            display_name: FASTA

        output_format:
          Specify main output file format (one of gbk, gff or sco).

          __metadata__:
            display_name: Output file format (gbk, gff or sco)

    """
    return predict_genes(
        fasta=fasta, sample_name=sample_name, output_format=output_format
    )
