# BergPro

Tekniskt beräkningsverktyg för bergmekanik, geometri, borrproduktion, vibrationsmätning, statistik, enhetsomvandling och ekonomi. Hela appen är **en enda fil: `index.html`** (HTML + CSS + JavaScript, ca 300 kB). Inga bibliotek, CDN:er, API:er eller servrar.

> **Viktigt:** BergPro är beräkningshjälp. Den ersätter aldrig behörig sprängteknisk kompetens eller en projektspecifik riskbedömning. Appen innehåller inga gränsvärden eller riktvärden, inga verifierade modeller för laddningsmängd, försättning, hålavstånd eller tändsekvens och inga dimensioneringsmallar. Under **Egna modeller** finns användarens egen, **ej verifierade** anteckning. Den är inte en tändsekvensmodell och får inte användas som dimensioneringsunderlag.

## Använda appen
1. Spara `index.html` på telefonen eller datorn.
2. Öppna filen i webbläsaren. På Android: öppna den från Filer/Nedladdningar och välj **Öppna med Chrome**, inte filhanterarens förhandsvisning. Ingen installation eller server behövs, och appen fungerar utan internet.
3. Lägg gärna till den på hemskärmen via webbläsarens meny.

Data sparas i webbläsarens `localStorage` på just den enheten. Det gäller favoriter, historik, sparade resultat, projekt, journaler och inställningar. Under **Inställningar** visas om lagringen är beständig. Exportera till JSON regelbundet som säkerhetskopia. Om lagring inte fungerar (t.ex. i vissa privata lägen) visas en varning, och data finns då bara kvar tills sidan stängs. Blir lagringen full tas de äldsta historikposterna bort automatiskt. Projekt och sparade resultat påverkas inte.

## Funktioner
- **Struktur för sprängarbasen:** startsidan har *Vanliga uppgifter* (räkna volym, vikt, borrmeter, borrtakt, analysera vibrationsmätning, mätjournal, kostnad per m³, omvandla enheter) och kategorierna grupperade efter arbetsmoment: *Före sprängning, Mätning, Uppföljning, Verktyg och dokument*. Varje kalkylator har en mening i klarspråk om när den används, och sidan *Så fungerar BergPro* förklarar appen, etiketterna och vad appen inte gör.
- **Startsida:**
  - sökning medan man skriver i namn, kategori, synonymer, beskrivning och relaterade begrepp
  - 8 snabbknappar och 13 kategorikort
  - favoriter, senast använda, senaste projekt samt sparade resultat och mätningar
- **59 kalkylatorer** i en gemensam komponent: formel, indata med enheter, validering, resultat, mellanled, kopiera, spara, favorit, antaganden, källa och verifieringsstatus.
- **63 formler** i ett sökbart register. Varje formel har uttryck, variabler med enheter, giltighetsområde, antaganden, en spårbar källa, version, verifieringsstatus och en granskningsanteckning.
- **Enhetsomvandlare** för 14 storheter med exakta definitionsfaktorer, och en **uttrycksräknare** med egen tolk (ingen `eval`).
- **Register:**
  - mätjournal med mätvärdets art (topp/RMS), komponent, frekvens, vägning, salvreferens, instrument och kalibrering
  - sprickregistrering per mätlinje och projekt
  - mätserier från journalen blandar aldrig olika projekt, platser, topp/RMS, komponenter eller instrument
  - bergförhållanden, källregister, riskanteckningar, antaganden och granskning
- **Projekt och rapporter:** kostnader och nyckeltal. Export till text, CSV, JSON och utskrift. För PDF väljer du **Spara som PDF** i utskriftsdialogen.
- **Lättanvänt:** resultatet uppdateras medan du skriver (Beräkna sparar i historiken), och sällan använda fält ligger under en hopfälld del ”Avancerat”.
- **Egna modeller:** din handskrivna modell, se nedan.

## Egna modeller (ej verifierade)
Kalkylatorn **”Egen modell: v och kvoten λ/v (ej verifierad)”** räknar v = K / B^a · l^b och t = λ / v enligt dina anteckningar. Den oberoende säkerhetsgranskningen ledde till följande:
- Kalkylatorn visar statusen och de öppna frågorna överst, i rött, innan man räknar:
  - Anteckningens λ-exempel är inkonsekvent: 40 % av 2 m är 0,8 m, inte 1,6 m.
  - Det är inte fastställt vilken fysikalisk storhet v är.
