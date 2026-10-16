# BergPro – testrapport

Körd: 2026-10-16 18:52 (UTC) mot `index.html` byggd från `src/`. Endast tester som faktiskt har körts redovisas.

| Svit | Miljö | Resultat |
|---|---|---|
| Självtest (beräkningsmotor, enheter, lagring) | Node v22.22.0 och i appen (Mer → Självtest) | **141/141** |
| Gränssnitt, dator | Chromium (Playwright), `file://`, 320–1200 px | **131/131 godkända** |
| Gränssnitt, Android-emulering | Chromium med Android-profiler (pekskärm, mobil-UA, DPR) | **92/92 godkända** |

## Vad emuleringen inte ersätter
Android-testerna körs i samma webbläsarmotor som Chrome för Android (Chromium) med riktiga enhetsprofiler, men inte på en fysisk telefon. Filåtkomst via filhanteraren, beständighet för lokala filer, systemets utskriftsdialog, tangentbord och TalkBack måste kontrolleras på telefonen – se checklistan sist.

## 1. Självtest (141 st)

- ✅ Svensk decimalinmatning: "1 234,5" = 1234,5
- ✅ Decimalpunkt och exponent: "1,2e-3"
- ✅ Unicode-minus accepteras
- ✅ Ogiltig text avvisas ("abc", "1,2,3", "1.234,5")
- ✅ Tomt fält ger "empty"
- ✅ Lista med komma-decimaler
- ✅ Formatering: 1234,5 → "1 234,5" (hårt mellanrum)
- ✅ Formatering: NaN/Infinity ger "–"
- ✅ Uttryck: 2+3*4 = 14
- ✅ Uttryck: (1+2)^2 = 9
- ✅ Uttryck: 2^3^2 = 512 (högerassociativ)
- ✅ Uttryck: -2^2 = -4
- ✅ Uttryck: sqrt(16)+1,5*2 = 7
- ✅ Uttryck: max(1;5;3) = 5
- ✅ Uttryck: sin(30) i grader = 0,5
- ✅ Uttryck: division med noll avvisas
- ✅ Uttryck: eval/skadlig kod avvisas
- ✅ Enhet: 1 tum = 25,4 mm
- ✅ Enhet: 1 kWh = 3,6 MJ
- ✅ Enhet: 1 atm = 101,325 kPa
- ✅ Enhet: 1 psi = 6894,757 Pa
- ✅ Enhet: 1 g/cm³ = 1000 kg/m³
- ✅ Enhet: 36 km/h = 10 m/s
- ✅ Enhet: 1 L = 0,001 m³ och 1 m³ = 35,3147 ft³
- ✅ Enhet: kgf/cm² ≠ kg/cm² (kraft): 1 kgf/cm² = 98,0665 kPa
- ✅ Enhet: rundresa längd→area→volym alla grupper
- ✅ Cirkelarea r=2 m → 12,566370614 m²
- ✅ Cirkelarea från diameter 4 m = samma
- ✅ Rektangelarea 3,5 × 2 = 7
- ✅ Triangelarea 4 × 3 = 6
- ✅ Cylindervolym r=0,5, h=2 → 1,5707963 m³
- ✅ Rätblock 2×3×4 = 24 m³ = 24000 L
- ✅ Rätblock med enhetsval: 200 cm × 1 m × 50 cm = 1 m³
- ✅ Trapetsmetoden: A=10,20,30 vid s=0,10,20 → 400 m³
- ✅ Trapetsmetoden: icke-stigande stationer avvisas
- ✅ Trapetsmetoden: en rad räcker inte
- ✅ Massa från volym: 10 m³ × 2,7 t/m³ = 27 t
- ✅ Volym från massa: 27 t / 2,7 t/m³ = 10 m³
- ✅ Normalspänning: 100 kN / 0,5 m² = 200 kPa = 0,2 MPa
- ✅ Normalspänning: 1000 N på 100 mm² = 10 MPa
- ✅ Normalspänning: area 0 avvisas
- ✅ Normalspänning: tomt fält avvisas
- ✅ Skjuvspänning: 50 kN / 0,25 m² = 0,2 MPa
- ✅ Relativ deformation: 0,5 mm / 100 mm = 0,005 = 0,5 %
- ✅ E-modul: 50 MPa / 0,001 = 50 GPa
- ✅ E-modul: ε = 0 avvisas (division med noll)
- ✅ Poissons tal: −(−0,0005)/0,002 = 0,25
- ✅ Poissons tal ≥ 0,5 avvisas
- ✅ Skjuvmodul: E=50 GPa, ν=0,25 → 20 GPa
- ✅ Volymmodul: E=60 GPa, ν=0,25 → 40 GPa
- ✅ Volymmodul: ν = 0,5 avvisas
- ✅ Densitet: 2700 kg / 1 m³ → 2,7 g/cm³
- ✅ Tunghet: 2700 kg/m³ · 9,81 = 26,487 kN/m³
- ✅ Effektiv spänning: 500 − 150 = 350 kPa
- ✅ Effektiv spänning: u > σ ger varning
- ✅ Mohr–Coulomb: c=10, σ′=100 kPa, φ=30° → 67,735 kPa
- ✅ Mohr–Coulomb: portryck minskar hållfastheten
- ✅ Mohr–Coulomb: säkerhetsfaktor
- ✅ Mohr–Coulomb: φ = 90° avvisas
- ✅ RQD: körlängd 1,5 m, bitar 30 25 8 20 15 12 5 cm → 70 %
- ✅ RQD: exakt 10 cm räknas med (≥ 100 mm)
- ✅ RQD: bitar längre än körlängden avvisas
- ✅ Sprickfrekvens: 12 sprickor på 6 m = 2 /m, s = 0,5 m
- ✅ Sprickfrekvens: icke-heltal avvisas
- ✅ Sprickavstånd: 6 m / 12 = 0,5 m
- ✅ Frekvens: T=0,02 s → 50 Hz
- ✅ Periodtid: 50 Hz → 20 ms
- ✅ Vinkelhastighet: 50 Hz → 314,159 rad/s
- ✅ Harmonisk: 50 Hz, v=10 mm/s → u=0,0318 mm, a=3,1416 m/s²
- ✅ Harmonisk: exakt en storhet krävs
- ✅ Sinus: topp 10 → RMS 7,0711, p–p 20
- ✅ Medelvärde av 2 4 4 4 5 5 7 9 = 5
- ✅ Stickprovsstandardavvikelse samma serie = 2,13809
- ✅ Standardavvikelse med 1 värde avvisas
- ✅ RMS av 3 och 4 = 3,5355
- ✅ Toppvärde (största absolut) av −7 3 5 = 7
- ✅ Topp-till-topp av −7 3 5 = 12
- ✅ Mätvärdeslista med ogiltigt värde avvisas
- ✅ Absolut avvikelse: 10,3 − 10 = 0,3
- ✅ Relativ avvikelse: 10,5 mot 10 = 5 %
- ✅ Relativ avvikelse: referens 0 avvisas
- ✅ Kombinerad osäkerhet: 3 och 4 → 5; U (k=2) = 10
- ✅ Mätserie: nyckeltal och diagram skapas
- ✅ Total borrad längd 18 + 21,5 + 20 = 59,5 m
- ✅ Borrmeter per timme: 120 m / 8 h = 15 m/h
- ✅ Arbetstid: 6 h + 2 h = 8 h, utnyttjande 75 %
- ✅ Maskintid: 8 − 2 = 6 h; stillestånd > arbetstid avvisas
- ✅ Stillestånd: 8 − 6 = 2 h
- ✅ Bränsle per maskintimme: 120 l / 6 h = 20 l/h
- ✅ Bränsle per enhet: 90 l / 300 m³
- ✅ Planerad mot faktisk: 800 → 740 = −60 (92,5 %)
- ✅ Total kostnad: 1000 + 2500,5 + 300 = 3800,5
- ✅ Kostnad per meter: 60000 kr / 120 m = 500
- ✅ Kostnad per m³: 90000 / 450 m³ = 200
- ✅ Kostnad per timme: 40000 / 80 h = 500
- ✅ Budgetavvikelse: 110 000 − 100 000 = +10 000; 10 %
- ✅ Budgetavvikelse i procent: budget 0 avvisas
- ✅ Bränslekostnad: 200 l × 18,5 kr = 3700 kr
- ✅ Nivå: 1 Pa → 93,9794 dB re 20 µPa
- ✅ Nivå: 1 kPa = 153,979 dB (enhetsval kPa)
- ✅ Tryck från nivå: 94 dB ≈ 1,0024 Pa (inversen)
- ✅ Summering av nivåer: 60 + 60 dB = 63,0103 dB
- ✅ Ljudhastighet (ISO 9613-1 A.5): 20 °C → 343,2 m/s exakt; 0 °C → 331,29 m/s; varning utanför −20…50 °C
- ✅ Ljudhastighet: under absoluta nollpunkten avvisas
- ✅ Avstånd från gångtid: 343 m/s · 2 s = 686 m
- ✅ Medelhastighet: 100 m / 20 s = 5 m/s = 18 km/h
- ✅ Inga NaN/Infinity i något resultat (provkörning av alla kalkylatorer med godtyckliga provvärden)
- ✅ Alla formler har obligatoriska fält och giltig status
- ✅ Formel-ID:n är unika och varje kalkylator har en formel
- ✅ Sökning: "volym" hittar cylinder; "decibel" hittar nivå; "rqd" hittar RQD
- ✅ Sökning: tomt resultat vid nonsens
- ✅ Import: giltig export accepteras, ogiltig avvisas
- ✅ Lagring: spara och läsa tillbaka via minnesbackend; otillgänglig lagring hanteras
- ✅ Egen modell: aritmetiken kontrollräknad (ingen validering av modellen)
- ✅ Egen modell: validering, enhetslåsning, begränsad precision och giltighetsområde
- ✅ Egen modell: söks inte fram på tändsekvens/fördröjning och benämns inte fördröjning
- ✅ Enheter: varje faktor stämmer med oberoende referenstabell (SI/NIST SP 811)
- ✅ Enheter: härledda samband (effekt × tid = energi, kraft/area = tryck)
- ✅ Inversa par: massa ↔ volym, frekvens ↔ period, nivå ↔ tryck
- ✅ Elasticitet: G och K från samma E, ν uppfyller E = 9KG/(3K+G) och ν = (3K−2G)/(2(3K+G))
- ✅ Hookes lag: spänning från F/A och töjning från ΔL/L₀ ger E = σ/ε
- ✅ Harmonisk svängning: samma resultat oavsett vilken storhet som anges
- ✅ Geometri: cylindervolym = cirkelarea · h; A = C·r/2; trapetsmetoden exakt för linjär area
- ✅ Mohr–Coulomb: c = 0 och φ = 45° ger τ_f = σ′; φ = 0 ger τ_f = c
- ✅ RQD: 100 % när alla bitar ≥ 10 cm fyller körlängden, 0 % när alla < 10 cm
- ✅ dB: en nivå summerad med sig själv n gånger = L + 10·log₁₀(n); orimliga nivåer avvisas
- ✅ Ljudhastighet: den äldre formeln 331,3·√(1 + T/273,15) avviker mindre än 0,02 m/s inom −20…50 °C
- ✅ Granskning: varje formel har granskningsanteckning, datum och precis källa
- ✅ Produktion och ekonomi: tidsposter och nyckeltal hänger ihop
- ✅ Inga tysta förifyllda material- eller miljöparametrar (endast g och modellexponenter)
- ✅ Inmatning: gällande siffror, nollor och tusentalsavgränsare
- ✅ Formatering: aldrig "e"-notation, alltid decimalkomma och minus-tecken
- ✅ Uttryck: avrundning bort från noll, prioritet och gränser
- ✅ Slumptest: 200 slumpade indatauppsättningar per kalkylator ger antingen giltigt resultat eller tydligt fel – aldrig krasch, NaN eller Infinity
- ✅ Diagram: långa serier förenklas men behåller största och minsta värdet (toppar)
- ✅ Lagring: full lagring tar bort äldsta historik, behåller projekt och sparade resultat
- ✅ Äldre poster: B sparad i annan enhet räknas om till meter med upplysning
- ✅ Sökning: friskrivningstext gör inte modellen sökbar (tändintervall, dimensionering, tändare)
- ✅ Status och exempelvärden: inga sprängtekniska talvärden i statustexter eller felmeddelanden
- ✅ Äldre poster från egna modellen visas med aktuella etiketter och 3 siffror
- ✅ Egen modell: K efter bergart enligt anteckningen (gnejs 22, granit 25, kvartsit 27, skiffer 18, alunskiffer 15)

