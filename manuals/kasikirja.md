# Geopro 202S Käsikirja

A transcription of `Geopro 202S Käsikirja.pdf` (in this folder). Each PDF page starts at an anchor `#sN`, where N is the PDF page index counted from 1; in the Käsikirja it equals the printed page number. [ADR 0006](../docs/adr/0006-manuals-are-markdown-transcriptions.md) sets the other conventions: figures, screens, key icons, what's left out, and the **Repo note** blocks the repo adds.

---

<a id="s1"></a>

## Sivu 1

*Sivulla ei ole tekstiä kuvan ulkopuolella.*

![Käsikirjan kansi](kasikirja/s1-kansi.png)

Kuvan kuvaus: kansisivu, jonka tekstit ovat osa kuvaa. Ylhäällä on Geopro-logo (vihreä teksti ja vihreä-punainen lehti) ja sen alla tekstit "202S" ja "Käsikirja". Keskellä on valkoinen, kaapin muotoinen maalämpöpumppu, jonka yläkannessa on säätimen näyttö ja näppäimet. Pumpun etuosan päällä on teksti "Maalämpöpumpun ohjaus- ja säätökeskus". Taustalla on aurinkoinen metsä ja nurmirinne. Vasemmalla alhaalla on merkki "PATENTOITU GSM CONTROL". Alareunan harmaassa palkissa on oikealla logo "Geopro by Oilon" ja vasemmalla koodi "202S1.14/0709".

---

<a id="s2"></a>

## Sivu 2

*Sivulla ei ole tekstiä.*

---

<a id="s3"></a>

## Sivu 3: ALUKSI

**Onnittelut erinomaisesta valinnastanne! Olet hankkinut monipuolisen uuden sukupolven asuin- ja liikerakennusten lämmönsäätimen - huipputuotteen joka soveltuu mitä erilaisimpiin käyttökohteisiin ja lämmitysjärjestelmiin.**

**Seuraavaksi esittelemme säätimen ja käyttöohjeen käytön perusperiaatteet.**

### Käyttöpaneeli

![Käyttöpaneeli selitteineen](kasikirja/s3-kayttopaneeli.png)

Kuvan kuvaus: valokuva säätimen käyttöpaneelista: ylhäällä nelirivinen näyttö, sen alla näppäinrivi. Punaiset viivat yhdistävät selitteet näytön ja näppäinten kohtiin. Näytössä lukee:

```
L1 Autom.säätö ▲
 Ulkol.    -12°C
 Menovesi   45°C
>Valinta
```

Näytön oikeassa reunassa on asteikko 80, 65, 50, 35, 20 ja C, alareunassa asteikko 20, 0, -20. Näppäimet vasemmalta oikealle: talon kuvalla merkitty näppäin, pystysuuntainen kaksoisnäppäin (nuolet ylös ja alas), -, OK ja + sekä oikeassa reunassa päällekkäin ESC ja i. Selitteet ja kohdat, joita ne osoittavat:

- "**Säätöpiiritunnus** ilmaisee, että kyseessä on lämmityksen säädin" osoittaa näytön ympyröityä tunnusta L1.
- "Esimerkkikuvassa nähdään säätöpiirin ohjaustapa" osoittaa tekstiä Autom.säätö.
- "**Venttiilimoottorin ohjaustapaa ilmaisevat symbolit.**" osoittaa näytön oikean yläkulman ympyröityä ▲-symbolia. Selitteen alla ovat symbolit ja niiden merkitykset:
  - ▲ Säädin ohjaa 3-tilaohjattua moottoria auki.
  - ▼ Säädin ohjaa 3-tilaohjattua moottoria kiinni.
  - osittain täytetty pylväs: Pylvään korkeus kuvaa jänniteohjatun venttiilimoottorin asentoa.
  - täysi pylväs: Venttiili on täysin auki (100%) ja ohjausjännite on 10 V.
  - tyhjä pylväs (kaksi pystyviivaa): Venttiili on täysin kiinni (0%) ja ohjausjännite on 0 V. 2 V (2 ... 10 V moottori).
- "**Selaus**- näppäimellä >osoitin liikkuu ylös ja alas" osoittaa nuolinäppäintä.
- "**Ryhmänvaihto-** näppäin, jolla pääset säätöpiiristä toiseen. **L1**, lämmityksen säätöpiiiri **L2**, lämmityksen säätöpiiri ja **ML**, maalämmityskojeen ohjauspiiri" osoittaa talon kuvalla merkittyä näppäintä.
- "**Vähennä-**näppäin" osoittaa näppäintä -.
- "**Hyväksy-**näppäin" osoittaa näppäintä OK.
- "**Lisää-**näppäin" osoittaa näppäintä +.
- "**Peruutus**-näppäin, paluu edelliseen näyttöön" osoittaa näppäintä ESC.
- "**INFO**-näppäimellä saat toimintaohjeita tai lisätietoa näyttöön tulevana tekstinä." osoittaa i-näppäintä.

**Huom!** Kun painat + näppäintä oheisessa perusnäyttötilassa, säädin näyttää vuorotellen kaikki mittaustulokset, jonka jälkeen se siirtyy takaisin perusnäyttötilaan.

### Sivun lukeminen:

![Esimerkkisivu ja sen osat](kasikirja/s3-sivun-lukeminen.png)

Kuvan kuvaus: pienennetty esimerkkisivu ASETUSARVOT ja sen vasemmalla puolella aaltosulkeilla merkityt selitteet, jotka nimeävät sivun osat ylhäältä alas:

- "Reitti perusnäytöstä sivun aiheeseen." kattaa sivun yläosan: perusnäytön L1 Autom.säätö ja valikon L1 Valitse, jossa osoitin on kohdassa Asetusarvot. Nuolet yhdistävät näytöt, ja niiden oikealla puolella on TOIMINTAOHJE-teksti.
- "Väripohjalla esitetään sivun varsinainen asia." kattaa vihreäpohjaisen alueen: näytöt L1 Aset.arvot ja ML Aset.arvot sekä ohjeet "Lämmityksen säätöpiirin asetusarvojen muuttaminen:" ja "Maalämmitys:".
- "Lisätietoja käsiteltävästä asiasta." kattaa taulukon TIETOJA ASETUSARVOISTA (sarakkeet Asetusarvo, Tehdasasetus, Vaihteluväli, Merkitys ja Huom!).
- "Näppäinten pikaohjeet." kattaa sivun alareunan rivin, jossa näppäinkuvakkeet ovat selityksineen.

Esimerkkisivun yläreunassa on otsikkopalkki (Geopro 202S, ASETUSARVOT) ja johdantoteksti, alareunassa Geopro-logo ja sivunumero 6.

Muutettavissa olevat arvot on sivulla merkitty **valkoisella**.

> **Repo note:** the sample page is an older version of p. 8, and its values differ: Vent.kesäsulk 25, an extra R1 lämpöraja line, and VaraajaYlä 70 where p. 8 has Var.ylä kesä and Var.ylä talvi. Read p. 8 for the settings.

---

<a id="s4"></a>

## Sivu 4

*Sivulla ei ole tekstiä.*

---

<a id="s5"></a>

## Sivu 5: SISÄLTÖ

### Käyttäjäopas

| | Sivu |
|---|---|
| Säätökäyrien asetukset | 6 |
| Asetusarvot | 8 |
| Mittaukset | 10 |
| Tietoa mittauksista ja anturikytkennöistä | 11 |
| Menovesi-info (menoveden lämpötilan määräytyminen) | 12 |
| Ohjaustavat | 13 |
| Kellotoiminnat | 14 |
| Kielivalinta/Tyyppitiedot | 16 |
| Starttitoiminta | 17 |
| Hälytykset | 18 |
| GSM-toiminnot | 19 |
| Maalämmitystoiminnot | 20 |

![Säätimen käyttö](kasikirja/s5-saatimen-kaytto.png)

Kuvan kuvaus: valokuva, jossa vihreäpuseroinen mies painaa etusormella seinään asennetun sinisen säätimen näppäintä. Säätimen yläpuolelta nousee johtoja, ja sen oikealla puolella on pienempi valkoinen laite.

### Huolto-opas

Näillä sivuilla on ohjeet valtuutetuille Geopro-huoltomiehille. Säätimen huoltotilaan pääseminen on suojattu huoltokoodilla.

#### Huolto

| | Sivu |
|---|---|
| Ohjeet huoltotilaan siirtymisestä | 24 |
| Viritysarvot | 25 |
| Huoltotilan asetusarvot | 26 |
| Trendit | 27 |
| Moottorivalinta | 28 |
| Jakoventtiilin ohjaustapa | 28 |

#### Erikoishuolto

| | Sivu |
|---|---|
| Tehdasasetusten palautus | 29 |
| Erikoishuoltotilan asetusarvot | 30 |
| Mittauksen 6 asetus | 31 |
| Tuuli-/ aurinkomittaus | 32 |
| Säätimen liittäminen LON-kenttäväylään | 33 |
| Väylämittaukset | 34 |
| Tekstiviestiyhteys modeemin kautta | 35 |
| Tekstiviestiyhteys väylän kautta | 36 |
| Selainkäyttö | 37 |
| Datayhteys suoraan tietokoneeseen | 38 |

| | Sivu |
|---|---|
| **Huolto-ohje** | 38 |
| **Yleiskykentäohje** | 39 |
| **Lisävarusteet** | 40 |
| **Hakusanat** | 41 |
| **Tekniset tiedot** | 42 |

> **Repo note:** "Yleiskykentäohje" is printed for Yleiskytkentäohje, the general wiring guide on p. 39.

---

<a id="s6"></a>

## Sivu 6: SÄÄTÖKÄYRIEN ASETUKSET

![Säätökäyrän kolme asettelupistettä](kasikirja/s6-saatokayra.png)

Kuvan kuvaus: kaareva säätökäyrä, jolla on kolme numeroitua pistettä. Piste 1 on käyrän oikeassa, korkeimmassa päässä, piste 2 keskellä ja piste 3 vasemmassa, matalimmassa päässä. Kunkin pisteen ylä- ja alapuolella on nuoli, eli pistettä voi nostaa ja laskea. Numerot vastaavat alla olevaa luetteloa: piste 1 on ulkolämpötilassa -20 °C, piste 3 ulkolämpötilassa +20 °C.

Tasaisen huonelämmön perusta on juuri oikean muotoinen säätökäyrä. Oikea säätökäyrän muoto riippuu monesta tekijästä. Geopro 202S:ssa voidaan säätökäyrää muokata tarkalleen kiinteistön tarpeita vastaavaksi kolmesta pisteestä;

1. **ulkolämpötilan arvolla - 20 °C**
2. **ulkolämpötilan arvolla 0 °C**
3. **ulkolämpötilan arvolla + 20 °C**

Geopro 202S estää väärän muotoisten säätökäyrien asettamisen. Se tekee korjausehdotuksen automaattisesti.

### TOIMINTAOHJE:

```
L1 Autom.säätö
 Ulkolämpö-15°C
 Menovesi  52°C
▶Valinta
```

Näytön takana on toinen näyttö, josta näkyy vain rivi "L2 Autom.säätö".

Paina **ESC** niin monta kertaa, että näyttö ei enää muutu.
Olet silloin oheisen kuvan mukaisessa "Valinta"-näytössä.
Paina **OK**.
Voit siirtyä säätöpiiristä toiseen (L1, L2, ML) [Ryhmänvaihto] -näppäimen avulla.

```
L1 Valitse
▶Säätökäyrien as
 Asetusarvot
 Mittaukset
 Menovesi-info
 Ohjaustavat
 Kellotoiminnat
 Kieli/ Språk
 Tyyppitiedot
 Starttitoiminta
 Huoltotila
```

Näytössä näkyy neljä riviä kerrallaan; valikon muut rivit on piirretty näytön alapuolelle, ja nuoli niiden vieressä osoittaa alas.

Siirrä osoitin kohtaan "Säätökäyrien as" [Selaus] -näppäimen avulla.

Paina **OK**.

```
L1 Käyrä:
▶-20 = 32°C
   0 = 26°C
 +20 = 19°C
```

Näytössä valkoisella: 32. Tämän ja kahden seuraavan näytön oikeassa reunassa on pieni kuva säätökäyrästä; pystyasteikko on 80, 65, 50, 35, 20 ja vaaka-asteikko 20, 0, -20 °C.

Paina **OK**.
Aseta **-** tai **+** -näppäimellä menoveden lämpötila -20°C ulkolämpötilassa.
Paina **OK**.

```
L1 Käyrä:
 -20 = 32°C
▶  0 = 26°C
 +20 = 19°C
```

Näytössä valkoisella: 26.

Paina **OK**.
Aseta **-** tai **+** -näppäimellä menoveden lämpötila 0°C ulkolämpötilassa.
Paina **OK**.

```
L1 Käyrä:
 -20 = 32°C
   0 = 26°C
▶+20 = 19°C
```

Näytössä valkoisella: 19.

Paina **OK**.
Aseta **-** tai **+** -näppäimellä menoveden lämpötila +20°C ulkolämpötilassa.
Paina **OK**.

Poistu tilasta **ESC**illä.

### KÄYRÄN LUKUOHJE:

```
L1 Käyrä:
▶-20 = 32°C
   0 = 26°C
 +20 = 19°C
```

Näytön oikeassa reunassa on säätökäyrä. Pystyasteikko on 80, 65, 50, 35, 20 ja sen otsikko "Menoveden lämpötila"; vaaka-asteikko on 20, 0, -20 °C ja sen otsikko "Ulkolämpötila". Käyrä nousee vasemmalta oikealle eli ulkolämpötilan laskiessa.

Kun ulkolämpötila on:

- \- 20°C, menovesi on +32°C
- 0°C, menovesi on +26°C
- \+ 20°C, menovesi on +21°C

**Huom!**
Menoveden lämpötila voi poiketa käyrän mukaisesta, jos säätimeen on kytketty yöalennus, huone-, tuuli- tai aurinkokompensointi tai jos jokin rajoitustoiminnoista rajoittaa lämpötilaa (ks. sivu 12).

**Mikäli ulkoanturi ei ole kytketty tai anturi on poikki, säädin olettaa ulkolämmöksi 0°C** (rakennusaikainen käyttö ilman ulkoanturia).

> **Repo note:** the reading guide gives +21°C at +20 °C, but the screen beside it shows +20 = 19°C.

---

<a id="s7"></a>

## Sivu 7: Ohjeita säätökäyrän asetteluun

### ESIMERKKEJÄ ERI LÄMMITYSJÄRJESTELMISTÄ:

a) Lattialämmitys

```
L1 Käyrä:
▶-20 = 32°C
   0 = 26°C
 +20 = 19°C
```

b) Lattialämmitys
(kosteat tilat, L2-piirin tehdasasetus)

```
L2 Käyrä:
▶-20 = 30°C
   0 = 27°C
 +20 = 20°C
```

Kummankin näytön oikeassa reunassa on pieni kuva säätökäyrästä; pystyasteikko on 80, 65, 50, 35, 20 ja vaaka-asteikko 20, 0, -20 °C. L2-käyrä on loivempi kuin L1-käyrä.

**OHJE:**

Jos pakkasella huonelämpö laskee, nosta käyrän asettelua -20°C:ssa.

Jos pakkasella huonelämpö nousee, laske käyrän asettelua -20°C:ssa.

Jos huonelämpö tuntuu kolealta nollakelillä, nosta käyrän asettelua 0°C:ssa.

Tällä tavoin voit asetella säätökäyrän juuri kiinteistösi lämmitystarpeen mukaiseksi.

**Huom!** Odota asetusten muutosten jälkeen riittävän kauan, että muutos ehtii vaikuttaa huonelämpötilaan.

### LATTIALÄMMITYSTALOT:

Aseta säätimen maksimirajoitus välille +35 … +40°C ja minimirajoitus välille +20 … +25°C.

Lattialämmitystaloissa on tärkeä varmistua siitä, että putkistoon ei milloinkaan pääse liian kuumaa vettä, joka saattaisi vaurioittaa rakenteita tai pinnotteita. Menovesiputkeen on asennettava mekaaninen termostaatti, joka pysäyttää kiertovesipumpun ylikuumenemistilanteessa.Tähän tarkoitukseen sopii pintatermostaatti C01A. Asettele termostaatin asetusarvoksi 40 ... 45°C.

![Pintatermostaatti C01A](kasikirja/s7-pintatermostaatti.png)

Kuvan kuvaus: valokuva oranssista, pitkulaisesta pintatermostaatista. Yläpäässä on pyöreä säätönuppi, jossa on merkintä EBERLE ja asteikko 20–90 °C. Alapäässä on musta kaapeliläpivienti ja kyljessä pieni metalliosa.

Pintatermostaatti C01A
vaihtokosketin

AC 250V 15 (2,5) A

| Malli | Alue °C säädett. | Eroalue °C kiinteä | Kotelon lämpötila, °C |
|---|---|---|---|
| CO1A | +20 ...+90 | 7 | -35 ...+120 |

#### Pintatermostaatin C01A kytkentä:

![Pintatermostaatin C01A kytkentä](kasikirja/s7-pintatermostaatin-kytkenta.png)

Kuvan kuvaus: kytkentäkaavio. Alhaalla on kolme riviliitintä, vasemmalta oikealle 2, 1 ja 3. Liittimestä 1 nousee vaihtokoskettimen kieli, joka on piirretty asentoon, jossa se on yhteydessä liittimeen 2; liittimen 3 kosketin on auki. Kosketinta ohjaa lämpötila (θ-merkki). Liittimeen 2 osoittaa alhaalta nuoli, jonka selite on "Pumpun ohjaus- 230 VAC". Liittimestä 1 lähtee alas ja oikealle nuoli, jonka selite on "Pumpun ohjaus".

### AVAINSANAT:

- Säätökäyrät
- L1 Säätökäyrä
- L2 Säätökäyrä

![Säätökäyrien kysely tekstiviestillä](kasikirja/s7-gsm-saatokayrat.png)

Kuvan kuvaus: kaksi kallistettua matkapuhelinta. Ensimmäisen näytössä on viesti "SÄÄTÖKÄYRÄT", ja puhelimesta lähtee poispäin punainen salaman muotoinen katkoviivanuoli. Toisen näytössä on viesti "L1 SÄÄTÖKÄYRÄ: (-20=58; 0=41; +20=19)", jossa luvut 58, 41 ja 19 ovat valkoisella; sen nuolessa on kärki kummassakin päässä.

> **Repo note:** the table writes the model as CO1A, with a letter O; the text and the caption write C01A.

---

<a id="s8"></a>

## Sivu 8: ASETUSARVOT

Geopro 202S:ssa säädintä ohjataan monilla erilaisilla asetusarvoilla. Se, mitä asetusarvoja sinulla on käytössä, riippuu anturikytkennöistä. Selaamalla näet, mitkä asetusarvot sinulla ovat käytössä. Arvojen selaus ja muuttaminen tapahtuvat seuraavasti:

### TOIMINTAOHJE:

```
L1 Autom.säätö
 Ulkolämpö-15°C
 Menovesi  52°C
▶Valinta
```

Näytön takana on kaksi muuta näyttöä, joista näkyy vain reunat: L2 Autom.säätö ja M-kirjaimella alkava ML-näyttö.

Paina **ESC** niin monta kertaa, että näyttö ei enää muutu.
Olet silloin oheisen kuvan mukaisessa "Valinta"-näytössä. Paina **OK**.
Voit siirtyä säätöpiiristä toiseen (L1, L2, ML) [Ryhmänvaihto] -näppäimen avulla.

```
L1 Valitse
 Säätökäyrien as
▶Asetusarvot
 Mittaukset
```

Siirrä osoitin kohtaan "Asetusarvot" [Selaus] -näppäimen avulla. Paina **OK**.

```
 L1 Aset.arvot °C
▶ Huonelämpö 21.5
  Yöalennus v.  0
  Minimiraja   15
  Maksimiraja  70
  Huonekomp.s 4.0
  Tuulikomp.s   0
  Aurinkokomp   0
  Esikorotus    0
  Syyskuivaus   2
  Vent.kesäsulk30
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle. Kaikki arvot on merkitty valkoisella.

**Lämmityksen säätöpiirin asetusarvojen muuttaminen:**

Vie osoitin [Selaus] -näppäimen avulla sen asetusarvon kohdalle, jonka arvoa haluat muuttaa. Paina **OK**.
Muuta asetusarvo **-** tai **+** -näppäimen avulla. Paina **OK**.
Poistu tilasta **ESC**illä.

```
ML Aset.arvot °C
▶VaraajaAlaMin 30
 SV_viiveaika 30m
 Var.ylä kesä 55
 Var.ylä talvi 65
 Lisälämmitys  50
 Lisäläm.aika  2h
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle. Kaikki arvot on merkitty valkoisella; yksiköt m ja h eivät.

**Maalämmitys:**
Siirry ML säätöpiiriin [Ryhmänvaihto] -näppäimen avulla. Paina **OK**.
Muuta arvo **-** tai **+** -näppäimen avulla. Paina **OK**.
Poistu tilasta **ESC**illä.

### TIETOJA ASETUSARVOISTA:

