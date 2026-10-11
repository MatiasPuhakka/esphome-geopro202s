# Geopro 202S Lämmönsäädin
## Käyttö- ja Huolto-opas

This file paraphrases `Geopro 202S Käsikirja.pdf` (in this folder) in condensed Finnish. It leaves out screens, pictures and repeated key instructions, and where it disagrees with the PDF, the PDF is right. Each section names the PDF pages it comes from as "s. N". These are PDF page indexes counted from 1, which in the Käsikirja equal the printed page numbers.

The Controller's control rules (compressor, electric heater, JV) are not repeated here; `docs/controller.md` has them, each with its page.

---

## ALUKSI

*Käsikirja s. 3*

Onnittelut erinomaisesta valinnastanne! Olet hankkinut monipuolisen uuden sukupolven asuin- ja liikerakennusten lämmönsäätimen - huipputuotteen joka soveltuu mitä erilaisimpiin käyttökohteisiin ja lämmitysjärjestelmiin.

---

## KÄYTTÖPANEELI

*Käsikirja s. 3*

### Näppäimet:

- **ESC** - Paluu edelliseen näyttöön
- **▲ / ▼** - Selausnäppäimet (osoitin liikkuu ylös ja alas)
- **+ / -** - Lisää/Vähennä arvoa
- **OK** - Hyväksyntänäppäin
- **Ryhmänvaihto** - Siirtyminen säätöpiiristä toiseen (L1, L2, ML)
- **INFO** - Toimintaohjeet ja lisätiedot

Perusnäytössä **+**-näppäin näyttää vuorotellen kaikki mittaustulokset.

### Säätöpiirit:

- **L1** - Lämmityksen säätöpiiri 1
- **L2** - Lämmityksen säätöpiiri 2
- **ML** - Maalämmityskojeen ohjauspiiri

### Venttiilimoottorin symbolit:

- **▲** - Säädin ohjaa 3-tilaohjattua moottoria auki
- **▼** - Säädin ohjaa 3-tilaohjattua moottoria kiinni
- **Pylväs (0-100%)** - Jänniteohjatun venttiilimoottorin asento (0 % = 0 V tai 2 V, 100 % = 10 V)

---

## SISÄLTÖ

*Käsikirja s. 5*

### Käyttäjäopas:
- Säätökäyrien asetukset (s. 6)
- Asetusarvot (s. 8)
- Mittaukset (s. 10)
- Tietoa mittauksista ja anturikytkennöistä (s. 11)
- Menovesi-info (s. 12)
- Ohjaustavat (s. 13)
- Kellotoiminnat (s. 14)
- Kielivalinta/Tyyppitiedot (s. 16)
- Starttitoiminta (s. 17)
- Hälytykset (s. 18)
- GSM-toiminnot (s. 19)
- Maalämmitystoiminnot (s. 20)

### Huolto-opas:
- Ohjeet huoltotilaan siirtymisestä (s. 24)
- Viritysarvot (s. 25)
- Huoltotilan asetusarvot (s. 26)
- Trendit (s. 27)
- Moottorivalinta (s. 28)
- Jakoventtiilin ohjaustapa (s. 28)
- Erikoishuolto: tehdasasetusten palautus (s. 29), erikoishuoltotilan asetusarvot (s. 30), mittauksen 6 asetus (s. 31), tuuli-/aurinkomittaus (s. 32), LON-kenttäväylä (s. 33), väylämittaukset (s. 34), tekstiviestiyhteys modeemin kautta (s. 35) ja väylän kautta (s. 36), selainkäyttö (s. 37), datayhteys suoraan tietokoneeseen (s. 38)
- Huolto-ohje (s. 38)
- Yleiskytkentäohje (s. 39)
- Lisävarusteet (s. 40)
- Hakusanat (s. 41; ei toistettu tässä)
- Tekniset tiedot (s. 42)

---

## SÄÄTÖKÄYRIEN ASETUKSET

*Käsikirja s. 6–7*

Tasaisen huonelämmön perusta on juuri oikean muotoinen säätökäyrä. Geopro 202S:ssa säätökäyrää voidaan muokata kolmesta pisteestä:

1. Ulkolämpötilassa -20°C
2. Ulkolämpötilassa 0°C
3. Ulkolämpötilassa +20°C

Säädin estää väärän muotoisten käyrien asettamisen ja tekee korjausehdotuksen. Jos ulkoanturia ei ole kytketty tai se on poikki, säädin olettaa ulkolämmöksi 0°C.

### Säätökäyrän asettaminen:

1. Paina **ESC** kunnes olet "Valinta"-näytössä
2. Paina **OK**
3. Siirrä osoitin kohtaan "Säätökäyrien as" → Paina **OK**
4. Aseta menoveden lämpötila -20°C kohdalla → **OK**
5. Aseta menoveden lämpötila 0°C kohdalla → **OK**
6. Aseta menoveden lämpötila +20°C kohdalla → **OK**
7. Poistu **ESC**:llä

### Ohjeita säätökäyrän asetteluun:

**Jos pakkasella huonelämpö:**
- Laskee → Nosta käyrän asettelua -20°C:ssa
- Nousee → Laske käyrän asettelua -20°C:ssa

**Jos huonelämpö tuntuu kolealta nollakelillä:**
- Nosta käyrän asettelua 0°C:ssa

⚠️ Odota asetusten muutosten jälkeen riittävän kauan, että muutos ehtii vaikuttaa huonelämpötilaan.

### Lattialämmitystalot:

- Aseta maksimirajoitus välille +35 … +40°C
- Aseta minimirajoitus välille +20 … +25°C
- Menovesiputkeen on asennettava mekaaninen termostaatti, joka pysäyttää kiertovesipumpun ylikuumenemistilanteessa (esim. pintatermostaatti C01A)
- Aseta termostaatin asetusarvo 40-45°C

**Esimerkkikäyrät (s. 7):**

| Ulkolämpö | a) Lattialämmitys (L1) | b) Lattialämmitys, kosteat tilat (L2:n tehdasasetus) |
|-----------|------------------------|------------------------------------------------------|
| -20°C | 32°C | 30°C |
| 0°C | 26°C | 27°C |
| +20°C | 19°C | 20°C |

