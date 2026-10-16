# BergPro – oberoende säkerhetsgranskning (sprängteknisk påverkan)

**Datum:** 2026-10-14
**Granskare:** AI-assistent (Claude), oberoende av den som byggde appen. Detta är **inte** en fackgranskning av behörig sprängtekniker och ersätter inte en sådan.
**Granskat:** `index.html` (byggd från `src/`), `src/core.js`, `src/catalog.js`, `src/ui1.js`, `src/ui2.js`, `src/ui3.js`, `src/tests.js`, `src/style.css`, `README.md`, `FORMELGRANSKNING.md`.
**Metod:**
- Läst all källkod som påverkar beräkningar, presentation, lagring och export.
- Kört självtestet (`node run-tests.js`): 133/133 godkända, 59 kalkylatorer, 63 formler.
- Kört beräkningsmotorn direkt i Node med normala, felaktiga och extrema indata (se bilaga A).
- Kört appen i Chromium (Playwright, `file://`, 390 px bredd). Kontrollerat kalkylatorsidan före och efter beräkning, kopierad text, spara/döp om, historik, startsida, favoriter, sökning (inklusive Enter), kategorisidor, formelsidor, självtest, projektrapport (TXT, CSV, JSON, utskrift) och utskrift av ett enskilt resultat. Inga JS-fel uppstod.
- Inga filer under `/home/claude/bergpro` har ändrats.

> Granskningen anger medvetet **inga** egna värden för K, försättning, laddningskoncentration, fördröjning, tändsteg eller gränsvärden. Siffror som 20,81 m/s eller 38,4 ms nedan är bara aritmetik på anteckningens egna exempelindata eller avsiktligt orimliga testindata. De är inte rimlighetsbedömda och får inte användas som underlag.

---

## 1. Sammanfattning

Appen följer i stort ägarens krav:
- Inga gränsvärden för vibration eller luftstötvåg.
- Inga förifyllda värden för K, B eller l.
- Ingen avrundning till tändarsteg och inga föreslagna fördröjningar.
- Borrkalkylatorerna dimensionerar inga salvor.
- Formlerna är typklassade.

Huvudrisken är kalkylatorn **`blast_model`** (”Hastighet och tid enligt egen modell”). Den producerar en tid i millisekunder som appen själv benämner och indexerar som en **fördröjning/tändsekvens**. Dessutom försvinner statusen ”ej verifierad” på flera ställen där resultatet lämnar kalkylatorsidan: kopierad text, historik, sparade resultat, startsidan, favoriter, sökning, CSV från historiken och JSON.

De öppna frågorna i modellen visas inte där siffran räknas fram. Det gäller λ-inkonsekvensen, som ger en faktor 2 i t, och vad v egentligen är.

| Allvarlighet | Antal |
|---|---|
| Kritisk | 0 |
| Hög | 5 |
| Medel | 11 |
| Låg | 10 |

**Varför inget fynd är Kritiskt:** Appen rekommenderar aldrig någon fördröjning, avrundar inte till tändarsteg och visar en tydlig varning direkt efter beräkningen. Den presenterar inte heller modellen som verifierad någonstans. De Höga fynden handlar om att statusen och de öppna frågorna går förlorade eller döljs på vägen. Sammantaget gör det att ett ms-värde ur en ej verifierad modell kan hamna i en tändplan utan att någon ser att det är overifierat.

**Allvarlighetsgrader:**
- **Kritisk:** appen ger själv ett direkt felaktigt eller farligt beslutsunderlag (rekommenderat värde, gränsvärde, falsk verifiering).
- **Hög:** troligt att ett overifierat resultat används som sprängtekniskt underlag utan att statusen syns.
- **Medel:** kan vilseleda eller försvaga spårbarheten, men kräver fler felsteg.
- **Låg:** kosmetiskt, dokumentation eller kantfall.

---

## 2. Översikt över fynd

| ID | Grad | Plats | Kort beskrivning |
|---|---|---|---|
| H1 | Hög | `ui1.js:243–252`, `catalog.js:410–419` | Kalkylatorsidan visar inte λ-inkonsekvensen, frågan om vad v är eller formeln för t. Statusen syns bara i dämpad text. |
| H2 | Hög | `catalog.js:20, 415, 419, 420, 435`, `ui3.js:240` | t ramas in som tändfördröjning: namnet ”Fördröjningstid”, synonymer som ”tändsekvens” och ”tid mellan rader”, ms med 6 siffror, och sökning + Enter öppnar modellen direkt. |
| H3 | Hög | `ui2.js:216–221`, `ui3.js:143, 150` | Kopierad text (från resultat och historik) saknar status och varning. |
| H4 | Hög | `ui3.js:97–107, 127–131`, `ui2.js:222–236`, `ui1.js:135, 143–145` | Historik, sparade resultat, startsida och historik-CSV saknar status. Ett sparat resultat kan döpas om till t.ex. ”Tändplan rad 2” och listas som ”Sparade mätningar”. |
| H5 | Hög | `tests.js:160–171`, `catalog.js:409` | Självtestet visar ett appvalt λ = 80 % (anteckningen säger 40 %) → ”≈ 76,9 ms” med grönt OK. Verifieringstexten säger att det är kontrollerat ”mot anteckningarnas exempel”. |
| M1 | Medel | `ui3.js:13–21, 29–76` | Rapporterna (TXT/CSV/utskrift) saknar varningstexten, formeln för t samt enhet för l och K. Statusen står sist och i liten stil. |
| M2 | Medel | `ui3.js:179`, `core.js:321` | Projekt-JSON och full JSON-export saknar status och formeltyp. |
| M3 | Medel | `ui1.js:163`, `ui2.js:250`, `README.md:29` | Friskrivningar som säger att tändsekvensmodeller ”ingår inte” stämmer inte längre. |
| M4 | Medel | `catalog.js:411, 421–426` | Enheter: K märks som dimensionslös, B har fri enhetsväljare, l saknar enhetsfält och λ > 100 % accepteras. |
| M5 | Medel | `ui1.js:298–308`, `style.css:166–168` | Resultatkortet ser ut som för verifierade formler och varningen ligger under Kopiera/Spara/Skriv ut. |
| M6 | Medel | `core.js:65`, `catalog.js:435–436` | Falsk precision: t.ex. 38,4376 ms från en overifierad modell. |
| M7 | Medel | `catalog.js:315–329` | Mätserie räknar medel/RMS/s på dB-värden utan varning, och statistik över separata toppvärden förklaras inte. |
| M8 | Medel | `ui2.js:150–157`, `ui3.js:160–164` | Mätjournal → mätserie blandar alla projekt, platser och instrument. |
| M9 | Medel | `ui2.js:55–70` | Mätjournalen saknar fält för topp/RMS, komponent, frekvens, vägning och salvreferens. |
| M10 | Medel | `catalog.js:24–30, 479, 514` | ”Verifierad teknisk modell” (grönt) används för formler som en AI kontrollerat mot sekundärkällor. |
| M11 | Medel | `ui2.js:158–171` | Sprickfrekvensen räknas på alla sprickor i registret mot en enda global mätlinjelängd. |
| L1 | Låg | `core.js:281` | Förvald favorit (ägarens val) visas utan status och återkommer efter ”Radera all lokal data” eller vissa importer. |
| L2 | Låg | `catalog.js:519` | ”Se säkerhetsgranskningen” hänvisar till ett dokument som inte finns i appen. |
| L3 | Låg | `catalog.js:426`, `ui1.js:187` | Etiketten visar ”(valfritt) (valfritt)” och exporteras med ”(valfritt)” i namnet. |
| L4 | Låg | `tests.js:119` | Testnamnet säger ”typiska värden”. |
| L5 | Låg | `catalog.js:285–290` | Sinus topp/RMS accepterar dB som enhet. |
| L6 | Låg | `README.md:30, 33–34` | README säger ”inga klassgränser”, men RQD-klasser finns. Testsiffrorna är föråldrade. |
| L7 | Låg | `ui3.js:13–21` | Rapporten visar formelstatus nu, inte vid beräkningen. Ingen formelversion per block och lagrade resultat räknas inte om. |
| L8 | Låg | `catalog.js:647–685` | Sökning på ”gränsvärde”, ”riktvärde” eller ”tillåten” ger inget klart besked om att appen saknar gränsvärden. |
| L9 | Låg | `catalog.js:250` | RQD: varningen vid < 50 % registrerad kärna är en tröskel som appen själv valt. |
| L10 | Låg | `catalog.js:29` | Typnamnet ”Ej verifierad referens” passar dåligt för en egen modell. |

---

## 3. Detaljerade fynd

### H1 – Kalkylatorsidan döljer modellens öppna frågor och formeln för t
**Grad:** Hög
**Plats:** `src/ui1.js:243–252` (`VIEWS.calc`), `src/ui1.js:215–221` (`metaCard`), `src/catalog.js:410–419`.

**Vad är fel:**
- Kalkylatorn kopplas bara till formeln `blast_v` (`f: 'blast_v'`). Därför visar formelkortet bara `v = K/B^a · l^b`. Formeln `t = λ / v` och symbolerna λ och t finns inte i symboltabellen.
- Den hopfällda panelen ”Antaganden, giltighetsområde och källa” visar bara `blast_v`:s antaganden. De två viktigaste förbehållen ligger bara i `blast_t:s` assump, som syns på en separat formelsida som man inte når från kalkylatorn:
  - anteckningens exempel säger ”40 % av B = 1,6” trots att 40 % av 2 m är 0,8 m
  - det är oklart vad v är