## 2. Gränssnitt på dator (131 kontroller)

- ✅ start renderar sökfält
- ✅ modellen är stjärnmärkt från start
- ✅ ingen horisontell scroll (hem, 390px)
- ✅ sök "volym" ger träffar
- ✅ sök synonym/tunghet träffar
- ✅ sök utan träff ger tomläge
- ✅ sökträff öppnar kalkylator
- ✅ sökning kvar efter tillbaka
- ✅ alla 12 kategorier öppnas
- ✅ vy #/help renderar
- ✅ ingen h-scroll #/help
- ✅ vy #/formulas renderar
- ✅ ingen h-scroll #/formulas
- ✅ vy #/units renderar
- ✅ ingen h-scroll #/units
- ✅ vy #/tool/quick renderar
- ✅ ingen h-scroll #/tool/quick
- ✅ vy #/reg/journal renderar
- ✅ ingen h-scroll #/reg/journal
- ✅ vy #/reg/fractures renderar
- ✅ ingen h-scroll #/reg/fractures
- ✅ vy #/reg/sources renderar
- ✅ ingen h-scroll #/reg/sources
- ✅ vy #/projects renderar
- ✅ ingen h-scroll #/projects
- ✅ vy #/settings renderar
- ✅ ingen h-scroll #/settings
- ✅ vy #/more renderar
- ✅ ingen h-scroll #/more
- ✅ vy #/favs renderar
- ✅ ingen h-scroll #/favs
- ✅ vy #/history renderar
- ✅ ingen h-scroll #/history
- ✅ vy #/verif renderar
- ✅ ingen h-scroll #/verif
- ✅ vy #/selftest renderar
- ✅ ingen h-scroll #/selftest
- ✅ vy #/about renderar
- ✅ ingen h-scroll #/about
- ✅ vy #/cats renderar
- ✅ ingen h-scroll #/cats
- ✅ alla kalkylatorer renderar
- ✅ rätblock 2·3·4 = 24
- ✅ tomt fält ger felmeddelande
- ✅ text avvisas
- ✅ decimalkomma: 1,5·2·2 = 6
- ✅ kopiera ger toast
- ✅ spara resultat lagras
- ✅ favorit lagras
- ✅ historik lagras
- ✅ data finns efter omladdning
- ✅ historiklista visar post
- ✅ sparade-flik visar post
- ✅ favoritlista visar post
- ✅ öppna tidigare resultat räknar om
- ✅ kategorin Egna modeller visar kalkylatorn och varning
- ✅ kalkylatorsidan visar statusruta och öppna frågor före formeln
- ✅ K, B, l är tomma från start
- ✅ val av bergart granit fyller K = 25 (från anteckningen)
- ✅ modell: v visas med 3 siffror (20,8 m/s), t = 0,0769 s
- ✅ modell visar ej-verifierad-varning
- ✅ resultatkortet märkt EJ VERIFIERAD med varningar före knapparna
- ✅ kopierad text innehåller status och tändintervallsvarning
- ✅ sparat namn får prefix [EJ VERIFIERAD egen modell]
- ✅ historiken visar EJ VERIFIERAD-etikett
- ✅ startsidan visar etikett på favorit/sparat
- ✅ sök tändsekvens: besked om att modeller saknas, modellen hittas inte
- ✅ sök gränsvärde: besked om att gränsvärden saknas
- ✅ Enter öppnar inte ej verifierad modell direkt
- ✅ 1 in = 25,4 mm
- ✅ 1 bar = 100 kPa
- ✅ ogiltigt enhetsvärde ger fel
- ✅ 2*(3+4)^2 = 98
- ✅ 1/0 ger fel, inte Infinity
- ✅ farlig kod körs ej (ingen eval)
- ✅ mätpost sparas (3 st)
- ✅ mätserie-knapp grupperar per plats (Punkt B ensam → ingen knapp)
- ✅ journal: tomt värde avvisas
- ✅ serieanalys-knapp visas
- ✅ serieanalys räknar och ger diagram
- ✅ sprickfrekvens per mätlinje: L1 3/10 = 0,3; L2 utan längd
- ✅ projekt skapas och öppnas
- ✅ kostnad 10000/100 m = 100 kr/m
- ✅ kostnad per m³ = 200
- ✅ textrapport innehåller projektnamn och kostnad
- ✅ CSV-rapport laddas ned
- ✅ JSON-rapport giltig
- ✅ rapport innehåller kopplad beräkning (formel+källa)
- ✅ textrapport: modellblock har status, båda formlerna och varningar
- ✅ CSV-rapport har STATUS-rad och varningskolumn
- ✅ projekt-JSON märker ej verifierade poster
- ✅ utskrift genererar rapport
- ✅ utskrift: statusruta för ej verifierad modell
- ✅ JSON-export innehåller data
- ✅ import (slå ihop) återställer projekt
- ✅ felaktig export avvisas
- ✅ ogiltig JSON ger felmeddelande
- ✅ ljust tema
- ✅ självtest i appen: alla OK
- ✅ självtest förorenar inte användardata
- ✅ rensa historik efter bekräftelse
- ✅ live: resultatet visas medan man skriver (3·4 = 12)
- ✅ live: sparas inte i historiken förrän man trycker Beräkna
- ✅ Beräkna sparar i historiken
- ✅ egna modellen: avancerade fält hopfällda
- ✅ egna modellen: live-resultat med bergart och en samlad varningsruta
- ✅ sök "standard" ger inget sprängbesked (N5)
- ✅ sök "sprickavstånd" ger inget sprängbesked (N5)
- ✅ sök "riskkonsekvens" ger inget sprängbesked (N5)
- ✅ sök "salvor" ger besked om att modeller saknas (N5)
- ✅ sök "tändintervall": besked visas, modellen hittas inte (N1)
- ✅ äldre post med B i mm räknas om till 2 m och visar upplysning (N2)
- ✅ kopierad text från äldre post innehåller omräkningsupplysning (N2)
- ✅ ingen h-scroll 320px på egna modellen (N6)
- ✅ formelfavorit från modellen har etikett på startsidan (N7)
- ✅ sidomeny syns på dator
- ✅ bottenmeny dold på dator
- ✅ ingen h-scroll 320px #/
- ✅ ingen h-scroll 320px #/cats
- ✅ ingen h-scroll 320px #/calc/series
- ✅ ingen h-scroll 320px #/formulas
- ✅ ingen h-scroll 320px #/units
- ✅ liggande läge utan h-scroll
- ✅ mätplats med "|" ger korrekt seriknapp (N8)
- ✅ serien med "|" i platsnamnet räknas (2 värden)
- ✅ efter "Radera all lokal data" + omstart kommer favoriten inte tillbaka (L1)
- ✅ varning visas när lagring saknas
- ✅ appen fungerar utan lagring (inga fel)
- ✅ fungerar offline
- ✅ inga JS-fel under hela körningen
- ✅ alla data-act har handler

