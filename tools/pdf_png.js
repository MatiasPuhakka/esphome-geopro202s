#!/usr/bin/osascript -l JavaScript
// Renders some pages of a PDF to PNG files, page N to <outdir>/page-N.png with N counted from 1,
// and prints each file's path and pixel size. macOS only: it reads the PDF with PDFKit.
ObjC.import('AppKit');
ObjC.import('PDFKit');
ObjC.import('stdlib');

const USAGE = `usage: tools/pdf_png.js <pdf> <outdir> <scale> <page>...
<scale> is pixels per PDF point: an A4 page is 595 x 842 points, 1785 x 2526 pixels at scale 3.
Each <page> is a page (22) or a range of pages (21-23).`;

// osascript writes console.log to stderr.
function fail(message, status = 1) {
  console.log(message);
  $.exit(status);
}

// The pages the arguments name, in order. tools/pdf_text.js reads its pages the same way.
function pageNumbers(args) {
  const pages = [];
  for (const arg of args) {
    const match = /^(\d+)(?:-(\d+))?$/.exec(arg);
    const first = match && Number(match[1]);
    const last = match && Number(match[2] || match[1]);
    if (!match || first < 1 || last < first) fail(`${USAGE}\n${arg} is not a page or a range`, 2);
    for (let page = first; page <= last; page++) pages.push(page);
  }
  return pages;
}

function run(argv) {
  if (argv.length < 4) fail(USAGE, 2);
  const [path, outdir, scaleArg, ...args] = argv;
  const scale = Number(scaleArg);
  if (!(scale > 0)) fail(`${USAGE}\n${scaleArg} is not a scale`, 2);
  const pages = pageNumbers(args);
  const doc = $.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(path));
  if (doc.isNil()) fail(`can't open ${path} as a PDF`);
  const count = doc.pageCount;
  const outside = pages.find((page) => page > count);
  if (outside) fail(`page ${outside} is outside the PDF's ${count} pages`);

  $.NSFileManager.defaultManager.createDirectoryAtPathWithIntermediateDirectoriesAttributesError(outdir, true, $(), $());
  const out = [];
  for (const page of pages) {
    const pdfPage = doc.pageAtIndex(page - 1);
    const box = pdfPage.boundsForBox($.kPDFDisplayBoxMediaBox);
    const size = $.NSMakeSize(Math.round(box.size.width * scale), Math.round(box.size.height * scale));
    const image = pdfPage.thumbnailOfSizeForBox(size, $.kPDFDisplayBoxMediaBox);
    const bitmap = $.NSBitmapImageRep.imageRepWithData(image.TIFFRepresentation);
    const png = bitmap.representationUsingTypeProperties($.NSBitmapImageFileTypePNG, $());
    const file = `${outdir}/page-${page}.png`;
    if (!png.writeToFileAtomically(file, true)) fail(`can't write ${file}`);
    out.push(`${file} ${bitmap.pixelsWide}x${bitmap.pixelsHigh}`);
  }
  return out.join('\n');
}
