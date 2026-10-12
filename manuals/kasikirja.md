# Geopro 202S Käsikirja

A transcription of `Geopro 202S Käsikirja.pdf` (in this folder). Each PDF page starts at an anchor `#sN`, where N is the PDF page index counted from 1; in the Käsikirja it equals the printed page number. [ADR 0006](../docs/adr/0006-manuals-are-markdown-transcriptions.md) sets the other conventions: figures, screens, key icons, what's left out, and the **Repo note** blocks the repo adds.

Transcribed so far: pp. 21–23. The other pages follow in #81 and #82; until then `geopro-202s-manual.md` paraphrases them.

---

<a id="s21"></a>

## Sivu 21: MAALÄMMITYSTOIMINNOT

### ASETUSARVOT, käyttäjätaso

| Asetusarvo: | Tehdasasetus: | Asettelualue: | Merkitys: |
|---|---|---|---|
| VaraajaAlaMin | 30°C | 30...55°C | Varaajan alaosan minimilämpötila (Maalämpökojeelta lähtevän lämmitysveden minimilämpötila) |
| SV_viiveaika | 30m | 0...120min | Varaajan keskiosa (mittaus 4) voi kytkeä lämpötilan mukaan sähkövastuksen päälle vasta, kun kompressori on ollut käynnissä tässä asetetun ajan (min) |
| Var.ylä kesä | 55°C | 30...75°C | Varaajan yläosan asetusarvo ulkolämpötilan ollessa ≥ +20°C. |
| Var.ylä talvi | 65°C | 30...75°C | Varaajan yläosan asetusarvo ulkolämpötilan ollessa ≤ -20°C. |
| VaraajaYlä: | Laskennallinen | | "Var.ylä kesä" ja "Var.ylä talvi" asetusarvojen mukaan määraytyvä varaajan yläosan lämpötila (ks. kuva). |
| Lisälämmitys | 50°C | 40...55°C | Lisälämpöpainikkeen painaminen asettaa varaajan alaosan minimin asetusarvoksi ko. asetusarvon |
| Lisäläm.aika | 2h | 0...6h | "Lisälämmitys"- asetusarvo on voimassa tässä aseteltavan ajan |

![Varaajan yläosan lämpötilakäyrä](kasikirja/s21-varaajayla-kayra.png)

Kuvan kuvaus: kaavio "Varaajan yläosan lämpötilakäyrä". Pystyakseli on varaajan yläosan lämpötila, °C (asteikko 50, 55, 60, 65, 70), vaaka-akseli ulkolämpötila, °C (asteikko -25 … 25). Käyrä on vaakasuora 65 °C:ssa ulkolämpötilan ollessa -20 °C tai alle, laskee suorana viivana -20 °C:sta +20 °C:seen ja on vaakasuora 55 °C:ssa +20 °C:sta ylöspäin. Lukemat 65, 55, -20 ja 20 on merkitty punaisella ja katkoviivoilla, eli kuva käyttää Var.ylä talvi- ja Var.ylä kesä -tehdasasetuksia.

### ASETUSARVOT, huoltotila

| Asetusarvo: | Tehdasasetus: | Asettelualue: | Merkitys: |
|---|---|---|---|
| Kompr.esto | 55°C | 45...55°C | Lämmitysvaraajan alaosan lämpötilan (mittaus 10) ylittäessä tämän asetusarvon pysäytetään kompressori aina, vaikka varaajan yläosa käskisi kompressoria käyntiin. |
| VarYläEroSv | 3 °C | 0...10°C | Sähkövastus käynnistyy, kun varaajan yläosan lämpötila laskee ["VaraajaYläEro" + "VaraajaYläEroSv"] lämpötilan verran alle laskennallisen "VaraajaYlä " asetusarvon. |
| VaraajaAlaEro | 5 °C | 3...7 °C | Varaajan alaosan lämmityksen ohjauksen eroalue |
| VaraajaYläEro | 3°C | 3...10°C | Varaajan yläosan lämmityksen ohjauksen eroalue |
| JV Esiavaus | 40% | 25...100% | Jakoventtiilin esiavauksen määrä. Esiavaus suoritetaan ennen sähkövastuksen päällekytkemistä |
| JV Esto | 60s | 30...240s | Jakoventtiilin kiinniajon eston kestoaika. Kiinniajon esto aloitetaan sähkövastuksen päällekytkemisestä |
| Maaliuos häl | -6 | -10...0°C | Hälytys maalämpökoneelta palaavan maaliuoksen alilämmöstä |

> **Repo note:** the Merkitys text of VarYläEroSv calls the setting "VaraajaYläEroSv"; the menu label is VarYläEroSv. Maaliuos häl's factory value has no unit; its range is in °C.