---

## ASETUSARVOT

*Käsikirja s. 8–9; ML-piiri myös s. 21*

### L1 ja L2 Lämmityspiirit:

| Asetusarvo | Merkitys | Tehdasasetus | Vaihteluväli |
|------------|----------|--------------|--------------|
| Huonelämpö | Käyttäjän asettama huonelämpötila | 21.5°C | 5...45°C |
| Yöalennus v. | Menoveden lämpötilan pudotus | 0°C | 0...35°C |
| Minimiraja | Menoveden alin sallittu lämpötila | 15°C | 5...95°C |
| Maksimiraja | Menoveden korkein sallittu lämpötila | 70°C | 15...125°C |
| Huonekomp.s | Huonekompensointisuhde | 4.0 | 0.0...7.0°C |
| Tuulikomp.s | Tuulikompensointisuhde | 0 | 0...7°C |
| Aurinkokomp.s | Aurinkokompensointisuhde | 0 | 0...-7°C |
| Esikorotus | Yöpudotuksen jälkeinen esikorotus | 0°C | 0...20°C |
| Syyskuivaus | Syysajan kuivauksen vaikutus | 2°C | 0...15°C |
| Vent.kesäsulk | Ulkolämpötilaraja, jossa L1-piirin venttiili sulkeutuu | 30°C | 5...50°C |

Vent.kesäsulk on 30°C sivuilla 8, 9 ja 29. Asennusohje (s. 16) sanoo tehdasasetukseksi +19°C.

### ML Maalämmityspiiri:

| Asetusarvo | Merkitys | Tehdasasetus | Vaihteluväli |
|------------|----------|--------------|--------------|
| VaraajaAlaMin | Varaajan alaosan minimilämpötila | 30°C | 30...55°C |
| SV_viiveaika | Kompressorin käyntiaika, jonka jälkeen varaajan keskiosa (M4) voi kytkeä sähkövastuksen | 30 min | 0...120 min |
| Var.ylä kesä | Varaajan yläosan asetusarvo, kun ulkolämpö ≥ +20°C | 55°C | 30...75°C |
| Var.ylä talvi | Varaajan yläosan asetusarvo, kun ulkolämpö ≤ -20°C | 65°C | 30...75°C |
| VaraajaYlä | Laskennallinen, Var.ylä kesä ja Var.ylä talvi -arvoista | - | - |
| Lisälämmitys | VaraajaAlaMin-arvo lisälämpöpainikkeen painamisen jälkeen | 50°C | 40...55°C |
| Lisäläm.aika | Lisälämmitys-arvon voimassaoloaika | 2 h | 0...6 h |

### Asetusarvojen muuttaminen:

1. Paina **ESC** kunnes olet "Valinta"-näytössä
2. Siirrä osoitin kohtaan "Asetusarvot" → **OK**
3. Valitse muutettava arvo → **OK**
4. Muuta arvoa **+/-** näppäimillä → **OK**
5. Poistu **ESC**:llä

ML-piiriin siirrytään ryhmänvaihtonäppäimellä.

---

## MITTAUKSET

*Käsikirja s. 10–11*

Geopro 202S:ssa on yhteensä 14 samanaikaista mittaustietoa (11 NTC-mittausta + 3 digitaalituloa). Näytössä näkyvät vain kytketyt mittaukset.

### Mittaukset:

| Riviliitin | Nimi | Mittausalue |
|------------|------|-------------|
| 1 | Ulkolämpö | -50...+50°C |
| 2 | L1 Menovesi | 0...+130°C |
| 3 | L1 Huone | -10...+80°C |
| 4 | VaraajaKeski | 0...+130°C |
| 5 | L2 Menovesi | 0...+130°C |
| 6 | Mittaus 6 / L2 Huone / Tuuli / Aurinko | -10...+80°C (tuuli ja aurinko % anturin alueesta) |
| 7 | Yläosa tulo (tulistimen ja sähkövastuksen jälkeen) | 0...+130°C |
| 8 | Maaliuos | -20...+60°C |
| 9 | VaraajaYlä | 0...+130°C |
| 10 | VaraajaAla | 0...+130°C |
| - | Kompr.Aika (kompressorin käyntilaskuri) | 0...9999 h |
| - | Sähköv.Aika (sähkövastuksen päälläololaskuri) | 0...9999 h |

Mittaus 11 (Mitt.11) on kompressorin käyntitieto, potentiaalivapaa kosketin (s. 11, 39). Mittausalueen ulkopuolella näytössä on - tai +, anturiviassa "err".

### Mittausten katselu:

**Pikaselaus:**
- Perusnäytössä paina **+** → Säädin näyttää vuorotellen kaikki mittaukset

**Yksityiskohtainen selaus:**
1. Valinta → Mittaukset → **OK**
2. Selaa mittauksia **▲/▼** näppäimillä
3. Poistu **ESC**:llä

### Mittauksen 6 nimeäminen:

1. Valinta → Mittaukset → Mittaus 6
2. Siirrä osoitin kohtaan "Anna uusi nimi" → **OK**
3. Kirjoita nimi tekstieditorilla → Hyväksy pitkällä **OK**:lla (yli 2 s)

### Antureiden käyttöönotto:

Ulkoanturin säädin ottaa käyttöön automaattisesti. Muiden antureiden lisäämisen tai poistamisen jälkeen on tehtävä starttitoiminta (s. 17). Anturityypit ja riviliittimet: ks. [Yleiset kytkentäohjeet](#yleiset-kytkentäohjeet).

---

## MENOVESI-INFO

*Käsikirja s. 12*

Menovesi-infossa nähdään, mistä tekijöistä säätimen määräämä menoveden lämpötila muodostuu.

### Vaikuttavat tekijät:

- **Käyrän muk.** - Säätökäyrän mukainen lämpötila
- **Huonekomp** - Huonekompensointivaikutus
- **Tuulikomp** - Tuulikompensointivaikutus
- **Aurinkokomp** - Aurinkokompensointivaikutus
- **Yö/Poissa** - Pudotuksen vaikutus
- **Esikorotus** - Esikorotuksen vaikutus
- **Syyskuivaus** - Syyskuivauksen vaikutus
- **Ulkol.hidast.** - Ulkolämpömittauksen hidastus
- **Max raj.vaik** - Maksimirajoitus
- **Min raj.vaik** - Minimirajoitus
- **Alasajo** - Vapaan pudotuksen vaikutus
- **Yhteisvaik.** - Säätimen määräämä menoveden lämpötila

### Katselu:

1. Valinta → Menovesi-info → **OK**
2. Selaa tietoja **▲/▼**
3. Poistu **ESC**:llä

---

## OHJAUSTAVAT

*Käsikirja s. 13; ML-piiri myös s. 21*

Jokaista säätöpiiriä voidaan ohjata eri ohjaustavoilla:

### L1 ja L2 Lämmityspiirit:

- **Autom.säätö** - Normaali säätö, kello-ohjatut pudotukset mahdollisia (tehdasasetus)
- **Jatkuva päivä** - Jatkuva normaali lämpötila (ei pudotuksia)
- **Jatkuva yö** - Jatkuva alennettu lämpötila
- **Alasajo** - Vapaa pudotus jäätymissuojarajaan
- **Käsiajo mek.** - Moottori sähkötön, vain mekaaninen käyttö
- **Käsiajo sähk.** - Venttiiliä ajetaan manuaalisesti sähköllä

### ML Maalämmityspiiri:

- **Kompr.+sähköv.** - Kompressori + tarvittaessa sähkövastus
- **Kompressori** - Vain maalämpö (ei sähkövastuksia)
- **Sähkövastus** - Vain sähkövastus

Jakoventtiilin ohjaustapa valitaan huoltotilassa (s. 28).

### Ohjaustavan muuttaminen:

1. Valinta → Ohjaustavat → **OK**
2. Valitse haluttu ohjaustapa → **OK**
3. Poistu **ESC**:llä

---

## KELLOTOIMINNAT

*Käsikirja s. 14–15*

Kello huomioi kesä- ja talviajan sekä karkausvuodet. Varakäynnin pariston kestoikä on noin 10 vuotta.

### Kellon asetus:

**Kellonaika:**
1. Kellotoiminnat → Kellonaika/pvm → **OK**
2. Aseta tunnit **+/-** → **OK**
3. Aseta minuutit **+/-** → **OK**

**Päivämäärä:**
1. Aseta päivä **+/-** → **OK**
2. Aseta kuukausi **+/-** → **OK**

**Vuosi ja viikonpäivä:**
1. Aseta vuosi **+/-** → **OK**
2. Aseta viikonpäivä **+/-** → **OK**

### Lämpötilan pudotusohjelmat:

Voit ohjelmoida lämmityspiirien L1 ja L2 pudotuksia haluaminasi aikoina.

**Ohjelman lisääminen:**

1. Kellotoiminnat → L1 Pudotusohj. → **OK**
2. Aseta pudotuksen aloitusaika:
   - Tunnit **+/-** → **OK**
   - Minuutit **+/-** → **OK**
3. Valitse viikonpäivät:
   - **+** = Päivä mukaan
   - **-** = Päivä pois
   - **OK** = Hyväksy
4. Aseta pudotuksen päättymisaika (sama tapa)
5. Valitse viikonpäivät → **OK**

Ohjelmajakso poistetaan poistamalla siitä kaikki viikonpäivät.

**Esimerkki (s. 15):**
- Pudotus päälle: Ma–Pe klo 19:30
- Pudotus pois: Ma–Pe klo 4:30
- Viikonloppuna pudotus kestää perjantai-illasta klo 19:30 maanantaiaamuun klo 4:30

---

## KIELI JA TYYPPITIEDOT

*Käsikirja s. 16*

### Kielen vaihto:

Geopro 202S on kaksikielinen. Yleisimmät yhdistelmät:
- Suomi / Svenska
- English / Eesti

**Vaihto:**
1. Valinta → Kieli/Språk → **OK**
2. Valitse kieli → **OK**

### Tyyppitiedot:

Näyttää säätimen:
- Mallin (GEOPRO 202S)
- Ohjelmistoversion
- Sarjanumeron

---

## STARTTITOIMINTA

*Käsikirja s. 17*

Starttitoiminnassa säädin:
- Tunnistaa kytketyt anturit
- Ottaa menovesiantureiden perusteella käyttöön säätöpiirit (L1 ja L2)
- Aktivoi antureiden vikahälytykset

### Milloin starttitoiminta tehdään:

- Kun anturi kytketään tai irrotetaan
- Käyttöönoton yhteydessä

### Säätötavan valinta:

**Perussäädin (tehdasasetus):**
- Ohjaa menoveden lämpötilaa säätökäyrän mukaisesti

**Itseoppiva säädin:**
- Muokkaa säätökäyrää automaattisesti huoneanturin palautteen perusteella
- Korjaa käyrää 0°C tai -20°C pisteessä, kun huonelämpö poikkeaa asetusarvostaan vähintään 1°C ulkolämmön ollessa vähintään 4 h alueella +5...-5°C tai -15...-25°C
- Korjausnopeus 1°C / 4 h, maksimivaikutus ±10 % käyrän asetusarvosta
- Vaatii huoneanturin TMR (ei TMR/P); ei toimi lämpötilan pudotusten aikana
- Merkitty "i"-kirjaimella säätökäyrässä

**Starttitoiminnan suoritus:**
1. Valinta → Starttitoiminta → **OK**
2. Valitse säätötapa → **OK**, tai poistu **ESC**:llä muuttamatta mitään

---

## HÄLYTYKSET

*Käsikirja s. 18; maalämpökojeen hälytykset myös s. 20*

Geopro 202S hälyttää poikkeavissa tilanteissa:
- Hälytysääni
- Hälytysilmoitus näytössä
- Hälytysreleen kosketin sulkeutuu (riviliittimet 31 ja 32)
- GSM-viesti (jos modeemi kytketty)

### Hälytystyypit:

**Anturivikahälytykset:**
- Mittausnimi + "err"
- Esim. "Hälytys! Mittaus 1 Ulkolämpö err"

**Jäätymisvaarahälytys:**
- Menoveden lämpötila alittaa vapaan pudotuksen alarajasta tai huonelämpötilan alarajasta lasketun raja-arvon
- "Jäätymisvaara! Mittaus 2 L1 Menovesi [lämpötila]"

**Poikkeamahälytys:**
- Menoveden lämpötila poikkeaa pysyvästi (tehdasasetus 60 min) säätimen määräämästä
- Raja ja kesto asetetaan erikoishuollossa (L1 Poikk.häl, PoikHälHid)

**Maalämpökojeen hälytykset:**
- Alilämpöhälytys / Mittaus 8 / Maaliuos: palaavan maaliuoksen alilämpö, raja "Maaliuos häl"
- Poikkeamahälytys / Mittaus 11 / Kompr.käynti: kompressori ohjataan päälle, mutta käyntitietoa ei tule. Säädin katkaisee kompressorin ohjauksen; hälytys kuittautuu itsestään 5 minuutin päästä, jolloin kompressori saa taas käynnistyä
- Hälytys / Dig 2 / Kompr. L-rele: kompressorin ylivirtasuoja (lämpörele) lauennut
- Hälytys / Dig 3 / Sähköv.ylik: sähkövastuksen ylikuumenemissuoja lauennut; kuitataan vain sähkövastuksen käsikuittauspainikkeella

**Ulkopuoliset hälytykset:**
- Vapaaseen mittaukseen 6 voi kytkeä potentiaalivapaan hälytyskoskettimen 30 kΩ vastuksen kanssa (sulkeutuva tai avautuva); hälytyksen voi nimetä

### Hälytyksen kuittaus:

1. Paina mitä tahansa näppäintä → Hälytysääni vaimentuu ja näyttö palaa edelliseen tilaan
2. Jos näppäimiin ei kosketa 20 sekuntiin, hälytysilmoitus palaa näyttöön, ellei vikaa ole korjattu
3. Viimeinen hälytys jää näyttöön, kunnes se kuitataan

---

## GSM-TOIMINNOT

*Käsikirja s. 19*

GSM-modeemi mahdollistaa:
- Kommunikoinnin säätimen kanssa tekstiviesteillä
- Hälytysten vastaanoton ja kuittauksen
- Käyttäjätason asetusten muuttamisen etänä
- Mittausten lukemisen

### Peruskäyttö:

**1. Avainsanojen pyytäminen:**
```
AVAINSANAT
```
Säädin lähettää listan käytettävissä olevista komennoista.

**2. Mittausten lukeminen:**
```
MITTAUKSET
```
Vastaus: "L1Menovesi=52/ L1Huone=21.5/ Ulkolämpö=-15/"

**3. Asetusarvojen lukeminen:**
```
L1 ASETUSARVOT
```

**4. Säätökäyrien lukeminen:**
```
SÄÄTÖKÄYRÄT
```

Säädin käsittelee yhden avainsanan viestiä kohden.

### Asetusten muuttaminen:

1. Pyydä nykyiset asetukset (esim. "L1 ASETUSARVOT")
2. Muokkaa säätimen lähettämää viestiä
3. Lähetä muokattu viesti takaisin
4. Säädin lähettää kuittauksen uusista asetuksista

### Laitetunnus:

Jos käytössä laitetunnus (esim. "TC1"), kirjoita se aina avainsanan eteen:
```
TC1 MITTAUKSET
```

---

## MAALÄMMITYSTOIMINNOT

*Käsikirja s. 20–23*

Säädin lämmittää varaajan alaosaa kompressorilla ja tarvittaessa sähkövastuksella S1 niin, että lämmitysverkostoon riittää lämpöä, ja yläosaa samoin niin, että saadaan lämmintä käyttövettä (s. 20).

Kompressorin, sähkövastuksen S1 ja jakoventtiilin (JV) ohjaussäännöt ovat tiedostossa `docs/controller.md`, kukin sivunumeroineen.

### Lisälämmitys:

*Käsikirja s. 20, 21, 23*

Kun odotetaan tavanomaista suurempaa käyttöveden tarvetta:
1. Paina lisälämpöpainiketta (lisävaruste, Dig 1)
2. Varaajan alaosan asetusarvo "VaraajaAlaMin" vaihtuu "Lisälämmitys"-arvoon (esim. 45°C)
3. Asetusarvo palautuu "Lisäläm.aika" kuluttua

---

## HUOLTOTILAAN SIIRTYMINEN

*Käsikirja s. 24*

Huoltotilaan pääsy vaatii huoltokoodin (4 numeroa).

### Siirtyminen:

1. Paina **ESC** kunnes olet "Valinta"-näytössä
2. Siirrä osoitin kohtaan "Huoltotila" → **OK**
3. Anna huoltokoodi numero kerrallaan **+/-** → **OK** jokaisen numeron jälkeen

### Huoltotilan valikko:

- **Viritysarvot** - PID-säätimen parametrit
- **Asetusarvot** - Huoltomiehen asetusarvot
- **Trendit** - Graafiset näytöt
- **Moottorivalinta** - Venttiilimoottorin tyyppi
- **JV ohjaustapa** - Jakoventtiilin ohjaus
- **Erikoishuolto** - Erikoistoiminnot

---

## VIRITYSARVOT

*Käsikirja s. 25*

PID-säätimen parametrit (normaalisti ei tarvitse muuttaa).

| Parametri | L1, L2 Tehdasasetus | ML Tehdasasetus | Alue |
|-----------|---------------------|-----------------|------|
| P-alue | 140°C | 250°C | 10...300°C |
| I-aika | 50 s | 25 s | 5...300 s |
| D-aika | 0.0 s | 0.0 s | 0.0...10.0 s |

**P-alue:** Menoveden lämpötilan muutoksen suuruus, jolla moottori ajaa venttiiliä 100%

**I-aika:** Jääneen poikkeaman korjausjakso

**D-aika:** Säädön reagoinnin nopeutus

⚠️ Varo vakiohuojuntaa!

Tehtaan alkuasetukset voivat poiketa taulukosta (s. 25).

---

## ASETUSARVOT (Huoltotila)

*Käsikirja s. 26; ML-piiri myös s. 21 ja 29*

### L1 ja L2 Piirit:

| Asetusarvo | Tehdasasetus | Alue | Merkitys |
|------------|--------------|------|----------|
| Ulkol.hidas | L1 2 h / L2 0 h | 0...20 h | Ulkolämmön keskiarvojakso |
| Esikorotus | 0 h | 0...5 h | Esikorotuksen kestoaika |

### ML Piiri:

| Asetusarvo | Tehdasasetus | Alue | Merkitys |
|------------|--------------|------|----------|
| Kompr.esto | 55°C | 45...55°C | Varaajan alaosan (M10) lämpötila, jossa kompressori pysäytetään aina |
| VarYläEroSv | 3°C | 0...10°C | Lisäero, jolla varaajan yläosa kytkee sähkövastuksen |
| VaraajaAlaEro | 5°C | 3...7°C | Alaosan ohjauksen eroalue |
| VaraajaYläEro | 3°C | 3...10°C | Yläosan ohjauksen eroalue |
| JV Esiavaus | 40% | 25...100% | Jakoventtiilin esiavaus ennen sähkövastuksen kytkemistä |
| JV Esto | 60 s | 30...240 s | Kiinniajon eston kesto sähkövastuksen kytkemisestä |
| Maaliuos häl | -6°C | -10...0°C | Alilämpöhälytysraja |

Kompr.esto ja VarYläEroSv ovat vain sivulla 21, eivät sivun 26 näytössä.

**Ristiriitaiset tehdasasetukset:** sivu 21 ja sivun 29 tehdasasetuslista antavat VaraajaAlaEro 5°C ja VaraajaYläEro 3°C. Sivu 26 vaihtaa ne keskenään sekä näytössä että taulukossa (VaraajaAlaEro 3°C, VaraajaYläEro 5°C). `docs/controller.md` kertoo, mitä arvoja säädin todella piti.

---

## TRENDIT

*Käsikirja s. 27*

Menoveden lämpötilan seuranta graafisella kuvaajalla.

### Käyttö:

1. Huoltotila → Trendit → **OK**
2. Katso graafinen kuvaaja → **OK**
3. Muuta tarvittaessa näyteväliä (tehdasasetus 1 s)

**Näytössä näkyy:**
- Menoveden lämpötilakäyrä
- Nykyinen lämpötila
- 3-tilamoottorin ajosuunta (+/-) tai jänniteohjatun moottorin asento (%)

---

## MOOTTORIVALINTA

*Käsikirja s. 28*

Valitaan venttiilimoottorin ohjaustapa kullekin piirille: L1 (ohjauslähtö M1), L2 (M2) ja ML:n jakoventtiili JV (M3).

### Vaihtoehdot:

- **3-tila/aika** - 24 VAC 3-tilaohjaus (+ ajoaika sekunteina)
- **0-10V** - DC-jännite-ohjaus 0...10 V
- **2-10V** - DC-jännite-ohjaus 2...10 V

### Ajoaika:

Aika (sekuntia), joka kuluu kun moottori ajaa venttiilin kiinni-asennosta auki-asentoon. Tehdasasetus: 35 s (s. 29)

### Moottorivalinnan muutos:

1. Huoltotila → Moottorivalinta → **OK**
2. Valitse ohjaustapa → **OK**
3. Aseta ajoaika **+/-** → **OK**

---

## JAKOVENTTIILIN OHJAUSTAPA

*Käsikirja s. 28*

Maalämmityksen jakoventtiili (JV) voidaan ohjata:

- **Autom.säätö** - Säädin ohjaa mittauksen 7 perusteella
- **Käsiajo mek.** - Moottori sähkötön, vain mekaaninen käyttö
- **Käsiajo sähk.** - Venttiiliä ajetaan näppäimillä

---

## ERIKOISHUOLTO

*Käsikirja s. 24*

Pääsy: Huoltotila → Erikoishuolto

### Valikko:

- **Aset.palautus** - Tehdasasetusten palautus
- **Asetusarvot** - Erikoisasetusarvot
- **Mitt.6 asetus** - Mittauksen 6 määritys
- **LON käytt.otto** - LON-väylän käyttöönotto
- **Väylämittaukset** - Väylältä luettavat mittaukset
- **Tekstiviestias.** - GSM-asetukset

---

## TEHDASASETUSTEN PALAUTUS

*Käsikirja s. 29*

### Palautus:

1. Erikoishuolto → Aset.palautus → **OK**
2. Siirrä osoitin kohtaan "Kyllä" → **OK**

### Palautus tekee seuraavat:

1. Palauttaa säätökäyrien tehdasasetukset
2. Poistaa kello-ohjelmoinnit
3. Palauttaa käyttäjä- ja huoltotason alkuasetusarvot
4. Valitsee ohjaustavaksi automaattiohjauksen
5. Valitsee säätimen tyypiksi perussäätimen
6. Tunnistaa kytketyt anturit ja olettaa niiden perusteella käytössä olevat säätöpiirit
7. Palauttaa viritysarvot ja trendien näytevälin
8. Valitsee moottorin ohjaustavaksi 3-tilaohjauksen, ajoaika 35 s L1:ssä ja L2:ssa
9. Väylältä ei lueta mittauksia
10. Nollaa puhelinnumeron ja palauttaa modeemiasetukset

Sivun 29 tehdasasetuslistassa ML Ohjaustavat -näytössä on valittuna Kompr.+sähköv.

---

## ERIKOISHUOLLON ASETUSARVOT

*Käsikirja s. 30*

| Asetusarvo | Tehdasasetus | Alue | Merkitys |
|------------|--------------|------|----------|
| Huonel.hid. | 0.5 h | 0...2 h | Sisälämmön keskiarvojakso huonekompensointia varten |
| L1mv.min (0) | 10°C | 5...20°C | L1 menoveden vapaan pudotuksen alaraja 0°C:ssa (alasajo) |
| L2mv.min (0) | 10°C | 5...20°C | L2 menoveden vapaan pudotuksen alaraja 0°C:ssa (alasajo) |
| L1mv.min(-20) | 30°C | 10...50°C | L1 menoveden vapaan pudotuksen alaraja -20°C:ssa (alasajo) |
| L2mv.min(-20) | 30°C | 10...50°C | L2 menoveden vapaan pudotuksen alaraja -20°C:ssa (alasajo) |
| L1 Poikk.häl | 75°C | 1...75°C | Hälytyksen aiheuttava poikkeama |
| L2 Poikk.häl | 75°C | 1...75°C | Hälytyksen aiheuttava poikkeama |
| PoikHälHid | 60 min | 0...90 min | Poikkeaman kesto ennen hälytystä |

Sivun 30 taulukko ja sivu 29 antavat yllä olevat arvot. Sivun 30 näytössä L1mv.min(-20) on 10 ja L2mv.min (0) 30.

---

## MITTAUKSEN 6 ASETUS

*Käsikirja s. 31–32*

Mittaus 6 voidaan määrittää:

- **Mittaus 6** - Vapaa lämpötilan mittaus, nimettävissä (tehdasasetus)
- **L2 Huonelämpö** - L2-piirin huonekompensointi
- **Tuulimittaus** - Tuulikompensointi (L1 ja L2)
- **Aurinkomittaus** - Aurinkokompensointi (L1 ja L2)
- **Ei kytketty** - Mittaus pois käytöstä

### Tuuli-/aurinkoanturin raja-arvot:

Jos valitset tuuli- tai aurinkomittauksen, aseta kompensointialueen raja-arvot prosentteina anturin mittausalueen maksimista:

- **Min** - Kompensointi alkaa (esim. 30%)
- **Max** - Kompensointi maksimissa (esim. 70%)

Anturit (0...10 V, 2...10 V, 0...20 mA tai 4...20 mA) sovitetaan vastuksilla niin, että säätimelle tuleva viesti on 0...5 V. Nollasta alkamattomille antureille sivulla 32 on muuntotaulukko.

---

## LON-KÄYTTÖÖNOTTO

*Käsikirja s. 33*

LON-200 sovitinkortti mahdollistaa säätimen liittämisen LON-kenttäväylään.

### Käyttöönotto:

1. Erikoishuolto → LON käytt.otto → **OK**
2. Siirrä osoitin kohtaan "Kyllä (Service switch)" → **OK**

Tämä ohjaa Neuron-prosessorin service pin:iä lähettämään tunnuksensa väylälle (48 bit Neuron ID).

### Kytkentä:

- Kytke virransyötön 230VAC suojamaa riviliittimelle 81
- LON-verkko (78 kbps): Esim. LONAK 2x1,3 mm²

---

## VÄYLÄMITTAUKSET

*Käsikirja s. 34*

Mittaustietojen lukeminen väylän kautta (LON-200, EH-485 tai MODBUS-sovitinkortti).

### Väylältä luettavissa olevat mittaukset:

- Ulkolämpötila
- L1 Huonelämpötila
- L2 Huonelämpötila
- Tuulimittaus (m/s)
- Aurinkomittaus (lux)
- Veden kulutus (m³)

### Väylämittauksen asettaminen:

1. Erikoishuolto → Väylämittaukset → **OK**
2. Valitse mittaus → **OK**
3. Siirrä osoitin kohtaan "On väylä" → **OK**

### Tuuli-/aurinkokompensointialueen asetus (väylä):

**Tuulimittaus:**
- Min: Tuulen nopeus, jossa kompensointi alkaa (m/s)
- Max: Tuulen nopeus, jossa kompensointi on maksimissa (m/s)

**Aurinkomittaus:**
- Min: Valoisuus, jossa kompensointi alkaa (lux)
- Max: Valoisuus, jossa kompensointi on maksimissa (lux)

---

## TEKSTIVIESTIASETUKSET (Suora GSM-modeemi)

*Käsikirja s. 35*

GSM-modeemi kytketään säätimeen modeemin mukana tulevalla sovitinkaapelilla. Säätimen riviliittimien B ja D väli yhdistetään hyppylangalla (ks. myös s. 39). Säädin alustaa modeemin starttitoiminnassa ja sen jälkeen 2 tunnin välein.

### Asetukset:

**1. Hälytysnumerot:**
- GSM 1: Ensisijainen hälytyksen vastaanottaja
- GSM 2: Toissijainen vastaanottaja (jos GSM 1 ei kuittaa 5 min sisällä, viesti lähtee molempiin)

**2. Laitetunnus:**
- Enintään 4 merkin tunnus (esim. "TC01")
- Toimii laitteen salasanana ja osoitteena
- Kirjoitetaan avainsanan eteen GSM-viesteissä

**3. Sanomakeskuksen numero:**
- Operaattorikohtainen numero
- Esimerkkejä:
  - TeliaSonera: +358 40 520 2000
  - Elisa: +358 50 877 1010
  - Saunalahti: +358 45 110 0100 (tehdasasetus)
  - DNA: +358 44 798 3500
  - Tele Finland: +358 40 520 2330

**4. PIN-koodi:**
- SIM-kortin PIN-koodi
- Säädin ei alusta modeemia ennen kuin PIN-koodi on asetettu

**5. Modeemin tyyppi:**
- Falcom
- Nokia/Siemens
- Ouman/Fargo (tehdasasetus)

### Fargo Maestro 20 modeemin LED-merkkivalot:

| LED-tila | Merkitys |
|----------|----------|
| Ei pala | Ei käyttöjännitettä - kytke verkkolaite |
| Palaa | Käyttöjännite OK, mutta ei valmiustilassa - tarkista PIN-koodi ja tee starttitoiminta |
| Vilkkuu hitaasti | Modeemi valmiustilassa |
| Vilkkuu nopeasti | Modeemi lähettää/vastaanottaa viestiä |

---

## TEKSTIVIESTIASETUKSET (Väyläratkaisu)

*Käsikirja s. 36*

Kun modeemia ei ole kytketty suoraan säätimeen, vaan säätimet kytketään RS-485 kenttäväylään EH-485 väyläsovitinkortilla ja GSM-modeemi väylään EH-686 (tai EH-60) laitteen kautta.

### Asetukset:

**1. Hälytysnumerot:**
- Sama kuin suorassa kytkennässä

**2. Laitetunnus:**
- Pakollinen väyläkäytössä
- Tunnistaa säätimen väylässä
- Esim. "TC01", "TC02", jne.

### Väyläkytkentä:

```
RS-485 kenttäväylä:
[Geopro 202S] --+
[Geopro 202S] --|-- [EH-686] -- [GSM-modeemi]
[Geopro 202S] --+
```

Jokaisella säätimellä oma laitetunnus → Viestit osoitetaan laitetunnuksella.

---

## SELAINKÄYTTÖ

*Käsikirja s. 37*

MODBUS-väyläsovitinkortin avulla säädin voidaan liittää EH-net web-palvelimeen.

### Järjestelmä:

```
Internet/Intranet
     |
  EH-net (web-palvelin)
     |
  MODBUS-väylä
     |
  Geopro 202S säätimet
```

### Ominaisuudet:

- Etäkäyttö mistä tahansa PC:ltä web-selaimella
- Tietojen lukeminen ja muuttaminen
- Käyttöoikeuksien rajoitus
- Hälytysten välitys sähköpostilla
- Hälytysten välitys tekstiviestillä (jos isäntälaitteeseen on kytketty GSM-modeemi)

---

## DATAYHTEYS PC:HEN

*Käsikirja s. 38; sama kytkentä s. 39 (NET)*

Geopro 202S voidaan kytkeä suoraan tietokoneeseen DATAJAMAK-kaapelilla (EIA-232, max. 25 m).

### Kytkentä:

**Säätimen riviliittimet (väyläliitäntä NET):**
- A - säätimen lähettämä data (PC:n RX)
- B - EIA-232 GND
- C - säätimen vastaanottama data (PC:n TX)
- D - ei käytössä PC-kytkennässä (s. 38). Sivun 39 kaaviossa ja modeemikytkennässä (s. 35) B ja D yhdistetään hyppylangalla.

Sivut 38 ja 39 nimeävät signaalit PC:n (kenttälaitteen) päästä: sivun 39 "EIA-232 RX" menee liittimeen A ja "EIA-232 TX" liittimeen C.

**PC:n sarjaportti:**

| Signaali | D-25 nasta | D-9 nasta | Säätimen liitin |
|----------|------------|-----------|-----------------|
| RX | 3 | 2 | A |
| GND | 7 | 5 | B |
| TX | 2 | 3 | C |

- PC:n päässä yhdistetään DCD, DTR ja DSR (D-25: 8, 20, 6; D-9: 1, 4, 6) sekä RTS ja CTS (D-25: 4, 5; D-9: 7, 8)
- Kaapeli DATAJAMAK 2x(2+1)x0,24. Häiriöiden sattuessa kokeile kaapelin vaipan kytkemistä D-25 -liittimen nastaan 1 (protective GND)

### Ohjelmisto:

Windows-ympäristössä toimiva sarjaliikenneajuri Geopro 202 laitteille on vapaasti ladattavissa osoitteesta www.ouman.fi

---

## HUOLTO-OHJEET

*Käsikirja s. 38*

### Sulakkeen vaihto:

1. Kytke säädin jännitteettömäksi
2. Paina sulakkeen kantaa ja kierrä vastapäivään
3. Vaihda 200 mA (5x20 mm) lasiputkisulake
4. Paina ja kierrä myötäpäivään sulakepesä paikoilleen

### Pariston vaihto:

**Milloin vaihtaa:**
- Jos sähkökatkoksen jälkeen kellonaika ei ole oikein

**Paristotyyppi:**
- Litium-nappiparisto CR 1220, 3V

**Vaihto:**
1. Irrota säätimen sulake
2. Kammaa vanha paristo varovasti pidikkeestään
3. Työnnä uusi paristo pidikkeeseen (+ puoli ylöspäin)
4. Vanha paristo voidaan panna talousjätteisiin

---

## YLEISET KYTKENTÄOHJEET

*Käsikirja s. 39; anturit myös s. 11, moottorit s. 28*

Riviliittimet kytkentäkaavion (YLEISKYTKENTÄKAAVIO) mukaan.

**Varoitus:** Riviliittimissä 83–84 on säätimen 230 VAC verkkojännite (N/L). Releliittimet 71–75 kytkevät maalämpökojeen 230 VAC piirejä.

### Antureiden kytkentä:

Jokaisella mittauksella on oma riviliitin ja oma maaliitin (⊥).

| Riviliitin | Mittaus | Anturi | Tyyppi | Kaapeli |
|------------|---------|--------|--------|---------|
| 1 + ⊥ | T1 (Mitt.1) | Ulkolämpö (M1) | TMO | 2x0.8 |
| 2 + ⊥ | T2 (Mitt.2) | L1 Menovesi (M2) | TMW/TMS | 2x0.8 |
| 3 + ⊥ | T3 (Mitt.3) | L1 Huone | TMR | 2x0.8 |
| 4 + ⊥ | T4 (Mitt.4) | VaraajaKeski (M4) | TMW/TMS | 2x0.8 |
| 5 + ⊥ | T5 (Mitt.5) | L2 Menovesi (M5) | TMW/TMS | 2x0.8 |
| 6 + ⊥ | T6 (Mitt.6) | Vapaa mittaus | TMW/TMS | 2x0.8 |
| 7 + ⊥ | T7 (Mitt.7) | Yläosa tulo (M7) | TME | 2x0.8 |
| 8 + ⊥ | T8 (Mitt.8) | Maaliuos (M8) | TMS | 2x0.8 |
| 9 + ⊥ | T9 (Mitt.9) | VaraajaYlä (M9) | TME | 2x0.8 |
| 10 + ⊥ | T10 (Mitt.10) | VaraajaAla (M10) | TME | 2x0.8 |
| 11 + ⊥ | T11 (Mitt.11) | Kompr.käynti (potentiaalivapaa kosketin) | - | 2x0.8 |

Sivulla 11 on NTC-anturien vastusarvotaulukko (10 000 Ω 25°C:ssa).

### Venttiilimoottorien kytkentä:

Moottorikaapeli 3x0.8.

**3-tilaohjattu moottori (24 VAC):**
- M1 (L1): Liittimet 51 (auki), 52 (⊥), 53 (kiinni)
- M2 (L2): Liittimet 55 (auki), 56 (⊥), 57 (kiinni)
- M3 (JV): Liittimet 59 (auki, tulistimelle), 60 (⊥), 61 (kiinni, varaajaan)

**Jänniteohjattu moottori (0-10V tai 2-10V):**
- M1 (L1): Liittimet 51 (24 VAC), 52 (⊥), 54 (ohjausjännite)
- M2 (L2): Liittimet 55 (24 VAC), 56 (⊥), 58 (ohjausjännite)
- M3 (JV): Liittimet 59 (24 VAC), 60 (⊥), 62 (ohjausjännite)

### Releohjaukset:

**Rele 1 (RE 1, Sähkövastus):**
- Liittimet 73-74-75
- 230 VAC, 6(1) A
- Vaihtokosk. rele
- Kaapeli 3x1.5 N

**Rele 2 (RE 2, Kompressori):**
- Liittimet 71-72
- 230 VAC, 6(1) A
- Sulkeutuva kosketin
- Kaapeli 2x1.5 N

**Hälytyskosketin (K1):**
- Liittimet 31-32
- Max. 46 V, 1 A (s. 39; sivuilla 18 ja 42 24 VAC / 1 A)
- Sulkeutuva kosketin, kytketään kiinteistön hälytyskeskukseen
- Kaapeli 2x0.8

### Muut liittimet:

- 24 VAC lähtö (AC): Liittimet 41-42
- Väyläliitäntä (NET): Liittimet A, B, C, D, kaapeli DATAJAMAK 2x(2+1)x0,24; B ja D yhdistetty hyppylangalla. Signaalit: ks. [Datayhteys PC:hen](#datayhteys-pchen)
- Suojamaa (PE): Liitin 81, kytketään jos säätimeen on liitetty LON-kortti
- Virransyöttö 230 VAC 50 Hz: Liittimet 83 (N) ja 84 (L), kaapeli 3x1.5 S

### Digitaalitulot:

Kaapeli 2x0.8.

- Dig 1 (X1), liittimet 21-22: Lisälämpöpainike (potentiaalivapaa kosketin)
- Dig 2 (X2), liittimet 23-24: Kompressorin ylivirtaussuoja (sulkeutuva)
- Dig 3 (X3), liittimet 25-26: Sähkövastuksen ylikuumenemissuoja (sulkeutuva)

---

## TEKNISET TIEDOT

*Käsikirja s. 42*

### Sähköiset ominaisuudet:

- **Käyttöjännite:** 230 VAC, 50 Hz, 200 mA
- **Suojausluokka:** IP 41 (ilman kansitiivistettä)
- **Käyttölämpötila:** 0 ... +50°C
- **Varastointilämpötila:** -20 ... +70°C

### Mekaniikka:

- **Kotelointi:** PC/ABS
- **Mitat:** 230 x 145 x 60 mm
- **Paino:** 1.2 kg
- **Kaapelointi:** Ylhäältä tai alhaalta (näyttö ja näppäimistö käännettävissä)

### Säätö:

- **Säädintyyppi:** PID-säädin lämmityspiireissä
- **Säätöperiaatteet:** ulkolämpötilan mukaan, lisänä huone-, tuuli- ja aurinkokompensointi tai niiden yhdistelmät

### Mittaukset:

- **10 kpl NTC 10kΩ lämpötilan mittausta** (sivu 10 sanoo 11 NTC-mittausta)
- **3 kpl digitaalituloa**, potentiaalivapaa kosketin, 6-9 VDC/20 mA

### Ohjauslähdöt:

**Moottoriohjaus:**
- 3 kpl moottoriohjauslähtöä
- 3-tila 24 VAC tai jänniteohjaus (0-10V tai 2-10V)
- Moottoreiden yhteisteho max. 25 VA

**Releohjaus:**
- 1 kpl vaihtokosk. rele 230 VAC/6(1) A
- 1 kpl sulkeutuva kosketin 230 VAC/6(1) A
- 1 kpl hälytysrele 24 VAC/1 A

### Kello-ohjelmat:

- Max. 7 ohjelmajaksoa/säätöpiiri
- Yhteensä 14 ohjelmajaksoa

### Tiedonsiirto:

- **Vakiona:** EIA-232C
- **Lisävarusteena:** RS-485, MODBUS tai LON

### Hyväksynnät:

**EMC-direktiivi (89/336/EEC, 92/31/EEC):**
- Häiriönsieto: EN 61000-6-1
- Häiriöpäästöt: EN 61000-6-3

**Pienjännitedirektiivi (73/23/EEC):**
- Turvallisuus: EN 60730-1

### Takuu:

- 2 vuotta

### Valmistaja:

**Ouman Finland Oy**, Kempele, Finland. Puh. 0424 840 1, Fax 0424 840 201.

---

## LISÄVARUSTEET

*Käsikirja s. 40; modeemimallit s. 35, EH-net s. 37*

### LON-200
Sovitinkortti, joka muuttaa säätimen sarjaliikenneväylän LON-kenttäväylään yhteensopivaksi. Sisältää FTT-10A väyläsovittimen.

### EH-485
Väyläsovitinkortti, joka muuttaa säätimen sarjaliikenneväylän RS-485 kenttäväylään yhteensopivaksi. Mahdollistaa liittämisen OuNet-valvomoon tai GSM-puhelimeen.

### MODBUS-200
Sovitinkortti, joka muuttaa säätimen sarjaliikenneväylän MODBUS RTU-kenttäväylään yhteensopivaksi. Galvaanisesti erotettu RS-485 liityntä.

### GSM-modeemi
Mahdollistaa kommunikoinnin säätimen kanssa tekstiviestien välityksellä. Yhteensopivat mallit (s. 35):
- Falcom A2D
- Nokia 30
- Siemens M20T ja TC35T
- Fargo Maestro 20

### EH-686
Input/output yksikkö, joka sisältää:
- Releitä
- Analogia- ja digitaalituloja
- Analogialähtöjä
- Voi toimia RS-485 väylän isäntälaitteena (master)

### EH-net
Web-palvelin (s. 37), joka mahdollistaa:
- Selainkäytön
- Etäkäytön internetin/intranetin kautta
- Hälytysten välityksen sähköpostilla