- Före beräkning syns statusen bara i den dämpade beskrivningstexten (”ej verifierad modell”). Badgen ”Ej verifierad referens” ligger i en stängd `<details>`. Kontrollerat i Playwright: båda panelerna har `open=false`.
- Förbehållet om v nämner bara två tolkningar (”partikel- eller fortplantningshastighet”). Den tolkning som orden ”hastighet på bergmassan” och ”förflyttning före nästa rad” närmast pekar på, alltså bergmassans eller försättningens rörelsehastighet, nämns inte. De tre är olika fysikaliska storheter. Anteckningens enhet ”m/s” avgör inte vilken som avses.

**Varför det spelar roll:** Tolkningen av λ ändrar t med en faktor 2. Med anteckningens 40 % blir t ungefär hälften av anteckningens eget slutresultat. Om v tolkas som en annan storhet blir hela t meningslöst. Användaren som räknar ser inget av detta.

**Åtgärd:**
1. Visa en fast varningsruta överst på `#/calc/blast_model`, före Indata och oberoende av beräkning. Den ska innehålla:
   - ”EJ VERIFIERAD egen modell”
   - λ-inkonsekvensen ordagrant från anteckningen, med upplysningen att tolkningen ändrar t med en faktor 2
   - ”v:s fysikaliska innebörd är inte fastställd (rörelsehastighet för bergmassan, partikelhastighet eller vågutbredningshastighet är olika storheter)”
2. Visa båda formlerna i formelkortet (stöd för `fs: ['blast_v','blast_t']` eller ett eget block) och ta med λ och t i symboltabellen.
3. Låt metaCard visa antaganden från båda formlerna, eller öppna panelen som standard när formeltypen är `unverified`.
4. Gör det möjligt att ange λ direkt i meter, som alternativ till procent. Då tvingas inte en tolkning av den inkonsekventa anteckningen fram.

### H2 – Tiden t ramas in som tändfördröjning och syns i sökningar på sprängtermer
**Grad:** Hög
**Plats:**
- `src/catalog.js:415`: formelnamnet ”Fördröjningstid t = λ / v (egen modell)”
- `catalog.js:419`: synonymer ”fördröjning”, ”tändsekvens”, ”tid mellan rader”, ”förflyttning”
- `catalog.js:420`: kalkylatorsynonymer ”tändsekvens”, ”fördröjning”, ”tid”
- `catalog.js:20`: kategorisynonymer ”sprängning”, ”fördröjning”, ”försättning”
- `catalog.js:435`: extra resultatrad i ms
- `ui3.js:240`: Enter i sökrutan öppnar första träffen

**Vad är fel:**
- Sökning (verifierat i Node och i webbläsaren):
  - ”tändsekvens” → `blast_model` som första träff. Enter öppnar kalkylatorn direkt (`#/calc/blast_model`).
  - ”tid” → `blast_model` som första träff, före ”Omvandla tid”, ”Arbetstid” och andra.
  - ”hastighet” → `blast_model` och `blast_v` före vibrationskalkylatorn för partikelhastighet.
  - ”laddning” → bara modellen och kategorin.
  - ”sprängning” → bara modellen och kategorin.
  - ”sekvens”, ”fördröjningstid”, ”förflyttning”, ”rader” → modellen.
- Sökträffarna visas som ”Kalkylator · Egna modeller”, utan ej verifierad-märkning.
- Resultatet visas som ”Tid (t) 0,0384376 s = 38,4376 ms”, med 6 gällande siffror.
- Ingenstans står att värdet **inte** är ett tändintervall eller att appen medvetet inte avrundar till standardsteg. Anteckningen beskriver att man väljer närmast högre standardintervall, så användaren kan förväntas göra det själv.

**Varför det spelar roll:** Ägarens krav är att tändsekvenser inte får baseras på overifierade modeller. Här visar appen själv en overifierad modell som verktyget för tändsekvens/fördröjning och ger ett precist ms-värde. Steget till att välja tändare utifrån värdet blir mycket kort.

**Åtgärd:**
1. Ta bort synonymerna ”tändsekvens”, ”sekvens”, ”fördröjning”, ”tid mellan rader” och ”tid” från `blast_model`, `blast_t` och kategorin `model`.
2. Byt namn på `blast_t` till t.ex. ”Kvot t = λ / v (egen modell – inte ett tändintervall)”. Byt resultatetiketten ”Tid” till t.ex. ”t = λ/v enligt egen modell (ej tändintervall)”.
3. Lägg till en fast varning i resultatet: ”Värdet är inte ett förslag på tändintervall. BergPro avrundar inte till tändarsteg och ger inga förslag på tändsekvens.”
4. Låt inte Enter i sökrutan öppna en kalkylator med typen `unverified` direkt. Visa i stället träfflistan.
5. Visa en röd ”EJ VERIFIERAD”-etikett på sökträffar (och i alla listor) för kalkylatorer vars formel har typen `unverified`.
6. Överväg att för ”tändsekvens”, ”laddningsmängd”, ”hålavstånd” och liknande visa ett tomläge som säger att sådana modeller inte ingår och kräver verifierade fackkällor och behörig person.

### H3 – Kopierad text saknar status och varning
**Grad:** Hög
**Plats:** `src/ui2.js:216–221` (`recText`), `src/ui3.js:143` (`copyres`), `src/ui3.js:150` (`hcopy`).

**Vad är fel:** ”Kopiera” på resultatet och kopiering från historiken ger bara titel, indata, resultat och tidsstämpel. Faktiskt utfall i Playwright:
```
Hastighet och tid enligt egen modell
Indata:
Bergartskonstant K: 25
Försättning B: 2 m
Laddningskoncentration l: 5
...
Resultat:
Hastighet på bergmassan (v) = 20,8129 m/s
Förflyttning (λ) = 0,8 m
Tid (t) = 0,0384376 s
(2026-10-14 19:47, BergPro)
```
Texten innehåller varken ”ej verifierad”, någon varning, källa eller enhet för l.

**Varför det spelar roll:** Kopierad text klistras in i sms, e-post och sprängplaner. Det är den mest troliga vägen ut ur appen, och där försvinner statusen helt.

**Åtgärd:** Låt `recText` alltid lägga till formeltyp och verifieringsstatus. För `unverified`-formler ska även hela varningstexten och raden ”EJ VERIFIERAD – inte dimensioneringsunderlag, inte ett tändintervall” följa med. Lägg också till enheter för l (kg/m) och K (se M4). Gör det för alla kalkylatorer så att regeln inte kan glömmas bort för nya modeller.

### H4 – Historik, sparade resultat, startsida och historik-CSV tappar statusen; namnet kan skrivas om
**Grad:** Hög
**Plats:**
- `src/ui3.js:97–107`: spara-dialogen har ett fritt namnfält
- `src/ui2.js:222–236`: historiklistan
- `src/ui3.js:127–131`: `histCSV`
- `src/ui1.js:143`: ”Senast använda beräkningar”
- `src/ui1.js:145`: ”Sparade mätningar” blandar in sparade beräkningsresultat
- `src/ui1.js:135`, `ui2.js:202–213`: favoritrader

**Vad är fel:**
- Inga listor visar någon status. Exempel från Playwright:
  - Historik: ”Hastighet och tid enligt egen modell · Hastighet på bergmassan: 20,8129 m/s”
  - Sparat resultat som döpts om: ”Tändplan rad 2 · Hastighet på bergmassan: 20,8129 m/s · Projekt: Testprojekt”
- Startsidans rubrik ”Sparade mätningar” visar ”Tändplan rad 2”. Ett modellresultat presenteras alltså som en mätning.
- CSV från historik och sparade resultat (kolumnerna Datum, Beräkning, Projekt, Indata, Resultat, Anteckning) saknar status. Efter omdöpning finns inget spår alls av att resultatet kommer från en egen, overifierad modell.

**Varför det spelar roll:** Sparade resultat och CSV-filer används längre fram i arbetet, ofta av andra personer. En post med titeln ”Tändplan …” utan status ser ut som ett färdigt beslut.

**Åtgärd:**
1. Visa en ”EJ VERIFIERAD”-badge på alla rader (historik, sparade, startsida, favoriter, projektets kopplade beräkningar) vars kalkylator har en `unverified`-formel.
2. Lås ett prefix i spara-dialogen för sådana kalkylatorer, t.ex. ”[EJ VERIFIERAD egen modell] ”, eller visa alltid ursprungskalkylatorn under titeln.
3. Lägg till kolumnerna ”Formeltyp” och ”Verifieringsstatus” (och ”Varning”) i `histCSV`.
4. Döp om startsidans avsnitt till ”Sparade resultat och mätningar” och skilj typerna åt visuellt. Ännu bättre är att bara visa journalposter under ”mätningar”.

### H5 – Självtestet visar exempelvärden och ett appvalt λ = 80 % med grönt ”OK”
**Grad:** Hög
**Plats:** `src/tests.js:160–171` (testnamnen syns i appen under Mer → Självtest), `src/catalog.js:409` (`VERIF_NOTE`).

**Vad är fel:**
- Självtestsidan visar raderna:
  - ”Egen modell: v = K/B^1,17·l^0,39 mot anteckningens exempel (K=25, B=2, l=5 ≈ 20,81 m/s) – OK”
  - ”Egen modell: t = λ/v (λ = 80 % av B = 2 m = 1,6 m → ≈ 76,9 ms) och validering – OK”