## 3. Android-emulering (92 kontroller)


**Pixel 7**

- ✅ UA är Android/mobil (412×839)
- ✅ alla vyer renderar
- ✅ ingen horisontell scroll i någon vy
- ✅ bottenmeny synlig, sidomeny dold
- ✅ bottenmenyn täcker inte sista innehållet
- ✅ inga JS-fel

**Pixel 7 landscape**

- ✅ UA är Android/mobil (863×360)
- ✅ alla vyer renderar
- ✅ ingen horisontell scroll i någon vy
- ✅ bottenmeny synlig, sidomeny dold
- ✅ bottenmenyn täcker inte sista innehållet
- ✅ inga JS-fel

**Galaxy S24**

- ✅ UA är Android/mobil (360×780)
- ✅ alla vyer renderar
- ✅ ingen horisontell scroll i någon vy
- ✅ bottenmeny synlig, sidomeny dold
- ✅ bottenmenyn täcker inte sista innehållet
- ✅ inga JS-fel

**Galaxy A55**

- ✅ UA är Android/mobil (480×1040)
- ✅ alla vyer renderar
- ✅ ingen horisontell scroll i någon vy
- ✅ bottenmeny synlig, sidomeny dold
- ✅ bottenmenyn täcker inte sista innehållet
- ✅ inga JS-fel

