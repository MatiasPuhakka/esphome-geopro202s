# Transcribing a manual page

How one PDF page in `manuals/` becomes its section of the transcription, such as `manuals/kasikirja.md` for the Käsikirja. [ADR 0006](../adr/0006-manuals-are-markdown-transcriptions.md) sets the format: the page anchor, what's left out, figures, screens, tables and **Repo note** blocks. This page covers getting the text and figures out of the PDF and checking the result against it.

The two tools read the PDF with PDFKit, so they need macOS. Each prints its usage when run without arguments. Page numbers count the PDF's pages from 1, so page N is the anchor `#sN`. The Käsikirja prints "CoreGraphics PDF has logged an error" on stderr whenever it is opened; the output is still complete.

## 1. Render the page

```sh
tools/pdf_png.js "manuals/Geopro 202S Käsikirja.pdf" .scratch/pages 3 22
```

This writes `.scratch/pages/page-22.png` and prints its path and size, 1785x2526 for an A4 page at scale 3. Keep renders under `.scratch/`, which git ignores. Scale 3 is enough to read the Käsikirja and to crop its figures. The Asennusohje's wiring drawings, from p. 20 on, need scale 6 for their terminal numbers.

View the whole render. A viewer may scale a page this size down: Claude Code's Read tool shows a scale-3 A4 page at 1413x2000 and says to multiply its coordinates by 1.26. Read small print from a crop (step 3) instead of the full view.

## 2. Print the text

```sh
tools/pdf_text.js "manuals/Geopro 202S Käsikirja.pdf" 22
```

This prints the page's text layer under `===== PAGE 22 / 44 =====`. A range such as `21-23` prints each page under its own marker, and a page with no text prints `(no text layer)`.

Copy the words from the text layer, so the transcription keeps the printed spelling and its typos, and take everything else from the render. The text layer:

- runs in the order the PDF drew it, so a table comes out column by column and a chart's labels land among the paragraphs around it.
- splits and reorders characters: on p. 21 the printed 65°C came out as `5°` and `6C` on separate lines, and ≥ and ≤ as `>` and `<`.
- holds the page furniture that ADR 0006 leaves out, such as the doubled banner `Geopro 202SGeopro 202S`, the page number and the key legend.
- lacks text drawn inside images. None of the labels on the Asennusohje's drawings, pp. 20–24, are in it, so they come from the render.

## 3. Crop each figure

Crop every figure, chart and drawing that ADR 0006 says becomes an image. Its caption and any text the transcription holds as text stay out of the crop.

1. Find the figure's box in the render: left x, top y, width and height in the render's pixels. Measured on a scaled-down view, multiply each by the view's factor.
2. Crop it with `sips`, which takes the height before the width and y before x:

   ```sh
   sips -c <height> <width> --cropOffset <y> <x> .scratch/pages/page-22.png --out manuals/kasikirja/s22-esimerkki-1.png
   ```

3. A drawing printed sideways, such as the Asennusohje's p. 20, gets turned upright: `sips -r 90 <file>` turns it 90° clockwise.

A crop goes in the folder named after its transcription, under the page anchor and the figure's name in lowercase ASCII with hyphens, such as `manuals/kasikirja/s22-esimerkki-1.png`.

To read small print, crop the area the same way from a scale-6 render into `.scratch/` and view the crop.

## 4. Write the page

Write the page's section of the transcription in the format ADR 0006 sets, each crop followed by its description.

## 5. Check against the render

The page is done when all three checks pass:

- **Each crop.** View it. Its edges cut nothing off the figure (a label, an axis title, an arrowhead) and hold no text the transcription already has. Fix a failing crop with a new box from step 3.
- **The transcription.** Go down the render from top to bottom and find each heading, paragraph, table row, screen, figure and note in the transcription, in the same order. Check every number, unit and symbol against the render.
- **The links.** `make check-manual-links` passes.