- Anteckningen anger 40 %. Testet har tyst tolkat inkonsekvensen till 80 %, en tolkning som inte står i anteckningen, och presenterar resultatet ≈ 76,9 ms som godkänt.
- `VERIF_NOTE` säger att aritmetiken kontrolleras ”mot anteckningarnas exempel”. För t stämmer det inte, eftersom indata har ändrats.
- Sidan visar alltså ett konkret exempel på K, B, l, λ-andel och ms-tid för en tändrelaterad modell, märkt grönt ”OK”.

**Varför det spelar roll:** Ägarens krav är att modeller för tändsekvens inte får fyllas med påhittade värden. 80 % är en tolkning som appen själv gjort, och ”OK” kan läsas som att ms-exemplet är validerat.

**Åtgärd:**
1. Döp om testerna så att inga sprängparametrar eller ms-värden syns i testnamnet, t.ex. ”Egen modell: aritmetiken kontrollräknad (ingen validering av modellen)”.
2. Lägg inte in någon tolkning av λ i testet. Testa bara aritmetiken (t = λ/v för ett godtyckligt λ i meter). Alternativt testas båda tolkningarna utan att någon av dem kallas anteckningens exempel.
3. Ändra `VERIF_NOTE` så att den säger exakt vad som kontrollerats: ”v räknat med anteckningens indata ger anteckningens v. t kontrolleras bara som kvoten λ/v. Anteckningens λ-exempel är inkonsekvent och har inte avgjorts.”

### M1 – Projektrapporter och utskrift: status finns, men varningen, t-formeln och enheter saknas
**Grad:** Medel
**Plats:** `src/ui3.js:13–21` (`calcBlock`), `ui3.js:29–48` (TXT), `ui3.js:49–58` (CSV), `ui3.js:59–76` (utskrift), `ui3.js:145` (utskrift av enskilt resultat).

**Vad är fel:**
- TXT, CSV och utskrift innehåller ”Verifieringsstatus: Ej verifierad referens – EJ VERIFIERAD …”. Det är bra.
- Varningstexten från beräkningen (”Resultatet är inte ett dimensioneringsunderlag … Appen ersätter inte behörig sprängteknisk kompetens …”) följer inte med. `calcBlock` tar inte med `warnings`.
- Bara `v`-formeln skrivs ut (”Formel: v = (K)/(B^a) · l^b”) trots att t redovisas.
- Indata redovisas utan enhet för l och K (”Laddningskoncentration l: 5”). λ-raden heter ”λ som procent av försättningen (valfritt): 40” utan %.
- I utskriften står statusen sist i blocket med 9,5 pt (`ui3.js:69`). Utskriften av ett enskilt resultat får rubriken ”BergPro – beräkningsresultat” och ser ut som ett formellt beräkningsdokument.
- En omdöpt titel (”Tändplan rad 2”) blir blockrubrik i rapporten.

**Varför det spelar roll:** Rapporter skickas vidare. Den som läser dem ska utan tolkning förstå att resultatet inte är underlag.

**Åtgärd:**
1. Lägg till `warnings` i `calcBlock` och i TXT, CSV och utskrift.
2. För `unverified`: visa en tydlig ruta direkt under blockrubriken i samma storlek som brödtexten, t.ex. ”EJ VERIFIERAD EGEN MODELL – inte dimensioneringsunderlag – inte ett tändintervall – kräver granskning av behörig person”.
3. Skriv ut alla formler som kalkylatorn använder.
4. Skriv enheten för l och den förutsatta enheten för K. Byt etiketten för λ-raden till ”λ (% av B)”.
5. Visa ursprungskalkylatorns namn bredvid en egen titel.

### M2 – JSON-exporter saknar status
**Grad:** Medel
**Plats:** `src/ui3.js:179` (projekt-JSON), `src/core.js:321` (`exportObj`).

**Vad är fel:** Projekt-JSON innehåller `saved`-posterna (calc, title, raw, results) utan formeltyp, verifieringsstatus eller varning. Samma gäller den fullständiga exporten.

**Varför det spelar roll:** JSON läses ibland av andra verktyg eller personer. Ett fält som `"label":"Tid","value":0,038…,"unit":"s"` utan status är lätt att återanvända fel.

**Åtgärd:** Lägg till `formulaType`, `verification`, `warnings` och `appVersion`/`formulaVersion` per sparad post i projekt-JSON. Projektexporten är ett utdatadokument och kan få det även om importformatet hålls stabilt.

### M3 – Friskrivningstexterna stämmer inte längre
**Grad:** Medel
**Plats:**
- `src/ui1.js:163`: noten i kategorin ”Standarder och dokumentation”: ”Operativa modeller för laddningsmängd, försättning, hålavstånd och tändsekvenser ingår inte …”
- `src/ui2.js:250`: Om-sidan: ”innehåller inga gränsvärden, laddningsmodeller eller dimensioneringsmallar”
- `README.md:29`: ”inga modeller för laddning, försättning, hålavstånd eller tändsekvens”

**Vad är fel:** Appen innehåller nu en modell som tar försättning och laddningskoncentration som indata och ger en tid ”före nästa rad detonerar”. Dessutom indexeras den under ”tändsekvens” (H2).

**Varför det spelar roll:** När en friskrivning uppenbart inte stämmer tappar användaren förtroendet för alla friskrivningar. Det kan också leda till slutsatsen att modellen som finns inte hör till de modeller friskrivningen gäller.

**Åtgärd:** Formulera om, t.ex.: ”BergPro innehåller inga verifierade modeller för laddningsmängd, försättning, hålavstånd eller tändsekvens. Under Egna modeller finns din egen, ej verifierade anteckning. Den är inte en tändsekvensmodell och får inte användas som dimensioneringsunderlag.” Gör samma ändring i README och på Om-sidan.

### M4 – Enheter och dimensioner i `blast_model`
**Grad:** Medel
**Plats:** `src/catalog.js:411` (variabler), `catalog.js:421–426` (indata).

**Vad är fel:**
- **K märks som ”–” (dimensionslös).** Om v ska bli m/s med B i m och l i kg/m kan K inte vara dimensionslös, eftersom exponenterna inte är heltal. K är bara giltig för de enheter som modellen kalibrerats i.
- **B har en fri enhetsväljare** (mm, cm, m, km, tum, fot …). Omräkningen till m är korrekt: 2000 mm ger samma resultat som 2 m. Men väljaren antyder att enheten är fri, när det i själva verket förutsätts att K bestämts för B i meter.
- **l saknar enhetsväljare.** Enheten (kg/m) finns bara i hjälptexten och saknas i export och kopiering.
- **λ-andelen har ingen övre gräns.** 500 % och 1 000 000 % accepteras utan varning. λ beskrivs som en andel av försättningen, och en andel över 100 % strider mot den egna definitionen. Detta är en definitionskontroll, inte en dimensioneringsgräns.
- **Inga rimlighetskontroller.** Uppenbara inmatningsfel ger resultat utan varning, t.ex. B = 2000 angivet i m → v ≈ 0,0064 m/s och t ≈ 124 382 s, eller B = 0,001 m → v ≈ 151 544 m/s. Appen ska inte uppfinna gränser (ägarens krav), men den kan låta användaren ange giltighetsområdet från sin egen källa.

**Varför det spelar roll:** Ett enhetsfel i en empirisk potenslag ger ett tyst och stort fel. Enheten för K och l är en del av modellens definition.

**Åtgärd:**
1. Ändra enheten för K till ”beror på källan – gäller endast för B i m och l i kg/m”.
2. Lås B till m (ta bort väljaren) eller visa texten ”B räknas om till m innan formeln används”.
3. Skriv ”(kg/m)” i etiketten för l och ta med enheten i `ins`.
4. Varna när λ-andelen är över 100 % (”λ större än B – kontrollera definitionen”).
5. Lägg till valfria fält ”Giltighetsområde enligt min källa” (min/max för B, l och K) som användaren fyller i själv. Varna när indata ligger utanför. Inga gränser ska vara förifyllda.

### M5 – Resultatkortet signalerar inte overifierad status
**Grad:** Medel
**Plats:** `src/ui1.js:298–308` (`resultHTML`), `src/style.css:166–168`.

**Vad är fel:** Huvudresultatet visas i samma accentfärgade kort med stor siffra som allmänna fysikformler. Varningsrutan kommer efter knapparna Kopiera, Spara och Skriv ut, och på mobil (390 px) måste man skrolla för att se den. Kortet innehåller ingen statusmarkering.

**Åtgärd:** Gör en egen variant av resultatkortet för `unverified`: varningsfärgad ram, etiketten ”EJ VERIFIERAD EGEN MODELL” ovanför siffran och varningen före åtgärdsknapparna. Överväg också att Kopiera, Spara och Skriv ut kräver att användaren bekräftar statusen en gång per session.

### M6 – Falsk precision
**Grad:** Medel
**Plats:** `src/core.js:65` (`CFG.sig = 6`), `src/catalog.js:435–436`.

**Vad är fel:** v och t visas med 6 gällande siffror (”38,4376 ms”), och i inställningarna kan man välja upp till 10. För en overifierad empirisk modell med handskrivna exponenter ger det ett sken av noggrannhet. Det gör också värdet mer likt ett tidsvärde man kan ”välja tändare efter”.

**Åtgärd:** Begränsa visningen för `unverified`-kalkylatorer (t.ex. till 2–3 gällande siffror, vilket är ett presentationsval och inget sprängtekniskt värde). Lägg till en rad om att noggrannheten är okänd. Behåll full precision internt.