**Galaxy S8**

- ✅ UA är Android/mobil (360×740)
- ✅ alla vyer renderar
- ✅ ingen horisontell scroll i någon vy
- ✅ bottenmeny synlig, sidomeny dold
- ✅ bottenmenyn täcker inte sista innehållet
- ✅ inga JS-fel

**Galaxy S8 landscape**

- ✅ UA är Android/mobil (740×360)
- ✅ alla vyer renderar
- ✅ ingen horisontell scroll i någon vy
- ✅ bottenmeny synlig, sidomeny dold
- ✅ bottenmenyn täcker inte sista innehållet
- ✅ inga JS-fel

**Galaxy Tab S9**

- ✅ UA är Android/mobil (640×1024)
- ✅ alla vyer renderar
- ✅ ingen horisontell scroll i någon vy
- ✅ bottenmeny synlig, sidomeny dold
- ✅ bottenmenyn täcker inte sista innehållet
- ✅ inga JS-fel

**Moto G4**

- ✅ UA är Android/mobil (360×640)
- ✅ alla vyer renderar
- ✅ ingen horisontell scroll i någon vy
- ✅ bottenmeny synlig, sidomeny dold
- ✅ bottenmenyn täcker inte sista innehållet
- ✅ inga JS-fel

**Pixel 7 (flöde)**

