from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import click
from pathlib import Path
from tqdm import tqdm
import os


@click.group()
def pdfmagic():
    """Tool for .pdf manipulation.
    """
    pass


@pdfmagic.command()
@click.argument("inputs", nargs=-1)
@click.option("--outpath", default=None, type=str, help="Path to the output file.")
def merge(inputs, outpath):
    """Merge all pdf files given in INPUTS argument.
    
    INPUTS can be a list of files, in this case, files will be merger in the order they are declared.
    If INPUTS is a folder, all .pdf files inside the folder will be merged, files will be ordered alphabetically.
    """
    
    if len(inputs) == 1 and Path(inputs[0]).is_dir():
        files = sorted(list(inputs[0].glob("*.pdf")))
    else:
        files = [Path(inp) for inp in inputs]
    if outpath is None:
        outpath = " ".join([path.stem for path in files]) + "_merged.pdf"

    output = PdfFileMerger()
    for pdfpath in tqdm(files):
        output.append(PdfFileReader(str(pdfpath)))

    output.write(str(outpath))


@pdfmagic.command()
@click.argument("file")
@click.argument("pages", type=str, nargs=-1)
@click.option("--outpath", default=None, type=str, help="Path to the output file.")
def extract(file, pages, outpath):
    """Extract input page numbers from .pdf (page numbers start on 1).
    
    PAGES: can be a number, e.g. 6 or a range, e.g. 1-9.
    """

    pospages = []
    for pg in pages:
        pre = [p.strip() for p in pg.split('-')]
        if len(pre) == 1:
            pospages.append(int(pre[0]))
        elif len(pre) == 2:
            assert int(pre[0]) < int(pre[1]), "the first page in the range should be a lower number than the second"
            pospages.extend(list(range(int(pre[0]), int(pre[1] + 1))))
        else:
            raise ValueError(f"Invalid page {pg} specification.")
    
    pdf = PdfFileReader(file)
    if max(pospages) > pdf.getNumPages():
        raise ValueError(f"File {file} has only {pdf.getNumPages()} pages.")

    output = PdfFileWriter()

    for page in pospages:
        output.addPage(pdf.getPage(page - 1))

    if outpath is None:
        outpath = (
            os.path.splitext(file)[0] + "_" + ",".join([str(p) for p in pospages]) + ".pdf"
        )
    print(outpath)
    with open(outpath, "wb") as f:
        output.write(f)

