#!/usr/bin/osascript -l JavaScript
// Prints the text layer of some pages of a PDF, each under a marker with its page number, counted
// from 1. macOS only: it reads the PDF with PDFKit.
ObjC.import('PDFKit');
ObjC.import('stdlib');

const USAGE = `usage: tools/pdf_text.js <pdf> <page>...
Each <page> is a page (22) or a range of pages (21-23).`;

// osascript writes console.log to stderr.
function fail(message, status = 1) {
  console.log(message);
  $.exit(status);
}

// The pages the arguments name, in order.
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
  if (argv.length < 2) fail(USAGE, 2);
  const [path, ...args] = argv;
  const pages = pageNumbers(args);
  const doc = $.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(path));
  if (doc.isNil()) fail(`can't open ${path} as a PDF`);
  const count = doc.pageCount;
  const outside = pages.find((page) => page > count);
  if (outside) fail(`page ${outside} is outside the PDF's ${count} pages`);

  const out = [];
  for (const page of pages) {
    const text = ObjC.unwrap(doc.pageAtIndex(page - 1).string) || '';
    out.push(`===== PAGE ${page} / ${count} =====`);
    out.push(text.trim() ? text : '(no text layer)');
  }
  return out.join('\n');
}