- ✅ sökning medan man skriver ("tryck")
- ✅ tryck på sökträff öppnar sida
- ✅ Android-bakåt behåller sökningen
- ✅ Enter i sökfältet öppnar första träffen
- ✅ kraft (kan vara negativ) får fullt tangentbord, area får decimaltangentbord
- ✅ inmatningsfält har minst 16 px text
- ✅ beräkna med pek: 100 kN / 0,5 m² = 0,2 MPa
- ✅ tomt fält: felmeddelande och fokus på fältet
- ✅ blandade decimaltecken avvisas
- ✅ enhetsval på mobil: 100 kN / 500 cm² = 2 MPa
- ✅ byte av storhet byter enhetslista (acceleration)
- ✅ flerradig inmatning i textruta ger tabell och diagram
- ✅ projekt skapas via pek
- ✅ kostnad läggs till, nyckeltal 60 kr/m
- ✅ dialogrutan ryms på skärmen
- ✅ sparade resultat syns i projektet (2 st)
- ✅ meddelanden (toast) visas ovanför bottenmenyn
- ✅ rapport TXT laddas ned (bergpro-android-test-2026-10-16.txt)
- ✅ rapport CSV laddas ned (bergpro-android-test-2026-10-16.csv)
- ✅ rapport JSON laddas ned (bergpro-android-test-2026-10-16.json)
- ✅ CSV har BOM och semikolon (öppnas rätt i svensk Excel)
- ✅ utskrift anropar webbläsarens utskriftsdialog
- ✅ användaren informeras om "Spara som PDF"
- ✅ utskrifts-PDF innehåller projekt, indata, formel, resultat, källa och status
- ✅ utskrift innehåller inte appens meny/knappar
- ✅ mättid använder inbyggd datum/tid-väljare
- ✅ topp/RMS från samma plats slås inte ihop till en mätserie (M8)
- ✅ mätpost redigeras
- ✅ mätpost raderas efter bekräftelse
- ✅ historiksökning filtrerar
- ✅ radera all data efter bekräftelse
- ✅ importdialog visar innehållet
- ✅ import återställer exakt samma data
- ✅ importerad data finns kvar efter omstart
- ✅ felaktig importfil avvisas med förklaring
- ✅ bakåt: kalkylator → kategori → kategorier → hem
- ✅ bakåtgest med öppen dialog lämnar ingen kvarglömd dialog
- ✅ appens tillbakaknapp fungerar
- ✅ ljust tema på mobil
- ✅ inga JS-fel under flödet