> **Repo note:** p. 26 swaps the factory values of VaraajaAlaEro and VaraajaYläEro (3 °C and 5 °C). The factory-reset list on p. 29 agrees with this page. [`docs/controller.md`](../docs/controller.md#factory-values-that-contradict-each-other) has what the Controller held.

### OHJAUSTAVAT:

```
ML Ohjaustavat
▶● Kompr.+sähköv.
   Kompressori
   Sähkövastus
```

**Maalämmityksen säätöpiirin (ML) ohjaustavat:**

Voit siirtyä maalämmityksen säätöpiiriin (ML) [Ryhmänvaihto] -näppäimen avulla.

**Kompressori + sähkövastus:**
Jos maalämpö ei riitä, kytkeytyy sähkövastus päälle.

**Kompressori:**
Varaajan lämmitys tapahtuu vain maalämmöllä (ei käytetä sähkövastuksia).

**Sähkövastus:**
Varaajan lämmitys tapahtuu ainoastaan sähkövastuksella.

---

<a id="s22"></a>

## Sivu 22: MAALÄMMITYSTOIMINNOT

![Maalämpöjärjestelmän periaatekuva](kasikirja/s22-maalampojarjestelma.png)

Kuvan kuvaus: periaatekuva maalämpöjärjestelmästä. Säädin on ylhäällä, ja siitä lähtee johdot antureille, venttiileille ja laitteille. Katkoviivalla piirretyt osat ovat valinnaisia.

- Lisälämpöpainike on kytketty säätimeen. Ulkoanturi M1 on talon seinässä.
- Maapiiri: maanpinnan alla oleva maaputkisto nousee kompressorin luo. Anturi M8 on maapiirin putkessa kompressorin vieressä.
- Kylmäainepiiri: kompressorilta piiri kulkee tulistimen (Tulistin) ja lauhduttimen (Lauhdutin) kautta takaisin kompressorille.
- Lauhduttimen vesipuoli: pumppu ottaa vettä varaajan alaosasta ja syöttää sen lauhduttimeen. Lauhduttimen yhde on yhdistetty jakoventtiiliin JV. JV:n kaksi muuta yhdettä ovat tulistimelle ja varaajan keskiosaan. Tulistimelta linja kulkee sähkövastuksen S1 ("Sähkövastus") ja anturin M7 kautta varaajan yläosaan.
- Varaaja: anturit M9 (yläosa), M4 (keskiosa) ja M10 (alaosa). Sähkövastus S2 on varaajan alaosassa ("Sähkövastus" varaajan alla).
- Varaajan läpi kulkee kaksiosainen kierukka. Kylmä vesi -linja tulee alempaan kierukkaan M4:n korkeudelle, ja kierukka jatkuu ylempään kierukkaan varaajan yläosassa. Ylemmän kierukan lähtö menee katkoviivalla rajatun alueen kolmitieventtiiliin, johon tulee myös kylmä vesi.
- L1 menovesi: varaajan oikealta sivulta lähtevä linja kulkee moottoroidun kolmitieventtiilin ja anturin M2 kautta lämmitysverkostoon. Paluulinja tulee lämmitysverkostosta pumpun kautta varaajan alaosaan, ja kolmitieventtiilin kolmas yhde on yhdistetty paluulinjaan.
- L2 menovesi on piirretty katkoviivalla samalla tavalla, anturina M5.

Huom! Varaajan keskianturin (M4) rikkoontuessa säädin käyttää ohjaavana anturina varaajan alaosan anturia (M10) ja päinvastoin.

> **Repo note:** the figure shows no flow direction on the JV's ports. [`docs/controller.md`](../docs/controller.md#jv) has the flow the owner confirmed for this unit.

### Esimerkki 1.

Maalämpökojeen ohjaus varaajan yläosan lämpötilan (mittaus 9) mukaan, kun "VaraajaYlä" asetusarvoksi on asetettu + 70°C ja ohjauksen eroalueeksi 5°C (VaraajaYläEro).

![Esimerkki 1: ohjaus mittauksen 9 mukaan](kasikirja/s22-esimerkki-1.png)

Kuvan kuvaus: kaavio, jossa on mittaus 9 (sininen käyrä) ajan funktiona. Vaakaviivat ovat 70 °C ("VaraajaYlä" asetusarvo, vihreä), 65 °C ("VaraajaYlä" asetusarvo - "VaraajaYläEro", vihreä) ja 62 °C ("VaraajaYlä" as.arvo - "VaraajaYläEro" - 3°C, punainen). Ensin mittaus 9 laskee 65 °C:seen: kompressori käynnistyy ("Kompressori on käynnissä") ja pysähtyy, kun mittaus 9 nousee 70 °C:seen. Toisella kerralla kompressori käynnistyy taas 65 °C:ssa, mutta mittaus 9 laskee edelleen alle 62 °C:n, jolloin sähkövastus menee päälle ("Sähkövastus on päällä"). Kompressori ja sähkövastus pysähtyvät yhtä aikaa, kun mittaus 9 nousee 70 °C:seen.

### Esimerkki 2.

Maalämpökojeen ohjaus varaajan alaosan lämpötilan mukaan (mittaus 10) ja varaajan keskiosan lämpötilan mukaan (mittaus 4), kun säätimen määräämä L1 menoveden lämpötila on +28 °C ja ohjauksen eroalueeksi (VaraajaAlaEro) on asetettu 3°C. (Käyntikäskyt annetaan mittauksen 4 perusteella ja poistetaan mittauksen 10 perusteella).

![Esimerkki 2: ohjaus mittausten 4 ja 10 mukaan](kasikirja/s22-esimerkki-2.png)

Kuvan kuvaus: kaavio, jossa on mittaus 4 (sininen käyrä) ja mittaus 10 (punainen käyrä) ajan funktiona. Vaakaviivat ja niiden selitteet:

| °C | Selite vasemmalla | Selite viivalla |
|---|---|---|
| 33 | Säätimen määrämä L1 menoveden lämpöt. + 5 °C | Kompressorin pysäytysraja |
| 31,5 | Säätimen määrämä L1 menoveden lämpöt. +5 °C - puolet "VaraajaAlaEro" | Sähkövastuksen pysäytysraja |
| 30 | Säätimen määrämä L1menoveden lämpöt. + 5 °C - "VaraajaAlaEro" | Kompressorin käynnistysraja |
| 29 | Säätimen määrämä L1menoveden lämpöt. + 5 °C - "VaraajaAlaEro"-1 | Sähkövastuksen käynnistysraja |

Ensimmäisellä kerralla mittaus 4 laskee 30 °C:seen ja kompressori käynnistyy ("Kompressori on käynnissä"). Mittaus 4 ei laske 29 °C:seen, joten sähkövastus ei mene päälle. Kompressori pysähtyy, kun mittaus 10 nousee 33 °C:seen. Toisella kerralla kompressori käynnistyy taas, kun mittaus 4 laskee 30 °C:seen, ja mittaus 4 laskee edelleen alle 29 °C:n. Sähkövastus menee päälle vasta, kun kompressorin käynnistyksestä on kulunut "SV_viiveaika" (merkitty pystysuoraan kompressorin käynnistyksen ja sähkövastuksen käynnistyksen väliin). Sähkövastus menee pois, kun mittaus 10 nousee 31,5 °C:seen, ja kompressori pysähtyy, kun mittaus 10 nousee 33 °C:seen.

Kaavion tekstit:

Huom! Sähkövastus kytkeytyy päälle vasta "SV_viiveaika" -ajan kuluttua (tehdasas. 30 min)

\*)Käynnistyy kun edellisestä käyntijaksosta on kulunut väh. 5 min.