| Asetusarvo: | Tehdasasetus: | Asettelualue: | Merkitys: | Huom! |
|---|---|---|---|---|
| Huonelämpö | 21.5°C | 5...45°C | Käyttäjän asettama huonelämpötilan asetusarvo. Yöalennuksen aikana säädin käyttää laskennallista huonelämmön arvoa. | Laskennallinen huonelämpö= **Huonelämpö - [Yöalenn. määrä / Huonekomp.suhde]** |
| Yöalennus vaikutus *“Yöalennus v.”* | 0°C | 0...35°C | Menoveden lämpötilan pudotuksen määrä, jonka kello-ohjelma tai ulkopuolinen kotona/ poissa kytkin tai GSM-ohjaus kytkee päälle. | |
| Minimiraja | 15°C | 5...95°C | Menoveden alin sallittu lämpötila | |
| Maksimiraja | 70°C | 15...125°C | Menoveden korkein sallittu lämpötila | |
| Huonekompensointisuhde *“Huonekomp.s”* | 4.0°C | 0.0...7.0°C | Mikäli huonelämpötila poikkeaa sille asetetusta asetusarvosta, huonekompensointitoiminta korjaa menoveden lämpötilaa. Esim. jos huonekompensointisuhde on 4 ja huonelämpötila on noussut 1,5°C asetusarvon yläpuolelle, säädin pudottaa menoveden lämpötilaa 6°C (4x1,5°C = 6°C). | **Huoneanturi** (TMR) on oltava kytkettynä (L1: mittaus 3, L2: mittaus 6, tai väylä). |
| Tuulikompensointisuhde *“Tuulikomp.s”* | 0°C | 0...7°C | Tuulisilla ilmoilla talo pyrkii jäähtymään. Silloin tuulikompensointi nostaa menoveden lämpötilaa. Lukuarvo kertoo, kuinka paljon tuulikompensointi voi enimmillään nostaa menoveden lämpötilaa. | **Tuulianturi** on oltava kytkettynä. Tuulimittaus on yhteinen säätöpiireille L1 ja L2 (mittaus 6 tai väylä). |

Huom!-sarakkeen kaavassa Yöalenn. määrä on murtoviivan yläpuolella ja Huonekomp.suhde sen alapuolella.

![Minimiraja ja Maksimiraja](kasikirja/s8-minimiraja-maksimiraja.png)

Kuvan kuvaus: Huom!-sarakkeessa Minimiraja- ja Maksimiraja-rivien kohdalla on kaksi pientä säätökäyrää, kummassakin pystyasteikko 80, 65, 50, 35, 20 ja vaaka-asteikko 20, 0, -20 °C. Ylemmässä käyrä nousee oikealle mutta on vasemmassa päässään vaakasuora noin 20 °C:ssa; nuoli selitteestä "Minimiraja" osoittaa tätä vaakasuoraa osaa. Alemmassa käyrä nousee oikealle ja tasaantuu oikeassa päässään vaakasuoraksi noin 50 °C:ssa; nuoli selitteestä "Maksimiraja" osoittaa tätä vaakasuoraa osaa.

> **Repo note:** the screen shows Aurinkokomp; p. 9 names the setting "Aurinkokomp.s".

---

<a id="s9"></a>

## Sivu 9: Lisätietoja asetusarvoista

| Asetusarvot | Tehdasasetus | Asettelualue: | Merkitys: |
|---|---|---|---|
| Aurinkokompensointisuhde *“Aurinkokomp.s”* | 0 °C | 0...-7 °C | Talossa, jossa on suuret etelänpuoleiset ikkunat, huonelämpötila nousee aurinkoisina päivinä pakkassäälläkin. Lukuarvo kertoo, kuinka paljon aurinkokompensointi voi enimmillään pudottaa menoveden lämpötilaa. **Aurinkoanturi** on oltava kytkettynä. Aurinomittaus on yhteinen säätöpiireille L1 ja L2 (mittaus 6 tai väylä). |
| Esikorotus | 0 °C | 0...20 °C | Yöpudotuksen jälkeen tapahtuva automaattisen esikorotuksen **määrä** asteina. Esikorotuksen ansiosta yöpudotuksen jälkeen saadaan huonelämpö nostettua nopeammin päivälämpöön. Esikorotusajan pituuden asettaa huoltomies (ks. huoltotila sivu 26). |
| Syyskuivaus | 2 °C | 0...15 °C | Syysajan kuivaustoiminnolla nostetaan syksyllä automaattisesti menoveden lämpötilaa 20 vuorokauden ajaksi. Toiminto kytkeytyy päälle, kun **vuorokauden keskilämpö** on yhtäjaksoisesti ollut vähintään 20 vrk:n ajan yli 7°C ja putoaa tämän jälkeen +7°C rajan alapuolelle. Toiminto on päällä niinä seuraavina 20 vrk:na, jolloin vrk:n keskilämpötila on alle 7°C. Syyskuivaus asetusarvo kertoo, kuinka paljon syysajan kuivaustoiminto nostaa menoveden lämpötilaa. Tehtaan alkuasetusarvo on 2°C. |
| Venttiilin kesäsulkeutuminen *”Vent.kesäsulk”* | 30 °C | 5...50 °C | Ulkolämpötilaraja, jossa L1-piirin venttiili sulkeutuu |

![Esikorotus](kasikirja/s9-esikorotus.png)

Kuvan kuvaus: Esikorotus-rivin kaavio. Pystyakselin otsikko on °C, ja vaaka-akselin alle vasemmalle on kirjoitettu "Vrk:n keskilämpö (ulkolämpötila)". Punainen viiva on ensin tasolla "Normaali lämpö", laskee ensimmäisen pystysuoran katkoviivan kohdalla tasolle "Alennettu lämpö = yöalennus" ja nousee toisen katkoviivan kohdalla normaalitason yläpuolelle. Korotettu jakso on väritetty punaiseksi, ja sen pituus toisen ja kolmannen katkoviivan välillä on merkitty kaksoisnuolella "Esikorotusaika (huoltomies asettaa)". Sen jälkeen viiva palaa normaalitasolle. Viivan oikeassa päässä on punainen teksti, josta näkyy vain M-kirjain (tekstikerroksessa "Menovesi"). Keltainen viiva "Huonelämpö" laskee loivasti alennuksen aikana ja nousee esikorotuksen aikana takaisin normaaliksi; laskun ja normaalitason välinen punertava alue on merkitty "Säästetty energia". Nuoli Esikorotus-otsikosta osoittaa korotettua jaksoa.

![Syyskuivaus](kasikirja/s9-syyskuivaus.png)

Kuvan kuvaus: Syyskuivaus-rivin kaavio. Pystyakselille on merkitty 7 °C, josta lähtee vaakasuora katkoviiva; vaaka-akselin otsikko on "Aika / vrk". Keltainen käyrä "Vrk:n keskilämpö käyrä" on alussa 7 °C:n yläpuolella; tämä jakso on merkitty vaaleanvihreällä alueella ja kaksoisnuolella "vähintään 20 vrk:n ajanjakso". Sitten käyrä laskee 7 °C:n alle, käy kahdesti hetken sen yläpuolella ja jää lopulta pysyvästi alle. Punaiset palkit merkitsevät vuorokaudet, joina keskilämpö on alle 7 °C. Ne on numeroitu 1–20 (1 2 3, 4 5 ja 6–20), ja käyrän käynnit 7 °C:n yläpuolella jäävät palkkien väliin rakoina. Palkkien selite on "Syysajan kuivaus - toiminto päällä".

**Maalämmitys:**

| Asetusarvot | Tehdasasetus | Asettelualue: | Merkitys: |
|---|---|---|---|
| VaraajaAlaMin | 30°C | 30...55°C | Varaajan alaosan minimilämpötila (Maalämpökojeelta lähtevän lämmitysveden minimilämpötila) |
| SV_viiveaika | 30m | 0...120min | Varaajan keskiosa (mittaus 4) voi kytkeä lämpötilan mukaan sähkövastuksen päälle vasta, kun kompressori on ollut käynnissä tässä asetetun ajan (min) |
| Var.ylä kesä | 55°C | 30...75°C | Varaajan yläosan asetusarvo ulkolämpötilan ollessa ≥ +20°C. |
| Var.ylä talvi | 65°C | 30...75°C | Varaajan yläosan asetusarvo ulkolämpötilan ollessa ≤ -20°C. |
| VaraajaYlä: | Laskennallinen | | "Var.ylä kesä" ja "Var.ylä talvi" asetusarvojen mukaan määraytyvä varaajan yläosan lämpötila (ks. kuva). |
| Lisälämmitys | 50°C | 40...55°C | Lisälämpöpainikkeen painaminen asettaa varaajan alaosan minimin asetusarvoksi ko. asetusarvon |
| Lisäläm.aika | 2h | 0...6h | “Lisälämmitys”- asetusarvo on voimassa tässä aseteltavan ajan |

![Varaajan yläosan lämpötilakäyrä](kasikirja/s9-varaajayla-kayra.png)

Kuvan kuvaus: kaavio "Varaajan yläosan lämpötilakäyrä", sama kuin sivulla 21. Pystyakseli on varaajan yläosan lämpötila, °C (asteikko 50, 55, 60, 65, 70), vaaka-akseli ulkolämpötila, °C (asteikko -25 … 25). Käyrä on vaakasuora 65 °C:ssa ulkolämpötilan ollessa -20 °C tai alle, laskee suorana viivana -20 °C:sta +20 °C:seen ja on vaakasuora 55 °C:ssa +20 °C:sta ylöspäin. Lukemat 65, 55, -20 ja 20 on merkitty punaisella ja katkoviivoilla, eli kuva käyttää Var.ylä talvi- ja Var.ylä kesä -tehdasasetuksia.

### AVAINSANAT:

- **L1 Asetusarvot**
- **L2 Asetusarvot**
- **ML Asetusarvot**

![Asetusarvojen kysely tekstiviestillä](kasikirja/s9-gsm-asetusarvot.png)

Kuvan kuvaus: kaksi kallistettua matkapuhelinta. Ensimmäisen näytössä on viesti "L1 ASETUSARVOT", ja puhelimesta lähtee poispäin punainen salaman muotoinen katkoviivanuoli. Toisen näytössä on viesti, joka jatkuu näytön reunan yli:

```
L1 Asetusarvot
Huonelämpö=21,5/
Yöalennus =0/
Minimiraja=15/
Maksimiraja=8
Huonekomp.s=0/
Esikorotus=2/
Syyskuivaus=2
```

Viestin luvut ovat valkoisella. Toisen puhelimen nuolessa on kärki kummassakin päässä.