**Moto G4 (4× långsammare CPU)**

- ✅ start till användbar sida: 354 ms
- ✅ sökresultat efter inmatning: 99 ms
- ✅ mätserie med 5000 värden (tabell + diagram): 387 ms
- ✅ tabellen anger att 200 av 5000 visas

## Kvar att testa på en riktig Android-telefon

Emuleringen täcker skärmstorlekar, pekskärm, Android-webbläsarens motor, utskriftslayout och nedladdningar. Följande beror på telefonen, filhanteraren och Android-versionen och kan bara kontrolleras på en riktig enhet (tar ca 10 minuter):

| # | Gör så här | Förväntat resultat |
|---|---|---|
| 1 | Kopiera `index.html` till telefonen. Öppna den från Filer/Nedladdningar och välj **Öppna med Chrome** (inte filhanterarens egen förhandsvisning). | Startsidan visas, ingen gul lagringsvarning. |
| 2 | Stjärnmärk en kalkylator. Stäng Chrome helt (svep bort appen) och öppna filen **på samma sätt** igen. | Stjärnan finns kvar. *Om den saknas sparar telefonen inte data för lokala filer – använd Exportera/Importera JSON eller lägg filen på en webbserver.* |
| 3 | Inställningar → titta på raden **Lagring**. | Helst ”beständig”. Står det att webbläsaren kan rensa: exportera JSON regelbundet. |
| 4 | Slå på **flygplansläge**, stäng och öppna filen igen, gör en beräkning. | Allt fungerar. |
| 5 | Tryck i ett fält som *Area* och sedan i *Kraft*. | Area: siffertangentbord med decimalkomma. Kraft: tangentbord där minustecken finns. |
| 6 | Projekt → **Skriv ut / PDF** → välj **Spara som PDF**. | PDF med projektnamn, indata, formel, resultat, enheter, källa och verifieringsstatus; ingen meny eller knappar. |
| 7 | Projekt → **CSV** och **Text**. Öppna filerna från Nedladdningar (t.ex. i Google Kalkylark). | Svenska tecken (å, ä, ö, ³) visas rätt; CSV delas upp i kolumner. |
| 8 | Inställningar → **Exportera JSON** → **Radera all lokal data** → **Importera JSON** → välj filen. | Filväljaren öppnas; allt kommer tillbaka. |
| 9 | Öppna en dialog (t.ex. Spara resultat) och använd **bakåtgesten**. | Dialogen stängs; du blir kvar på sidan. |
| 10 | Tryck **Kopiera** under ett resultat och klistra in i t.ex. Anteckningar. | Resultatet med enheter klistras in. |
| 11 | Android-inställningar → Teckenstorlek **största**. Öppna en kalkylator. | Texten blir större utan att innehållet hamnar utanför skärmen. |
| 12 | Vrid telefonen till liggande läge på en kalkylator och på projektsidan. | Ingen sidledsscroll; menyn nås. |
| 13 | (Valfritt) Slå på TalkBack och navigera på en kalkylator. | Fält läses upp med namn och enhet; felmeddelanden läses upp. |