- **t presenteras inte som ett tändintervall.** Det heter "Kvot λ/v – inte ett tändintervall" och visas bara i sekunder med 3 gällande siffror. Appen avrundar inte till tändarsteg och föreslår ingen tändsekvens.
- **K efter bergart:** väljer du bergart föreslås K enligt din anteckning – gnejs 22, granit 25, kvartsit 27, skiffer 18, alunskiffer 15 – med anteckningen som källa och markerat som ej verifierat. Du kan skriva ett eget K; avviker det från anteckningens värde visas en upplysning och ditt värde används.
- B, l och λ fylls aldrig i av appen. B är låst till m och l till kg/m, som anteckningen förutsätter. Exponenterna 1,17 och 0,39 är förifyllda från anteckningen och kan ändras.
- λ anges i % av B eller i meter. Du kan ange ett eget giltighetsområde från din källa, och appen varnar om indata ligger utanför det.
- Statusen **EJ VERIFIERAD** följer med resultatet överallt:
  - i listor och sökträffar
  - i kopierad text och sparade namn (prefix)
  - i historik-CSV, projektrapporter (text, CSV, JSON), utskrift och JSON-export
- Modellen hittas inte på sökord som "tändsekvens" eller "fördröjning". Den är stjärnmärkt vid allra första start, och stjärnan kommer inte tillbaka efter rensning.

## Avgränsningar
- **RMR och Q-systemet är inte implementerade**, eftersom fullständiga, verifierade regler och källor saknas i appen.
- **Inga gränsvärden eller riktvärden** för vibration, luftstötvåg eller miljö. Inga priser och inga standardnummer är förifyllda.
- **Inbyggda klassgränser:** RQD-kalkylatorn visar Deeres beskrivande klasser (25/50/75/90 %). De är bekräftade i sekundärlitteratur och markerade så.
- **Granskning:** formelgranskningen och säkerhetsgranskningen är gjorda av en AI-assistent mot angivna källor. **De ersätter inte fackgranskning av behörig person.** Formler som har kontrollerats mot källa märks "Kontrollerad mot källa (ej fackgranskad)".

## Kvalitetsarbete 2026-10-14
1. **Matematikmotorn rättades:**
   - kcal/h var inkonsekvent med kcal
   - uttrycksräknaren kraschade vid djup nästling och avrundade −2,5 fel
   - för många siffror tappade precision utan att det syntes
   - minustecken i tiopotensform
   - förifyllda värden för ν = 0,25 och c = 343 m/s som kunde användas utan att man märkte det
   - en krasch vid ogiltig enhet i trapetsmetoden
2. **Alla 63 formler granskades** med avseende på enheter, antaganden, giltighetsområde och spårbar källa. Detaljerna står i `FORMELGRANSKNING.md`, som genereras från appens register. Ljudhastigheten följer nu ISO 9613-1. Nya varningar gäller dB-summering av toppnivåer, Biot-koefficienten och skenbart sprickavstånd.
3. **Android:** prestandan för långa mätserier förbättrades (3,6 s → 0,7 s på en strypt äldre telefon). Det gjordes även bättre tryckytor (≥ 44 px), skydd mot full lagring, dialoger som stängs vid bakåtgest och ett sökindex som byggs i förväg.
4. **Oberoende säkerhetsgranskning:** 26 fynd, varav 5 höga och 0 kritiska. Granskaren gjorde två uppföljningar av åtgärderna:
   - 25 av de 26 fynden och 6 av 9 nya fynd bekräftades som åtgärdade.
   - De sista punkterna (en README-detalj och tre små fynd med låg allvarlighetsgrad) åtgärdades efteråt och verifierades med automatiska tester, men inte i en ny granskningsomgång.
   - Allt redovisas i `SAKERHETSGRANSKNING.md`.

## Tester som faktiskt körts
Se `TESTRAPPORT.md` för detaljer, inklusive en checklista för test på riktig Android-telefon.
- **Självtest** (`node run-tests.js`, även Mer → Självtest i appen): **141/141**. Det omfattar:
  - kända värden för alla kalkylatorer
  - en oberoende referenstabell för samtliga enhetsfaktorer
  - inversa samband
  - ett slumptest med 200 slumpade indatauppsättningar per kalkylator
  - omräkning av äldre poster
  - lagring, import och export
  - modellens status
- **Gränssnitt i Chromium på dator: 131/131.**
- **Android-emulering: 92/92.** Testat på Pixel 7, Galaxy S24, Galaxy A55, Galaxy S8, Galaxy Tab S9 och Moto G4 med pekskärm. Utskriften renderades till riktig PDF.
- **Inte testat:** riktig Android-telefon, iOS/Safari, Firefox, TalkBack och den riktiga utskriftsdialogen.

## Utveckling
Källan ligger i `src/`: kärna, katalog, tester, tre gränssnittsfiler, CSS och HTML-skal. Kommandon:
- `node build.js` sätter ihop `index.html`.
- `node run-tests.js` kör självtestet.
- `node review-report.js` genererar `FORMELGRANSKNING.md`.