Huom! Esimerkissä oletetaan, että säätöpiiri L1 pyytää ylintä lämpötilaa, jolloin ohjaus on esitetty L1:n mukaan. Jos L2 tai "VaraajaAlaMin" edellyttävät ylempää lämpötilaa kuin L1, tapahtuu ohjaus niiden perusteella.

> **Repo note:** VaraajaYläEro 5 °C and VaraajaAlaEro 3 °C are the examples' own settings; [`docs/controller.md`](../docs/controller.md#factory-values-that-contradict-each-other) has the factory values. The asterisk of the 5-minute footnote isn't attached to anything in the chart; p. 23 states the same wait for a start on mittaus 4.

---

<a id="s23"></a>

## Sivu 23: MAALÄMMITYSTOIMINNOT

### KOMPRESSORIN KÄYNNIN OHJAUS:

- **Kompressori käynnistyy varaajan yläosan perusteella, kun:**
  **mittaus 9** alittaa asetusarvon "VaraajaYlä" - "VaraajaYläEro".

- **Kompressori pysähtyy varaajan yläosan perusteella, kun:**
  **mittaus 9** ylittää asetusarvon "VaraajaYlä".

- **Kompressori käynnistyy varaajan alaosan perusteella, kun:**
  edellisestä kompressorin käyntijaksosta on kulunut vähintään 5 minuuttia **ja mittaus 4** alittaa jonkin seuraavista asetusarvoista:
  - säätimen määräämä menoveden lämpötila L1 + 5°C - "VaraajaAlaEro" tai
  - säätimen määräämä menoveden lämpötila L2 + 5°C - "VaraajaAlaEro" tai
  - "VaraajaAlaMin" tai
  - "Lisälämmitys", mikäli lisälämmityspainiketta on painettu.