### M7 – Mätserie: statistik som saknar fysikalisk mening ges utan varning
**Grad:** Medel
**Plats:** `src/catalog.js:315–329` (`series`).

**Vad är fel:**
- Med storheten ”Annan storhet” och enheten dB (vilket blir följden när journalens ”Luftstötvåg (tryck)” eller ”Ljudnivå” har enheten dB) räknas aritmetiskt medelvärde, RMS och standardavvikelse direkt på dB-talen. Utfall: ”RMS 125,067 dB”. RMS av dB-tal är fysikaliskt meningslöst, och ett aritmetiskt medelvärde av nivåer är inte ett energimedelvärde. Ingen varning visas.
- När journalposter skickas till serien är varje värde normalt ett enskilt toppvärde från en egen händelse, t.ex. PPV per salva. Serien räknar ”RMS” och ”Medelvärde” över dessa toppvärden utan att förklara att det inte är signalens RMS och inte ett mått som ska jämföras med något krav.

**Åtgärd:**
1. Varna när enheten innehåller ”dB”: ”Aritmetiskt medelvärde/RMS av dB-nivåer är inte energimässigt korrekt. Topptrycksnivåer kan inte medelvärdesbildas energetiskt.”
2. Lägg till en fast notering när serien kommer från journalen: ”Värdena är separata mätningar. RMS och medel beskriver spridningen mellan mätningar, inte en signal.”

### M8 – Journal → mätserie blandar projekt, platser och instrument
**Grad:** Medel
**Plats:** `src/ui2.js:150–157` (`regSummaryHTML`), `src/ui3.js:160–164` (`ACT.series`).

**Vad är fel:** Knappen ”Analysera mätserie” grupperar bara på typ och enhet i hela journalen. Mätningar från olika projekt, mätplatser och instrument slås ihop till en serie med ett gemensamt max och medel.

**Åtgärd:** Gruppera även på projekt och mätplats, eller låt användaren filtrera (projekt, plats, instrument, datumintervall) innan serien skickas. Visa vilka filter som gäller i seriens indata.

### M9 – Mätjournalen saknar viktig metadata
**Grad:** Medel
**Plats:** `src/ui2.js:55–70` (`REGS.journal`).

**Vad är fel:** En post har typ, värde, fritext-enhet, tid, plats, instrument, projekt och anteckning. Det finns inga fält för:
- om värdet är topp eller RMS
- komponent eller riktning (vertikal, radiell, transversell, vektorsumma)
- frekvens vid toppvärdet
- filter eller vägning (luftstöt)
- kalibreringsdatum
- vilken salva mätningen gäller

Notisen säger att man ska skilja på storheterna, men formuläret hjälper inte till med det.

**Varför det spelar roll:** Mätdata delas och jämförs med krav som finns utanför appen. Utan metadata kan värden jämföras på fel grund.

**Åtgärd:** Lägg till valfria fält med alternativet ”okänt”: Storhet (topp/RMS/annat), Komponent, Frekvens (Hz), Filter/vägning, Salvreferens. Inga förifyllda värden och inga gränsvärden.

### M10 – ”Verifierad teknisk modell” för formler som en AI kontrollerat
**Grad:** Medel
**Plats:** `src/catalog.js:24–30` (`FTYPES`), `catalog.js:479` (RQD: ”Klassgränser bekräftade endast i sekundärkälla”), `catalog.js:514` (ljudhastighet: ”kontrollerad via sekundärkälla: pyfar”).

**Vad är fel:** Sju formler har den gröna badgen ”Verifierad teknisk modell”. Verifieringen är gjord av en AI-assistent mot angivna källor, delvis sekundära. Att det inte är fackgranskat syns bara i liten text i granskningsfältet.

**Varför det spelar roll:** Ordet ”verifierad” i grönt väger tungt. Ägarens kategori ”verifierad” bör betyda verifierad av behörig person mot primärkälla.

**Åtgärd:** Byt etikett till t.ex. ”Kontrollerad mot källa (ej fackgranskad)” tills en behörig person har granskat. Alternativt kan typen sänkas där kontrollen bara gjorts mot sekundärkälla.

### M11 – Sprickregistreringen blandar mätlinjer och projekt
**Grad:** Medel
**Plats:** `src/ui2.js:158–171`.

**Vad är fel:** Sprickfrekvensen och medelavståndet räknas på **alla** sprickor i registret mot en enda global mätlinjelängd (`prefs.scanline`), oavsett projekt eller mätlinje.

**Varför det spelar roll:** Sprickfrekvens används för att bedöma bergmassan, som indirekt påverkar sprängtekniska bedömningar. Om flera linjer blandas blir frekvensen fel utan att någon märker det.

**Åtgärd:** Inför ett mätlinje-ID med egen längd per linje, och filtrera per projekt och linje innan frekvensen räknas.

### L1 – Förvald favorit
**Grad:** Låg (ägarens uttryckliga önskemål)
**Plats:** `src/core.js:281` (`favs: ['c:blast_model']`).

**Vad är fel:** På en ny installation är den overifierade modellen det första verktyget under ”Favoriter” på startsidan, utan status. Den kommer tillbaka efter ”Radera all lokal data” och när man importerar en fil utan `favs`, både vid ”Slå ihop” och ”Ersätt”.

**Åtgärd:** Behåll stjärnan om ägaren vill det, men visa ”EJ VERIFIERAD” på favoritraden (se H4). Lägg inte tillbaka favoriten efter rensning eller import, eftersom användaren då aktivt har tagit bort den.

### L2 – Hänvisning till dokument som inte finns i appen
**Grad:** Låg
**Plats:** `src/catalog.js:519` (”Se säkerhetsgranskningen.”).

**Åtgärd:** Ta bort hänvisningen eller sammanfatta slutsatserna direkt i granskningsfältet.

### L3 – Dubbelt ”(valfritt)”
**Grad:** Låg
**Plats:** `src/catalog.js:426` (etiketten innehåller ”(valfritt)”) och `ui1.js:187` (lägger till ”(valfritt)” för `opt`).

**Vad är fel:** Fältet visas som ”λ som procent av försättningen (valfritt) (valfritt)”, och ”(valfritt)” följer med i export och kopiering.

**Åtgärd:** Ta bort ”(valfritt)” ur etiketten.

### L4 – Testnamnet ”typiska värden”
**Grad:** Låg
**Plats:** `src/tests.js:119`.

**Vad är fel:** Namnet ”provkörning av alla kalkylatorer med typiska värden” syns i appen. Det kan uppfattas som att appen innehåller typiska värden.

**Åtgärd:** Byt till ”godtyckliga provvärden”.

### L5 – Sinus topp/RMS med dB
**Grad:** Låg
**Plats:** `src/catalog.js:285–290`.

**Vad är fel:** Med enheten ”dB” blir resultatet ”RMS 7,07107 dB” för toppvärdet 10 dB, vilket är meningslöst.

**Åtgärd:** Varna om enheten innehåller dB: sambandet gäller amplituder, inte nivåer.

### L6 – README stämmer inte
**Grad:** Låg
**Plats:** `README.md:30` (”Inga … klassgränser är förifyllda”), `README.md:33–34` (115/115, 98/98, ”12 kategorier och 58 kalkylatorer”).

**Vad är fel:** RQD-klasserna enligt Deere (25/50/75/90 %) finns inbyggda. Självtestet ger nu 133/133, och det finns 13 kategorier och 59 kalkylatorer. Webbläsartestet är alltså inte omkört efter att `blast_model` lades till, eller så har README inte uppdaterats.

**Åtgärd:** Uppdatera README. Kör om och dokumentera webbläsartestet för den aktuella versionen.

### L7 – Rapportens status gäller nu, inte vid beräkningen
**Grad:** Låg
**Plats:** `src/ui3.js:13–21`.

**Vad är fel:** `calcBlock` hämtar formelstatus och källa från dagens register. Om modellen senare får en annan status visas den nya statusen även för gamla resultat. Ingen formelversion eller appversion sparas per resultat. Lagrade resultat räknas inte om, så en redigerad eller importerad fil kan innehålla resultat som inte stämmer med indata.

**Åtgärd:** Spara `formulaType`, `ver` och `appVersion` i posten när den sparas, och skriv ut dem i rapporten. Räkna gärna om resultaten från `raw` och markera avvikelser.

### L8 – Sökning på gränsvärden
**Grad:** Låg
**Plats:** `src/catalog.js:647–685`.

**Vad är fel:** ”gränsvärde”, ”riktvärde” och ”tillåten” ger inga träffar. ”vibration gräns” och ”ppv gräns” ger mätserien som träff.

**Åtgärd:** För sådana termer, visa en fast rad i stil med ”BergPro innehåller inga gränsvärden. Gällande krav finns i föreskrifter och projektets villkor.”

### L9 – RQD-varning med egen tröskel
**Grad:** Låg
**Plats:** `src/catalog.js:250`.

**Vad är fel:** Varningen vid ”< 50 % av körlängden registrerad” bygger på en tröskel som appen valt själv.

**Åtgärd:** Visa i stället alltid andelen registrerad kärna som en resultatrad, utan tröskel.

### L10 – Typnamnet ”Ej verifierad referens”
**Grad:** Låg
**Plats:** `src/catalog.js:29`.

**Vad är fel:** En egen modell är ingen ”referens”.

**Åtgärd:** Byt till ”Ej verifierad (egen/okänd källa)”.

---

## 4. Spårbarhet för `blast_model`: var syns statusen?