> **Repo note:** the Asennusohje ([p. 16](asennusohje.md#s16)) gives +19 °C as the factory value of the summer closing (Vent.kesäsulk); this page, the screen on p. 8 and the factory list on p. 29 give 30 °C.

---

<a id="s10"></a>

## Sivu 10: MITTAUKSET

Geopro 202S:ssa on yhteensä 14 samanaikaista lämpötilan mittaustietoa (11 NTC- mittausta + 3 digit. tuloa). Säädin voi lukea mittaustietoja myös väylän kautta. Mittausta 6 voi käyttää ulkopuolisten hälytysten ilmaisuun (lisätietoja hälytyksistä sivu 18).
HUOM! **Näytössä esiintyvät vain säätimeen kytketyt mittaukset.**

### TOIMINTAOHJE:

```
L1 Autom.säätö
 Ulkolämpö-15°C
 Menovesi  52°C
▶Valinta
```

Näytön takana on päällekkäin kaksi muuta näyttöä, joista näkyvät vain ylimmät rivit: "L2 Autom.säätö" ja "ML Kompressori".

Paina **ESC** niin monta kertaa, että näyttö ei enää muutu.
Olet silloin oheisen kuvan mukaisessa "Valinta"-näytössä.
Kun painat **+** -näppäintä tässä perusnäyttötilassa, säädin näyttää vuorotellen kaikki mittaustulokset, jonka jälkeen siirtyy takaisin perusnäyttötilaan.
Voit myös mennä "Mittaukset" -näyttöön selaamaan mittaustietoja.
Paina **OK**.

```
L1 Valitse
 Säätökäyrien as
 Asetusarvot
▶Mittaukset
 Menovesi-info
```

Rivi Menovesi-info on piirretty näytön alapuolelle.

Siirrä osoitin kohtaan "Mittaukset" [Selaus] -näppäimen avulla. Paina **OK**.

```
Mittaukset °C
▶L1 Menovesi  52
 L1 Huone   21,2
 Ulkolämpö  -15
 L2 Menovesi  48
 VaraajaYlä   70
 VaraajaKeski 50
 VaraajaAla   40
 Yläosa tulo  72
 Maaliuos      2
 Mittaus6      5
 Kompr.Aika    0
 Sähköv.Aika   0
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle. Näytön vasemmalla puolella on punainen teksti "Vapaasti nimettävissä oleva lämpötilamittaus", ja sen nuoli osoittaa riviä VaraajaKeski.

**Mittausten selaus:**
Voit selata näytössä eri mittaustietoja **+** -näppäimen tai [Selaus] -näppäimen avulla. Mittaukset näytössä esitetään kaikkien säätöpiirien mittaukset.
Poistu "Mittaukset"-näytöstä painamalla **ESC.**

Jokaisella anturilla on oma tyypillinen mittausalueensa (esim. ulkoanturi -50...+50 °C). Jos anturin mittausarvo on tämän alueen ulkopuolella, tulee "Mittaukset"-näyttöön kyseisen anturin mittausarvon paikalle - tai **+** -merkki osoittamaan, onko arvo mittausalueen ala- vai yläpuolella.

Mikäli kyseessä on anturivika, säädin hälyttää (ks. sivu 20) ja mittausarvon paikalla on "**err**".

<table>
<tr><th>Riviliitin</th><th>Mittaus:</th><th>Tietoa mittauksesta:</th><th>Mittausalue</th><th>Huom!</th></tr>
<tr><td>1</td><td>Ulkolämpö</td><td>Ulkolämpötila</td><td>-50...+50</td><td>Luettavissa myös väylältä</td></tr>
<tr><td>2</td><td>L1 Menovesi</td><td>Menoveden lämpötila säätöpiirissä L1</td><td>0...+130</td><td></td></tr>
<tr><td>3</td><td>L1 Huone</td><td>Huonelämpötila säätöp. L1 (huonekomp.)</td><td>-10...+80</td><td>Luettavissa myös väylältä</td></tr>
<tr><td>4</td><td>VaraajaKeski</td><td>Varaajan keskiosan lämpötila</td><td>0...+130</td><td></td></tr>
<tr><td>5</td><td>L2 Menovesi</td><td>Menoveden lämpötila säätöpiirissä L2</td><td>0...+130</td><td></td></tr>
<tr><td>6</td><td>Mittaus 6</td><td>Nimettävissä oleva vapaa lämpötilamittaus</td><td>-10...+80</td><td rowspan="4"><u>Keskenään vaihtoehtoisia</u> (s. 31). Jos tarvitaan useampaa kompensointia, luetaan tieto väylältä, jolloin tuuli on m/s ja valo on lux (s. 34).</td></tr>
<tr><td>6</td><td>L2 Huone</td><td>Huonelämpötila säätöp. L2. (huonekomp.)</td><td>-10...+80</td></tr>
<tr><td>6</td><td>Tuuli</td><td>Tuulen nopeus (% anturin mitta-alueesta)</td><td></td></tr>
<tr><td>6</td><td>Aurinko</td><td>Valon määrä (% anturin mitta-alueesta)</td><td></td></tr>
<tr><td>7</td><td>Yläosa tulo</td><td>Lämpötila tulistimen ja sähkövastuksen jälkeen</td><td>0...+130</td><td></td></tr>
<tr><td>8</td><td>Maaliuos</td><td>Maaliuoksen lämpötila</td><td>-20...+60</td><td></td></tr>
<tr><td>9</td><td>VaraajaYlä</td><td>Varaajan yläosan lämpötila</td><td>0..+130</td><td></td></tr>
<tr><td>10</td><td>VaraajaAla</td><td>Varaajan alaosan lämpötila</td><td>0..+130</td><td></td></tr>
<tr><td></td><td>Kompr.Aika</td><td>Kompressorin yhteenlaskettu käyntiaika tunteina (käyntilaskuri)</td><td>9999</td><td></td></tr>
<tr><td></td><td>Sähköv.Aika</td><td>Sähkövastuksen yhteenlaskettu lämmitysaika tunteina (päälläololaskuri)</td><td>9999</td><td></td></tr>
</table>

> **Repo note:** the red label for the freely nameable measurement points at VaraajaKeski, but the table gives that role to Mittaus 6 (Mittaus6 on the screen).

> **Repo note:** sensor-fault alarms are described on p. 18; p. 20, cited for them here, covers the heat pump's own alarms.

> **Repo note:** p. 42 lists 10 NTC measurements where the intro has 11. Measurement 11 is the compressor's run signal Kompr.käynti (p. 20).

---

<a id="s11"></a>

## Sivu 11: MITTAUKSET Lisätietoja

**Mittaus 6:** Vapaa info-tyyppinen lämpötilamittaus, joka on nimettävissä, tai se voidaan ottaa säätöön vaikuttavaksi mittaukseksi (L2 huone-, tuuli- tai aurinkokompensointi, ks. erikoishuolto, s. 31 - 32).

### MITTAUKSEN 6 UUDELLEEN NIMEÄMINEN:

Siirrä osoitin mittauksen 6 kohdalle . Paina **OK**.

```
Nimen vaihto
▶Mittaus6
 Anna uusi nimi
```

Siirrä osoitin kohtaan "Anna uusi nimi". Paina **OK**.

```
Nimen vaihto
 Mittaus6
▶a
```

Alemmassa näytössä a-kirjain vilkkuu. Näyttöjen vasemmalla puolella on punaisella vinoon kirjoitettuja esimerkkinimiä: Uima-allas, Kellari, Sauna ja Varaaja.

Näytössä on "a"-kirjain. Voit siirtyä merkkijonossa eteen tai taakse päin **+** tai **-** -näppäimellä. Hyväksy kirjain/merkki painamalla **OK**, jolloin seuraavan merkin kohdalla vilkkuu viimeksi valittu merkki. Viimeksi syötetty merkki poistetaan painamalla **ESC**. Mikäli painat pitkään yhtäjaksoisesti **ESC**-näppäintä saadaan uusi nimi poistettua, ja entinen nimi jää voimaan. **Kun olet kirjoittanut nimen, paina pitkään OK:ta** (yli 2 sek.), jolloin päästään pois kirjoitustilasta ja kirjoitettu nimi tulee käyttöön.

**Tekstieditorin merkit esiintymisjärjestyksessä:** "Tyhjä" . - numerot 0 ... 9 kirjaimet A ...Z ja a ... z ä ö å

### ANTUREIDEN KYTKENTÄOHJE:

![Antureiden kytkentäohje](kasikirja/s11-antureiden-kytkentaohje.png)

Kuvan kuvaus: kytkentäkaavio. Vasemmalla ovat anturit ja niiden anturityypit, keskellä kaapeli (2 x 0.8) ja oikealla säätimen riviliitinrima. Kaapelin pää on merkitty tunnuksella T1 … T11, ja sen kaksi johdinta kytketään riviliittimeen, jonka numero on sama kuin mittauksen, sekä sen alla olevaan maaliittimeen (⊥). Liittimien oikealla puolella on mittauksen nimi Mitt.1 … Mitt.11.

| Anturi | Anturityyppi | Kaapeli | Merkintä | Riviliittimet | Mittaus |
|---|---|---|---|---|---|
| Ulkoanturi | TMO | 2 x 0.8 | T1 | 1 ja ⊥ | Mitt.1 |
| L1 Menovesianturi | TMW tai TMS | 2 x 0.8 | T2 | 2 ja ⊥ | Mitt.2 |
| L1 Huoneanturi | TMR | 2 x 0.8 | T3 | 3 ja ⊥ | Mitt.3 |
| Varaajan keskiosan anturi | TMW tai TMS | 2 x 0.8 | T4 | 4 ja ⊥ | Mitt.4 |
| L2 Menovesianturi | TMW tai TMS | 2 x 0.8 | T5 | 5 ja ⊥ | Mitt.5 |
| Vapaa mittaus (Mittaus 6) | TMW tai TMS | 2 x 0.8 | T6 | 6 ja ⊥ | Mitt.6 |
| Yläosan tulolämpöanturi | TME | 2 x 0.8 | T7 | 7 ja ⊥ | Mitt.7 |
| Maaliuosanturi | TMS | 2 x 0.8 | T8 | 8 ja ⊥ | Mitt.8 |
| Varaajan yläosan anturi | TME | 2 x 0.8 | T9 | 9 ja ⊥ | Mitt.9 |
| Varaajan alaosan anturi | TME | 2 x 0.8 | T10 | 10 ja ⊥ | Mitt.10 |
| Kompressorin käyntitieto | katkoviivalla piirretty kosketin | 2 x 0.8 | T11 | 11 ja ⊥ | Mitt.11 |

### Vastusarvot

| °C | Ω |
|---|---|
| -30 | 177 100 |
| -25 | 130 400 |
| -20 | 96 890 |
| -15 | 72 830 |
| -10 | 55 340 |
| -5 | 42 340 |
| 0 | 32 660 |
| 5 | 25 400 |
| 10 | 19 900 |
| 15 | 15 710 |
| 20 | 12 490 |
| 25 | 10 000 |
| 30 | 8 064 |
| 35 | 6 531 |
| 40 | 5 330 |
| 45 | 4 368 |
| 50 | 3 602 |
| 55 | 2 987 |
| 60 | 2 490 |
| 65 | 2 084 |
| 70 | 1 753 |
| 75 | 1 482 |
| 80 | 1 259 |
| 90 | 917 |
| 100 | 680 |
| 110 | 511 |

### ANTUREIDEN KÄYTTÖÖNOTTO JA POISTAMINEN KÄYTÖSTÄ:

Jos ulkoanturi ei ole kytketty, säädin olettaa ulkolämmöksi 0°C ja näytössä on anturivika ilmoitus (ulkolämpö err). Kun ulkoanturi kytketään, säädin ottaa sen käyttöön automaattisesti. **Muiden antureiden lisäämisen tai antureiden poistamisen jälkeen täytyy käydä starttitoiminnassa!** (ks. sivu 17)

### AVAINSANA:

- Mittaukset

![GSM-viestit: Mittaukset](kasikirja/s11-gsm-mittaukset.png)

Kuvan kuvaus: kaksi GSM-puhelinta. Vasemman puhelimen salamanuoli osoittaa puhelimesta poispäin, oikean puhelimen nuolessa on kärki kumpaankin suuntaan. Vasemman puhelimen näytössä on viesti "MITTAUKSET", oikean puhelimen näytössä:

```
MITTAUKSET:
L1Menovesi= 52/
L1Huone= 21.5/
Ulkolämpö=-15/
```

---

<a id="s12"></a>

## Sivu 12: MENOVESI-INFO

Menovesi-infossa nähdään, mistä tekijöistä säätimen määräämä menoveden lämpötila tarkasteluhetkellä muodostuu. Lähtökohtana on säätökäyrän mukainen menoveden lämpötila tämänhetkisellä ulkolämpötilalla. Menovesi-infosta havaitaan myös asetusvirheet (esim. virheell. rajoitus).

### TOIMINTAOHJE:

```
L1 Autom.säätö
 Ulkolämpö-15°C
 Menovesi  52°C
▶Valinta
```

Näytön takana on L2:n perusnäyttö, josta näkyy vain ylärivi "L2 Autom.säätö".

Paina **ESC** niin monta kertaa, että näyttö ei enää muutu.
Olet silloin oheisen kuvan mukaisessa "Valinta"-näytössä. Paina **OK**.
Voit siirtyä säätöpiiristä toiseen (L1, L2) [Ryhmänvaihto] -näppäimen avulla.

```
L1 Valitse
 Säätökäyrien as
 Asetusarvot
 Mittaukset
▶Menovesi-info
 Ohjaustavat
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle.

Siirrä osoitin kohtaan "Menovesi-info" [Selaus] -näppäimellä. Paina **OK**.

Voit selata [Selaus] -näppäimen avulla, mitkä tekijät vaikuttavat menoveden lämpötilaan. Poistu tilasta **ESC**illä.

```
L1 Menovesi °C
▶Käyrän muk.
 Huonekomp
 Tuulikomp
 Aurinkokomp
 Yö/ Poissa
 Esikorotus
 Syyskuivaus
 Ulkol.hidast.
 Max raj.vaik
 Min raj.vaik
 Alasajo
 Yhteisvaik. =
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle. Punaiset viivat yhdistävät kunkin rivin selitteeseen:

| Näytön rivi | Selite |
|---|---|
| Käyrän muk. | Menoveden lämpötila käyrän mukaan tämänhetkisellä ulkolämmöllä |
| Huonekomp | Huonekomp. :Huonekompens. vaikutus menoveteen/ vaihtoehtoisesti Huonek. yö: Huonekomp.vaikutus menoveteen yöalennuksen aikana. |
| Tuulikomp | Tuulikompensoinnin nostava vaikutus menoveteen |
| Aurinkokomp | Aurinkokompensoinnin laskeva vaikutus menoveteen |
| Yö/ Poissa | Kellon ohjaaman yöpudotuksen laskeva vaikutus menoveteen (GSM:llä ohjattu pudotus) |
| Esikorotus | Yöpudotuksen jälkeisen esikorotuksen nostava vaikutus menoveteen |
| Syyskuivaus | Automaattisen syyskuivaustoiminnan nostava vaikutus menoveteen |
| Ulkol.hidast. | Ulkolämpötilan mittauksen hidastustoiminnan vaikutus menoveteen |
| Max raj.vaik | Maksimirajoituksesta johtuva menoveden lämmön pudotus |
| Min raj.vaik | Minimirajoituksesta johtuva menoveden lämmön korotus |
| Alasajo | Vapaan lämpötilan pudotuksen laskeva vaikutus menoveteen |
| Yhteisvaik. = | **Säätimen määräämä menoveden lämpötila tällä hetkellä (°C)** |

### ESIMERKKI

```
L1 Menovesi °C
▶Käyrän muk.  35
 Syyskuivaus   4
 Ulkol.hidast.-2
 Max raj.vaik  0
 Min raj.vaik  0
 Yhteisvaik. =37
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle.

Kuvan esimerkissä on käyrän mukainen menoveden lämpötila 35°C. Syysajan kuivaustoiminta nostaa sitä 4°C. Ulkolämmön mittauksen hidastustoiminta pudottaa menoveden lämpötilaa 2°C. Näiden yhteisvaikutuksena säädin määrää menoveden lämpötilaksi +37°C (35+4-2=37).

### AVAINSANAT:

- **L1 Menovesi-info**
- **L2 Menovesi-info**

![GSM-viestit: Menovesi-info](kasikirja/s12-gsm-menovesi-info.png)

Kuvan kuvaus: kaksi GSM-puhelinta. Vasemman puhelimen salamanuoli osoittaa puhelimesta poispäin, oikean puhelimen nuolessa on kärki kumpaankin suuntaan. Vasemman puhelimen näytössä on viesti "L1 MENOVESI-INFO", oikean puhelimen näytössä viesti, joka jatkuu näytön reunan yli:

```
L1 MENOVESI:
Käyrän muk. 35/
Syyskuivaus 4/
Ulkol.hidast.=-2/
Max.raj.vaik.=0/
Min.raj.vaik.=0/
Yhteisvaik=37
```

---

<a id="s13"></a>

## Sivu 13: OHJAUSTAVAT

Jokaista säätöpiiriä voidaan ohjata alla mainituilla ohjaustavoilla. Tehdasasetuksena oleva automaattisäätö on normaali säätötilanne, jossa myös kello-ohjatut lämpötilan pudotukset ovat mahdolliset.

**Valittu ohjaustapa näkyy aina perusnäytössä ylimmällä rivillä.**

### TOIMINTAOHJE:

```
L1 Autom.säätö
 Ulkolämpö-15°C
 Menovesi  52°C
▶Valinta
```

Näytön takana on pinossa L2:n ja ML:n perusnäytöt, joista näkyvät vain ylärivit "L2 Autom.säätö" ja "ML Kompressori". Keltainen katkoviivanuoli osoittaa lauseesta "Valittu ohjaustapa näkyy aina perusnäytössä ylimmällä rivillä." perusnäytön ylimpään riviin.

Paina **ESC** niin monta kertaa, että näyttö ei enää muutu.
Olet silloin oheisen kuvan mukaisessa "Valinta"-näytössä. Paina **OK**.
Voit siirtyä säätöpiiristä toiseen (L1, L2, ML) [Ryhmänvaihto] -näppäimen avulla.

```
L1 Valitse
 Säätökäyrien as
 Asetusarvot
 Mittaukset
 Menovesi-info
 Ohjaustavat
▶Kellotoiminnat
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle.

Siirrä osoitin kohtaan "Ohjaustavat" [Selaus] -näppäimen avulla. Paina **OK**.

> **Repo note:** the screen above has its cursor on Kellotoiminnat, though this step moves it to Ohjaustavat and the next screen is L1 Ohjaustavat.

Voit selata eri ohjaustavat [Selaus] -näppäimellä.

● -merkki osoittaa, mikä ohjaustapa on valittu käyttöön.

```
L1 Ohjaustavat
▶● Autom.säätö
   Jatkuva päivä
   Jatkuva yö
   Alasajo
   Käsiajo mek.
   Käsiajo sähk.
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle.

**Ohjaustavan muuttaminen:** Vie osoitin [Selaus] -näppäimellä sen ohjaustavan kohdalle, jonka haluat ottaa käyttöön. Paina **OK**. Poistu tilasta **ESC**illä.

**Venttiilimoottorin mekaaninen käsiajo:**
Moottori on sähkötön.
Vain mekaaninen käsikäyttö on mahdollinen.

**Venttiilimoottorin käsiajo sähköllä:** Paina **OK**.
Muuta venttiilimoottorin asentoa **-** tai **+** -näppäimellä.
Näytössä näkyy, mihin suuntaan venttiilimoottoria ajetaan.
Asennon %-luku osoittaa venttiililmoottorin asennon, mikäli käytetään jänniteohjattua 0 (2) ... 10V venttiilimoottoria (0% = kiinni, 100%=auki).

![Käsiajon näppäimet](kasikirja/s13-kasiajo-nappaimet.png)

Kuvan kuvaus: näppäimet -, OK ja + rivissä; käsi painaa +-näppäintä.

```
Käsiajo sähk.
▶Ohjaus    --
 Asento: 39%
```

L1 Ohjaustavat -näytön riviltä "Käsiajo sähk." nuoli johtaa tähän näyttöön. Luku 39 on valkoisella.

**Maalämmityksen säätöpiirin (ML) ohjaustavat:**

Voit siirtyä maalämmityksen säätöpiiriin (ML) [Ryhmänvaihto] -näppäimen avulla.

```
ML Ohjaustavat
▶● Kompr.+sähköv.
   Kompressori
   Sähkövastus
```

**Kompressori + sähkövastus:**
Jos maalämmön tuottama lämpö ei riitä, kytkeytyy sähkövastus päälle.

**Kompressori:**
Varaajien lämmitys tapahtuu vain maalämmöllä (ei käytetä sähkövastuksia).

**Sähkövastus:**
Varaajan lämmitys tapahtuu vain sähkövastuksella.

**Jakoventtiilin ohjaustavan valinta on huoltopuolella.**

### LISÄTIETOA LÄMMITYKSEN SÄÄTÖPIIRIEN L1 JA L2 OHJAUSTAVOISTA:

![L1:n ja L2:n ohjaustavat](kasikirja/s13-l1-l2-ohjaustavat.png)

Kuvan kuvaus: neljä vierekkäistä kaaviota ajan funktiona ilman asteikkoja. Sininen käyrä on menoveden lämpötila ("Menovesi"), punainen huonelämpötila ("Huonelämpö"). Kunkin kaavion otsikon vieressä on ohjaustavan kuvake.

- Automaattisäätö (kuvake: kaksi toisiinsa kietoutuvaa kaarta): menovesi laskee portaittain alemmalle tasolle, nousee myöhemmin hetkeksi alkutasoa korkeammalle ja palaa sitten alkutasolle. Huonelämpö laskee hieman menoveden alemman jakson aikana ja nousee sen jälkeen takaisin.
- Jatkuva päivä (kuvake: aurinko): menovesi ja huonelämpö pysyvät tasaisina.
- Jatkuva yö (kuvake: kuu): menovesi pysyy tasaisena, alempana kuin Jatkuva päivä -kaaviossa; huonelämpö laskee alussa ja pysyy sitten tasaisena alemmalla tasolla.
- Alasajo (kuvake: virtakytkin): menovesi laskee ensin jyrkästi ja sitten hitaasti, huonelämpö laskee tasaisesti. Selitetekstin sanasta "jäätymissuojarajaan" lähtee katkoviivanuoli käyrien loppupäähän.

| Automaattisäätö | Jatkuva päivä | Jatkuva yö | Alasajo |
|---|---|---|---|
| Lämpötilan pudotukset tapahtuvat kello-ohjelman mukaisesti. | Kello-ohjelmista riippumaton normaali päivälämpö on päällä. | Kello-ohjelmista riippumaton jatkuva lämpötilan pudotus on päällä. | Vapaa menoveden lämpötilan pudotus aina jäätymissuojarajaan saakka (stand by-toiminta). |

### AVAINSANAT:

- **L1 Ohjaustapa**
- **L2 Ohjaustapa**

![GSM-viestit: Ohjaustapa](kasikirja/s13-gsm-ohjaustapa.png)

Kuvan kuvaus: kaksi GSM-puhelinta. Vasemman puhelimen salamanuoli osoittaa puhelimesta poispäin, oikean puhelimen nuolessa on kärki kumpaankin suuntaan. Vasemman puhelimen näytössä on viesti "L1 OHJAUSTAPA", oikean puhelimen näytössä viesti, joka jatkuu näytön reunan yli. Tähti ja luvut 000 ovat valkoisia:

```
L1 OHJAUSTAPA:
*Autom.säätö/
Jatkuva päivä/
Jatkuva yö/
Käsiajo sähk.
auki=000%/
Käsiajo sähk.
kiinni=000%/
Venttiilin
huuhtelu/
```

---

<a id="s14"></a>

## Sivu 14: KELLOTOIMINNAT Ajan asetus

Kellon ajan asettaminen tapahtuu seuraavasti:

Geopro 202S säätimen kello huomioi kesä- ja talviajan muutokset ja karkausvuodet. Kellossa on varakäynti lyhytaikaisia sähkökatkoksia vastaan. Pariston kestoikä on noin 10 vuotta.

### TOIMINTAOHJE:

```
L1 Autom.säätö
 Ulkolämpö-15°C
 Menovesi  52°C
▶Valinta
```

Näytön takana on pinossa L2:n ja ML:n perusnäytöt, joista näkyvät vain ylärivit "L2 Autom.säätö" ja "ML Kompressori".

Paina **ESC** niin monta kertaa, että näyttö ei enää muutu.
Olet silloin oheisen kuvan mukaisessa "Valinta"-näytössä. Paina **OK**.

```
L1 Valitse
 Säätökäyrien as
 Asetusarvot
 Mittaukset
 Menovesi-info
 Ohjaustavat
▶Kellotoiminnat
 Kieli/ language
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle.

Siirrä osoitin kohtaan "Kellotoiminnat" [Selaus] -näppäimellä. Paina **OK**.

```
Kellotoiminnat
▶Kellonaika/pvm
 L1 Pudotusohj.
 L2 Pudotusohj.
```

Osoitin on kohdassa "Kellonaika/pvm". Paina **OK**.

```
Kellonaika/pvm
▶15:45 tunn/min
 09/11 pv/kk
 2006  Maanantai
```

15:45 on valkoisella.

**Kellonajan asetus:**
Osoitin on kohdassa kellon aika. Paina **OK**.
Tunnit vilkkuvat. Aseta tunnit käyttäen **-** tai **+** -näppäintä. Paina **OK**.
Minuutit vilkkuvat. Aseta minuutit käyttäen **-** tai **+** -näppäintä. Paina **OK**.

```
Kellonaika/pvm
 15:45 tunn/min
▶09/11 pv/kk
 2006  Maanantai
```

09/11 on valkoisella.

**Päivämäärän asetus:** Paina **OK**.
Pvm vilkkuu. Aseta kuukauden päivä **-** tai **+** -näppäimellä. Paina **OK**.
Kuukausi vilkkuu. Aseta kuukausi **-** tai **+** -näppäimellä. Paina **OK**.

```
Kellonaika/pvm
 15:45 tunn/min
 09/11 pv/kk
▶2006  Maanantai
```

2006 ja Maanantai on valkoisella.

**Vuoden ja viikonpäivän asetus:** Paina **OK**.
Vuosi vilkkuu. Aseta vuosi **-** tai **+** -näppäimellä. Paina **OK**.
Viikonpäivä vilkkuu. Aseta viikonpäivä **-** tai **+** -näppäimellä. Paina **OK**.
Poistu tilasta **ESC**illä.

---

<a id="s15"></a>

## Sivu 15: Kello-ohjelmien selaus, lisäys, poisto

Vapaasti ohjelmoitavan vuorokausi-/ viikkokellon avulla voit:
**Pudottaa lämmitystä haluaminasi aikoina (lämmityspiirit L1 ja L2).**

### TOIMINTAOHJE:

```
L1 Autom.säätö
 Ulkolämpö-15°C
 Menovesi  52°C
▶Valinta
```

Näytön takana on pinossa L2:n ja ML:n perusnäytöt, joista näkyvät vain ylärivit "L2 Autom.säätö" ja "ML Kompressori".

Paina **ESC** niin monta kertaa, että näyttö ei enää muutu.
Olet silloin oheisen kuvan mukaisessa "Valinta"-näytössä. Paina **OK**.

```
L1 Valitse
 Säätökäyrien as
 Asetusarvot
 Mittaukset
 Menovesi-info
 Ohjaustavat
▶Kellotoiminnat
 Kieli/ language
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle.

Siirrä osoitin kohtaan "Kellotoiminnat" [Selaus] -näppäimellä. Paina **OK**.

```
Kellotoiminnat
 Kellonaika/pvm
▶L1 Pudotusohj.
 L2 Pudotusohj.
```

Siirrä osoitin [Selaus] -näppäimen avulla osoittamaan sitä säätöpiiriä, jonka aikaohjauksia haluat käsitellä (selata, lisätä tai poistaa). Paina **OK**.

### SELAUS/ OHJELMAN LISÄYSPAIKAN HAKEMINEN:

```
▶00:00 PudON L1
 _ _ _ _ _ _ _
 00:00 PudPOIS
 _ _ _ _ _ _ _
```

Ensimmäinen 00:00 on valkoisella ja vilkkuu. Näytön oikeassa reunassa on kaarisulku, joka rajaa ohjelmajakson neljä riviä. Viivat ovat viikonpäivien paikat.

Selaa [Selaus] -näppäimen avulla, mitä kello-ohjelmia on tehty.

Halutessasi ohjelmoida lisää, siirrä osoitin ensimmäiseen ohjelmoimattomaan ohjelmajaksoon.

```
▶19:30 PudON L1
 _ _ _ _ _ _ _
 00:00 PudPOIS
 _ _ _ _ _ _ _
```

19:30 on valkoisella ja vilkkuu.

**Lämpötilan pudotuksen aloitusajan asettaminen:** Paina **OK**.
Pudotuksen aloitusajan tunnit vilkkuvat.
Aseta tunnit **-** tai **+** -näppäimellä. Paina **OK**.
Minuutit vilkkuvat. Aseta minuutit **-** tai **+** -näppäimellä. Paina **OK**.

```
 19:30 PudON L1
▶MaTiKeToPe _ _
 00:00 PudPOIS
 _ _ _ _ _ _ _
```

MaTiKeToPe on valkoisella ja vilkkuu.

**Viikonpäivien asettaminen (em. aloitusajalle):**
Viikonpäivä valitaan käyttöön **+** -näppäimellä.
Päivä jätetään valitsematta/ valinta poistetaan **-** -näppäimellä.
**OK**:lla otetaan käyttöön tarjolla oleva valinta.
Tee valinta päiväkohtaisesti ja lopuksi paina **OK**.

```
 19:30 PudON L1
 MaTiKeToPe _ _
▶04:30 PudPOIS
 _ _ _ _ _ _ _
```

04:30 on valkoisella ja vilkkuu.

**Lämpötilan pudotuksen päättymisajan asettaminen:** Paina **OK**.
Tunnit vilkkuvat. Aseta tunnit **-** tai **+** -näppäimellä. Paina **OK**.
Minuutit vilkkuvat. Aseta minuutit **-** tai **+** -näppäimellä. Paina **OK**.

```
 MaTiKeToPe _ _
 04:30 PudPOIS
▶MaTiKeToPe _ _
 00:00 PudON L1
 _ _ _ _ _ _ _
 00:00 PudPOIS
 _ _ _ _ _ _ _
jne.
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle. Kolmannen rivin MaTiKeToPe on valkoisella ja vilkkuu. Ensimmäisen ohjelmajakson kaarisulku päättyy rivillä "00:00 PudON L1", ja siitä alkaa uusi kaarisulku, joka rajaa seuraavan ohjelmajakson (00:00 PudON L1 … 00:00 PudPOIS). Punainen viiva alleviivaa tekstin "Kaaren sisällä" ja päättyy nuolena uuteen kaarisulkuun.

**Viikonpäivien asettaminen (em. lopetusajalle):** Paina **OK**.
Viikonpäivä valitaan käyttöön **+** -näppäimellä.
Päivä jätetään valitsematta/ valinta poistetaan **-** -näppäimellä.
**OK**:lla otetaan käyttöön tarjolla oleva valinta.
Tee valinta päiväkohtaisesti ja lopuksi paina **OK**.
Kaaren sisällä on aina yksi ohjelmajakso (pudotus päälle ja pois päältä).
Osoitin siirtyy seuraavan ohjelmajakson alkuun (uusi kaarisulku).
Jatka ohjelmointia kuten edellä tai poistu ohjelmointitilasta **ESC**illä.
*Kuvan esimerkissä pudotus on päällä työviikon aikana klo 19:30 - 4:30 välisen ajan. Viikonloppuna pudotus alkaa perjantai iltana klo 19:30 ja päättyy maanantaiaamuna kello 4:30.*

### OHJELMAJAKSON POISTO:

```
▶19:30 PudON L1
 _ _ _ _ _ _ _
 04:30 PudPOIS
 _ _ _ _ _ _ _
```

Punainen nuoli osoittaa tekstistä näytön oikeassa reunassa olevaan kaarisulkuun.

Voit poistaa kaarisulun sisällä olevan ohjelmajakson niin, että poistat viikonpäivät kyseisestä ohjelmajaksosta **-** -näppäimellä.

---

<a id="s16"></a>

## Sivu 16: KIELI/ TYYPPITIEDOT

Geopro 202S säädin on kaksikielinen. Säätimessä on yleisimmin käytetty kieliyhdistelmiä suomi- ruotsi (svenska) ja englanti (english) - eesti.

Säätimen kielen vaihtaminen tapahtuu seuraavasti:

### TOIMINTAOHJE:

```
L1 Autom.säätö
 Ulkolämpö-15°C
 Menovesi  52°C
▶Valinta
```

Näytön takana on pinossa L2:n ja ML:n perusnäytöt, joista näkyvät vain ylärivit "L2 Autom.säätö" ja "ML kompressori".

Paina **ESC** niin monta kertaa, että näyttö ei enää muutu.
Olet silloin oheisen kuvan mukaisessa "Valinta"-näytössä. Paina **OK**.

```
L1 Valitse
 Säätökäyrien as
 Asetusarvot
 Mittaukset
 Menovesi-info
 Ohjaustavat
 Kellotoiminnat
▶Kieli/ språk
 Tyyppitiedot
 Starttitoiminta
 Huoltotila
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle.

Siirrä osoitin kohtaan "Kieli/ språk" [Selaus] -näppäimen avulla. Paina **OK**.

```
Kieli/ Språk
▶● Suomi
   Svenska
```

Siirrä osoitin [Selaus] -näppäimen avulla sen kielen kohdalle, jonka haluat ottaa käyttöön. Paina **OK**.

> **Repo note:** pp. 14 and 15 show this menu item as "Kieli/ language".

### TYYPPITIEDOT

Tyyppitiedot kertovat, mikä säädin on kyseessä ja mikä ohjelmaversio on käytössä. Geopro 202S säätimessä on kaksi lämmityspiiriä ja maalämpökojeen toiminnan ohjaus.

#### TOIMINTAOHJE:

```
L1 Autom.säätö
 Ulkolämpö-15°C
 Menovesi  52°C
▶Valinta
```

Näytön takana on pinossa L2:n ja ML:n perusnäytöt, joista näkyvät vain ylärivit "L2 Autom.säätö" ja "ML Kompressori".

Paina **ESC** niin monta kertaa, että näyttö ei enää muutu.
Olet silloin oheisen kuvan mukaisessa "Valinta"-näytössä. Paina **OK**.

```
L1 Valitse
 Säätökäyrien as
 Asetusarvot
 Mittaukset
 Menovesi-info
 Ohjaustavat
 Kellotoiminnat
 Kieli/ Språk
▶Tyyppitiedot
 Starttitoiminta
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle.

Siirrä osoitin kohtaan "Tyyppitiedot" [Selaus] -näppäimen avulla. Paina **OK**.

```
 Tyyppitiedot
 GEOPRO 202S
  Versio 1.xx
▶  00122611
```

Ouman Finland Oy panostaa voimakkaasti jatkuvaan tuotekehitykseen. Versionumero kertoo valmistajalle, mikä ohjelmaversio on kyseessä.

Sarjanumero liittyy tuotantoprosessiin ja kertoo säätimen valmistajalle täsmällisesti, mistä yksilöstä on kyse.

---

<a id="s17"></a>

## Sivu 17: STARTTITOIMINTA Säätötavan valinta

**Starttitoiminnassa** säädin tunnistaa siihen kytketyt anturit. Menovesiantureiden perusteella säädin ottaa käyttöön säätöpiirit (L1ja L2). Oletuksena on perussäädin jokaisessa säätöpiirissä. Halutessasi voit muuttaa lämmityksen säätöpiirin (L1 ja L2) itseoppivaksi säätimeksi. Starttitoiminta aktivoi käyttöön myös antureiden vikahälytykset.

**Perussäädin** ohjaa menoveden lämpötilaa asetetun säätökäyrän mukaisesti. **Itseoppiva säädin** muokkaa säätökäyrää automaattisesti huoneanturilta saamansa palautteen perusteella. Itseoppivuuden maksimivaikutus on 10%. Säätökäyrän asettelu -näytössä **i**-kirjain kertoo, että itseoppivuus on käytössä.

### TOIMINTAOHJE:

```
L1 Autom.säätö
 Ulkolämpö-15°C
 Menovesi  52°C
▶Valinta
```

Näytön takana on pinossa L2:n ja ML:n perusnäytöt, joiden ylärivit "L2 Automaattiohj" ja "ML Kompressori" jäävät osin kuvan yläreunan taakse.

Paina **ESC** niin monta kertaa, että näyttö ei enää muutu.
Olet silloin oheisen kuvan mukaisessa "Valinta"-näytössä. Paina **OK**.

```
L1 Valitse
 Säätökäyrien as
 Asetusarvot
 Mittaukset
 Menovesi-info
 Ohjaustavat
 Kellotoiminnat
 Kieli/ Språk
 Tyyppitiedot
▶Starttitoiminta
 Huoltotila
```

**Antureiden käyttöönotto ja antureiden poistaminen käytöstä:**
Jos kytket anturin säätimeen tai irrotat anturin säätimeltä, tulee sinun käydä starttitoiminnassa, jolloin säädin ottaa käyttöön tai poistaa anturit käytöstä.
Siirrä osoitin kohtaan "Starttitoiminta" [Selaus] -näppäimen avulla. Paina **OK**.
Säädin tunnistaa siihen kytketyt ja poistetut anturit ja näyttää valittavissa olevat säätötavat. Jos et halua muuttaa säätötapaa, voit poistua säätötapanäytöstä ESC:llä muuttamatta mitään.

Säätimen tehdasasetuksena on perussäädin.

```
Säätötapa
▶● L1 perussäädin
   L1 itseoppiva
   L1 ei käytössä
 ● L2 perussäädin
   L2 itseoppiva
   L2 ei käytössä
```

Näytössä näkyy neljä riviä kerrallaan; muut rivit on piirretty näytön alapuolelle.

**Selaus:**
Selaa valittavissa olevat säädintyypit säätöpiireittäin [Selaus] -näppäimellä.
● -merkki osoittaa, mikä säädintyyppi on valittu käyttöön missäkin säätöpiirissä.

**Säädintyypin muuttaminen:**
Vie osoitin haluamaasi kohtaan [Selaus] -näppäimellä ja paina **OK**.

### TIETOA ITSEOPPIVUUDESTA:

![Huoneanturit TMR ja TMR/P](kasikirja/s17-huoneanturit.png)

Kuvan kuvaus: valokuva kahdesta huoneanturista, vasemmalla TMR ja oikealla TMR/P, jossa on pyöreä säätöasteikko. TMR/P on yliviivattu punaisella rastilla. Niiden oikealla puolella on kuun kuvake, joka on myös yliviivattu punaisella rastilla.

Itseoppivuutta tapahtuu, mikäli huonelämpö poikkeaa vähintään 1°C asetusarvostaan ulkolämpötilan ollessa vähintään 4 tunnin ajan alueella +5...-5°C tai -15...-25°C.

Säätökäyrän automaattinen korjaus tapahtuu 0°C tai -20°C asettelupisteen kohdalla. Korjauksen nopeus on 1°C 4 tunnin aikana. Korjauksen maksimimäärä on +/- 10% käyrän asetusarvosta. Mikäli säätökäyrän asettelua muutetaan, itseoppivuus alkaa alusta.

Itseoppivuus edellyttää, että käytetään huoneanturiaTMR (ei TMR/P). Lämpötilan pudotusten aikana itseoppivuus ei ole toiminnassa.

![Itseoppivuuden merkki ja itseoppivuusalue](kasikirja/s17-itseoppivuus.png)

Kuvan kuvaus: kaksi säätökäyrän asettelunäyttöä päällekkäin. Kummankin näytön teksti on:

```
L1 Käyrä:i
▶-20 = 58°C
   0 = 41°C
 +20 = 18°C
```

Näytön oikeassa reunassa on pieni kaavio säätökäyrästä: pystyakselin asteikko 20, 35, 50, 65, 80, vaaka-akselin asteikko 20, 0, -20 ja yksikkö °C. Ylempi näyttö: rivi "-20 = 58°C" ja vaaka-akselin -20 ovat punaisia, ja käyrän -20 °C:n päähän on piirretty punainen viuhka. Selite "Itseoppivuuden merkki" osoittaa nuolella i-kirjaimeen rivillä "L1 Käyrä:i". Alempi näyttö: rivi "0 = 41°C" ja vaaka-akselin 0 ovat oransseja, ja viuhka on käyrän keskellä 0 °C:n kohdalla. Selitteestä "Itseoppivuusalue" lähtevät viivat kumpaankin viuhkaan.

**Esimerkkejä itseoppivan säätimen toiminnasta:**
Jos ulkolämpötila on välillä -15...-25°C, itseoppivuus tapahtuu säätökäyrän asettelupisteessä: -20°C. Esimerkiksi asetusarvon ollessa 58°C, itseoppivuusalue on 52...64°C (+/- 10% asetusarvosta).

Jos ulkolämpötila on välillä -5...+5°C, itseoppivuus tapahtuu säätökäyrän asettelupisteessä: -0°C. Esimerkiksi asetusarvon ollessa 41°C, itseoppivuusalue on 37...45°C (+/- 10% asetusarvosta).

---

<a id="s18"></a>

## Sivu 18: HÄLYTYKSET

Geopro 202S hälyttää poikkeavissa tilanteissa. Hälytystilanteessa säätimestä kuuluu hälytysääni ja näyttöön tulee hälytysilmoitus. Lisäksi hälytysreleen kosketin sulkeutuu. Huom! Vaikka hälytyksen syy on poistunut, jää viimeinen hälytys pysyvästi näyttöön kunnes se kuitataan. Mikäli säätimeen on kytketty GSM-modeemi, välittyy hälytys haluttuun GSM-puhelimeen tekstiviestinä. Geopro 202S:ssa on mahdollista kytkeä myös yksi hälytys mittaukseen 6, mikäli se on vapaana. esim. kosteushälytyksen jatko-ohjaus (hälytysten nimeäminen tapahtuu tekstieditorilla).

### Anturivikahälytykset:

```
Hälytys!

Mittaus 1
Ulkolämpö err
```

Anturivikatapauksessa säätimestä kuuluu hälytysääni ja näyttöön tulee hälytysilmoitus: Hälytys! mittausnumero ja mittausnimi sekä err. Hälytysreleen kosketin sulkeutuu (riviliittimet 31 ja 32).

### Jäätymisvaarahälytys:

```
Jäätymisvaara!

Mittaus 2
L1 Menovesi 11
```

Säädin antaa jäätymisvaarahälytyksen, jos menoveden lämpötila alittaa menoveden vapaan pudotuksen alarajasta tai huonelämpötilan alarajasta lasketun raja-arvon. Näytössä on menoveden lämpötila. (ks. sivu 28).

### Poikkeamahälytys:

```
Poikkeamahälytys

Mittaus 2
L1 Menovesi 25
```

Säädin antaa poikkeamahälytyksen, jos menoveden lämpötila poikkeaa pysyvästi (tehdasasetus 60 min) säätimen määräämästä menoveden lämpötilasta. (Sallittu maksimipoikkeama annetaan erikoishuollon "L1PoikHäl" -asetusarvossa ja hälytyksen edellyttämä poikkeaman kesto "PoikHälHid" -asetusarvossa, sivu 28.)

> **Repo note:** p. 28 is Moottorivalinta. Both "sivu 28" references describe settings on p. 30: the menoveden vapaan pudotuksen alarajat (L1mv.min, L2mv.min), L1 Poikk.häl and PoikHälHid. Page 30 writes "L1 Poikk.häl" where this page has "L1PoikHäl".

### Maalämpökojeen hälytykset:

```
Alilämpöhälytys!

 Mittaus 8
 Maaliuos   -15
```

**Alilämpöhälytys/ Mittaus 8/ Maaliuos** = Maalämpökoneelta palaavan maaliuoksen alilämpö. Hälytysrajan asettaminen: Huoltotila/ asetusarvot/ "maaliuos häl"-asetusarvo.

**Poikkeamahälytys/ Mittaus 11/ Kompr.käynti** = Säädin ei saa käyntitietoa kompressorilta, vaikka kompressorin tulisi käydä. Hälytys estää säätimen kompressorin käyntiyritykset 5 min ajan, jonka jälkeen säädin yrittää käynnistää kompressorin uudelleen.

**Hälytys/ Dig 2/ Kompr. L-rele** = Kompressorin ylivirtaussuojan hälytys. (lämpörele)

**Hälytys/ Dig 3/ Sähköv.ylik** = Sähkövastuksen ylikuumenemissuojan hälytys. Huom! Hälytys voidaan kuitata vain sähkövastuksen käsikuittaus- painikkeella.

### ULKOPUOLISET HÄLYTYKSET:

**Mittaus 6 hälytyskäytössä:**

Mittausta 6 voidaan käyttää myös ulkopuolisten hälytysten ilmaisuun (potentiaalivapaa kosketin). Tällöin tulee kyseisen mittauksen riviliittimille kytkeä 30kΩ vastus. Hälytykset voidaan nimetä (ks. sivu 8).

> **Repo note:** alarms are named with the text editor on p. 11, not p. 8; the index on p. 41 lists Hälytysten nimeäminen on pp. 11 and 18.

Otsikon alla on punaisella vinoon kirjoitettuja esimerkkinimiä: “Kosteusvaara!” ja “Lokasäiliö!”.

**Sulkeutuva hälytys**

![Sulkeutuva hälytys](kasikirja/s18-sulkeutuva-halytys.png)

Kuvan kuvaus: kaksi riviliitintä yläreunassa. Niiden välissä on 30kΩ:n vastus, ja vastuksen rinnalla alareunassa on avoin kosketin.

Kun kosketin on auki, näytössä on "1 ". Kun kosketin sulkeutuu, tapahtuu hälytys, ja näytössä näkyy kyseinen hälytys.

**Avautuva hälytys**

![Avautuva hälytys](kasikirja/s18-avautuva-halytys.png)

Kuvan kuvaus: kaksi riviliitintä yläreunassa. Vasemmasta liittimestä johdin kulkee 30kΩ:n vastuksen kautta alas ja sieltä oikealle koskettimelle, joka on piirretty kahtena liitäntäpisteenä oikean liittimen alle. Vastus ja kosketin ovat sarjassa.

Kun kosketin on kiinni, näytössä on "1 ". Kun kosketin avautuu, tapahtuu hälytys, ja näytössä näkyy kyseinen hälytys.

### HÄLYTYSRELEEN KYTKENTÄ:

![Hälytysreleen kytkentä](kasikirja/s18-halytysreleen-kytkenta.png)

Kuvan kuvaus: hälytysreleen kosketin, jonka vieressä on merkintä "24 VAC/ 1A", on kytketty riviliittimiin 31 ja 32. Liittimiltä kaapeli 2 x 0.8 kulkee laatikkoon "Kiinteistön hälytyskeskus".

### HÄLYTYKSEN KUITTAUS:

Hälytysääni vaiennetaan painamalla mitä tahansa näppäintä. Samalla näyttö palaa siihen tilaan, jossa se oli vian ilmetessä tai jos on muita hälytyksiä, näyttöön tulee niistä hälytystiedot. Jos näppäimiin ei kosketa 20 sekuntiin, hälytysilmoitus palaa näyttöön ellei vikaa ole korjattu.

GSM-control ominaisuus tarjoaa edullisen "minivalvomo-ratkaisun". Hälytystieto ohjataan haluttuihin GSM-numeroihin (1 ja 2). Ks. s. 33). Hälytystilanteessa säädin lähettää ensin GSM 1:een tekstiviestin, jossa ilmenee hälytyksen syy. Hälytys kuitataan GSM:llä lähettämällä sama viesti takaisin säätimelle. Mikäli hälytystä ei kuitata GSM 1:stä 5 min sisällä, säädin lähettää uudelleen tekstiviestin molempiin GSM-numeroihin.

> **Repo note:** the GSM numbers (Häl.nro GSM 1 and Häl.nro GSM 2) are set on p. 35; p. 33 is LON-käyttöönotto.

---

<a id="s19"></a>

## Sivu 19: GSM-TOIMINNOT

Geopro 202S:n kytkettävä GSM-modeemi mahdollistaa käyttäjän kommunikoinnin säätimen kanssa GSM-puhelimella tekstiviestien välityksellä (käyttöönotto s. 35). GSM- puhelimella voidaan tehdä lähes kaikki tässä ohjekirjassa mainitut käyttäjätason asiat, kuten mittaukset, asetusarvot, säätökäyrän asetukset, menovesi-info ja säätimen ohjaustapa. Kellojen voimassaoleva aikaohjelma voidaan ohittaa joko pysyvästi tai määräaikaisesti. GSM-puhelimeen välittyy myös hälytykset, jotka voidaan kuitata lähettämällä hälytysviesti takaisin säätimelle.

### KOMMUNIKOINTI SÄÄTIMEN KANSSA GSM:N VÄLITYKSELLÄ:

![GSM-viesti: Avainsanat](kasikirja/s19-gsm-avainsanat.png)

Kuvan kuvaus: GSM-puhelin, jonka näytössä on viesti. Viestin loppu jatkuu näytön reunan yli:

```
AVAINSANAT:
Mittaukset/
Säätökäyrät/
L1 Asetusarvot/
L2 Asetusarvot/
ML Asetusarvot/
L1 Ohjaustapa/
L2 Ohjaustapa
L1 Menovesi-info
L2 Menovesi-info
```

Lähetä seuraava tekstiviesti säätimelle: **AVAINSANAT**

Mikäli säätimellä on käytössä laitetunnus (s. 35, 36), kirjoita aina laitetunnus avainsanan eteen (esim. TC1 AVAINSANAT). Säädin lähettää tekstiviestinä listan avainsanoista, joiden avulla saat tietoja säätimen toiminnasta. Jokainen avainsana on erotettu toisistaan /-merkillä.

### Tietojen saanti säätimeltä GSM:llä:

![GSM-viesti: Mittaukset](kasikirja/s19-gsm-mittaukset.png)

Kuvan kuvaus: GSM-puhelin, jonka näytössä on viesti:

```
MITTAUKSET:
L1Menovesi= 52/
L1Huone= 21.5/
L1Paluuvesi=28/
Ulkolämpö=-15/
```

Lähetä tekstiviesti säätimelle käyttäen säätimen antamia avainsanoja. Säädin tunnistaa vain yhden pyynnön kerrallaan, joten kirjoita vain yksi avainsana/viesti. Voit kirjoittaa avainsanan isoilla tai pienillä kirjaimilla. (Mikäli säätimellä on käytössä laitetunnus (ks.s. 35, 36), kirjoita laitetunnus avainsanan eteen.)

Säädin vastaa pyyntösi lähettämällä pyytämäsi tiedot.

### Säätimen ohjaus GSM:llä:

![GSM-viesti: L1 Asetusarvot](kasikirja/s19-gsm-l1-asetusarvot.png)

Kuvan kuvaus: GSM-puhelin, jonka näytössä on viesti alla. Luvut 21,5, 0, 15 ja 85 ovat valkoisia, ja luvun 21,5 ympärillä on punainen ympyrä:

```
L1 ASETUSARVOT
Huonelämpö=21,5/
Yöalennus =0/
Minimiraja=15/
Maksimiraja=85
```

Voit muuttaa GSM-puhelimella säätökäyrän asetuksia, käyttäjätason asetusarvoja, säätimen ohjaustapaa.
Lähetä tekstiviesti säätimelle, jossa pyydät avainsanalla tietoja siitä toiminnosta, jonka asetuksia haluat muuttaa (tai ota tieto esille puhelimesi muistista). **Muokkaa säätimen lähettämän tekstiviestin lukuarvoja ja lähetä muokattu viesti säätimelle**. Säädin tekee pyydetyt muutokset ja lähettää kuittauksena tekstiviestin, jossa näkyy uudet asetukset.

![GSM-viesti: L1 Säätökäyrä](kasikirja/s19-gsm-l1-saatokayra.png)

Kuvan kuvaus: GSM-puhelin taulukon Säätökäyrät-rivin vieressä. Näytössä on viesti alla. Luvut 58, 41 ja 19 ovat valkoisia, ja luvun 58 ympärillä on punainen ympyrä:

```
L1 SÄÄTÖKÄYRÄ:
(-20=58;
0=41;
+20=19)
```

| Avainsana: | Toimintaohje, jos haluat muuttaa asetusta |
|---|---|
| Säätökäyrät | Kirjoita haluttu menoveden lämpötila entisen asetusarvon paikalle tekstiviestin “muokkaa” tilassa. |
| L1 Asetusarvot | Kirjoita asetusarvo entisen asetusarvon paikalle |
| L1 Ohjaustapa | Vaihda tähti (\*) sen ohjaustavan eteen, jonka haluat ottaa käyttöön. Käsiajon kuittaussanomassa säädin lähettää myös tiedon menoveden lämpötilasta ja venttiilin asennosta (0-10V ohjatut moottorit).<br><br>**Huom!** Sähköistä käsiajoa käytettäessä on oltava erityisen varovainen jäätymisvaaran ja ylilämpövaaran vuoksi.<br><br>Venttiilin huuhtelutoiminnassa säädin ajaa venttiilin auki ja sitten kiinni, jonka jälkeen säätö palautuu automaatille. Toiminnalla voidaan yrittää puhdistaa tukkeentunut venttiili roskista. |

![GSM-viesti: L1 Ohjaustapa](kasikirja/s19-gsm-l1-ohjaustapa.png)

Kuvan kuvaus: GSM-puhelin taulukon L1 Ohjaustapa -rivin vieressä. Näytössä on viesti, joka jatkuu näytön reunan yli. Tähti on valkoinen, ja sen ympärillä on punainen ympyrä:

```
L1 OHJAUSTAPA:
*Autom.säätö/
Jatkuva päivä/
Jatkuva yö/
Käsiajo sähk.
auki=000%/
Käsiajo sähk.
kiinni=000%/
Venttiilin
huuhtelu/
```

### Hälytysten kuittaus:

![GSM-viesti: hälytys](kasikirja/s19-gsm-halytys.png)

Kuvan kuvaus: GSM-puhelin, jonka näytössä on viesti:

```
Esimerkki talo
Hälytys:DIg1/
Lokakaivo
```

Voit kuitata hälytyksen GSM:n avulla lähettämällä saman viestin takaisin säätimelle.

---

<a id="s20"></a>

## Sivu 20: MAALÄMMITYSTOIMINNOT

### KIINTEISTÖN JA KÄYTTÖVEDEN LÄMMITTÄMINEN

Geopro 202S säätimessä on 2 lämmityksen säätöpiiriä (L1 ja L2). Niiden asettelut on esitetty sivuilla 4-7. Lämmitysvaraajan alaosaa lämmitetään kompressorilla ja tarvittaessa sähkövastuksella S1 niin, että lämmitysverkostoon riittää lämpöä lämmitystarpeen aikana ja yläosaa kompressorilla sekä tarvittaessa sähkövastuksen S1 avulla niin, että saadaan lämmintä käyttövettä.

> **Repo note:** p. 4 is blank. The contents on p. 5 put the säätökäyrien asetukset on pp. 6–7 and the asetusarvot on pp. 8–9.

**Lämpimän käyttöveden suureen kulutukseen varautuminen:**
Kun on odotettavissa tavanomaista suurempi lämpimän käyttöveden tarve, voidaan käyttöveden lämmitystä tehostaa lisälämmityksellä. Käyttöveden lisälämmityksen ohjaus tapahtuu painamalla erillistä lisälämpöpainiketta (lisävaruste). Kun painiketta painetaan, muuttuu alaosan minimilämpötilan asetusarvo “VaraajaAlaMin” “Lisälämmitys”-asetusarvoksi (esim. 45°C) asetusarvon “Lisäläm.aika” pituiseksi ajaksi. Tällä toiminnalla saadaan myös LV-varaajan alaosa kuumemmaksi, jolloin lämpimän käyttöveden kapasiteetti kasvaa.

### MAALÄMPÖKOJEEN HÄLYTYKSET

**Alilämpöhälytys/ Mittaus 8/ Maaliuos** = Alilämpöhälytys, jos maalämpökoneelta palaavan maaliuoksen lämpötila laskee alle asetellun hälytysrajan. Hälytysrajan asettaminen: Huoltotila/ Asetusarvot/ "Maaliuos häl"-asetusarvo.

**Poikkeamahälytys/ Mittaus 11/ Kompr.käynti** = Poikkeamahälytys, jos kompressoria ohjataan päälle ja käyntitietoa ei tule takaisinkytkennän kautta. **Huom!** Tämän hälytyksen tullessa katkaistaan kompressorin ohjaus. Hälytys kuittaantuu automaattisesti 5 minuutin päästä, jolloin kompressorin päällemeno sallitaan uudelleen.

**Hälytys/ Dig 2/ Kompr. L-rele** = Hälytys, jos kompressorin ylivirtasuoja on lauennut. (Lämpörele, sulkeutuva kosketin).

**Hälytys/ Dig 3/ Sähköv.ylik** = Hälytys, jos sähkövastuksen ylikuumenemissuoja on lauennut. Huom! Hälytys voidaan kuitata vain sähkövastuksen käsikuittauspainikkeella. (Hälytys sulkeutuvalta koskettimelta).

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

---

<a id="s24"></a>

## Sivu 24: HUOLTOTILAAN SIIRTYMINEN

Tästä alkaa huoltomiehelle tarkoitettu huolto-opas (s. 22 - 42).

Geopro 202S:ssa huoltotilaan pääsy rajoitetaan käyttäjäoikeuksilla. Huoltotilaan pääsevät vain sellaiset henkilöt, joilla on käytössään huoltokoodi.

**Huoltotilassa** on tyypillisiä viritysarvoja ja asetusarvoja, joita huoltomies tarvitsee järjestelmän käyttöönoton yhteydessä. Tavallinen kaukolämmönvaihtimen viritys tapahtuu tässä tilassa.

**Erikoishuoltotilassa** voidaan tehdä harvemmin tarvittavia asetuksia, kuten tehtaan alkuasetusten palautus, erikoisasetusarvot, mittauksen 6 asetukset, LON- asetukset, väylämittausten käyttöönotto sekä modeemiasetukset ja tekstiviestiasetukset.

### HUOLTOTILAAN SIIRTYMINEN:

Kuvan kuvaus: kolme näyttöä päällekkäin. Takimmaisena on ML-näyttö ("ML Kompressori"), sen edessä L2-näyttö ("L2 Autom.säätö") ja edessä L1-näyttö:

```
L1 Autom.säätö
  Ulkolämpö-15°C
  Menovesi  52°C
▶ Valinta
```

Paina **ESC** niin monta kertaa, että näyttö ei enää muutu. Olet silloin oheisen kuvan mukaisessa "Valinta"-näytössä. Paina **OK**.

Voit siirtyä säätöpiiristä toiseen (L1, L2, ML) [Ryhmänvaihto] -näppäimen avulla.

```
L1 Valitse
  Säätökäyrien as
  Asetusarvot
  Mittaukset
  Menovesi-info
  Ohjaustavat
  Kellotoiminnat
  Kieli/ Språk
  Tyyppitiedot
  Starttitoiminta
▶ Huoltotila
```

Siirrä osoitin kohtaan "Huoltotila" [Selaus] -näppäimellä. Paina **OK**.

```
L1 Huoltotila
Anna huoltokoodi
▶ 0000
```

Paina **OK**. Aseta huoltokoodi numero kerrallaan oikeaksi **-** tai **+** -näppäimellä ja paina kunkin numeron jälkeen **OK**.

### HUOLTOTILA:

```
L1 Huoltotila
▶ Viritysarvot
  Asetusarvot
  Trendit
  Mootorivalinta
  JV ohjaustapa
  Erikoishuolto
```

Valitse oheisesta valikosta [Selaus] -näppäimellä, mitä asiaa haluat käsitellä.

Jokainen kohta on esitetty yksityiskohtaisesti omalla sivullaan.

### ERIKOISHUOLTO:

Nuoli vie Huoltotila-valikon kohdasta "Erikoishuolto" tähän valikkoon.

```
Erikoishuolto
▶ Aset.palautus
  Asetusarvot
  Mitt. 6 asetus
  LON käytt.otto
  Väylämittaukset
  Tekstiviestias.
```

> **Repo note:** this page gives the Huolto-opas as pp. 22–42; it starts here, on p. 24, as the contents on p. 5 list it. The Huoltotila menu here spells Moottorivalinta "Mootorivalinta", which pp. 27 and 28 spell in full, and the Erikoishuolto menu has "Mitt. 6 asetus" where pp. 29–31 and 33–36 have "Mitt.6 asetus".

---

<a id="s25"></a>

## Sivu 25: VIRITYSARVOT

Geopro 202S:ssa on kaksi PID-säädintä. Viritysarvojen muuttaminen saattaa tulla tarpeelliseksi käyttöönottotilanteessa, mikäli tehtaan alkuasetusarvoilla tapahtuu säädössä huojuntaa.

Ohjeet huoltotilaan siirtymisestä on esitetty sivulla 22.

Viritys tapahtuu seuraavasti:

```
L1 Huoltotila
▶ Viritysarvot
  Asetusarvot
  Trendit
```

Osoitin on kohdassa "Viritysarvot". Paina **OK**.

```
L1 Viritysarvot
▶ P-alue:  140 °C
  I-aika:   50  s
  D-aika:  0.0  s
```

Siirrä osoitin haluamaasi kohtaan [Selaus] -näppäimellä. Paina **OK**. Tee muutokset **-** tai **+** -näppäimellä. Hyväksy painamalla **OK**.

Siirtyminen säätöpiiristä toiseen tapahtuu [Ryhmänvaihto] -näppäimellä.

### TIETOJA VIRITYSARVOISTA:

| Asetusarvo: | Tehdasasetus: | Asettelualue: | Merkitys: | Huom! |
|---|---|---|---|---|
| P-alue | L1, L2: 140 °C<br>ML: 250°C | 10...300 °C | Menoveden lämpötilan muutoksen suuruus, jolla moottori ajaa venttiiliä 100%. | Esim. Jos menoveden lämpötila muuttuu 10°C ja P-alue on 100 °C, muuttuu moottorin asento 10%. |
| I-aika | L1, L2: 50 s<br>ML: 25 s | 5...300 s | Menoveteen jäänyt lämpötilan poikkeama asetusarvoon nähden korjataan ajamalla P-ajomäärä joka I-jakson aikana. | |
| D-aika | L1, L2: 0.0 s<br>ML: 0.0 s | 0.0...10.0 s | Säädön reagoinnin nopeutus lämpötilan muuttuessa. | Varo vakiohuojuntaa! |

Huom! Tehtaan alkuasetukset voivat poiketa edellä mainituista.

> **Repo note:** this page points to "sivulla 22" for entering huoltotila; the instructions are on p. 24.

---

<a id="s26"></a>

## Sivu 26: ASETUSARVOT

Geopro 202S:ssa on kolmenlaisia asetusarvoja:

a) **käyttäjätason** asetusarvot, joita käyttäjä saa muuttaa (s. 8-9)

b) **huoltotilan** asetusarvot, joita huoltomies voi joutua muuttamaan

c) **erikoishuoltotilan** harvoin muutettavat asetusarvot (s. 30)

Tehtaalla asetettujen alkuasetusten palautus tehdään erikoishuollossa (s. 29).

Ohjeet huoltotilaan siirtymisestä on esitetty sivulla 24.

```
L1 Huoltotila
  Viritysarvot
▶ Asetusarvot
  Trendit
```

Siirrä osoitin kohtaan "Asetusarvot" [Selaus] -näppäimellä. Paina **OK**.

```
L1 Asetusarvot
▶ Ulkol.hidas 2h
  Esikorotus  0h
```

Siirrä osoitin [Selaus] -näppäimellä sen asetuksen kohdalle, jonka arvoa haluat muuttaa. Paina **OK**. Muuta asetusarvoa **-** tai **+** -näppäimellä. Paina **OK**.

```
ML Asetusarvot
▶ VaraajaAlaEro 3°C
  VaraajaYläEro 5°C
  JV Esiavaus   40%
  JV Esto       60s
  Maaliuos häl  -6
```

Siirry maalämmön säätöpiiriin [Ryhmänvaihto] -näppäimen avulla.

Siirrä osoitin [Selaus] -näppäimellä sen asetuksen kohdalle, jonka arvoa haluat muuttaa. Paina **OK**. Muuta asetusarvoa **-** tai **+** -näppäimellä. Paina **OK**.

### TIETOJA HUOLTOTILAN ASETUSARVOISTA:

| Asetusarvo: | Tehdasasetus: | Asettelualue: | Merkitys: |
|---|---|---|---|
| Ulkolämpötilan hidastus | L1: 2 h<br>L2: 0 h | 0...20h<br>0...20h | Ulkolämmön mittauksen seuranta-jakson pituus, jolta säädin laskee keskiarvon. Keskiarvomittauksen perusteella tapahtuvat menoveden säätö ja pumpun ohjaus. |
| Esikorotus | L1: 0 h<br>L2: 0 h | 0...5h<br>0...5h | Yöpudotuksen jälkeisen automaattisen esikorotuksen kestoaika. |
| VaraajaAlaEro | 3 °C | 3...7 °C | Varaajan alaosan lämmityksen ohjauksen eroalue |
| VaraajaYläEro | 5°C | 3...10°C | Lämmitysvaraajan yläosan lämmityksen ohjauksen eroalue |
| JV Esiavaus | 40% | 25...100% | Jakoventtiilin esivauksen määrä. Esiavaus suoritetaan ennen sähkövastuksen päällekytkemistä. |
| JV Esto | 60s | 30...240s | Jakoventtiilin kiinniajon eston kestoaika. Kiinniajon esto aloitetaan sähkövastuksen päällekytkemisestä. |
| Maaliuos häl | -6 | -10...0°C | Hälytys maalämpökoneelta palaavan maaliuoksen alilämmöstä. |

> **Repo note:** p. 21 gives VaraajaAlaEro 5 °C and VaraajaYläEro 3 °C, and the factory-reset list on p. 29 agrees with p. 21. This page swaps them, in both its ML Asetusarvot screen and its table. [`docs/controller.md`](../docs/controller.md#factory-values-that-contradict-each-other) has what the Controller held.

> **Repo note:** Kompr.esto and VarYläEroSv, which p. 21 lists as huoltotila settings and p. 29 lists among the huoltotaso factory values, are on neither this page's screen nor its table.

---

<a id="s27"></a>

## Sivu 27: TRENDIT

Trendinäytössä on mahdollista seurata menoveden lämpötilan vaihtelua graafisen kuvaajan avulla. Voit itse määrittää, kuinka usein lämpötilaa mitataan. Tehdasasetuksena näytteenottoväli on sekunti.

Ohjeet huoltotilaan siirtymisestä on esitetty sivulla 24.

```
L1 Huoltotila
  Viritysarvot
  Asetusarvot
▶ Trendit
  Moottorivalinta
```

Siirrä osoitin kohtaan "Trendit" [Selaus] -näppäimellä. Paina **OK**.

```
L1 Menov.trendi
▶ Trendinäyttö
  Näyteväli 1s
```

Jos haluat nähdä menoveden lämpötilakuvaajan, paina **OK**.
Voit lukea graafisesti menoveden lämpötilan vaihteluita. Näytön oikeaan reunaan on painettu menoveden lämpötila-asteikko. Menoveden tarkka lämpötila näkyy myös lukuarvona.

![Trendinäyttöjen kuvaajat](kasikirja/s27-trendi.png)

Kuvan kuvaus: kahden trendinäytön oikea puoli; näyttöjen tekstit ovat alla. Kummassakin on menoveden lämpötilan kuvaaja ja näytön oikeassa reunassa pystyasteikko 20, 35, 50, 65, 80, otsikkona "Menoveden lämpötila". Kuvaaja notkahtaa vasemmassa päässä noin 41:een ja jatkuu sitten katkoviivana vaakasuorana noin 45:n kohdalla. Kuvaaja on kummassakin näytössä sama; näytöt eroavat vain alimmalta riviltään.

```
Trendi
L1 Menovesi
   45 °C
Ajos.[+]
```

Jos käytössä on 3-tilaohjattu moottori, näytössä näkyy, mihin suuntaan venttiilimoottoria ajetaan. \+ merkki osoittaa, että venttiilimoottoria ajetaan auki suuntaan. - merkki osoittaa, että venttiilimoottoria ajetaan kiinni suuntaan.

```
Trendi
L1 Menovesi
   45 °C
Asento 0%
```

Jos käytössä on jänniteohjattu moottori, (0…10V tai 2...10V) näytössä näkyy, venttiilimoottorin asentotieto. (0% = kiinni, 100% = auki).

Painamalla ryhmänvaihtonäppäintä [Ryhmänvaihto] voit tarkastella muiden säätöpiirien menoveden lämpötilaa trendinäyttönä.

Poistu näytöstä **ESC**illä.

```
L1 Menov.trendi
  Trendinäyttö
▶ Näyteväli 1s
```

Jos haluat muuttaa näyteväliä, siirrä osoitin kohtaan "Näyteväli" [Selaus] -näppäimellä. Paina **OK**. Aika vilkkuu. Aseta aika **-** tai **+** -näppäimellä. Paina **OK**.

---

<a id="s28"></a>

## Sivu 28: MOOTTORIVALINTA

Moottorivalinnassa valitaan L1 ja L2 säätöpiirin venttiilimoottorin ohjaustapa sekä jakoventtiilin JV moottorin ohjaustapa. Vaihtoehtoina on joko 24VAC 3-tilaohjaus tai DC -jännite-ohjaus (0...10V tai 2...10V).

Säätöpiirin L1 venttiilimoottorin ohjauslähtö on M1.
Säätöpiirin L2 venttiilimoottorin ohjauslähtö on M2.
Maalämmityksen ML jakoventtiilin (JV) moottorin ohjauslähtö on M3.

Ohjeet huoltotilaan siirtymisestä on esitetty sivulla 24.

```
L1 Huoltotila
  Viritysarvot
  Asetusarvot
  Trendit
▶ Moottorivalinta
  JV ohjaustapa
```

Siirrä osoitin kohtaan "Moottorivalinta" [Selaus] -näppäimellä. Paina **OK**.

```
L1 Moott.valinta
▶● 3tila/aika 35s
   0-10V
   2-10V
```

Siirrä osoitin sen moottorin ohjaustavan kohdalle, jonka haluat ottaa käyttöön [Selaus] -näppäimellä. Paina **OK**.

Valittuasi moottorille ohjaustavan, säädin kysyy moottorin ajoaikaa. Ajoaika kertoo, kuinka monta sekuntia kuluu, jos moottori ajaa yhtäjaksoisesti venttiilin kiinni asennosta auki asentoon.
Aseta aika **-** tai **+** -näppäimellä. Paina **OK**.
● -merkki osoittaa, mikä ohjaustapa on valittu käyttöön.

```
ML Moott.valinta
▶● 3tila/aika 35s
   0-10V
   2-10V
```

[Ryhmänvaihto] -näppäimellä voit siirtyä säätöpiiristä toiseen.

### VENTTIILIMOOTTOREIDEN KYTKENTÄ:

**3-tilaohjattu moottori (24VAC)**

![3-tilaohjatun moottorin kytkentä](kasikirja/s28-3-tilaohjattu-moottori.png)

Kuvan kuvaus: säätimen riviliittimet 51–62 kahdessa rivissä (ylärivi 51, 53, 55, 57, 59, 61; alarivi 52, 54, 56, 58, 60, 62). Kukin kolmesta moottorista on kytketty kolmella johtimella kolmeen liittimeen; liittimiin 54, 58 ja 62 ei ole kytketty mitään. L2:n liittimet ja moottori on korostettu tummemmalla vihreällä. Moottorin liittimet ovat Auki, ⊥ ja Kiinni (3-tila 24 VAC):

| Moottori | Auki | ⊥ | Kiinni |
|---|---|---|---|
| L1 moottori (ohjauslähtö M1) | 51 | 52 | 53 |
| L2 moottori (ohjauslähtö M2) | 55 | 56 | 57 |
| JV moottori (ohjauslähtö M3) | 59 | 60 | 61 |

**0...10V tai 2...10V DC-ohjattu moottori (24 VAC)**

![DC-ohjatun moottorin kytkentä](kasikirja/s28-dc-ohjattu-moottori.png)

Kuvan kuvaus: samat riviliittimet 51–62. Kukin moottori on kytketty kolmella johtimella; liittimiin 53, 57 ja 61 ei ole kytketty mitään. L2:n liittimet ja moottori on korostettu tummemmalla vihreällä. Moottorin liittimet ovat 24 VAC, ⊥ ja 0-10V tai 2-10V:

| Moottori | 24 VAC | ⊥ | 0-10V tai 2-10V |
|---|---|---|---|
| L1 moottori (ohjauslähtö M1) | 51 | 52 | 54 |
| L2 moottori (ohjauslähtö M2) | 55 | 56 | 58 |
| JV moottori (ohjauslähtö M3) | 59 | 60 | 62 |

### JAKOVENTTIILIN OHJAUSTAPA

```
L1 Huoltotila
  Viritysarvot
  Asetusarvot
  Trendit
  Moottorivalinta
▶ JV ohjaustapa
```

```
JV ohjaustapa
▶● Autom.säätö
   Käsiajo mek.
   Käsiajo sähk.
```

**Automaattisäätö:**
Säädin ohjaa jakoventtiiliä mittauksen 7 perusteella.

**Venttiilimoottorin mekaaninen käsiajo:**
Moottori on sähkötön.
Vain mekaaninen käsikäyttö on mahdollinen.

**Venttiilimoottorin käsiajo sähköllä:** Paina **OK**.
Muuta venttiilimoottorin asentoa **-** tai **+** -näppäimellä.
Näytössä näkyy, mihin suuntaan venttiilimoottoria ajetaan.
Asennon %-luku osoittaa venttiililmoottorin asennon, mikäli käytetään jänniteohjattua 0 (2) ... 10V venttiilimoottoria (0% = kiinni, 100%=auki).

---

<a id="s29"></a>

## Sivu 29: ASETUSTEN PALAUTUS

**Asetusarvon palautus:**

1. Säädin palauttaa tehdasasetukset säätökäyrien asetuksiin
2. Poistaa kello-ohjelmoinnit
3. Palauttaa sekä käyttäjä- että huoltotason alkuasetusarvot
4. Valitsee ohjaustavaksi automaattiohjauksen
5. Valitsee säätimen tyypiksi perussäätimen
6. Tunnistaa kytketyt anturit ja tekee oletuksen käytössä olevista säätöpiireistä
7. Palauttaa tehdasasetukset viritysarvoihin ja trendien näyteväliin
8. Valitsee moottorin ohjaustavaksi 3-tilaohjauksen, jolla on ajoaikana 35 s L1:ssä ja L2:ssa
9. Väylältä ei lueta mittauksia
10. Nollaa puhelinnumeron ja palauttaa tehdasasetukset modeemiasetuksiin

Ohjeet erikoishuoltoon siirtymisestä on esitetty sivulla 24.

**Voit palauttaa tehtaan alkuasetusarvot säätimelle seuraavasti:**

```
Erikoishuolto
▶ Aset.palautus
  Asetusarvot
  Mitt.6 asetus
  LON käytt.otto
  Väylämittaukset
  Tekstiviestias.
```

Siirrä osoitin kohtaan "Erikoishuolto" [Selaus] -näppäimellä. Paina **OK**.

Osoitin on kohdassa "Aset.palautus". Paina **OK**.

```
Tehtaan alkuase-
tusten palautus
▶ Ei
  Kyllä
```

**Tehtaan alkuasetusarvon palautus:**

Siirrä osoitin kohtaan "Kyllä" [Selaus] -näppäimellä. Paina **OK**.

### TEHTAAN ALKUASETUSARVOT:

**Säätökäyrät:**

```
L1 Käyrä:
▶ -20 = 32°C
    0 = 26°C
  +20 = 19°C
```

```
L2 Käyrä:
▶ -20 = 30°C
    0 = 27°C
  +20 = 20°C
```

![L1- ja L2-käyränäyttöjen säätökäyrät](kasikirja/s29-saatokayrat.png)

Kuvan kuvaus: yllä olevien L1- ja L2-käyränäyttöjen oikea reuna, jossa on säätökäyrän kuvaaja: pystyasteikko 20, 35, 50, 65, 80 ja vaaka-asteikko 20, 0, -20 °C vasemmalta oikealle. Käyrä nousee vasemmalta oikealle eli ulkolämpötilan laskiessa ja loivenee kylmässä päässä. Käyrät on piirretty näyttöjen lukujen mukaan: L1-käyrä nousee jyrkemmin (19 °C → 32 °C), L2-käyrä loivemmin (20 °C → 30 °C).

**Ohjaustapa:**

```
L1 Ohjaustavat
▶● Autom.säätö
   Jatkuva päivä
   Jatkuva yö
   Alasajo
   Käsiajo mek.
   Käsiajo sähk.
```

```
ML Ohjaustavat
▶● Kompr.+sähköv
   Kompressori
   Sähkövastus
```

**Moottorin ohjaustapa:**

```
L1 Moott.valinta
▶● 3tila/aika 35s
   0-10V
   2-10V
```

| Käyttäjätason asetusarvot: | Tehdasasetus: |
|---|---|
| Huonelämpö | 21.5 °C |
| Yöalennus (menovedelle) | 0 °C |
| Minimiraja | 15 °C |
| Maksimiraja | 70 °C |
| Huonekompensointisuhde | 4 °C |
| Tuulikompensointisuhde | 0 °C |
| Aurinkokompensointisuhde | 0 °C |
| Esikorotus | 0 °C |
| Syyskuivaus | 2 °C |
| Venttiilin kesäsulkeutuminen | 30°C |
| VaraajaAlaMin | 30°C |
| Varaaja yläosa kesä | 55°C |
| Varaaja yläosa talvi | 65°C |
| Lisälämmitys | 50°C |
| Lisäläm.aika | 2h |
| SV-viiveaika | 30min |
| **Huoltotason asetusarvot:** | |
| Ulkolämpötilan hidastus L1/L2 | 2 h/ 0 h |
| Esikorotus | 0 h |
| Kompressorin esto | 55°C |
| Var. yläosan eroalue sähkövast. | 3°C |
| VaraajaAlaEro | 5°C |
| VaraajaYläEro | 3°C |
| JV Esiavaus | 40% |
| JV Esto | 60s |
| Maaliuos häl | -6°C |
| **Erikoishuollon asetusarvot:** | |
| Huonelämpötilan hidastus | 0.5h |
| Menov. min. 0°C:ssa L1:ssä | 10°C |
| Menov. min. 0°C:ssa L2:ssä | 10°C |
| Menov. min. -20°C:ssa L2:ssä | 30°C |
| Menov. min. -20°C:ssa L1:ssä | 30°C |
| Poikkeaman suuruus aset.arvosta, joka aih. hälytyksen L1/L2 | 75°C |
| Poikkeaman kesto, joka aih. hälyt. | 60 min |

**Starttitoiminta:**

```
Säätötapa
▶● L1 perussäädin
   L1 itseoppiva
   L1 ei käytössä
 ● L2 perussäädin
   L2 itseoppiva
   L2 ei käytössä
```

**Viritysarvot:**

```
L1 Viritysarvot
▶ P-alue: 140°C
  I-aika:  50 s
  D-aika: 0.0 s
```

```
ML Viritysarvot
▶ P-alue: 250°C
  I-aika:  25 s
  D-aika:  0.0s
```

> **Repo note:** the list names some settings differently from their menu labels on p. 21: Varaaja yläosa kesä and talvi are Var.ylä kesä and Var.ylä talvi, SV-viiveaika is SV_viiveaika, Kompressorin esto is Kompr.esto, and Var. yläosan eroalue sähkövast. is VarYläEroSv. Its VaraajaAlaEro and VaraajaYläEro agree with p. 21; p. 26 swaps them.

---

<a id="s30"></a>

## Sivu 30: ERIKOISHUOLLON ASETUSARVOT

Geopro 202S lämmönsäätimessä suurimman osan säätimen asetusarvoista voi käyttäjä asettaa (ks. asetusarvot s. 7-9). Osa säätimen toimintaa ohjaavista asetusarvoista voidaan asetella huoltotilassa (ks. s. 26) ja osa erikoishuoltotilassa. Erikoishuollossa voidaan asetella harvoin tarvittavia asetusarvoja.

Ohjeet erikoishuoltoon siirtymisestä on esitetty sivulla 24.

```
Erikoishuolto
  Aset.palautus
▶ Asetusarvot
  Mitt.6 asetus
```

Siirrä osoitin kohtaan "Asetusarvot" [Selaus] -näppäimellä. Paina **OK**.

```
Asetusarvot
▶ Huonel.hid.0.5h
  L1mv.min (0) 10
  L1mv.min(-20)10
  L2mv.min (0) 30
  L2mv.min(-20)30
  L1 Poikk.häl 75
  L2 Poikk.häl 75
  PoikHälHid60min
```

Siirry [Selaus] -näppäimellä sen parametrin kohdalle, jonka arvoa haluat muuttaa. Paina **OK**.

Muuta asetusarvoa **-** tai **+** - näppäimellä. Paina **OK**.

### TIETOJA ERIKOISHUOLLON ASETUSARVOISTA:

<table>
<tr><th>Asetusarvo:</th><th>Tehdasasetus:</th><th>Asetelualue:</th><th>Merkitys:</th></tr>
<tr><td>Huonel.hid.</td><td>0.5h</td><td>0...2</td><td>Sisälämmön keskiarvomittausten aika, jota huonekom-pensointi käyttää.</td></tr>
<tr><td>L1mv.min (0)</td><td>10°C</td><td>5...20</td><td rowspan="2">Menoveden vapaan pudotuksen alaraja säätöpiirissä L1/ L2 , kun ulkolämpötila on 0°C (alasajotoiminta).</td></tr>
<tr><td>L2mv.min (0)</td><td>10°C</td><td>5...20</td></tr>
<tr><td>L1mv.min(-20)</td><td>30°C</td><td>10...50</td><td rowspan="2">Menoveden vapaan pudotuksen alaraja säätöpiirissä L1/L2 , kun ulkolämpötila on -20°C (alasajotoiminta)</td></tr>
<tr><td>L2mv.min(-20)</td><td>30°C</td><td>10...50</td></tr>
<tr><td>L1 Poikk.häl</td><td>75°C</td><td>1...75</td><td rowspan="2">L1/L2 menoveden lämpötilan poikkeama säätimen määräämästä asetusarvosta, joka aiheuttaa hälytyksen.</td></tr>
<tr><td>L2 Poikk.häl</td><td>75°C</td><td>1...75</td></tr>
<tr><td>PoikHälHid</td><td>60min</td><td>0...90</td><td>Hälytys tapahtuu, jos poikkeama on kestänyt asetetun ajan.</td></tr>
</table>

> **Repo note:** the screen shows L1mv.min(-20) 10 and L2mv.min (0) 30. The table and the factory list on p. 29 give L1mv.min(-20) 30 °C and L2mv.min (0) 10 °C.

---

<a id="s31"></a>

## Sivu 31: MITTAUKSEN 6 ASETUS

Tässä erikoishuollon tilassa voidaan vaihtaa mittauksen 6 merkitys pelkästä vapaasta lämpötilan mittauksesta säätöpiirin L2 huonekompensoinnin tai säätöpiirien L1 ja L2 yhteisen tuuli- tai aurinkokompensoinnin mittaukseksi. Tehdasasetuksena on vapaa lämpötilan mittaus, joka on nimetty "Mittaus 6" -mittaukseksi. Nimen voi muuttaa tekstieditorilla.

Ohjeet huoltotilaan siirtymisestä on esitetty sivulla 24.

```
Erikoishuolto
  Aset.palautus
  Asetusarvot
▶ Mitt.6 asetus
```

Siirrä osoitin kohtaan "Mitt.6 asetus" [Selaus] -näppäimellä. Paina **OK**.

**Mittauksen 6 merkityksen valinta:**

```
Mitt.6 asetus
▶● Mittaus 6
   L2 Huonelämpö
   Tuulimittaus
   Aurinkomittaus
   Ei kytketty
```

Siirry [Selaus] -näppäimellä sen asian kohdalle, jonka haluat kytkeä mittaukseen 6. Paina **OK**.
● -merkki osoittaa, mikä mittaus on valittu mittaukseen 6.

Kuvan kuvaus: nuolet vievät rivistä "Mittaus 6" alla olevaan nimeämisnäyttöön ja riveistä "Tuulimittaus" ja "Aurinkomittaus" alla olevaan raja-arvon asettamiseen.

**Mittauksen 6 nimeäminen tekstieditorilla:**

```
Nimen vaihto
▶ Mittaus 6
  Anna uusi nimi
```

Mittauksessa 6 tehdasasetuksena on "Mittaus 6" -mittaus. Uudelleen nimeäminen esitellään sivulla 11.

**Tuuli- tai aurinkoanturin mittausviestin raja-arvon asettaminen:**

Tuuli- tai aurinkomittaukselle joudut asettamaan kompensointialueen raja-arvot. Minimi kertoo, missä lähettimen viestialueen kohdassa kompensointi alkaa ja maksimi kertoo, mistä viestialueen kohdasta lähtien kompensointi on maksimissaan.

Aurinko- ja tuulianturin kytkennästä lisää tietoa seuraavalla sivulla.

```
Komp./Mitt.viesti
▶ Min / 30 %
  Max / 70 %
```

Paina **OK**.
Aseta raja-arvo **-** tai **+** -näppäimellä ja hyväksy painamalla **OK**.

---

<a id="s32"></a>

## Sivu 32: Mittaus 6: Tuuli-/aurinkomittaus

Kun tuuli- tai aurinkoanturi kytketään mittaukseen 6, annetaan säätimelle ohjeet siitä, milloin tuuli- tai aurinkokompensoinnin halutaan toimivan. Kompensoinnin raja-arvot (min/max) lasketaan samalla tavalla huolimatta siitä, millainen anturi on käytössä.

Tuuli- ja aurinkokompensointisuhde kertoo, montako astetta menoveden lämpötilaa voidaan muuttaa kompensoinnin avulla ja sen voi käyttäjä asettaa (ks. asetusarvot s. 8-9).

Tuuli- ja aurinkoantureiden mittaussignaali voi olla 0...10 V, 2...10 V, 0...20 mA tai 4...20 mA. Anturit sovitetaan säätimeen vastuksien avulla niin, että säätimelle tuleva mittausviesti on aina 0...5 V.

**Kompensointialueen laskeminen**

![Tuulikompensoitu menoveden lämpötilakäyrä](kasikirja/s32-tuulikompensointi.png)

Kuva. Tuulikompensoitu menoveden lämpötilakäyrä.

Kuvan kuvaus: kaavio, jonka pystyakseli on menoveden lämpötila (°C, ei asteikkoa) ja vaaka-akseli tuulen nopeus (m/s, merkkinä tuulen symboli); oikeassa yläkulmassa on tuulimyllyn kuva. Sininen käyrä "Menovesi" on vaakasuora tuulen nopeuteen 6 m/s asti, nousee suorana 6 m/s:sta 14 m/s:iin ja on taas vaakasuora 14 m/s:sta ylöspäin. Käyrän ja sen alemman tason väliin jäävä alue on merkitty "Tuulikompensointi". Punaiset pystysuorat pisteviivat ovat kohdissa 6, 14 ja 20 m/s. Akselin alla on jana "Tuulianturin mittausalue", joka alkaa 0 V:sta ja päättyy kohtaan 20 m/s = 10 V. Janan alle on merkitty punaisella 30% (6 m/s, "min.komp. raja-arvo"), 70% (14 m/s, "max.komp. raja-arvo") ja 100% (20 m/s).

```
Komp./Mitt.viesti
▶ Min   /  30%
  Max  /  70%
```

Esimerkki: Käytössä on tuulianturi, jonka mittausalue on 0...20 m/s. Haluat, että tuulikompensointi alkaa, kun tuulen nopeus on 6m/s (min.raja) ja kompensointi saa maksimiarvon, kun tuulen nopeus on vähintään 14m/s (max raja). Laske, montako prosenttia tuulen kompensoinnin raja-arvot (min. raja ja max raja) ovat mittausalueen maksimista (=20m/s), ja aseta ne minimi- ja maksimikompensoinnin prosenteiksi.

Min. komp.raja = (min. raja / mittausalueen maks.) x 100% = (6 m/s / 20 m/s) x 100% = 30%

Maks.komp.raja = (max raja / mittausalueen maks.) x 100% = (14 m/s / 20 m/s) x 100% = 70%

Jos käytössä on nollasta lähtevät mitta-anturit ( 0...10V tai 0...20 mA), aseta yllä olevilla kaavoilla lasketut arvot minimi- ja maksimikompensoinniksi.

**Minimi- ja maksimikompensoinnin asettaminen, kun anturin mittausalue ei lähde nollasta**

| Kaavasta saatu arvo | 2-10V<br>4 -20 mA |
|---|---|
| 10 % | 28 % |
| 20 % | 36 % |
| 30 % | 44 % |
| 40 % | 52 % |
| 50 % | 60 % |
| 60 % | 68 % |
| 70 % | 76 % |
| 80 % | 84 % |
| 90 % | 92 % |
| 100 % | 100 % |

1. Laske "min.komp.raja" ja "maks.komp.raja" kaavalla kompensoinnin prosentit.

2. Katso vastaavuustaulukosta, mitkä arvot asetat säätimelle.

**Tuuli- tai aurinkoanturin kytkentä:**

![Tuuli- tai aurinkoanturin kytkentä](kasikirja/s32-anturin-kytkenta.png)

Kuvan kuvaus: kaksi kytkentäkuvaa, kummassakin ylhäällä säätimen liittimet "Mittaus 6", ⊥, 41 ja 42 ja alhaalla "Tuuli- tai aurinkomittauslähetin". Vasemmalla virtaviestilähetin (liittimet "0 - 20 mA (4 - 20 mA)", ⊥, 24 VAC, ⊥) ja punainen teksti "Lisää rinnakkaisvastus": 250Ω:n vastus on Mittaus 6:n ja ⊥:n välissä. Oikealla jänniteviestilähetin (liittimet "0 - 10 V (2 - 10 V)", ⊥, 24 VAC, ⊥) ja punainen teksti "Lisää sarja- ja rinnakkaisvastus": 1 kΩ:n vastus on Mittaus 6:n ja ⊥:n välissä, ja toinen 1 kΩ:n vastus on sarjassa lähettimen viestijohtimessa ennen Mittaus 6:ta. Kytkennät:

| Säätimen liitin | 0 - 20 mA (4 - 20 mA) -lähetin | 0 - 10 V (2 - 10 V) -lähetin |
|---|---|---|
| Mittaus 6 | 0 - 20 mA (4 - 20 mA); 250Ω Mittaus 6:n ja ⊥:n välissä | 0 - 10 V (2 - 10 V) sarjavastuksen 1 kΩ kautta; 1 kΩ Mittaus 6:n ja ⊥:n välissä |
| ⊥ | ⊥ | ⊥ |
| 41 | 24 VAC | 24 VAC |
| 42 | ⊥ | ⊥ |

---

<a id="s33"></a>

## Sivu 33: LON-KÄYTTÖÖNOTTO

Geopro 202S:än on saatavana lisävarusteena LON-200 sovitinkortti (sis. FTT-10A väyläsovitin), joka mahdollistaa säätimen liittämisen LON-kenttäväylään.
Tässä erikoishuollon tilassa ohjataan LON-200 -kortilla olevan Neuron-prosessorin ns. service pin:iä niin, että Neuron lähettää väylälle oman tunnuksensa (48 bit Neuron ID). Tämä toimenpide on tarpeellinen asennettaessa Geopro 202S + LON-200 osaksi kiinteistön LON-verkkoa.

Ohjeet erikoishuoltoon siirtymisestä on esitetty sivulla 24.

```
Erikoishuolto
  Aset.palautus
  Asetusarvot
  Mitt.6 asetus
▶ LON käytt.otto
  Väylämittaukset
```

Siirrä osoitin kohtaan "LON-käytt.otto" [Selaus] -näppäimellä. Paina **OK**.

```
LON käyttöönotto
▶ Ei
  Kyllä (Service
          switch)
```

Siirrä osoitin kohtaan "Kyllä" (service switch) [Selaus] -näppäimellä. Paina **OK**.

**Kytkentäohje:**
**Käytettäessä LON-väylää kytketään virransyötön 230VAC suojamaa säätimen riviliittimelle 81!**

![LON-väylän kytkentä](kasikirja/s33-lon-kytkenta.png)

Kuvan kuvaus: liittimet A ja C (vihreät liitinkilvet) kytketään kaapelilla LON-verkkoon. Kummankin liittimen johdin yhtyy yhdeksi viivaksi (kaapeli, merkintä "Esim. LONAK 2x1,3 mm²"), joka päättyy vaakasuoraan väylään "LON-verkko (78kbps)".

**LON-200-sovitinkortti**

![LON-200-sovitinkortti](kasikirja/s33-lon-200-sovitinkortti.png)

Kuvan kuvaus: valokuva. Vasemmalla ylhäällä on lähikuva sovitinkortista: piirilevyllä on Toshiban suuri piiri (merkinnät "TOSHIBA" ja "© ECHELON"), Echelonin väyläsovitin (merkinnät "ECHELON FTT-10A 50051 9801A"), kannassa oleva MX-muistipiiri, kaksi kondensaattoria ja kaksirivinen liitinrima. Oikealla kortti asennetaan kädellä säätimen avatun kotelon sisään, vihreiden riviliitinten yläpuolelle.

LON-200 sovitinkortin mukana toimitetaan asennus- ja käyttöönotto-ohje.

> **Repo note:** the text calls the menu item "LON-käytt.otto"; the Erikoishuolto menus on this page and p. 24 show "LON käytt.otto".

---

<a id="s34"></a>

## Sivu 34: VÄYLÄMITTAUKSET

Geopro 202S:än on saatavana lisävarusteena LON-200 sovitinkortti, joka mahdollistaa säätimen liittämisen LON-väylään ja EH-485 ja MODBUS-väyläsovitinkortit, jotka muuttavat Geopro 202S säätimen sarjaliikenneväylän RS-485 kenttäväylään yhteensopivaksi. Tässä erikoishuollon tilassa valitaan, mitä mittaustietoja luetaan väylän kautta. Jos valitsit tuuli- tai aurinkomittauksen luettavaksi väylän kautta, joudut asettamaan kompensointialueen tässä tilassa.

Ohjeet erikoishuoltoon siirtymisestä on esitetty sivulla 24.

```
Erikoishuolto
  Aset.palautus
  Asetusarvot
  Mitt.6 asetus
  LON käytt.otto
▶ Väylämittaukset
  Tekstiviestias.
```

Siirrä osoitin kohtaan "Väylämittaukset" [Selaus] -näppäimellä. Paina **OK**.

```
Väylämittaukset
▶● Ulkol.mittaus
   L1 Huonemittaus
   L2 Huonemittaus
 ● Tuulimittaus
 ● Aurinkomittaus
   Veden kulut.m3
```

Näytöstä lähtevät nuolet Ulkol.mittaus-näyttöön, Tuulimittaus-riviltä m/s-raja-arvojen näyttöön ja Aurinkomittaus-riviltä lx-raja-arvojen näyttöön.

### Väylämittausten selaus:

Selaamalla [Selaus] -näppäimellä näet, mitä mittauksia on yleensä luettavissa väylän kautta.

### Väylämittausten asettaminen:

```
Ulkol.mittaus
▶● Ei väylä
   On väylä
```

Siirrä osoitin haluamasi mittauksen kohdalle ja paina **OK**. Jos haluat valita kyseiselle mittaukselle sarjaliikenneväylän, siirrä osoitin kohtaan "On väylä" ja paina **OK**. ● -merkki osoittaa, että mittaustieto luetaan väylän kautta.

> **Repo note:** the Väylämittaukset screen marks Ulkol.mittaus with ●, which means it is read over the bus, but the Ulkol.mittaus screen has ● on Ei väylä.

### Tuuli- tai aurinkomittauksen asettaminen (väylä):

Tuuli- tai aurinkomittaukselle joudut asettamaan kompensoinnin raja-arvot. Minimi kertoo, millä arvolla kompensointi alkaa, ja maksimi kertoo, mistä arvosta lähtien kompensointi on maksimissaan. Raja-arvot asetetaan tuulimittauksessa tuulen nopeutena (m/s) ja aurinkomittauksessa valoisuuden määränä (lx).

```
Komp/Mitt.viesti
▶ Min/0.0m/s
  Max/10.0m/s
```

**Raja-arvojen asettaminen:**
Paina **OK**.
Aseta raja-arvo **-** tai **+** - näppäimellä ja hyväksy painamalla **OK**.

```
Komp/Mitt.viesti
▶ Min/   0lx
  Max/9000lx
```

Huom! Tuuli- ja aurinkokompensointisuhde asetetaan kohdassa "Asetusarvot" (ks. sivu 8-9).

---

<a id="s35"></a>

## Sivu 35: MODEEMIASETUKSET (TEKSTIVIESTIYHTEYS)

Tekstiviestiyhteys edellyttää, että säätimeen on kytketty GSM-modeemi (lisävaruste). Modeemin mukana toimitetaan D-liittimellä varustettu sovitinkaapeli, jonka avulla modeemi kytketään säätimeen. Säätimen riviliittimien B-D väli yhdistetään hyppylangalla.

GSM-modeemin käyttöönotto tapahtuu starttitoiminnassa. Säädin alustaa automaattisesti GSM-modeemin aina 2 tunnin välein. Tällä varmistetaan GSM-yhteys sähkökatkojen jälkeen.

Ohjeet erikoishuoltoon siirtymisestä on esitetty sivulla 24.

```
Erikoishuolto
  Aset.palautus
  Asetusarvot
  Mitt.6 asetus
  LON käytt.otto
  Väylämittaukset
▶ Tekstiviestias.
```

```
Tekstiv.asetuk.
  Häl.nro GSM 1
  Häl.nro GSM 2
▶ Laitetunnus
  Sanomak. nro.
  PIN-koodi
  Modeemin tyyppi
```

### Hälytysviestien vastaanottajien asettaminen:

Anna puhelinnumero, johon säädin lähettää automaattisesti tekstiviestin hälytyksestä hälytystilanteessa. Hälytysviesti lähetään aluksi vain GSM 1:n numeroon. Mikäli tästä numerosta hälytystä ei kuitata, lähettää säädin 5 minuutin kuluttua uuden hälytyksen sekä GSM 1 että GSM 2 numeroon.

```
Puhelinnumero
▶
  Muuta
```

Siirrä osoitin [Selaus] -näppäimellä kohtaan “Muuta”. Paina **OK**. “0” vilkkuu. Kirjoita puhelinnumero käyttäen tekstieditoria.

Voit siirtyä merkkijonossa eteen tai taakse päin **+** tai **-** -näppäimellä. Hyväksy numero painamalla **OK**, jolloin seuraavan numeron kohdalla vilkkuu viimeksi valittu numero. Viimeksi valittu poistetaan painamalla **ESC**. Mikäli painat pitkään yhtäjaksoisesti **ESC**-näppäintä, saadaan numero poistettua ja aikaisemmin syötetty puhelinnumero jää voimaan. Kun olet valmis, paina pitkään **OK**:ta (yli 2 sek.).

### Laitetunnus:

Säätimelle voidaan antaa laitetunnus, joka toimii laitteen salasanana ja osoitetietona. Laitetunnus on vapaasti nimettävissä. Kommunikoitaessa säätimen kanssa GSM:llä laitetunnus kirjoitetaan aina avainsanan eteen.

```
Laitetunnus
▶ Ei käytössä
  Käytössä ----
```

Siirrä osoitin kohtaan “Käytössä”. Paina **OK**. “-” vilkkuu. Kirjoita maks. 4 merkin pituinen laitetunnus. Tekstieditorilla on kirjaimet A ...Z ja numerot 0 ... 9. Voit siirtyä merkkijonossa eteen tai taakse päin **+** tai **-** -näppäimellä. Hyväksy merkki painamalla **OK**.

### Sanomakeskuksen numeron asettaminen:

```
Puhelinnumero
▶ +.....

  Muuta
```

Anna operaattorikohtainen sanomakeskuksen numero **+** tai **-** -näppäimellä. Hyväksy **OK**.

| Muutamia sanomakeskusnumeroita | |
|---|---|
| TeliaSonera | +358 40 520 2000 |
| Elisa | +358 50 877 1010 |
| Saunalahti | +358 45 110 0100 |
| DNA | +358 44 798 3500 |
| Tele Finland | +358 40 520 2330 |

### Modeemin PIN-koodin asettaminen säätimelle:

```
PIN-koodi
▶ ----
  Muuta
```

Anna SIM-kortin PIN-koodi. Säädin ei alusta GSM-modeemia ennen kuin PIN-koodi on asetettu. Modeemin PIN-koodin muuttaminen tehdään käyttämällä SIM-kortti GSM-puhelimessa. Vaihdettuasi PIN-koodin, aseta SIM-kortti takaisin modeemiin.

### Modeemin tyypin valinta:

```
Modeemin tyyppi
   Falcom
   Nokia/Siemens
▶● Ouman/Fargo
```

Geopro 202S on yhteensopiva Falcomin A2D, Nokian 30 ja Siemensin M20T ja TC35T sekä Fargon Maestro 20 modeemien kanssa. Tehdasasetuksena on Ouman/Fargo.

### Pikaohje Fargo Maestro 20 modeemin kytkennästä ja käyttöönotosta:

![Fargo-modeemin kytkentä säätimeen](kasikirja/s35-modeemin-kytkenta.png)

Kuvan kuvaus: Fargo-modeemin kytkentä säätimeen. Ylhäällä on valokuva Fargo-modeemista (Fargo modeemi) ja sen verkkolaitteesta (Verkkolaite). Modeemin kytkentäjohto haarautuu kolmeksi johtimeksi: Keltainen menee säätimen riviliittimeen A, Ruskea liittimeen B ja Vihreä liittimeen C. Hyppylanka yhdistää liittimet B ja D. Riviliittimien alla on valokuva säätimestä.

| LED merkkivalo | Modeemin tila/ toimintaohje |
|---|---|
| LED ei pala: | Modeemissa ei ole käyttöjännitettä. Kytke verkkolaite modeemiin. |
| LED palaa: | Modeemissa on käyttöjännite, mutta modeemi ei ole valmiustilassa. Tarkista seuraavat asiat:<br>1. Geopro 202S:ssä on sama PIN-koodi kuin GSM-modeemin SIM-kortin PIN-koodi.<br>2. Tee starttitoiminta. Starttitoiminta tehdään menemällä säätimellä kohtaan Starttitoiminta, painetaan OK ja poistutaan starttitilasta ESC:llä muuttamatta mitään asetuksia. |
| LED vilkkuu hitaasti: | Modeemi on valmiustilassa. |
| LED vilkkuu nopeasti: | Modeemi lähettää tai vastaanottaa viestiä. Mikäli säätimeltä ei tule viestiä tarkista lähettämästäsi tekstiviestistä, onko laitetunnus ja avainsana kirjoitettu oikein. Tarkista myös, että säätimellä on sen operaattorin sanomakeskusnumero, jonka GSM-liittymä sinulla on käytössä. Tehdasasetuksena on Saunalahden liittymä. |

---

<a id="s36"></a>

## Sivu 36: TEKSTIVIESTIASETUKSET(väyläratkaisu)

Tällä sivulla esitettävät asiat ovat voimassa silloin, kun säätimeen ei ole suoraan kytketty modeemia. Kommunikointi tapahtuu säätimen RS-485 kenttäväylän kautta. Järjestelmään voidaan liittää useita säätimiä EH-485 väyläsovitinkortin avulla ja kytkeä GSM- modeemi RS-485 kenttäväylään väyläliikennettä ohjaavan laitteen EH-686 kautta.

Jotta Geopro 202S säädin voidaan kytkeä RS-485 kenttäväylään, täytyy säätimeen asentaa EH-485 väyläsovitinkortti (ks. asennus- ja käyttöönotto-ohje EH-485 kortin mukana toimitetusta ohjeesta). Väylään kytketyille säätimille annetaan laitetunnus (esim. TC 1), jolloin järjestelmä tunnistaa, minkä säätimen kanssa milloinkin kommunikoidaan. Kommunikoitaessa säätimen kanssa avainsanan eteen kirjoitetaan aina laitetunnus.

Esimerkki väyläkytkennästä

![Esimerkki väyläkytkennästä](kasikirja/s36-esimerkki-vaylakytkennasta.png)

Kuvan kuvaus: kytkentäkuva. Ylhäällä vasemmalla on Geopro 202S (valokuvassa säädin, jossa merkintä TC01) ja sen riviliittimet järjestyksessä D, C, A, B. Ylhäällä oikealla on Fargo modeemi (Käyttöjännitesyöttö 5...32VDC). Alhaalla on Isäntälaite EH-60/ EH-686 (merkintä TC00) ja sen liittimet D-, D+, B, C, A ja ⊥. Säätimeltä isäntälaitteelle kulkee DATAJAMAK 2x(2+1)x0,24 -kaapeli, joka on piirretty yhtenä viivana; johtimet ovat samassa järjestyksessä kummassakin päässä:

| Geopro 202S | EH-60/ EH-686 |
|---|---|
| C | D- |
| A | D+ |
| B | B |
| D | ei kytketty |

Liittimeen B tulee kummassakin päässä kaksi johdinta. Kaapelin kummassakin päässä on 120 Ω vastus: säätimellä liittimien C ja A välissä, isäntälaitteella liittimien D- ja D+ välissä. Modeemin kytkentäjohdon johtimet menevät isäntälaitteelle: Vihreä liittimeen C, Keltainen liittimeen A ja Ruskea liittimeen ⊥.

> **Repo note:** this drawing puts the Controller's terminals in the order D, C, A, B; on p. 39 the strip runs A, B, C, D.

![RS-485-kenttäväylä](kasikirja/s36-rs-485-kenttavayla.png)

Kuvan kuvaus: väyläjärjestelmä. Neljä säädintä on ketjutettu punaisella viivalla RS-485 - kenttäväylään järjestyksessä TC 4, TC 3, TC 2, TC 1, ja TC 1:ltä väylä jatkuu isäntälaitteelle (Isäntälaite (I/O -master)). Isäntälaitteelta lähtee EIA-232-yhteys GSM-modeemiin (GSM-modeemi), ja katkoviiva (GSM-verkko) johtaa matkapuhelimeen, jonka näytössä on viesti:

```
TC01 MITTAUKSET:
L1 Menovesi 52/
L1 Huone 21,2/
L1 Paluuvesi 28/
```

Ohjeet erikoishuoltoon siirtymisestä on esitetty sivulla 24.

```
Erikoishuolto
  Aset.palautus
  Asetusarvot
  Mitt.6 asetus
  LON käytt.otto
  Väylämittaukset
▶ Tekstiviestias.
```

Siirrä osoitin kohtaan "Tekstiviestias.” [Selaus] -näppäimellä. Paina **OK**.

```
Tekstiv.asetuk.
▶ Häl.nro GSM1
  Häl.nro GSM2
  Laitetunnus
```

### Hälytysviestien vastaanottajien asettaminen:

GSM-puhelin voi vastaanottaa hälytyksiä ja GSM:n kautta voidaan myös kuitata hälytyksiä. Tässä annetaan puhelinnumero, johon säädin lähettää automaattisesti tekstiviestin hälytyksestä hälytystilanteessa. Hälytysviesti lähetään aluksi vain GSM 1:n numeroon. Mikäli tästä numerosta hälytystä ei kuitata, lähettää säädin 5 minuutin kuluttua uuden hälytyksen sekä GSM 1 että GSM 2 numeroon.

```
Puhelinnumero
▶
  Muuta
```

Siirrä osoitin [Selaus] -näppäimellä kohtaan “Muuta”. Paina **OK**. “0” vilkkuu. Kirjoita puhelinnumero käyttäen tekstieditoria.

Voit siirtyä merkkijonossa eteen tai taakse päin **+** tai **-** -näppäimellä. Hyväksy numero painamalla **OK**, jolloin seuraavan numeron kohdalla vilkkuu viimeksi valittu numero. Viimeksi valittu poistetaan painamalla **ESC**. Mikäli painat pitkään yhtäjaksoisesti **ESC**-näppäintä, saadaan numero poistettua ja aikaisemmin syötetty puhelinnumero jää voimaan. Kun olet valmis, paina pitkään **OK**:ta (yli 2 sek.), jolloin pääset pois kirjoitustilasta ja säädin ottaa käyttöön valitun puhelinnumeron.

### Laitetunnuksen asettaminen:

Kun tekstiviestiyhteyksissä käytetään RS-485 kenttäväylää, tunnistetaan säätimet laitetunnusten avulla. Vapaasti nimettävissä oleva 4 merkin pituinen laitetunnus toimii osoitetietona. Laitetunnus annetaan seuraavasti:

```
Laitetunnus
▶ Ei käytössä
  Käytössä ----
```

Siirrä osoitin [Selaus] -näppäimellä kohtaan “Käytössä”. Paina **OK**. “-” vilkkuu. Kirjoita maks. 4 merkin pituinen laitetunnus **-** tai **+** -näppäimellä.

### Pikaohje Fargo Maestro 20 modeemin käyttöönotosta:

| LED merkkivalo | Modeemin tila/ toimintaohje |
|---|---|
| LED ei pala: | Modeemissa ei ole käyttöjännitettä. Kytke verkkolaite modeemiin. |
| LED palaa: | Modeemissa on käyttöjännite, mutta modeemi ei ole valmiustilassa. Tarkista seuraavat asiat:<br>1. EH-60/EH-686 on sama PIN-koodi kuin GSM-modeemin SIM-kortin PIN-koodi. GSM-modeemin käyttöönottotilanteessa PIN-koodin on oltava 0000.<br>2. Käytä laitetta virrattomana modeemin kytkemisen jälkeen. |
| LED vilkkuu hitaasti: | Modeemi on valmiustilassa. |
| LED vilkkuu nopeasti: | Modeemi lähettää tai vastaanottaa viestiä. Mikäli säätimeltä/ohjauslaitteelta ei tule viestiä tarkista lähettämästäsi tekstiviestistä, onko laitetunnus ja avainsana oikein kirjoitettu. Tarkista myös, että EH-60/EH-686:ssa on sen operaattorin sanomakeskusnumero, jonka GSM-liittymä sinulla on käytössä. Oletuksena on Saunalahden liittymä. |

Yksityiskohtaiset ohjeet GSM-modeemin kytkemisestä isäntälaitteeseen saat EH-60/EH-686 käsikirjan kohdasta GSM-modeemn käyttöönotto.

---

<a id="s37"></a>

## Sivu 37: SELAINKÄYTTÖ

Jos Geopro 202S säätimeen on asennettu MODBUS-väyläsovitinkortti (lisävaruste), voidaan säädin liittää selainpohjaiseen käyttöliittymään Modbus väylän kautta EH-netin avulla.

EH-net kytketään kiinteän IP-osoitteen avulla julkiseen internet verkkoon tai paikallisverkkoon, intranettiin. Jos EH-net kytketään suoraan julkiseen IP-osoitteeseen, suosittelemme käyttämään palomuurilaitetta EH-netin ja verkon välillä.

Selainkäyttö mahdollistaa kommunikaation Geopro 202S säätimen kanssa, mistä tahansa pc:ltä. Pc:ltä on luettavissa ja muutettavissa tietoja säätimeltä. Haluttaessa voidaan rajoittaa pääsyä tiettyihin toimintoihin tai estää näkymästä sellaisia asioita, joihin liittyy turvallisuusriskejä tai jotka eivät muuten ole kohteen kannalta mielenkiintoisia.

Mikäli säädin hälyttää, tieto hälytyksestä voidaan välittää sähköpostina. Mikäli isäntälaitteeseen on kytketty GSM-modeemi, tieto hälytyksistä voidaan välittää myös tekstiviestinä GSM-puhelimeen.

Väyläsovitinkortin mukana saat yksityiskohtaiset ohjeet MODBUS-kortin asentamisesta Geopro 202S säätimeen ja käyttöönotosta. EH-netin mukana toimitetaan ohje verkkokytkennöistä ja käyttöönotosta.

![Selainkäytön järjestelmä](kasikirja/s37-selainkaytto.png)

Kuvan kuvaus: selainkäytön järjestelmäkuva. Alhaalla ovat laitteet Geopro 202S, EH-105 ja MODBUS-600 + EH-686, jotka on ketjutettu Modbus-väylällä (Modbus-väylä); väylä jatkuu oikealle katkoviivana. Väylä nousee vasemmalta EH-net-laitteelle (EH-net web-palvelin). EH-net on yhdistetty Internet/Intranet-pilveen, ja pilvestä viiva jatkuu pc:lle, jonka näytössä on EH-netin selainnäkymä. Punainen kaksipäinen salamanuoli kuvaa etäkäyttöä (Etäkäyttö pc:ltä web-selaimella), ja punainen nuoli pilvestä kohti pc:tä hälytysten siirtoa sähköpostina (Hälytysten siirto, Sähköposti). EH-netiin on kytketty GSM-modeemi, josta punainen nuoli (Hälytysten siirto) osoittaa GSM-puhelimeen (Tekstiviestinä GSM-puhelimeen).

---

<a id="s38"></a>

## Sivu 38: DATAYHTEYS (SUORAAN TIETOKONEESEEN)

Geopro 202S säädin voidaan kytkeä suoraan tietokoneeseen. Kytkentään käytetään DATAJAMAK-kaapelia.

Huom! Mikäli tiedonsiirrossa esiintyy häiriöitä, kannattaa kokeilla kaapelin vaipan kytkemistä D-25 -liittimen nastaan nro 1 (protective GND).

Windows-ympäristössä toimiva sarjaliikenneajuri Geopro 202 laitteille on vapaasti ladattavissa osoitteesta www.ouman.fi.

![Säädin kytkettynä tietokoneeseen](kasikirja/s38-datayhteys.png)

Kuvan kuvaus: pc on kytketty kaapelilla Geopro 202S -säätimeen. Kaapelin merkinnät ovat EIA-232 ja max. 25 m.

### Kytkentäohje:

**Säätimen kytkeminen suoraan PC:hen:**
D-25 liitin (naaras)

![Kytkentä PC:n D-25-liittimeen](kasikirja/s38-d-25-kytkenta.png)

Kuvan kuvaus: kytkentäkuva. Vasemmalla on PC:n D-25-liitin (PC), jonka nastat 1–13 ovat yhdessä rivissä ja 14–25 toisessa. Keskellä on PC:n signaalien ja liittimen nastanumeroiden taulukko, oikealla Geopro 202S:n riviliittimet A, B, C ja D. DATAJAMAK 2x(2+1)x0,24 -kaapeli on piirretty yhtenä viivana PC:n nastoista RX, GND ja TX säätimen liittimiin A, B ja C samassa järjestyksessä; GND ja B on piirretty kaksoisviivalla. Liitin D jää kytkemättä. RX-nastaan osoittaa nuoli, ja TX-nastasta lähtee nuoli.

<table>
<tr><th>Signaali</th><th>liittimen nastanumero</th><th>Kytkentä</th></tr>
<tr><td>RX</td><td>3</td><td>Geopro 202S, liitin A</td></tr>
<tr><td>GND</td><td>7</td><td>Geopro 202S, liitin B</td></tr>
<tr><td>TX</td><td>2</td><td>Geopro 202S, liitin C</td></tr>
<tr><td>DCD</td><td>8</td><td rowspan="3">kytketään PC päässä yhteen</td></tr>
<tr><td>DTR</td><td>20</td></tr>
<tr><td>DSR</td><td>6</td></tr>
<tr><td>RTS</td><td>4</td><td rowspan="2">kytketään PC päässä yhteen</td></tr>
<tr><td>CTS</td><td>5</td></tr>
</table>

**Säätimen kytkeminen suoraan PC:hen:**
D-9 liitin (naaras)

![Kytkentä PC:n D-9-liittimeen](kasikirja/s38-d-9-kytkenta.png)

Kuvan kuvaus: kytkentäkuva samaan tapaan kuin D-25-liittimellä. Vasemmalla on PC:n D-9-liitin (PC), jonka nastat 1–5 ovat yhdessä rivissä ja 6–9 toisessa. DATAJAMAK 2x(2+1)x0,24 -kaapeli on piirretty yhtenä viivana PC:n nastoista RX, GND ja TX Geopro 202S:n liittimiin A, B ja C samassa järjestyksessä; GND ja B on piirretty kaksoisviivalla. Liitin D jää kytkemättä.

<table>
<tr><th>Signaali</th><th>liittimen nastanumero</th><th>Kytkentä</th></tr>
<tr><td>RX</td><td>2</td><td>Geopro 202S, liitin A</td></tr>
<tr><td>GND</td><td>5</td><td>Geopro 202S, liitin B</td></tr>
<tr><td>TX</td><td>3</td><td>Geopro 202S, liitin C</td></tr>
<tr><td>DCD</td><td>1</td><td rowspan="3">kytketään PC päässä yhteen</td></tr>
<tr><td>DTR</td><td>4</td></tr>
<tr><td>DSR</td><td>6</td></tr>
<tr><td>RTS</td><td>7</td><td rowspan="2">kytketään PC päässä yhteen</td></tr>
<tr><td>CTS</td><td>8</td></tr>
</table>

> **Repo note:** this page draws no jumper between B and D; pp. 35 and 39 join B and D with one (hyppylanka).

> **Repo note:** RX and TX are the PC's signals. Terminal A goes to the PC's RX, so it carries the data the Controller sends, and terminal C goes to the PC's TX, the data the Controller receives. Page 39 names them from the same end: EIA-232 RX on A, EIA-232 TX on C.

### Geopro 202S huolto-ohjeita:

**Sulakkeen vaihto:**

![Sulakkeen vaihto](kasikirja/s38-sulakkeen-vaihto.png)

Kuvan kuvaus: valokuva avatusta säätimestä. Valkoinen nuoli osoittaa piirilevyllä olevaa mustaa sulakepesää, ja käsi pitelee irrotettua sulaketta.

Kytke säädin jännitteettömäksi. Paina sulakkeen kantaa ja kierrä vastapäivään. Vaihda 200mA (5x20mm) lasiputkisulake. Paina ja kierrä myötäpäivään sulakepesä paikoilleen.

**Pariston vaihto:**

![Pariston vaihto](kasikirja/s38-pariston-vaihto.png)

Kuvan kuvaus: valokuva piirilevystä. Valkoinen nuoli osoittaa pidikkeessä olevaa nappiparistoa (RENATA CR1220), ja meisselin kärki on pariston vieressä.

Geopro 202S:ssa on kellonajan ja kello-ohjelman säilyttävä varakäynti lyhytaikaisia sähkökatkoksia vastaan. Jos sähkökatkoksen jälkeen kellonaika ei ole oikein, on paristo vaihdettava. Paristotyyppi: Litium -nappiparisto CR 1220, 3V. Irrota säätimen sulake (ks. yläkuva).Vanha paristo kammetaan varovasti esimerkiksi ohuella meisselillä pidikkeestään. Uusi paristo työnnetään pidikkeeseen + puoli ylöspäin. Vanha paristo voidaan panna talousjätteisiin.

---

<a id="s39"></a>

## Sivu 39: YLEISKYTKENTÄKAAVIO

![Yleiskytkentäkaavio](kasikirja/s39-yleiskytkentakaavio.png)

Kuvan kuvaus: kaavio säätimen kaikista kytkennöistä. Sarakkeet ovat Kenttälaite, Kaapelointi ja GEOPRO 202S. Jokaisella rivillä kenttälaitteen nimi on vasemmalla ja sen tyyppi tai symboli Kenttälaite-sarakkeessa. Kaapeli on piirretty yhtenä viivana säätimen liitäntään (pystysuora merkintä, kuten NET tai T1), josta johtimet haarautuvat riviliittimiin; johtimet on piirretty samassa järjestyksessä kummassakin päässä. Riviliittimien oikealla puolella on liitännän nimi. ⊥ on maaliitin. Taulukoissa Kohde on rivin vasemmalla puolella oleva teksti, Liitäntä säätimen pystysuora merkintä ja Nimi riviliittimien oikealla puolella oleva teksti.

Vasemmassa yläkulmassa on laatikko "Modeemin kytkentä": Fargo-modeemin kytkentäjohdon johtimet Ke, Ru ja Vi menevät Geopro 202S säätimen liittimiin A, B ja C, ja Hyppylanka yhdistää liittimet B ja D. Laatikossa lukee:

Jos modeemi kytketään RS-485 väylään, katso kytkentä RS-485 kortin mukana toimitetusta ohjeesta

Väyläliitäntä (NET):

| Riviliitin | Kenttälaite, kaapeli DATAJAMAK 2x(2+1)x0,24 | Modeemin kytkentä |
|---|---|---|
| A | EIA-232 RX | Ke |
| B | EIA-232 GND | Ru |
| C | EIA-232 TX | Vi |
| D | kaari liittimestä B (ei nimeä) | Hyppylanka liittimestä B |

EIA-232 RX:ään osoittaa nuoli, ja EIA-232 TX:stä lähtee nuoli. Kaavion muut rivit:

| Kohde | Kenttälaite | Kaapelointi | Liitäntä | Riviliittimet | Nimi |
|---|---|---|---|---|---|
| Ulkoanturi (M1) | TMO | 2 x 0.8 | T1 | 1, ⊥ | Mitt.1 |
| L1 Menovesianturi | TMW tai TMS | 2 x 0.8 | T2 | 2, ⊥ | Mitt.2 |
| L1 Huoneanturi | TMR | 2 x 0.8 | T3 | 3, ⊥ | Mitt.3 |
| Varaajan keskiosan lämpötila-anturi (M4) | TMW tai TMS | 2 x 0.8 | T4 | 4, ⊥ | Mitt.4 |
| L2 Menovesianturi | TMW tai TMS | 2 x 0.8 | T5 | 5, ⊥ | Mitt.5 |
| Vapaa mittaus (Anna nimi tekstieditorilla) | TMW tai TMS | 2 x 0.8 | T6 | 6, ⊥ | Mitt.6 |
| Varaajan yläosan tulolämpötila-anturi (M7) | TME | 2 x 0.8 | T7 | 7, ⊥ | Mitt.7 |
| Maaliuosanturi (M8) | TMS | 2 x 0.8 | T8 | 8, ⊥ | Mitt.8 |
| Varaajan yläosan lämpötila-anturi (M9) | TME | 2 x 0.8 | T9 | 9, ⊥ | Mitt.9 |
| Lämmitys varaajan alaosan anturi (M10) | TME | 2 x 0.8 | T10 | 10, ⊥ | Mitt.10 |
| Kompressorin käyntitieto) | kosketin, piirretty kiinni | 2 x 0.8 | T11 | 11, ⊥ | Mitt.11 |
| Lisälämpöpainike | kosketin, piirretty auki | 2 x 0.8 | X1 | 21, 22 | Dig 1 |
| Kompressorin ylivirtaussuoja | kosketin, piirretty auki | 2 x 0.8 | X2 | 23, 24 | Dig 2 |
| Sähkövastuksen ylikuumenemissuoja | kosketin, piirretty auki | 2 x 0.8 | X3 | 25, 26 | Dig 3 |
| Hälytystieto säätimeltä, max. 46V, 1A (kosketin, piirretty auki) | Hälytyskeskus | 2 x 0.8 | K1 | 31, 32 | Hälytyskosketin |
| 24 VAC ulostulo | 24 VAC, ⊥ | 2 x 0.8 | AC | 41, 42 | 24 VAC lähtö |
| Moottorin ohjaus L1-piiri lähtö M1 (24 VAC) | 3-tilaohjattu moottori: Auki, ⊥, Kiinni | 3 x 0.8 | M1 | 51, 52, 53 | Moott. L1 |
| Moottorin ohjaus L2-piiri lähtö M2 (24 VAC) | 3-tilaohjattu moottori: Auki, ⊥, Kiinni | 3 x 0.8 | M 2 | 55, 56, 57 | Moott. L2 |
| Jakoventtiilin moottorin ohjaus, lähtö M3 (24 VAC) | 3-tilaohjattu moottori: Auki (Tulistimelle), ⊥, Kiinni (Varaajaan) | 3 x 0.8 | M 3 | 59, 60, 61 | Moott. JV |
| Releohjaus (230VAC, 6(1)A) Maalämpökojeen kompressorin ohjaus | L sisään, lähtö ulos | 2 x 1.5□N | RE 2 | 71, 72 | Rele 2 |
| Releohjaus, (230VAC, 6(1)A) Maalämpökojeen sähkövastuksen ohjaus | L sisään, lähtö ulos | 3 x 1.5□N | RE 1 | 73, 74, 75 | Rele 1 |
| Ryhmäkeskus virransyöttö 230 VAC | N, L | 3 x 1.5□S | 230 V 50 Hz | 83 (N), 84 (L) | |

Moottorilähtöjen johtimet riviliittimittäin. 3-tilaohjattu moottori kytketään kuten taulukossa yllä; jänniteohjattu moottori (Jänniteohjattu moottori, kaavion vasemmassa reunassa) kytketään liittimiin, jotka on piirretty sen viereen:

| Lähtö | 3-tila: Auki | 3-tila: ⊥ | 3-tila: Kiinni | Jännite: 24 VAC | Jännite: ⊥ | Jännite: 0...10V DC-ohj. |
|---|---|---|---|---|---|---|
| M1 (Moott. L1) | 51 | 52 | 53 | 51 | 52 | 54 |
| M2 (Moott. L2) | 55 | 56 | 57 | 55 | 56 | 58 |
| M3 (Moott. JV) | 59 (Tulistimelle) | 60 | 61 (Varaajaan) | 59 | 60 | 62 |

Rele 2 on piirretty sulkeutuvaksi koskettimeksi liittimien 71 ja 72 välille, auki-asentoon. Rele 1 on vaihtokosketin, jonka yhteinen napa on 73; kosketin on piirretty liittimen 74 puolelle, ja liittimen 75 kosketin on auki. Liitin 81 on suojamaaliitin (⏚), ja liittimellä 82 ei ole merkintää eikä kytkentää.

Huom! Suojajohdin kytketään,jos Geopro 202S:ään on liitetty LON-kortti.

> **Repo note:** this page rates the alarm contact (K1, terminals 31–32) max. 46V, 1A; p. 42 gives the alarm relay as 24VAC/ 1A. The label "Kompressorin käyntitieto)" has a stray parenthesis.

---

<a id="s40"></a>

## Sivu 40: LISÄVARUSTEET

### LON-200

![LON-200](kasikirja/s40-lon-200.png)

Kuvan kuvaus: valokuva LON-200-sovitinkortista (piirilevyllä ECHELON FTT-10A -piiri) ja kortin asentamisesta säätimeen.

LON-200 on sovitinkortti, joka muuttaa Geopro 202S -säätimen sarjaliikenneväylän LON-kenttäväylään yhteensopivaksi. LON-200 sovitinkortin mukana toimitetaan asennus- ja käyttöönotto-ohje.

### EH-485

![EH-485](kasikirja/s40-eh-485.png)

Kuvan kuvaus: valokuva EH-485-väyläsovitinkortista.

Geopro 202S:än on saatavana lisävarusteena EH-485 väyläsovitinkortti, joka muuttaa Geopro 202S -säätimen sarjaliikenneväylän RS-485 kenttäväylään yhteensopivaksi. Tämä tarjoaa edullisen vaihtoehdon kytkeä Geopro 202S säädin OuNet-valvomoon tai GSM-puhelimeen.

### MODBUS-200

![MODBUS-200](kasikirja/s40-modbus-200.png)

Kuvan kuvaus: valokuva MODBUS-200-sovitinkortista.

MODBUS-200 on sovitinkortti, joka muuttaa Geopro 202S säätimen sarjaliikenneväylän MODBUS RTU-kenttäväylään yhteensopivaksi. Kortilla oleva fyysinen liityntä kenttäväylään on galvaanisesti erotettu RS-485.

### GSM-modeemi

![GSM-modeemi](kasikirja/s40-gsm-modeemi.png)

Kuvan kuvaus: valokuva Fargo Maestro 20 -GSM-modeemista, jossa on antenni ja D-liittimeen kytketty johto.

GSM -modeemi mahdollistaa kommunikoinnin Geopro 202S säätimen kanssa tekstiviestien välityksellä. Selainpohjaisessa etäkäytössä hälytykset voidaan välittää tekstiviestinä GSM-puhelimeen.

### EH-686

![EH-686](kasikirja/s40-eh-686.png)

Kuvan kuvaus: valokuva kiskoon asennettavasta Ouman-yksiköstä, jonka etupaneelissa lukee EH-60.

Input/output yksikkö, joka sisältää releitä, analogia- ja digitaalituloja sekä analogialähtöjä. Yksikön avulla voidaan toteuttaa aikaohjattuja reletoimintoja, siirtää hälytyksiä digitaalitulojen kautta ja sen avulla voidaan tehdä yksittäinen säätöpiiri. EH-686 voi myös toimia Ouman RS-485 väylällä isäntälaitteena (master), jolloin sen tehtävänä on ohjata väyläliikennettä.

---

<a id="s41"></a>

## Sivu 41: HAKUSANAT

- Aikaohjaukset 14, 15, 19
- Alasajo 13, 30
- Anturivikahälytys 18
- Aurinkokompensointi 9, 31, 32,34
- Automaattisäätö 13

- Bakteerien tappotoiminto 15

- Datayhteys 38

- EH-485 väyläsovitinkortti 34, 36, 40
- EH-net 35, 38
- Esikorotuksen määrä 8, 9, 19
- Esikorotuksen kestoaika 26

- GSM-modeemi 35, 36, 40
- GSM-toiminnot 19

- Huonekompensointi 8, 19, 31, 34
- Huonelämpötilan hidastus 30
- Hyväksynnät 42
- Hälytykset 18
- Hälytysten nimeäminen 11, 18
- Hälytysten ohjaus GSM:ään 35, 36

- Input/Output yksikkö 36, 39
- Itseoppivuus 17

- Jakoventtiili 21, 23
- Jakoventtiilin ohjaustapa 28
- Jäätymissuojausrajat 30
- Jäätymisvaarahälytys 18

- Kello-ohjelmat 15
- Kenttäväylä 34
- Kielisyyden vaihto 16
- Kompressorin ohjaus 21-23
- Kosteusvaarahälytys 18
- Kytkentäohje 39
- Käsiajo 13, 19

- Laitetunnus 35, 36
- Lattialämmitys 7
- Lokasäiliöhälytys 18
- LON käyttöönotto 33
- LON-väyläsovitinkortti 33, 40
- LON-mittaukset 34
- Lämpötilan pudotus 13, 15

- Maalämmitystoiminnot 20-23
- Maalämpökojeen hälytykset 20
- Maksimiraja (menovesi) 8
- Menovesi-info 12
- Minimiraja (menovesi) 8
- Mittaukset 10, 11, 31
- Mittausten nimeäminen 11
- MODBUS-väyläsovitinkortti 34,38,40
- Modeemin kytkentä 35, 36
- Moottorivalinta 28

- Nimen vaihto 11

- Ohjauslähdöt 28

- Pakkoajo 13, 19
- Palohälytys 18, 19
- Paluuveden maksimi 30
- Paluuveden minimi 30
- Pariston vaihto 39
- PID- säätö 25
- Pintatermostaatti 7
- Poikkeamahälytys 18, 19, 30
- Poikkeamahälytyksen hidastus 30
- Päivälämpö 13, 19

- RS-485 kenttäväylä 34, 36, 40

- Selainkäyttö 37, 40
- Starttitoiminta 17
- Stand by-toiminto 13, 30
- Sulakkeen vaihto 38
- Suojausluokka 42
- Syyskuivaus 9
- Sähkövastuksen toiminta 20-23
- Säätökäyrien asetus 6, 7, 19
- Säätötapa 17

- Tehdasasetusten palautus 29
- Tekstieditori 11
- Tekstiviestiasetukset 35, 36
- Trendinäytöt 27
- Tuulikompensointi 8, 9, 31, 32, 34
- Tyyppitiedot 16

- Ulkolämpötila 11, 34
- Ulkolämpötilan hidastus 26

- Vedenpainehälytys 18, 19
- Venttiilin kesäsulkeutuminen 8,9
- Venttiilin huuhtelu 19
- Viritys 25
- Väylämittaukset 34
- Väyläsovitinkortti 33, 34, 36, 38, 40

- Yöalennus 8, 13, 19

> **Repo note:** some entries give the wrong page. EH-net, listed on pp. 35 and 38, is on p. 37, and so is the MODBUS card, which MODBUS-väyläsovitinkortti and Väyläsovitinkortti list on p. 38. Input/Output yksikkö (EH-686) is on p. 40, where the index has 39, and Pariston vaihto is on p. 38, where the index has 39.

---

<a id="s42"></a>

## Sivu 42

### Tekniset tiedot:

| | |
|---|---|
| Käyttöjännite: | 230 VAC, 50 Hz, 200m A |
| Kotelointi: | PC/ ABS |
| Suojausluokka: | Ilman kansitiivistettä IP 41 |
| Mitat (mm): | |
| Paino: | 1.2 kg |
| Kaapelointisuunta: | Ylhäältä tai alhaalta (näyttö ja näppäimistö käännettävissä). Läpivientiaihiot myös pohjassa. |
| Säädintyyppi | Lämmityspiireissä PID |
| Kello-ohjelmat: | - maks. 7 ohjelmajaksoa/ säätöpiiri (säätöpiireillä yhteensä 14 ohjelmajaksoa) |
| Mittaukset: | 10 kpl (NTC 10 kΩ) |
| Digitaalitulot: | 3 kpl<br>Digitaalituloon kytketään potentiaalivapaa kosketin (kuormitus 6…9 VDC/ 20 mA) |
| Ohjauslähdöt: | 3 kpl moottoriohjauslähtöä<br>3-tila 24 VAC tai jänniteohjaus (0…10 V tai 2…10 V)<br>Moottoreiden yhteisteho max. 25 VA |
| Releohjauslähdöt: | 1 kpl vaihtokosk. rele 230VAC/ 6(1)A<br>1 kpl sulkeutuva kosketin rele 230VAC/ 6(1)A |
| Hälytysrelelähdöt: | 1 kpl 24VAC/ 1A |
| Tiedonsiirtoliitäntä: | Vakiona:EIA-232C<br>Lisävarusteena: RS-485, MODBUS tai LON |
| Käyttölämpötila: | 0 … +50°C |
| Varastointilämpötila: | -20 … +70 °C |
| Hyväksynnät: | |
| EMC-direktiivi | 89/336/EEC, 92/31/EEC |
| - Häiriönsieto | EN 61000-6-1 |
| - Häiriöpäästöt | EN 61000-6-3 |
| Pienjännitedirektiivi | 73/23/EEC |
| - Turvallisuus | EN 60730-1 |
| Takuu: | 2 vuotta |
| Valmistaja: | Ouman Finland Oy<br>Kempele Finland<br>Puh. 0424 840 1<br>Fax 0424 840 201 |

![Säätimen mitat](kasikirja/s42-mitat.png)

Kuvan kuvaus: Mitat (mm) -kohdan piirros säätimen kotelosta vinosta kuvattuna. Leveys on 230, korkeus 145 ja syvyys 60.

Hyväksynnät-kohdan vieressä ovat CE-merkki ja FI-merkki.

### Säätöperiaatteet:

| Kuvake | Säätöperiaate |
|---|---|
| talo ja ulkolämpömittari | Ulkolämpötilan mukaan tapahtuva menoveden säätö. |
| talo, sisälämpömittari ja ulkolämpömittari | Ulkolämpötilan mukaan tapahtuva menoveden säätö, jossa mukana sisälämpötilan mittaus (huonekompensointi). |
| tuuli, talo ja ulkolämpömittari | Ulkolämpötilan mukaan tapahtuva menoveden säätö, jossa mukana tuulikompensointi. |
| aurinko, talo ja ulkolämpömittari | Ulkolämpötilan mukaan tapahtuva menoveden säätö, jossa mukana aurinkokompensointi. |
| tuuli, talo, sisälämpömittari ja ulkolämpömittari | Ulkolämpötilan mukaan tapahtuva menoveden säätö, jossa mukana sisälämpötilan mittaus (huonekompensointi) sekä tuulikompensointi. |
| aurinko, talo, sisälämpömittari ja ulkolämpömittari | Ulkolämpötilan mukaan tapahtuva menoveden säätö, jossa mukana sisälämpötilan mittaus (huonekompensointi) sekä aurinkokompensointi. |
| aurinko, tuuli, talo, sisälämpömittari ja ulkolämpömittari | Ulkolämpötilan mukaan tapahtuva menoveden säätö, jossa mukana sisälämpötilan mittaus, (huonekompensointi), aurinkokompensointi sekä tuulikompensointi. |

> **Repo note:** p. 10 counts 11 NTC measurements; this page counts 10. On p. 39, Mitt.11 is wired to the compressor's running contact (Kompressorin käyntitieto).

---

<a id="s43"></a>

## Sivu 43

*Sivulla ei ole tekstiä.*

---

<a id="s44"></a>

## Sivu 44

GEOPRO SYSTEMS OY\
Metsä-Pietilänkatu 1, PL 5\
15801 LAHTI\
Puh. (03) 857 6400\
Fax. (03) 857 6499\
geopro@oilon.com\
www.geopro.fi
