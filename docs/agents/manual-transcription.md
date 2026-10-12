# Transcribing a manual page

How one PDF page in `manuals/` becomes its section of the transcription, such as `manuals/kasikirja.md` for the Käsikirja. [ADR 0006](../adr/0006-manuals-are-markdown-transcriptions.md) sets the format: the page anchor, what's left out, figures, screens, tables and **Repo note** blocks. This page covers getting the text and figures out of the PDF and checking the result against it.

The two tools read the PDF with PDFKit, so they need macOS. Each prints its usage when run without arguments. Page numbers count the PDF's pages from 1, so page N is the anchor `#sN`. Printing the text of the Käsikirja's p. 18 also logs "CoreGraphics PDF has logged an error" on stderr; the page's text is still complete.

## 1. Render the page

```sh
tools/pdf_png.js "manuals/Geopro 202S Käsikirja.pdf" .scratch/pages 3 22
```

This writes `.scratch/pages/page-22.png` and prints its path and size, 1785x2526 for an A4 page at scale 3. Keep renders under `.scratch/`, which git ignores. Scale 3 is enough to read the Käsikirja and to crop its figures.

View the whole render. A viewer may show a page this size scaled down, as Claude Code's Read tool does, and say which factor maps its coordinates back to the render's pixels. Small print, such as the terminal numbers on the Asennusohje's wiring drawings from p. 20 on, needs a scale-6 render: crop the area from it into `.scratch/` the way step 3 crops a figure, and view the crop.

## 2. Print the text

```sh
tools/pdf_text.js "manuals/Geopro 202S Käsikirja.pdf" 22
```

This prints the page's text layer under `===== PAGE 22 / 44 =====`. A range such as `21-23` prints each page under its own marker, and a page with no text prints `(no text layer)`.

Copy the words from the text layer, which keeps the spelling as printed, and take everything else from the render. The text layer:

- runs in the order the PDF drew it, so a table comes out column by column and a chart's labels land among the paragraphs around it.
- splits and reorders characters: on p. 21 the printed 65°C came out as `5°` and `6C` on separate lines, and ≥ and ≤ as `>` and `<`.
- holds the page furniture that ADR 0006 leaves out, such as the doubled banner `Geopro 202SGeopro 202S`, the page number and the key legend.
- lacks text drawn inside images. None of the labels on the Asennusohje's drawings, pp. 20–23, are in it, so they come from the render.

## 3. Crop each figure

Crop every figure, chart and drawing that ADR 0006 says becomes an image, with the file name and the bounds the ADR sets.

1. Find the figure's box in the render: left x, top y, width and height in the render's pixels. Measured on a scaled-down view, multiply each by the view's factor.
2. Crop it with `sips`, which takes the height before the width and y before x:

   ```sh
   sips -c <height> <width> --cropOffset <y> <x> .scratch/pages/page-<N>.png --out manuals/<transcription>/s<N>-<name>.png
   ```

   `sips` reads `--cropOffset 0 0` as no offset and crops the middle of the image, so a box at the top-left corner starts at `1 1`.

3. A drawing printed sideways, such as the Asennusohje's p. 20, gets turned upright: `sips -r 90 <file>` turns it 90° clockwise.

## 4. Write the page

Write the page's section of the transcription in the format ADR 0006 sets.

## 5. Check against the render

The page is done when all three checks pass:

- **Each crop.** View it. Its edges cut nothing off the figure (a label, an axis title, an arrowhead) and hold no text the transcription already has. Fix a failing crop with a new box from step 3.
- **The transcription.** Go down the render from top to bottom and find each heading, paragraph, table row, screen, figure and note in the transcription, in the same order. Check every number, unit and symbol against the render.
- **The links.** `make check-manual-links` passes.