| Yta | ”Ej verifierad” syns? | Varningstexten syns? | Fynd |
|---|---|---|---|
| Kategorisidan Egna modeller | Ja (varningsruta och beskrivning) | Ja | OK |
| Kategoriruta på startsidan och i Kategorier | Ja (beskrivning) | – | OK |
| Kalkylatorsidan före beräkning | Bara dämpad beskrivning; badgen ligger i stängd panel | Nej | H1 |
| Resultatkortet efter beräkning | Ja, i varningsrutan under knapparna | Ja | M5 |
| Kopiera (resultat) | **Nej** | **Nej** | H3 |
| Historiklistan | **Nej** | **Nej** | H4 |
| Kopiera från historik | **Nej** | **Nej** | H3 |
| Sparade resultat (titeln kan ändras) | **Nej** | **Nej** | H4 |
| Startsidan: Senast använda | **Nej** | **Nej** | H4 |
| Startsidan: ”Sparade mätningar” | **Nej** (och kallas mätning) | **Nej** | H4 |
| Favoriter (startsida och Favoriter-vyn) | **Nej** | **Nej** | L1, H4 |
| Sökträffar | **Nej** (”Kalkylator · Egna modeller”) | **Nej** | H2 |
| Formelsidorna `blast_v`/`blast_t` | Ja (badge och status) | Delvis (λ-frågan bara på `blast_t`) | H1 |
| Formelsamling och Verifieringsstatus | Ja | – | OK |
| Projektrapport TXT | Ja (statusrad) | Nej | M1 |
| Projektrapport CSV | Ja (kolumn på resultatrader) | Nej | M1 |
| Utskrift/PDF (projekt och enskilt resultat) | Ja (9,5 pt, sist i blocket) | Nej | M1 |
| Projekt-JSON | **Nej** | **Nej** | M2 |
| Full JSON-export | **Nej** | **Nej** | M2 |
| CSV från historik och sparade | **Nej** | **Nej** | H4 |
| Självtest | Grönt ”OK” med exempelvärden | – | H5 |

---

## 5. Kontrollerat och godtagbart

**Förifyllda värden och mallar**
- K, B, l och λ är tomma från start. Självtestet säkerställer att K, B och l inte har standardvärden (`tests.js:169`). De enda förifyllda talen i hela appen är `g` och exponenterna a = 1,17 och b = 0,39, som kommer från ägarens anteckning, är märkta som det och kan ändras (`tests.js:269–272`).
- `defVal` används bara för portryck (0, tomt = torrt) och täckningsfaktor (k = 2, med förklaring). Inget av dem är sprängtekniskt.
- Platshållarna (`ph:`) är formatexempel som ”t.ex. mm/s, Pa, dB”. Inga gränsvärden eller typiska värden.
- Mätseriens hjälptext ”Exempel: 1,2 3,4 2,2 0,8 4,1” är ett formatexempel. Det kan med fördel märkas så, men det är inget gränsvärde.
- Ingen kalkylator beräknar laddningsmängd, försättning, hålavstånd, specifik laddning eller tändsekvens. Sökningar på ”laddningsmängd”, ”hålavstånd”, ”salva”, ”sprängplan”, ”dimensionering”, ”säkerhetsavstånd”, ”burden” och ”tändning” ger inga träffar.

**Tändintervall**
- Ingen avrundning till tändarsteg. Inga förslag på intervall eller sekvens. Strängen ”25 ms” och ord som ”tändare”, ”detonator” och ”elektronisk” finns inte i källkoden.

**`blast_model`: numerik och validering**
- K, B och l ≤ 0, tomma fält och exponenter ≤ 0 avvisas med fältfel. λ-andelen ≤ 0 avvisas.
- Resultat som inte är ändliga stoppas, både i `compute` och i `Engine.run`.
- Omräkningen mm → m för B stämmer: 2000 mm ger exakt samma resultat som 2 m.
- Formeln tolkas som (K/B^a)·l^b, vilket är den tolkning som återger anteckningens v-exempel. Bråknotationen på skärmen är otvetydig.
- Varningen efter beräkning är tydlig och innehåller ”EJ VERIFIERAD”, ”inte ett dimensioneringsunderlag”, ”låt behörig person granska” och ”ersätter inte behörig sprängteknisk kompetens eller en projektspecifik riskbedömning”.
- Kategorinoten för Egna modeller är tydlig, och modellen har typen `unverified`, vilket självtestet kontrollerar.

**Vibration**
- Frekvens, period och ω avvisar noll och negativa värden.
- Harmonisk rörelse kräver exakt en storhet och varnar för att sambandet bara gäller ren sinus. Förskjutning, hastighet och acceleration hålls isär med egna enhetsgrupper.
- Sinusberäkningen varnar för likkomponent.
- Mätserien varnar för m/s jämfört med mm/s och för accelerationsenheter.
- Vibrationskategorin säger uttryckligen att appen inte anger några gränsvärden.

**Luftstötvåg**
- `spl_p` ger ”dB re 20 µPa” och varnar för RMS kontra topp och för frekvens- och tidsvägning. Kontrollräkning: 1 Pa ger 93,98 dB och 200 Pa ger 140 dB, båda korrekta.
- `sum_levels` varnar uttryckligen för att topptrycksnivåer inte kan summeras energetiskt.
- `c_sound` varnar utanför −20 till +50 °C. `dist_delay` saknar förifyllt c.
- Ingen funktion jämför mot krav. Det finns ingen efterlevnadskontroll någonstans i appen.

**Mätjournal**
- Inga gränsvärden. Introt säger det uttryckligen.
- Värdet valideras som tal och enheten är obligatorisk.

**Borrning och produktion**
- Rena nyckeltal. Kategorinoten säger att salvor inte dimensioneras, och `drill_len` varnar för samma sak.
- Arbetstid 0 avvisas, negativa längder avvisas och maskintid längre än arbetstid avvisas.

**RQD och sprickor**
- RQD-definitionen är korrekt: bitar på exakt 10 cm räknas med, och bitar längre än körlängden avvisas.
- Klassgränserna är Deeres publicerade värden, märkta ”bekräftade endast i sekundärkälla”.
- Sprickavståndet varnar för skenbart kontra vinkelrätt avstånd.

**Övrigt**
- Mohr–Coulomb anger ingen rekommenderad säkerhetsfaktor, bara en varning vid FS < 1. Det är inte sprängtekniskt.
- Geometrikalkylatorerna med synonymen ”borrhål” är allmän geometri utan förifyllda densiteter. Användaren kan själv räkna hålvolym gånger densitet, men appen erbjuder ingen laddningsmodell.
- På varje kalkylatorsida finns texten ”Beräkningshjälp – ersätter inte kontroll mot gällande krav …”.
- Om-sidan och kategorin ”Standarder och dokumentation” friskriver tydligt (men se M3).
- Uttrycksräknaren använder ingen `eval`.
- JSON-importen rensar bort `__proto__` och liknande nycklar.
- Formelsidor, Formelsamling och Verifieringsstatus visar modellens status korrekt.

---

## 6. Begränsningar i granskningen
- Den handskrivna anteckningen är bara känd genom beskrivningen i uppdraget och appens texter. Originalet har inte granskats.
- Modellens fysikaliska giltighet har inte bedömts, och inga värden har rimlighetsprövats. Det ska en behörig sprängtekniker göra mot en fackkälla.
- Ingen test på riktiga mobiler, ingen faktisk PDF-generering, ingen test med skärmläsare. Utskriftsvägen kontrollerades genom att läsa `#printRoot` med `window.print` utbytt mot en tom funktion.
- Standardhänvisningarna (ISO, IEC, ASTM, GUM) har inte kontrollerats mot originalen.

---

## 7. Föreslagen prioritering
1. **H2 och H1:** ta bort synonymerna för tändsekvens och fördröjning, byt namn på t och lägg en fast varning om att det inte är ett tändintervall. Visa λ-inkonsekvensen och frågan om v på kalkylatorsidan.
2. **H3 och H4:** se till att status och varning alltid följer med vid kopiering, i listor, i historik-CSV och vid omdöpning.
3. **H5:** byt namn på självtesterna och ta bort 80 %-tolkningen. Rätta `VERIF_NOTE`.
4. **M1–M6:** komplettera rapporterna och JSON, rätta friskrivningarna, gör enheterna och användarens eget giltighetsområde tydliga, ge resultatkortet en egen form och begränsa precisionen.
5. **M7–M11** och de Låga fynden.

---

## Bilaga A – körda prov på `blast_model` (bara aritmetik, inga rimlighetsbedömda värden)

| Indata | Utfall | Kommentar |
|---|---|---|
| Anteckningens exempel K, B, l, utan λ | v = 20,8129 m/s, bara v visas | Återger anteckningens v |
| Samma, λ = 40 % | λ = 0,8 m, t = 0,0384376 s = 38,4376 ms | Anteckningens procentsats |
| Samma, λ = 80 % | λ = 1,6 m, t = 76,8753 ms | Återger anteckningens slutresultat; faktor 2 mot 40 % |
| B = 2000 med enheten mm | Identiskt med B = 2 m | Omräkningen fungerar |
| B = 2000 med enheten m (inmatningsfel) | v = 0,00643 m/s, t = 124 382 s | Ingen varning (M4) |
| B = 0,001 m | v = 151 544 m/s | Ingen varning (M4) |
| λ = 500 % och 1 000 000 % | Accepteras, λ = 10 m resp. 20 000 m | Ingen varning (M4) |
| l = 5000 (t.ex. om g/m angetts) | v = 307,8 m/s, t = 2,6 ms | Ingen enhetsväljare (M4) |
| a = 100 | t ≈ 2·10²⁸ s | Accepteras |
| a = 0, a < 0, a tomt | Fältfel | OK |
| K, B, l ≤ 0 eller tomma | Fältfel | OK |
| Ogiltig enhetsnyckel för B (bara via manipulerad eller importerad post) | Faller tyst tillbaka till m | Låg risk |