- **Lisälämpöpainike:** painikkeen painaminen vaihtaa varaajan alaosan asetusarvon "VaraajaAlaMin" asetusarvoksi "Lisälämmitys". Lisälämmitysasetusarvo on voimassa määriteltävän ajan "Lisäläm.aika".

- **Kompressori pysähtyy varaajan alaosan perusteella, kun:**
  **mittaus 10** ylittää seuraavat asetusarvot:
  - säätimen määräämä menoveden lämpötila L1 + 5°C ja
  - säätimen määräämä menoveden lämpötila L2 + 5°C ja
  - "VaraajaAlaMin" + "VaraajaAlaEro" ja
  - "Lisälämmitys" + "VaraajaAlaEro", mikäli lisälämmityspainiketta on painettu.

- **Kompressori pysäytetään aina, kun:**
  **mittauksen 10 lämpötila nousee "Kompr.esto" lämpötilaan.** (Tämän pysäytyksen jälkeen kompressori voi käynnistyä uudelleen vasta kun mittaus 10:n lämpötila on laskenut asetusarvon "VaraajaAlaEro" verran alle "Kompr.esto" lämpötilan).

- **Kompressori ei voi käynnistyä, jos:**
  - mittaus 10 on yli "Kompr.esto" lämpötilan tai
  - valikosta on valittu maalämmityksen ohjaustavaksi "Sähkövastus", tällöin kompressorin ohjaus muutetaan sähkövastuksen ohjaukseksi tai
  - kompressorin käyntitietohälytys (pressostaattihälytys) on aktiivinen.

### SÄHKÖVASTUKSEN OHJAUS:

- **Sähkövastus menee päälle varaajan yläosan perusteella, kun:**
  **mittaus 9** alittaa asetusarvon "VaraajaYlä" - "VaraajaYläEro" - "VarYläEroSv".

- **Sähkövastus kytkeytyy pois päältä varaajan yläosan perusteella, kun:**
  **mittaus 9** ylittää asetusarvon "VaraajaYlä".

- **Sähkövastus menee päälle varaajan alaosan perusteella, kun:**
  kompressorin ohjaus on ollut päällä "SV-viiveaika"-asetusarvon ajan ja **mittaus 4** alittaa jonkin seuraavista asetusarvoista:
  - säätimen määräämä menoveden lämpötila L1 + 5°C - "VaraajaAlaEro" - 1°C tai
  - säätimen määräämä menoveden lämpötila L2 + 5°C - "VaraajaAlaEro" - 1°C tai
  - "VaraajaAlaMin" - 1°C tai
  - "Lisälämmitys"- 1°C, mikäli lisälämmityspainiketta on painettu.

- **Sähkövastuksen päällekytkemisen ennakointi:**
  Ennakointi suoritetaan **aina** ennen sähkövastuksen päällekytkemistä. Sähkövastus kytketään päälle vasta kun ennakointi on suoritettu loppuun. Kun sähkövastus halutaan päälle:
  - jakoventtiiliä JV ajetaan pakkoajolla auki asetusarvon "JV Esiavaus" verran, jotta saadaan suurempi vesivirtaama sähkövastukselle ja estetään sähkövastuksen ylikuumeneminen
  - sähkövastus kytketään päälle
  - estetään jakoventtiilin ajo kiinni-suuntaan asetusarvolla "JV esto" määriteltäväksi ajaksi.

- **Huom! Jakoventtiilin JV ohjaus tapahtuu mittauksen 7 perusteella; asetusarvo on "VaraajaYlä" + 5°C.**

- **Sähkövastus kytkeytyy pois päältä varaajan alaosan perusteella, kun:**
  **mittaus 10** ylittää seuraavat asetusarvot:
  - säätimen määräämä menoveden lämpötila L1 + 5°C - 1/2 \* "VaraajaAlaEro" ja
  - säätimen määräämä menoveden lämpötila L2 + 5°C - 1/2 \* "VaraajaAlaEro" ja
  - "VaraajaAlaMin" + 1/2 \* "VaraajaAlaEro" ja
  - "Lisälämmitys" + 1/2 \* "VaraajaAlaEro", mikäli lisälämmityspainiketta on painettu

- **Sähkövastus ei voi mennä päälle, jos:**
  - sähkövastuksen ennakointia ei ole suoritettu loppuun tai
  - valikosta on valittu maalämmityksen ohjaustavaksi "Kompressori", tällöin sähkövastuksen ohjaus muutetaan kompressorin ohjaukseksi.

> **Repo note:** this page writes SV_viiveaika (p. 21) as "SV-viiveaika" and JV Esto as "JV esto".