---

## 8. Uppföljning efter åtgärder

**Datum:** 2026-10-14 (andra genomgången, fortfarande skrivskyddad – inget under `/home/claude/bergpro` har ändrats).

**Metod:**
- Läst om `src/catalog.js`, `core.js`, `ui1.js`, `ui2.js`, `ui3.js`, `tests.js` och `README.md`.
- Kontrollerat att `index.html` innehåller exakt den aktuella JS- och CSS-källan (ja).
- `node run-tests.js`: **136/136 OK**, 59 kalkylatorer, 63 formler.
- Kört motorn och sökningen i Node.
- Kört appen i Chromium (Playwright, 320 och 390 px). Kontrollerat:
  - kalkylatorsidan före och efter beräkning
  - kopiering, spara med eget namn, historik, sparade, startsida, favoriter, kategori, formelsida och självtest
  - sökning och Enter
  - projektrapport (TXT, CSV, JSON, utskrift) och utskrift av enskilt resultat (beräknad stil på `.unvbox`)
  - full JSON-export
  - mätjournal → mätserie, sprickregistrering, RQD och sinus med dB
  - ”Radera all lokal data” följt av omladdning
  - import utan `favs`
  - en äldre historikpost (gammalt format med B i mm)
- Inga JS-fel uppstod.

**Utvecklarens påståenden som stämmer inte:**
- README är inte omskriven. Filen är oförändrad sedan 19:18 och innehåller fortfarande ”inga modeller för … tändsekvens”, ”115/115”, ”98/98”, ”12 kategorier och 58 kalkylatorer” och ”inga … klassgränser”.
- Favoriten sätts inte bara vid allra första start. Den kommer tillbaka efter ”Radera all lokal data” och omladdning. Kodkommentaren i `ui3.js:311` påstår motsatsen.

### 8.1 Status per fynd

| ID | Status | Belägg |
|---|---|---|
| H1 | **Åtgärdat** | `ui1.js:255` visar en röd ruta med `UNVERIFIED_NOTICE` och fyra öppna frågor (λ-inkonsekvensen med faktor 2, vad v är, enheten för K, exponenternas ursprung) överst på sidan, före Indata. Båda formlerna visas (`fs`, `ui1.js:251–257`), symboltabellen tar med λ och t, och båda metapanelerna har `open=true` (Playwright). |
| H2 | **Åtgärdat** (rest se N1) | `blast_t` heter ”Kvot t = λ / v (egen modell – inte ett tändintervall)” och ms-raden är borttagen (`catalog.js:455`). Synonymerna tändsekvens, fördröjning och tid är borttagna (`catalog.js:20, 426, 431, 433`). Sökning: ”tändsekvens”, ”tid mellan rader”, ”sekvens” och ”fördröjningstid” ger inga modellträffar; ”tid” och ”hastighet” ger inte längre modellen. Spärrade ämnen visar en friskrivningsruta (`ui1.js:130–131`). Enter öppnar inte overifierade träffar (`ui3.js:272`; Playwright: ”laddning”, ”konstant” och ”dimensionering” + Enter stannar på `#/`). Resultatet säger uttryckligen att appen inte avrundar till tändarsteg. |
| H3 | **Åtgärdat** | `statusText`/`recText` (`ui2.js:229–245`) lägger till ”*** EJ VERIFIERAD EGEN MODELL … ***”, formeltyp, version vid beräkningen, verifieringsstatus och varningar. Kontrollerat i både Kopiera och historikkopiering. Enheter för K och l följer med (”25 enl. källan”, ”5 kg/m”). |
| H4 | **Åtgärdat** (liten lucka se N7) | Röd badge ”EJ VERIFIERAD” finns i sökträffar, kategori, historik, sparade, startsidans favoriter, Senast använda och Sparade samt i projektets kopplade beräkningar (`ui1.js:121, 134, 142, 150, 152, 184`; `ui2.js:218–219, 259, 414`). Namnet får tvångsprefixet ”[EJ VERIFIERAD egen modell] ” (`ui3.js:129–136`; Playwright: ”[EJ VERIFIERAD egen modell] Tändplan rad 2”). Historik-CSV har kolumner för formeltyp, verifieringsstatus och varning (`ui3.js:160–161`). Startsidans rubrik heter ”Sparade resultat och mätningar” och posterna märks Mätning respektive Beräkning. |
| H5 | **Åtgärdat** (rest se N3) | Självtestnamnen är neutrala: ”Egen modell: aritmetiken kontrollräknad (ingen validering av modellen)”, utan siffror och utan 80 % (Playwright). Testet av t använder godtyckliga värden och `lamM` (`tests.js:166–168`). `VERIF_NOTE` är omskriven (`catalog.js:413`). |
| M1 | **Åtgärdat** | TXT, CSV och utskrift har statusruta per block, båda formlerna, varningar, ursprungskalkylator, enheter och raden ”Vid beräkningen: …” (`ui3.js:14–105`). Utskriftens `.unvbox` är 14,7 px, fet och har ram. Rubriken för ett enskilt resultat är ”BergPro – resultat från EJ VERIFIERAD egen modell”. |
| M2 | **Åtgärdat** (äldre poster se N2) | Projekt-JSON har fälten `notice`, `unverified`, `formulaType`, `verification`, `warnings` och `formulaVersionNow` (`ui3.js:211`). Full export har `notice`, och nya poster bär `meta.type` (`core.js` `exportObj`, `ui1.js:304`, `ui3.js:137`). |
| M3 | **Delvis åtgärdat** | Noten i kategorin std (`ui1.js:170`) och Om-sidan (`ui2.js:275`) är korrekt omskrivna. **README.md är oförändrad**: rad 24 (”λ anges som procent av försättningen”, gammal titel), rad 28 och rad 29 (”inga modeller för laddning, försättning, hålavstånd eller tändsekvens”). |
| M4 | **Åtgärdat** | K har enheten ”enl. källan … gäller bara för B i m och l i kg/m”. B och l saknar enhetsväljare (0 `select[data-unit]` i Playwright) och har fasta enhetsetiketter. λ kan anges i % eller i m, och båda samtidigt avvisas. Varning visas vid λ > 100 % och vid λ > B. Egna giltighetsintervall för B, l och K är tomma från start och varnar utanför intervallet (`catalog.js:432–459`). |
| M5 | **Åtgärdat** | `section.result.unv` har etiketten ”EJ VERIFIERAD EGEN MODELL”. Ordningen i kortet är tre röda varningsrutor och sedan knapparna (`ui1.js:309–321`; Playwright). |
| M6 | **Delvis åtgärdat** | Skärm, kopiering, TXT, utskrift och historik-CSV visar 3 gällande siffror (`RS`, `sig: 3`), och en varning om okänd noggrannhet finns. **Projekt-CSV exporterar fortfarande 12 siffror** via `Format.raw` (`ui3.js:73`), t.ex. ”0,0384376450111” s och ”20,8129296103” m/s. |
| M7 | **Åtgärdat** | dB-varningen och varningen om separata mätningar visas (`catalog.js:323–324`), verifierat via journal → serie med dB-värden. |
| M8 | **Delvis åtgärdat** | Grupperingen sker nu på typ, enhet, projekt och plats (`ui2.js:160`, `ui3.js:192–195`). **Mätvärdets art (topp/RMS), komponent och instrument blandas fortfarande.** Playwright: gruppen ”Vibration – hastighet (mm/s) · P1 – 3 st” innehöll Toppvärde/Vertikal, RMS/Vektorsumma och Toppvärde/Radiell (instrument A) i samma serie. |
| M9 | **Åtgärdat** | Journalen har fälten Mätvärdets art, Komponent/riktning, Frekvens, Filter/vägning, Salvreferens och Kalibreringsdatum (`ui2.js:65–71`). De ingår i listtexten, journal-CSV och projekt-CSV. (Mindre: utskriftens mätningstabell visar art och komponent men inte frekvens, vägning, salva och kalibrering, `ui3.js:101`.) |
| M10 | **Åtgärdat** | `FTYPES.verified` heter nu ”Kontrollerad mot källa (ej fackgranskad)” och `unverified` heter ”Ej verifierad (egen/okänd källa)” (`catalog.js:24–30`). Syns i Formelsamling och Verifieringsstatus. (Mindre: verktygsbeskrivningen `TOOLS.verif`, `catalog.js:678`, säger fortfarande ”verifierad”.) |
| M11 | **Åtgärdat** | Sprickor grupperas per projekt och linje med egen längd per linje (`ui2.js:165–181`, `prefs.scanlines`). Playwright: L1 2 st/4 m → 0,5 1/m, L2 1 st/10 m → 0,1 1/m, ”Utan linje-ID” utan längd ger ”–”. |
| L1 | **Delvis åtgärdat** | Favoriten sätts via `Store.firstRun` (`core.js` `init`, `ui3.js:312`). En borttagen stjärna förblir borta efter omladdning, och import utan `favs` lägger inte tillbaka den. **Men ”Radera all lokal data” tar bort lagringsnyckeln (`ui3.js:145`), så nästa start räknas som första start och favoriten kommer tillbaka.** Playwright: `[]` direkt efter rensning och `["c:blast_model"]` efter omladdning. |
| L2 | **Åtgärdat** | ”Se säkerhetsgranskningen” är ersatt av en sammanfattning i granskningsnoten (`catalog.js:542–543`). |
| L3 | **Åtgärdat** | Etiketten heter ”λ som andel av försättningen B” och visas med ett enda ”(valfritt)” (Playwright). |
| L4 | **Åtgärdat** | Testnamnet säger ”godtyckliga provvärden” (`tests.js:119`). |
| L5 | **Åtgärdat** | Sinus med dB ger varningen ”… resultatet är meningslöst för dB-värden” (`catalog.js:288`; Playwright). |
| L6 | **Ej åtgärdat** | README rad 30 och 33–34 är oförändrade (”inga … klassgränser”, 115/115, 98/98, 12 kategorier och 58 kalkylatorer). Självtestet ger nu 136/136. |
| L7 | **Åtgärdat** | `meta` (typ, typetikett, formelversion, appversion) sparas i historik och sparade poster. Rapporterna skriver ”Vid beräkningen: …” och kontrollräknar lagrat resultat (`ui3.js:17–33`). Verifierat: en manipulerad äldre post flaggas med ”Lagrat resultat stämmer inte med omräkning från indata”. (Mindre: i kopierad text visar ”Formeltyp” nuvarande typetikett, och bara versionen kommer från `meta`.) |
| L8 | **Åtgärdat** (rest se N5) | ”gränsvärde”, ”riktvärde” och ”tillåten” visar friskrivningsrutan (`ui1.js:130–131`). |
| L9 | **Åtgärdat** | Tröskeln på 50 % är borttagen. I stället visas alltid raden ”Registrerad kärna av körlängden” (`catalog.js:250`). |
| L10 | **Åtgärdat** | Typetiketten heter ”Ej verifierad (egen/okänd källa)”. |

**Summering:** 21 Åtgärdade, 4 Delvis åtgärdade (M3, M6, M8, L1), 1 Ej åtgärdat (L6).

### 8.2 Nya fynd efter åtgärderna

| ID | Grad | Plats | Beskrivning och belägg | Åtgärd |
|---|---|---|---|---|
| N1 | Låg | `catalog.js:427, 433`, `catalog.js:687` (sökindexet tar med `desc` och `name`) | Friskrivningar med negation indexeras som sökord. ”dimensionering” ger **en enda träff: `blast_model`** (via ”inte dimensioneringsunderlag”). ”tändintervall” ger `blast_t` och `blast_model`, och ”tändare” ger `blast_t` som första träff. Risken begränsas av spärrnotisen, den röda badgen och att Enter är blockerat. | Indexera inte negerade friskrivningstexter. Lägg till ett `noindex`-fält eller ta bort overifierade poster ur träfflistan när spärrnotisen visas. |
| N2 | Medel | `catalog.js:434–436` (B och l har inte längre `unitGroup`), `ui1.js:247` (en gammal post öppnas med `rec.units`) | **Äldre poster tolkas om tyst.** En historik- eller sparad post från förra versionen, där B angavs i mm, cm eller ft, räknas nu som meter när den öppnas (`?h=`/`?s=`). Playwright: B = 2000 mm → v ≈ 0,00643 m/s och t ≈ 124 000 s, utan varning på kalkylatorsidan, och en ny historikpost skapas. Med ft blir felet rimligt stort i stället för absurt: 6,56 ft räknas som 6,56 m och v ändras ungefär 4 gånger, vilket inte syns som uppenbart fel. Rapporterna flaggar avvikelsen, men kopierad text gör det inte. Äldre poster saknar `meta`, så exportens `notice` (som bygger på `meta.type`) täcker dem inte. | Räkna om `raw.B` till m vid inläsning när `rec.units.B` inte är `m`, eller vägra öppna posten med ett tydligt meddelande. Visa kontrollräkningens avvikelse även på kalkylatorsidan och i kopierad text. Märk äldre `blast_model`-poster i exporten utifrån `calc` och inte bara `meta`. |
| N3 | Låg | `catalog.js:413` (`VERIF_NOTE`), `FORMELGRANSKNING.md:986, 1001` | Statustexten innehåller ett fristående modellvärde, ”(≈ 20,81 m/s)”, utan de indata som gav det. Texten följer med i varje kopia, CSV, TXT, utskrift och JSON och kan läsas som ett referens- eller typvärde för v. | Ta bort siffran ur `VERIF_NOTE`, t.ex. ”v räknat med anteckningens exempelindata återger anteckningens v”. |
| N4 | Låg | `catalog.js:593` | Felmeddelandet för intervallfälten är ”Skriv intervallet som min–max, **t.ex. 1,5–3**.” Det visas för B (m), l (kg/m) och K. I fältet för B blir det ett siffersatt exempel på ett försättningsintervall, trots att hjälptexten medvetet säger ”a–b” och ”Appen fyller inte i något”. | Använd samma platshållare som i hjälptexten (”min–max, t.ex. a–b”) eller ett meddelande utan siffror. |
| N5 | Låg | `ui1.js:130` | Spärrmönstret matchar delsträngar. `tand` finns i ”standard”, ”avstånd”, ”stillestånd”, ”sprickavstånd” och ”medelavstånd”, så friskrivningen om sprängmodeller visas för helt orelaterade sökningar (Playwright). Det leder till att användaren slutar läsa varningar. | Matcha bara i början av ord, t.ex. `(^|\s)tand`. |
| N6 | Låg | `ui1.js:226` (`dl.kv dd`, metapanelerna är nu öppna), `style.css` | Horisontell scroll på `#/calc/blast_model` vid 320 px: `scrollWidth` 344 mot 320 (orsakat av ett `DD` i granskningsnoten). Övriga kontrollerade sidor och 390 px är utan överflöde. | `overflow-wrap:anywhere` på `.kv dd`. |
| N7 | Låg | `ui1.js:142` | Startsidans favoritrad för **formelfavoriter** (`f:blast_v`, `f:blast_t`) saknar EJ VERIFIERAD-badge, medan Favoriter-vyn har den (`ui2.js:219`). Namnet på `blast_t` innehåller inte ”ej verifierad”. | Skicka badgen även för `ty === 'f'` med typen `unverified`. |

**Nya påhittade värden eller påståenden:**
- Inga nya förifyllda värden för K, B, l, λ, intervall eller tändsteg. Självtestet kontrollerar att de inte finns (`tests.js:180, 288`).
- Inga nya gränsvärden, typvärden eller efterlevnadskontroller.
- Två siffersatta texter är nya: N3 (20,81 m/s i statustexten) och N4 (1,5–3 i felmeddelandet).
- Kodkommentaren `ui3.js:311` (”återställs inte efter rensning/import”) är delvis felaktig (L1).
- Utvecklarens uppgift om att README är omskriven stämmer inte (M3, L6).

### 8.3 Kvar att göra, i prioritetsordning
1. **N2:** omtolkning av äldre poster med annan enhet för B.
2. **M8:** gruppera också på mätvärdets art, komponent och instrument.
3. **L1:** låt inte ”Radera all lokal data” trigga första-start-favoriten.
4. **M3 och L6:** uppdatera README.
5. **M6:** begränsa siffrorna även i projekt-CSV för overifierade resultat.
6. **N3, N4:** ta bort siffror ur statustext och felmeddelande.
7. **N1, N5, N6, N7.**

---

## 9. Andra uppföljningen

**Datum:** 2026-10-14 (tredje genomgången, skrivskyddad). Bara de 12 punkter som inte var helt åtgärdade i avsnitt 8 har kontrollerats: M3, M6, M8, L1, L6 och N1–N7.

**Metod:**
- `index.html` innehåller exakt den aktuella källan (JS och CSS).
- `node run-tests.js`: **139/139 OK**.
- `README.md` lästes om. Filen är ändrad 20:07, efter min förra läsning, så M3 bedöms nu på den nya texten.
- Sökning, spärrmönster, `migrateLegacy` och felmeddelanden har körts i Node.
- I Chromium (Playwright) har följande kontrollerats:
  - startsidans favoriter
  - projekt-CSV och projekt-JSON
  - mätjournal → mätserie med blandad art, komponent och instrument
  - öppning, kopiering och rapport av en äldre post med B i ft
  - horisontellt överflöde vid 320, 360 och 390 px på 8 sidor
  - ”Radera all lokal data” följt av två omladdningar
  - spärrnotisen
- Inga JS-fel uppstod.

### 9.1 Status

| ID | Status | Belägg |
|---|---|---|
| M3 | **Åtgärdat** | README har nu en ”Viktigt”-ruta och ett avsnitt ”Egna modeller (ej verifierade)” som stämmer med appen: inga verifierade modeller för laddningsmängd, försättning, hålavstånd eller tändsekvens, och den egna anteckningen är inte en tändsekvensmodell. Påståendena i README om sökord, prefix, enhetslåsning och favorit har kontrollerats och stämmer. |
| M6 | **Åtgärdat** | Projekt-CSV skriver resultat med `sig` med 3 gällande siffror (`ui3.js:74`): ”20,8” m/s, ”0,8” m, ”0,0384” s. Allmänna formler har kvar full precision (”3,14159265359”). Projekt-JSON har full precision i `value`, vilket är rimligt för maskinläsbar data eftersom posten bär status och `sig: 3`. |
| M8 | **Åtgärdat** (ny bugg N8) | Nyckeln består av typ, enhet, projekt, plats, art, komponent och instrument (`ui2.js:160`, filtret `ui3.js:195`). Playwright: tre grupper på samma plats (Toppvärde/Vertikal, RMS/Vektorsumma, Toppvärde/Vertikal/instrument A) gav tre separata serier med 2 värden var. |
| L1 | **Åtgärdat** | `clearAllData` behåller nyckeln (`ui3.js:146`). Playwright: `[]` direkt efter rensning (nyckeln finns kvar), `[]` efter första omladdningen och `[]` efter andra. Vid allra första start är det fortfarande `["c:blast_model"]`, enligt ägarens önskemål. |
| L6 | **Delvis åtgärdat** | Klassgränserna (RQD/Deere) redovisas nu korrekt, liksom 13 kategorier, 59 kalkylatorer och 63 formler. **Men README säger ”Självtest … 136/136”, medan självtestet ger 139/139.** README hänvisar också till `TESTRAPPORT.md` och `SAKERHETSGRANSKNING.md`, som inte finns i `/home/claude/bergpro` (se N9). |
| N1 | **Åtgärdat** | Sökindexet tar bort negerade friskrivningar innan det indexerar (`catalog.js:710–712`). Node: ”tändintervall”, ”dimensionering”, ”dimensioneringsunderlag”, ”tändarsteg”, ”tändsekvens”, ”sekvens” och ”tändning” ger inga träffar. ”tändare” ger ingen modellträff. (Fortfarande gäller att ”laddning” och ”konstant” ger modellen via synonymen ”laddningskoncentration” och ”bergartskonstant”. Det är inte en negationsfråga, och träffarna har röd badge och Enter-spärr.) |
| N2 | **Åtgärdat** (kosmetisk rest) | `migrateLegacy` (`catalog.js:549–566`) räknar om B från mm, cm eller ft till m och tar bort den gamla enhetsnyckeln. Okända enheter ger en anteckning om att enheten inte längre stöds. Den används när en post öppnas, med en synlig gul ruta (`ui1.js:247, 258`), i kopierad text (`ui2.js:233–234`) och vid omräkning i rapporter (`ui3.js:19–25`). Playwright: posten 6,5617 ft öppnades som B = 2,00000616 m med texten ”Äldre post: Försättning B angavs som 6,5617 fot (ft) och har räknats om till 2,00001 m.” Kopierad text innehåller samma ”OBS: …”. Node: 2000 mm → 2 m, 200 cm → 2 m och resultatet blir som för 2 m. Exportens `notice` nämner nu `calc = "blast_model"` och äldre poster (`core.js:344`). *Rest:* en äldre posts lagrade resultat visas fortfarande med den gamla etiketten ”Tid (t) = 0,0384376 s” och 6 siffror i kopierad text och listor, eftersom lagrade resultat inte skrivs om. Statusraderna och ”inte ett tändintervall” följer ändå med. |
| N3 | **Åtgärdat** | `VERIF_NOTE` säger nu ”… återger anteckningens eget exempelvärde för v …” utan siffra (`catalog.js:413`). `FORMELGRANSKNING.md` är omgenererad (139/139) och innehåller inte längre ”20,81”. |
| N4 | **Åtgärdat** | Felmeddelandet är ”Skriv intervallet som två tal med bindestreck emellan (min–max).” utan siffror. |
| N5 | **Delvis åtgärdat** | ”tand” och de andra termerna kräver nu ordstart (`ui1.js:130`). ”standard”, ”avstånd”, ”stillestånd”, ”sprickavstånd”, ”medelavstånd” och ”tillstånd” visar inte längre notisen (Node och Playwright). **Men `sekvens` står kvar utan ordstart**, så ”konsekvens” och ”riskkonsekvens” visar friskrivningen om sprängmodeller (Playwright). ”konsekvens” är ett vanligt ord i riskbedömningar. ”salvor” (plural) fångas inte av `salva\b`. |
| N6 | **Åtgärdat** | `.kv dd{overflow-wrap:anywhere}`, badges får brytas och `.kv` blir en kolumn under 380 px (`style.css:184–186, 264–266`). Playwright: inget horisontellt överflöde vid 320, 360 eller 390 px på `#/calc/blast_model`, `#/formula/blast_t`, `#/formula/blast_v`, `#/calc/rqd`, `#/calc/c_sound`, `#/history`, `#/reg/journal` och `#/`. |
| N7 | **Åtgärdat** | Startsidans favoriter visar ”EJ VERIFIERAD” för `f:blast_v` och `f:blast_t` men inte för `f:freq` (`ui1.js:142`, Playwright). |

**Summering:** 10 Åtgärdade (M3, M6, M8, L1, N1, N2, N3, N4, N6, N7), 2 Delvis åtgärdade (L6, N5), 0 Ej åtgärdade.

### 9.2 Nya fynd

| ID | Grad | Plats | Beskrivning och belägg | Åtgärd |
|---|---|---|---|---|
| N8 | Låg | `ui2.js:160–163`, `ui3.js:193–195` | Grupperingsnyckeln för mätserier sätts ihop med tecknet `\|` av fritextfält (plats och instrument). Om en mätplats innehåller `\|` (t.ex. ”P\|X”) blir knappetiketten förvanskad (”X · Toppvärde · P · Vertikal”), och ett klick ger ”Kan inte beräkna. Rätta de markerade fälten.”, eftersom ingen post matchar filtret (Playwright). Inga felaktiga värden skapas, men serien går inte att öppna. | Skicka gruppens index (eller URI-kodade delar) i `data-k` i stället för en sammanslagen sträng. |
| N9 | Låg | `README.md` (”Tester som faktiskt körts”, punkt 4 i ”Kvalitetsarbete”) | README hänvisar till `TESTRAPPORT.md` och `SAKERHETSGRANSKNING.md`, men ingen av dem finns i projektmappen. Testpåståendena (”Gränssnitt i Chromium 111/111”, ”Android-emulering 91/91”, ”utskriften renderades till riktig PDF”) går därför inte att kontrollera. Raden ”26 fynd … Alla har åtgärdats” stämmer inte så länge L6 och N5 bara är delvis åtgärdade. | Lägg dokumenten i projektmappen eller ta bort hänvisningarna. Uppdatera självtestsiffran till aktuellt antal. Formulera statusen för säkerhetsgranskningen så att den stämmer med detta dokument. |

**Nya påhittade värden eller påståenden:** Inga nya förifyllda värden, gränsvärden, typvärden eller rekommenderade fördröjningar. De två sifferexemplen från förra omgången (N3, N4) är borttagna. Det enda nya påstående som inte stämmer är README:s ”Alla har åtgärdats” och hänvisningen till dokument som saknas (N9).

### 9.3 Kvar att göra
1. **N5:** kräv ordstart även för `sekvens` (så att ”konsekvens” inte träffas). Överväg att även fånga pluralformer som ”salvor”.
2. **L6 och N9:** uppdatera självtestsiffran i README (139/139), lägg till eller ta bort hänvisningarna till `TESTRAPPORT.md` och `SAKERHETSGRANSKNING.md`, och justera ”Alla har åtgärdats”.
3. **N8:** använd inte `|` som avgränsare för fritextfält i `data-k`.
4. (Kosmetiskt, N2:) äldre posters lagrade resultatetiketter (”Tid”) kan visas med nuvarande etikett, eller märkas ”äldre post”, i listor och kopior.

## 10. Utvecklarens åtgärder efter andra uppföljningen

> Avsnittet är skrivet av **utvecklaren**, inte av granskaren. Åtgärderna har verifierats med automatiska tester (se `TESTRAPPORT.md`). Granskaren har **inte** gjort någon tredje genomgång av dem.

| ID | Åtgärd | Verifiering |
|---|---|---|
| N5 | Spärrmönstret kräver nu ordstart även för `sekvens` och fångar `salva`, `salvan`, `salvor` och `salvorna` (`ui1.js`). | Gränssnittstester: ”riskkonsekvens” ger ingen notis och ”salvor” ger notis. Tidigare kontroller av ”standard” och ”sprickavstånd” är fortsatt utan notis. |
| N8 | Grupperingsnyckeln för mätserier är nu JSON i stället för en sträng med `\|` (`ui2.js`, `ui3.js`). | Gränssnittstest: mätplatsen ”Punkt \| C” ger en korrekt knapp, och serien räknas med 2 värden. |
| N2 (rest) | Ny funktion `shownResults()`: lagrade poster från ej verifierade modeller räknas om från de migrerade indata. Listor, kopierad text och rapporter visar därför alltid aktuella etiketter och 3 gällande siffror. Vanliga formler visar lagrade värden som förut. | Självtest ”Äldre poster från egna modellen visas med aktuella etiketter och 3 siffror”. |
| L6, N9 | README har uppdaterade testsiffror. `TESTRAPPORT.md` och `SAKERHETSGRANSKNING.md` ligger i projektmappen. Statusen för säkerhetsgranskningen formuleras så att den stämmer med det här dokumentet. | Manuell kontroll av README mot `TESTRAPPORT.md`. |

**Samlad status efter alla genomgångar:**

| Status | Antal |
|---|---|
| Ursprungliga fynd (H1–H5, M1–M11, L1–L10) bekräftat åtgärdade av granskaren | 25 av 26 |
| Ursprungliga fynd åtgärdade av utvecklaren efter sista granskningen och verifierade med tester | 1 (L6) |
| Nya fynd (N1–N9) bekräftat åtgärdade av granskaren | 6 (N1, N2 i huvudsak, N3, N4, N6, N7) |
| Nya fynd åtgärdade av utvecklaren och verifierade med tester | N5, N8, N9 och resten av N2 |
