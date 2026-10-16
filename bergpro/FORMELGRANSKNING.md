# BergPro – formelgranskning

Granskningsdatum: 2026-10-14  
Granskare: AI-assistent (Claude) mot angivna källor – ej fackgranskad av behörig person  
Självtest vid generering: **141/141 godkända**  
Antal formler: 63 · Kalkylatorer: 59

> Rapporten genereras automatiskt från appens formelregister (`node review-report.js`), så den visar exakt det som finns i appen. Granskningen är gjord av en AI-assistent mot de angivna källorna och ersätter inte fackgranskning av behörig person.

## Sammanfattning

| Typ | Antal |
|---|---|
| Allmän fysikalisk formel | 39 |
| Kontrollerad mot källa (ej fackgranskad) | 7 |
| Empirisk modell | 0 |
| Projektspecifik modell | 15 |
| Ej verifierad (egen/okänd källa) | 2 |

## Ändringar i denna granskning

Källhänvisningen har preciserats för 61 formler (version 1.1). Innehållsliga ändringar och tillägg:

- **Volym mellan tvärsektioner (trapetsmetoden)** (`vol_trap`): Tillägg: känd överskattning vid icke-linjär areavariation dokumenterad.
- **Normalspänning** (`stress_n`): Tillägg: teckenkonventionen förtydligad.
- **Skjuvmodul** (`shear_mod`): Kontrollerat mot E = 9KG/(3K+G) i självtestet. Förifyllt ν = 0,25 borttaget – värdet ska komma från provning eller verifierad källa.
- **Volymmodul** (`bulk_mod`): Kontrollerat. Förifyllt ν = 0,25 borttaget.
- **Effektiv normalspänning** (`eff_stress`): Tillägg: antagandet α = 1 (Biot) dokumenterat och visas som varning.
- **Mohr–Coulombs brottvillkor (idealiserat)** (`mohr`): Ändrat: mellanleden visar nu enheter och fältet heter Total normalspänning (tryck positivt). Kontrollerat (c = 0, φ = 45° ger τ_f = σ′).
- **Medelavstånd mellan sprickor** (`frac_spacing`): Tillägg: skillnaden mellan skenbart och verkligt (vinkelrätt) sprickavstånd enligt ISRM dokumenterad.
- **Summering av nivåer (dB)** (`sum_levels`): Tillägg: summering av topptrycksnivåer är inte giltig – dokumenterat och visas som varning.
- **Ljudhastighet i luft** (`c_sound`): Ändrat: tidigare 331,3·√(1 + T/273,15) ersatt med standardens formel (skillnad < 0,02 m/s). Varning utanför giltighetsområdet.
- **Avstånd från gångtid** (`dist_delay`): Kontrollerat. Förifyllt c = 343 m/s borttaget – ange c för aktuell temperatur.
- **Uttrycksräknare** (`expr`): Ändrat: avrundning bort från noll, gräns för längd (500 tecken) och nästling (60 nivåer).
- **Enhetsomvandling** (`units_conv`): Ändrat: kcal/h räknades med internationell kalori (1,163 W) medan kcal använde termokemisk – nu konsekvent termokemisk (4184/3600 W). Alla faktorer kontrolleras mot en oberoende referenstabell i självtestet.

## Formler per kategori

### Miniräknare

#### Medelhastighet — `speed_avg` (v1.1)

| | |
|---|---|
| Uttryck | `v = (s)/(t)` |
| Typ | Allmän fysikalisk formel |
| Variabler | v: Medelhastighet [m/s]; s: Sträcka [m]; t: Tid [s] |
| Giltighetsområde | t > 0 |
| Antaganden | Konstant eller medelvärdesbildad hastighet. |
| Källa | ISO 80000-3:2019 Storheter och enheter – Del 3: Rum och tid (hastighet) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `speed_avg` |
| Tester som anropar kalkylatorn | 1 |

#### Uttrycksräknare — `expr` (v1.1)

| | |
|---|---|
| Uttryck | `a + b · c − d / e` |
| Typ | Allmän fysikalisk formel |
| Variabler | + − · / ^: Grundoperationer []; sqrt, sin, ln …: Funktioner [] |
| Giltighetsområde | – |
| Antaganden | Tolkas av en egen säker tolkare (ingen eval). Argument separeras med semikolon, decimal med komma eller punkt. |
| Källa | Intern funktion (egen tolkare, ingen eval) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Ändrat: avrundning bort från noll, gräns för längd (500 tecken) och nästling (60 nivåer). |
| Kalkylator | – |
| Tester som anropar kalkylatorn | 0 |

### Bergmekanik

#### Normalspänning — `stress_n` (v1.1)

| | |
|---|---|
| Uttryck | `σ = (F)/(A)` |
| Typ | Allmän fysikalisk formel |
| Variabler | σ: Normalspänning [Pa]; F: Kraft vinkelrät mot ytan [N]; A: Area [m²] |
| Giltighetsområde | A > 0 |
| Antaganden | Jämnt fördelad last över hela arean. Teckenkonvention: i ISO 80000-4 och allmän mekanik är drag positivt; i bergmekanik räknas tryck ofta positivt – ange vilken konvention som används. |
| Källa | ISO 80000-4:2019 Storheter och enheter – Del 4: Mekanik (normalspänning); Jaeger, J.C., Cook, N.G.W. & Zimmerman, R.W. (2007). Fundamentals of Rock Mechanics, 4th ed. Blackwell |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Tillägg: teckenkonventionen förtydligad. |
| Kalkylator | `stress_n` |
| Tester som anropar kalkylatorn | 5 |

#### Skjuvspänning — `stress_s` (v1.1)

| | |
|---|---|
| Uttryck | `τ = (F_s)/(A)` |
| Typ | Allmän fysikalisk formel |
| Variabler | τ: Skjuvspänning [Pa]; F_s: Kraft parallell med ytan [N]; A: Area [m²] |
| Giltighetsområde | A > 0 |
| Antaganden | Jämnt fördelad skjuvkraft. |
| Källa | ISO 80000-4:2019 Storheter och enheter – Del 4: Mekanik (skjuvspänning) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `stress_s` |
| Tester som anropar kalkylatorn | 1 |

#### Relativ deformation (töjning) — `strain` (v1.1)

| | |
|---|---|
| Uttryck | `ε = (ΔL)/(L_0)` |
| Typ | Allmän fysikalisk formel |
| Variabler | ε: Relativ deformation [–]; ΔL: Längdändring [m]; L_0: Ursprunglig längd [m] |
| Giltighetsområde | L₀ > 0 |
| Antaganden | Små deformationer. Tecken: ΔL > 0 är förlängning (konvention kan skilja – kompression är ofta positiv i bergmekanik). |
| Källa | ISO 80000-4:2019 Storheter och enheter – Del 4: Mekanik (relativ längdändring / linjär töjning) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. Teckenkonvention dokumenterad. |
| Kalkylator | `strain` |
| Tester som anropar kalkylatorn | 2 |

#### Hookes lag (enaxligt) — `hooke` (v1.1)

| | |
|---|---|
| Uttryck | `σ = E · ε` |
| Typ | Allmän fysikalisk formel |
| Variabler | σ: Spänning [Pa]; E: Elasticitetsmodul [Pa]; ε: Töjning [–] |
| Giltighetsområde | Inom elasticitetsgränsen |
| Antaganden | Linjärelastiskt, isotropt material. Verkligt berg är ofta sprucket, olinjärt och riktningsberoende. |
| Källa | Jaeger, J.C., Cook, N.G.W. & Zimmerman, R.W. (2007). Fundamentals of Rock Mechanics, 4th ed. Blackwell, kap. 5 (linjär elasticitet) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `young` |
| Tester som anropar kalkylatorn | 3 |

#### Elasticitetsmodul (E-modul) — `young` (v1.1)

| | |
|---|---|
| Uttryck | `E = (σ)/(ε)` |
| Typ | Allmän fysikalisk formel |
| Variabler | E: Elasticitetsmodul [Pa]; σ: Spänning [Pa]; ε: Töjning [–] |
| Giltighetsområde | ε ≠ 0 |
| Antaganden | Linjärelastiskt, isotropt, homogent. Verkligt berg är ofta sprucket och riktningsberoende; E beror på spänningsnivå och definition (tangent/sekant). |
| Källa | ISO 80000-4:2019 Storheter och enheter – Del 4: Mekanik (elasticitetsmodul); Jaeger, J.C., Cook, N.G.W. & Zimmerman, R.W. (2007). Fundamentals of Rock Mechanics, 4th ed. Blackwell |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. Tangent/sekant ska anges i projektet. |
| Kalkylator | `young` |
| Tester som anropar kalkylatorn | 3 |

#### Poissons tal — `poisson` (v1.1)

| | |
|---|---|
| Uttryck | `ν = − (ε_tvär)/(ε_axiell)` |
| Typ | Allmän fysikalisk formel |
| Variabler | ν: Poissons tal [–]; ε_tvär: Tvärgående töjning [–]; ε_axiell: Axiell töjning [–] |
| Giltighetsområde | ε_axiell ≠ 0 |
| Antaganden | Linjärelastiskt, isotropt. För isotropa material gäller −1 < ν < 0,5. |
| Källa | ISO 80000-4:2019 Storheter och enheter – Del 4: Mekanik (Poissons tal); Jaeger, J.C., Cook, N.G.W. & Zimmerman, R.W. (2007). Fundamentals of Rock Mechanics, 4th ed. Blackwell |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. Intervallet −1 < ν < 0,5 gäller isotropt linjärelastiskt material och kontrolleras i kalkylatorn. |
| Kalkylator | `poisson` |
| Tester som anropar kalkylatorn | 2 |

#### Skjuvmodul — `shear_mod` (v1.1)

| | |
|---|---|
| Uttryck | `G = (E)/(2 · (1 + ν))` |
| Typ | Allmän fysikalisk formel |
| Variabler | G: Skjuvmodul [Pa]; E: Elasticitetsmodul [Pa]; ν: Poissons tal [–] |
| Giltighetsområde | E > 0, −1 < ν < 0,5 |
| Antaganden | Isotropt, linjärelastiskt material. |
| Källa | Jaeger, J.C., Cook, N.G.W. & Zimmerman, R.W. (2007). Fundamentals of Rock Mechanics, 4th ed. Blackwell, kap. 5 (samband mellan elastiska konstanter) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat mot E = 9KG/(3K+G) i självtestet. Förifyllt ν = 0,25 borttaget – värdet ska komma från provning eller verifierad källa. |
| Kalkylator | `shear_mod` |
| Tester som anropar kalkylatorn | 2 |

#### Volymmodul — `bulk_mod` (v1.1)

| | |
|---|---|
| Uttryck | `K = (E)/(3 · (1 − 2ν))` |
| Typ | Allmän fysikalisk formel |
| Variabler | K: Volymmodul [Pa]; E: Elasticitetsmodul [Pa]; ν: Poissons tal [–] |
| Giltighetsområde | E > 0, −1 < ν < 0,5 |
| Antaganden | Isotropt, linjärelastiskt material. |
| Källa | Jaeger, J.C., Cook, N.G.W. & Zimmerman, R.W. (2007). Fundamentals of Rock Mechanics, 4th ed. Blackwell, kap. 5 (samband mellan elastiska konstanter) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. Förifyllt ν = 0,25 borttaget. |
| Kalkylator | `bulk_mod` |
| Tester som anropar kalkylatorn | 3 |

#### Densitet — `density` (v1.1)

| | |
|---|---|
| Uttryck | `ρ = (m)/(V)` |
| Typ | Allmän fysikalisk formel |
| Variabler | ρ: Densitet [kg/m³]; m: Massa [kg]; V: Volym [m³] |
| Giltighetsområde | m ≥ 0, V > 0 |
| Antaganden | Homogent prov. Ange om densiteten avser torr, naturfuktig eller mättad bergmassa. |
| Källa | ISO 80000-4:2019 Storheter och enheter – Del 4: Mekanik (densitet) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `density` |
| Tester som anropar kalkylatorn | 1 |

#### Tunghet — `unit_weight` (v1.1)

| | |
|---|---|
| Uttryck | `γ = ρ · g` |
| Typ | Allmän fysikalisk formel |
| Variabler | γ: Tunghet [N/m³]; ρ: Densitet [kg/m³]; g: Tyngdacceleration [m/s²] |
| Giltighetsområde | ρ ≥ 0, g > 0 |
| Antaganden | g ≈ 9,81 m/s² (normalvärde 9,80665). Lokalt g varierar något med latitud och höjd. Tunghet är kraft per volym – förväxla inte med densitet. |
| Källa | Definition γ = ρ·g; normaltyngdacceleration g_n = 9,80665 m/s² enligt BIPM, The International System of Units (SI), 9th ed. (2019) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `unit_weight` |
| Tester som anropar kalkylatorn | 1 |

#### Effektiv normalspänning — `eff_stress` (v1.1)

| | |
|---|---|
| Uttryck | `σ′ = σ − u` |
| Typ | Kontrollerad mot källa (ej fackgranskad) |
| Variabler | σ′: Effektiv normalspänning [Pa]; σ: Total normalspänning [Pa]; u: Portryck [Pa] |
| Giltighetsområde | u ≥ 0 |
| Antaganden | Terzaghis princip för vattenmättade porösa/sprickiga material, tryck positivt. Formeln förutsätter effektivspänningskoefficienten (Biots α) = 1, vilket är vanligt för sprickor och fogar. För intakt berg kan α vara mindre än 1 (σ′ = σ − α·u) och då ger formeln för låg effektivspänning. Negativ σ′ betyder att kontakten kan öppnas. |
| Källa | Terzaghi, K. (1936). The shearing resistance of saturated soils and the angle between the planes of shear. Proc. 1st Int. Conf. Soil Mech. Found. Eng., Cambridge MA, vol. 1, 54–56; Jaeger, J.C., Cook, N.G.W. & Zimmerman, R.W. (2007). Fundamentals of Rock Mechanics, 4th ed. Blackwell |
| Verifieringsstatus | Princip kontrollräknad i självtestet; gäller idealiserat – verifiera för aktuell bergmassa. |
| Granskning | Tillägg: antagandet α = 1 (Biot) dokumenterat och visas som varning. |
| Kalkylator | `eff_stress` |
| Tester som anropar kalkylatorn | 2 |

#### Mohr–Coulombs brottvillkor (idealiserat) — `mohr` (v1.1)

| | |
|---|---|
| Uttryck | `τ_f = c + σ′ · tan φ` |
| Typ | Kontrollerad mot källa (ej fackgranskad) |
| Variabler | τ_f: Skjuvhållfasthet [Pa]; c: Kohesion [Pa]; σ′: Effektiv normalspänning [Pa]; φ: Friktionsvinkel [°] |
| Giltighetsområde | c ≥ 0, 0° ≤ φ < 90°, σ′ ≥ 0 |
| Antaganden | Idealiserad linjär envelope. Verkligt berg är ofta sprucket, riktningsberoende och har olinjär brottkurva; c och φ måste komma från provning eller verifierad källa. |
| Källa | Jaeger, J.C., Cook, N.G.W. & Zimmerman, R.W. (2007). Fundamentals of Rock Mechanics, 4th ed. Blackwell, kap. 4; Brady, B.H.G. & Brown, E.T. (2004). Rock Mechanics for Underground Mining, 3rd ed. Kluwer |
| Verifieringsstatus | Samband kontrollräknat i självtestet; parametrar (c, φ) är användarens ansvar. |
| Granskning | Ändrat: mellanleden visar nu enheter och fältet heter Total normalspänning (tryck positivt). Kontrollerat (c = 0, φ = 45° ger τ_f = σ′). |
| Kalkylator | `mohr` |
| Tester som anropar kalkylatorn | 8 |

### Bergkvalitet och sprickor

#### RQD – Rock Quality Designation — `rqd` (v1.1)

| | |
|---|---|
| Uttryck | `RQD = (Σ längd av hela kärnbitar ≥ 100 mm)/(borrad längd (körlängd)) · 100 %` |
| Typ | Kontrollerad mot källa (ej fackgranskad) |
| Variabler | RQD: Rock Quality Designation [%]; Σ: Summa av hela, hårda kärnbitar ≥ 100 mm mätta längs kärnans mittlinje [m]; körlängd: Borrad längd för kärnsatsen [m] |
| Giltighetsområde | 0–100 % |
| Antaganden | Summan av hela, hårda och sunda kärnbitar ≥ 100 mm (4 in) mätta längs kärnans mittlinje, delat med körlängden. Mekaniska brott från borrning/hantering räknas inte som sprickor. Metoden infördes för NX-kärna (ca 54,7 mm). Klassgränserna 25/50/75/90 % återges enligt Deere i sekundärlitteraturen – kontrollera mot originalkällan och projektets krav. |
| Källa | Deere, D.U. (1964). Technical description of rock cores for engineering purposes. Rock Mechanics and Engineering Geology 1, 16–22; Deere, D.U. & Deere, D.W. (1988). The RQD index in practice. ASTM STP 984, 91–101; ASTM D6032/D6032M-17 |
| Verifieringsstatus | Definition; kontrollräknad i självtestet. Klassbeskrivningen följer Deeres tabell – verifiera mot projektets krav. |
| Granskning | Definition kontrollerad mot ASTM D6032 (via TxDOT Geotechnical Manual) och Deere (1964). Klassgränser bekräftade endast i sekundärkälla. |
| Kalkylator | `rqd` |
| Tester som anropar kalkylatorn | 5 |

#### Sprickfrekvens längs mätlinje — `frac_freq` (v1.1)

| | |
|---|---|
| Uttryck | `λ = (N)/(L)` |
| Typ | Kontrollerad mot källa (ej fackgranskad) |
| Variabler | λ: Sprickfrekvens [1/m]; N: Antal sprickor längs mätlinjen [–]; L: Mätlinjens längd [m] |
| Giltighetsområde | N ≥ 0, L > 0 |
| Antaganden | Antal sprickor per meter längs en rak mätlinje. Resultatet beror på mätlinjens riktning i förhållande till sprickornas orientering (orienteringsbias). |
| Källa | ISRM (1978). Suggested methods for the quantitative description of discontinuities in rock masses. Int. J. Rock Mech. Min. Sci. & Geomech. Abstr. 15(6), 319–368 |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `frac_freq` |
| Tester som anropar kalkylatorn | 2 |

#### Medelavstånd mellan sprickor — `frac_spacing` (v1.1)

| | |
|---|---|
| Uttryck | `s_medel = (L)/(N)` |
| Typ | Kontrollerad mot källa (ej fackgranskad) |
| Variabler | s_medel: Medelavstånd [m]; L: Mätlinjens längd [m]; N: Antal sprickor [–] |
| Giltighetsområde | N ≥ 1, L > 0 |
| Antaganden | L/N är ett skenbart medelavstånd längs mätlinjen. ISRM definierar sprickavstånd vinkelrätt mellan intilliggande sprickor i samma grupp – för en sprickgrupp ska avståndet korrigeras för vinkeln mellan linjen och sprickplanens normal. N sprickor ger N − 1 mellanrum. |
| Källa | ISRM (1978). Suggested methods for the quantitative description of discontinuities in rock masses. Int. J. Rock Mech. Min. Sci. & Geomech. Abstr. 15(6), 319–368 |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Tillägg: skillnaden mellan skenbart och verkligt (vinkelrätt) sprickavstånd enligt ISRM dokumenterad. |
| Kalkylator | `frac_spacing` |
| Tester som anropar kalkylatorn | 1 |

### Volym, area och massa

#### Rektangulär area — `area_rect` (v1.1)

| | |
|---|---|
| Uttryck | `A = b · h` |
| Typ | Allmän fysikalisk formel |
| Variabler | A: Area [m²]; b: Bredd [m]; h: Höjd [m] |
| Giltighetsområde | b, h > 0 |
| Antaganden | Räta vinklar, plan yta. |
| Källa | Euklidisk geometri (matematisk definition) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Enheter och uttryck kontrollerade. Inga anmärkningar. |
| Kalkylator | `area_rect` |
| Tester som anropar kalkylatorn | 1 |

#### Triangelarea — `area_tri` (v1.1)

| | |
|---|---|
| Uttryck | `A = (1)/(2) · b · h` |
| Typ | Allmän fysikalisk formel |
| Variabler | A: Area [m²]; b: Bas [m]; h: Höjd vinkelrät mot basen [m] |
| Giltighetsområde | b, h > 0 |
| Antaganden | Höjden mäts vinkelrätt mot vald bas. |
| Källa | Euklidisk geometri (matematisk definition) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Enheter och uttryck kontrollerade. Inga anmärkningar. |
| Kalkylator | `area_tri` |
| Tester som anropar kalkylatorn | 1 |

#### Cirkelarea — `area_circle` (v1.1)

| | |
|---|---|
| Uttryck | `A = π · r^2` |
| Typ | Allmän fysikalisk formel |
| Variabler | A: Area [m²]; r: Radie [m] |
| Giltighetsområde | r > 0 |
| Antaganden | Perfekt cirkulärt tvärsnitt. |
| Källa | Euklidisk geometri (matematisk definition) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. Radie/diameter-val hanteras (r = d/2). |
| Kalkylator | `area_circle` |
| Tester som anropar kalkylatorn | 4 |

#### Cirkelomkrets — `circ` (v1.1)

| | |
|---|---|
| Uttryck | `C = 2 · π · r` |
| Typ | Allmän fysikalisk formel |
| Variabler | C: Omkrets [m]; r: Radie [m] |
| Giltighetsområde | r > 0 |
| Antaganden | Perfekt cirkel. |
| Källa | Euklidisk geometri (matematisk definition) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. Inga anmärkningar. |
| Kalkylator | `circ` |
| Tester som anropar kalkylatorn | 1 |

#### Rätblockets volym — `vol_box` (v1.1)

| | |
|---|---|
| Uttryck | `V = l · b · h` |
| Typ | Allmän fysikalisk formel |
| Variabler | V: Volym [m³]; l: Längd [m]; b: Bredd [m]; h: Höjd [m] |
| Giltighetsområde | l, b, h > 0 |
| Antaganden | Rätblock med räta vinklar (fastvolym). |
| Källa | Euklidisk geometri (matematisk definition) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. Inga anmärkningar. |
| Kalkylator | `vol_box` |
| Tester som anropar kalkylatorn | 2 |

#### Cylindervolym — `vol_cyl` (v1.1)

| | |
|---|---|
| Uttryck | `V = π · r^2 · h` |
| Typ | Allmän fysikalisk formel |
| Variabler | V: Volym [m³]; r: Radie [m]; h: Höjd/längd [m] |
| Giltighetsområde | r, h > 0 |
| Antaganden | Rak cirkulär cylinder. |
| Källa | Euklidisk geometri (matematisk definition) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. Inga anmärkningar. |
| Kalkylator | `vol_cyl` |
| Tester som anropar kalkylatorn | 2 |

#### Volym mellan tvärsektioner (trapetsmetoden) — `vol_trap` (v1.1)

| | |
|---|---|
| Uttryck | `V = Σ (A_i + A_i+1)/(2) · (s_i+1 − s_i)` |
| Typ | Allmän fysikalisk formel |
| Variabler | V: Volym [m³]; A_i: Tvärsnittsarea i sektion i [m²]; s_i: Station (läge längs sträckan) [m] |
| Giltighetsområde | Minst 2 sektioner, stationer i stigande ordning, A ≥ 0 |
| Antaganden | Arean antas variera linjärt mellan sektionerna. När tvärsnittets form ändras mellan sektionerna (t.ex. pyramid- eller konformade övergångar) kan metoden överskatta volymen – prismoidformeln eller tätare sektioner ger bättre noggrannhet. |
| Källa | Trapetsregeln för numerisk integration (medelareametoden för massberäkning) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Tillägg: känd överskattning vid icke-linjär areavariation dokumenterad. |
| Kalkylator | `vol_trap` |
| Tester som anropar kalkylatorn | 7 |

#### Massa från volym och densitet — `mass_from_vol` (v1.1)

| | |
|---|---|
| Uttryck | `m = ρ · V` |
| Typ | Allmän fysikalisk formel |
| Variabler | m: Massa [kg]; ρ: Densitet [kg/m³]; V: Volym [m³] |
| Giltighetsområde | ρ, V > 0 |
| Antaganden | Homogent material. Skilj på fast (fast mått) och lösvolym (utsprängd/upplockad) densitet. |
| Källa | ISO 80000-4:2019 Storheter och enheter – Del 4: Mekanik (densitet) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. Skillnad fast/lös densitet påpekas. |
| Kalkylator | `mass_from_vol` |
| Tester som anropar kalkylatorn | 2 |

#### Volym från massa och densitet — `vol_from_mass` (v1.1)

| | |
|---|---|
| Uttryck | `V = (m)/(ρ)` |
| Typ | Allmän fysikalisk formel |
| Variabler | V: Volym [m³]; m: Massa [kg]; ρ: Densitet [kg/m³] |
| Giltighetsområde | m > 0, ρ > 0 |
| Antaganden | Homogent material. |
| Källa | ISO 80000-4:2019 Storheter och enheter – Del 4: Mekanik (densitet) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `vol_from_mass` |
| Tester som anropar kalkylatorn | 2 |

### Borrning och produktion

#### Total borrad längd — `drill_len` (v1.1)

| | |
|---|---|
| Uttryck | `L_tot = Σ L_i` |
| Typ | Projektspecifik modell |
| Variabler | L_tot: Total borrad längd [m]; L_i: Längd för hål i [m] |
| Giltighetsområde | L_i ≥ 0 |
| Antaganden | Redovisningsprincip (t.ex. inkl. överborrning) bestäms av projektet. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `drill_len` |
| Tester som anropar kalkylatorn | 1 |

#### Borrmeter per arbetstimme — `drill_rate` (v1.1)

| | |
|---|---|
| Uttryck | `p_bor = (L_tot)/(t_arbete)` |
| Typ | Projektspecifik modell |
| Variabler | p_bor: Borrproduktion [m/h]; L_tot: Borrad längd [m]; t_arbete: Arbetstid [h] |
| Giltighetsområde | t > 0 |
| Antaganden | Definition av "arbetstid" (inkl./exkl. stillestånd) avgör nyckeltalet – ange alltid vilken som används. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `drill_rate` |
| Tester som anropar kalkylatorn | 2 |

#### Arbetstid — `worktime` (v1.1)

| | |
|---|---|
| Uttryck | `t_arbete = t_maskin + t_stillestånd` |
| Typ | Projektspecifik modell |
| Variabler | t_arbete: Arbetstid [h]; t_maskin: Maskintid (drift) [h]; t_stillestånd: Stilleståndstid [h] |
| Giltighetsområde | t ≥ 0 |
| Antaganden | Definitionen följer projektets tidredovisning. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `worktime` |
| Tester som anropar kalkylatorn | 2 |

#### Maskintid — `machtime` (v1.1)

| | |
|---|---|
| Uttryck | `t_maskin = t_arbete − t_stillestånd` |
| Typ | Projektspecifik modell |
| Variabler | t_maskin: Maskintid (drift) [h]; t_arbete: Arbetstid [h]; t_stillestånd: Stilleståndstid [h] |
| Giltighetsområde | 0 ≤ t_stillestånd ≤ t_arbete |
| Antaganden | Definitionen följer projektets tidredovisning. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `machtime` |
| Tester som anropar kalkylatorn | 3 |

#### Stilleståndstid — `downtime` (v1.1)

| | |
|---|---|
| Uttryck | `t_stillestånd = t_arbete − t_maskin` |
| Typ | Projektspecifik modell |
| Variabler | t_stillestånd: Stilleståndstid [h]; t_arbete: Arbetstid [h]; t_maskin: Maskintid [h] |
| Giltighetsområde | 0 ≤ t_maskin ≤ t_arbete |
| Antaganden | Definitionen följer projektets tidredovisning. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `downtime` |
| Tester som anropar kalkylatorn | 2 |

#### Bränsle per maskintimme — `fuel_h` (v1.1)

| | |
|---|---|
| Uttryck | `q_h = (V_bränsle)/(t_maskin)` |
| Typ | Projektspecifik modell |
| Variabler | q_h: Bränsleförbrukning [l/h]; V_bränsle: Förbrukat bränsle [l]; t_maskin: Maskintid [h] |
| Giltighetsområde | t_maskin > 0 |
| Antaganden | Bränslet avser samma tidsperiod och maskin som tiden. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `fuel_h` |
| Tester som anropar kalkylatorn | 2 |

#### Bränsle per producerad enhet — `fuel_unit` (v1.1)

| | |
|---|---|
| Uttryck | `q_enhet = (V_bränsle)/(P)` |
| Typ | Projektspecifik modell |
| Variabler | q_enhet: Bränsle per enhet [l/enhet]; V_bränsle: Förbrukat bränsle [l]; P: Producerad mängd (m, m³, ton …) [enhet] |
| Giltighetsområde | P > 0 |
| Antaganden | Enheten (borrmeter, m³, ton) väljs av användaren. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `fuel_unit` |
| Tester som anropar kalkylatorn | 1 |

#### Planerad mot faktisk produktion — `plan_act` (v1.1)

| | |
|---|---|
| Uttryck | `Δ = P_faktisk − P_plan , uppfyllnad = (P_faktisk)/(P_plan) · 100 %` |
| Typ | Projektspecifik modell |
| Variabler | Δ: Avvikelse [enhet]; P_plan: Planerad produktion [enhet]; P_faktisk: Faktisk produktion [enhet] |
| Giltighetsområde | P_plan > 0 |
| Antaganden | Samma enhet och period för plan och utfall. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `plan_act` |
| Tester som anropar kalkylatorn | 1 |

### Vibrationer

#### Frekvens — `freq` (v1.1)

| | |
|---|---|
| Uttryck | `f = (1)/(T)` |
| Typ | Allmän fysikalisk formel |
| Variabler | f: Frekvens [Hz]; T: Periodtid [s] |
| Giltighetsområde | T > 0 |
| Antaganden | Periodisk signal. |
| Källa | ISO 80000-3:2019 Storheter och enheter – Del 3: Rum och tid (frekvens) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `freq` |
| Tester som anropar kalkylatorn | 2 |

#### Periodtid — `period` (v1.1)

| | |
|---|---|
| Uttryck | `T = (1)/(f)` |
| Typ | Allmän fysikalisk formel |
| Variabler | T: Periodtid [s]; f: Frekvens [Hz] |
| Giltighetsområde | f > 0 |
| Antaganden | Periodisk signal. |
| Källa | ISO 80000-3:2019 Storheter och enheter – Del 3: Rum och tid (periodtid) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `period` |
| Tester som anropar kalkylatorn | 2 |

#### Vinkelhastighet (vinkelfrekvens) — `omega` (v1.1)

| | |
|---|---|
| Uttryck | `ω = 2 · π · f` |
| Typ | Allmän fysikalisk formel |
| Variabler | ω: Vinkelhastighet [rad/s]; f: Frekvens [Hz] |
| Giltighetsområde | f > 0 |
| Antaganden | Harmonisk svängning. |
| Källa | ISO 80000-3:2019 Storheter och enheter – Del 3: Rum och tid (vinkelfrekvens) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `omega` |
| Tester som anropar kalkylatorn | 1 |

#### Förskjutning – hastighet – acceleration (harmonisk) — `harm` (v1.1)

| | |
|---|---|
| Uttryck | `v_topp = ω · u_topp , a_topp = ω · v_topp = ω^2 · u_topp` |
| Typ | Allmän fysikalisk formel |
| Variabler | u_topp: Förskjutningsamplitud [m]; v_topp: Hastighetsamplitud [m/s]; a_topp: Accelerationsamplitud [m/s²]; ω: Vinkelhastighet [rad/s] |
| Giltighetsområde | f > 0, enkel sinus |
| Antaganden | Gäller endast för en ren sinusformad svängning med en enda frekvens. Verkliga mätsignaler har bredare frekvensinnehåll – använd mätta toppvärden och redovisa vilken storhet som mäts. |
| Källa | Kinematik för harmonisk (sinusformad) svängning; terminologi enligt ISO 2041:2018 Mechanical vibration, shock and condition monitoring – Vocabulary |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat: samma resultat oavsett vilken storhet som anges (självtest). |
| Kalkylator | `harm` |
| Tester som anropar kalkylatorn | 6 |

#### Sinus: topp, RMS och topp-till-topp — `sine_rms` (v1.1)

| | |
|---|---|
| Uttryck | `x_RMS = (x_topp)/(√2) , x_pp = 2 · x_topp` |
| Typ | Allmän fysikalisk formel |
| Variabler | x_topp: Toppvärde (amplitud) [enhet]; x_RMS: Effektivvärde [enhet]; x_pp: Topp-till-topp [enhet] |
| Giltighetsområde | Ren sinus |
| Antaganden | Gäller endast för ren sinus utan likkomponent. |
| Källa | Matematisk definition (ren sinus: x_RMS = x_topp/√2) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `sine_rms` |
| Tester som anropar kalkylatorn | 1 |

### Mätserier och statistik

#### Aritmetiskt medelvärde — `mean` (v1.1)

| | |
|---|---|
| Uttryck | `x̄ = (Σ x_i)/(n)` |
| Typ | Allmän fysikalisk formel |
| Variabler | x̄: Medelvärde [enhet]; x_i: Mätvärde i [enhet]; n: Antal värden [–] |
| Giltighetsområde | n ≥ 1 |
| Antaganden | Alla värden i samma enhet. |
| Källa | JCGM 100:2008 Evaluation of measurement data – Guide to the expression of uncertainty in measurement (GUM), avsnitt 4.2.1, ekv. (3) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `mean` |
| Tester som anropar kalkylatorn | 2 |

#### RMS (effektivvärde) — `rms` (v1.1)

| | |
|---|---|
| Uttryck | `x_RMS = √((Σ x_i^2)/(N))` |
| Typ | Allmän fysikalisk formel |
| Variabler | x_RMS: RMS-värde [enhet]; x_i: Mätvärde i [enhet]; N: Antal värden [–] |
| Giltighetsområde | N ≥ 1 |
| Antaganden | Diskreta, jämnt fördelade samplingar. RMS av en tidsserie beror på valt tidsfönster. |
| Källa | Matematisk definition (kvadratiskt medelvärde) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `rms` |
| Tester som anropar kalkylatorn | 1 |

#### Toppvärde (största absolutvärde) — `peak` (v1.1)

| | |
|---|---|
| Uttryck | `x_topp = max \|x_i\|` |
| Typ | Allmän fysikalisk formel |
| Variabler | x_topp: Toppvärde [enhet] |
| Giltighetsområde | n ≥ 1 |
| Antaganden | Ingen filtrering – påverkas av enstaka avvikande värden. |
| Källa | Matematisk definition; terminologi enligt ISO 2041:2018 |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `peak` |
| Tester som anropar kalkylatorn | 1 |

#### Topp-till-topp-värde — `p2p` (v1.1)

| | |
|---|---|
| Uttryck | `x_pp = max(x_i) − min(x_i)` |
| Typ | Allmän fysikalisk formel |
| Variabler | x_pp: Topp-till-topp [enhet] |
| Giltighetsområde | n ≥ 2 rekommenderas |
| Antaganden | Ingen filtrering. |
| Källa | Matematisk definition; terminologi enligt ISO 2041:2018 |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `p2p` |
| Tester som anropar kalkylatorn | 1 |

#### Stickprovsstandardavvikelse — `stdev` (v1.1)

| | |
|---|---|
| Uttryck | `s = √((Σ(x_i − x̄)²)/(n − 1))` |
| Typ | Allmän fysikalisk formel |
| Variabler | s: Standardavvikelse [enhet]; x_i: Mätvärde i [enhet]; x̄: Medelvärde [enhet]; n: Antal [–] |
| Giltighetsområde | n ≥ 2 |
| Antaganden | Oberoende, ungefär normalfördelade mätvärden. |
| Källa | JCGM 100:2008 Evaluation of measurement data – Guide to the expression of uncertainty in measurement (GUM), avsnitt 4.2.2, ekv. (4) (experimentell standardavvikelse) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `stdev` |
| Tester som anropar kalkylatorn | 2 |

#### Absolut mätavvikelse — `abs_err` (v1.1)

| | |
|---|---|
| Uttryck | `Δ = x_mätt − x_ref` |
| Typ | Allmän fysikalisk formel |
| Variabler | Δ: Absolut avvikelse [enhet]; x_mätt: Mätt värde [enhet]; x_ref: Referensvärde [enhet] |
| Giltighetsområde | – |
| Antaganden | Referensvärdet antas vara känt/sant. |
| Källa | JCGM 200:2012 International vocabulary of metrology (VIM), 3rd ed., 2.16 (mätavvikelse) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `abs_err` |
| Tester som anropar kalkylatorn | 1 |

#### Relativ mätavvikelse — `rel_err` (v1.1)

| | |
|---|---|
| Uttryck | `δ = (Δ)/(x_ref) · 100 %` |
| Typ | Allmän fysikalisk formel |
| Variabler | δ: Relativ avvikelse [%]; Δ: Absolut avvikelse [enhet]; x_ref: Referensvärde [enhet] |
| Giltighetsområde | x_ref ≠ 0 |
| Antaganden | Referensvärdet antas vara känt/sant. |
| Källa | JCGM 200:2012 International vocabulary of metrology (VIM), 3rd ed., 2.16 (mätavvikelse), relativ form |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `rel_err` |
| Tester som anropar kalkylatorn | 2 |

#### Kombinerad standardosäkerhet (oberoende bidrag) — `comb_unc` (v1.1)

| | |
|---|---|
| Uttryck | `u_c = √(Σ u_i^2) , U = k · u_c` |
| Typ | Kontrollerad mot källa (ej fackgranskad) |
| Variabler | u_c: Kombinerad standardosäkerhet [enhet]; u_i: Standardosäkerhet för bidrag i [enhet]; k: Täckningsfaktor [–]; U: Utvidgad osäkerhet [enhet] |
| Giltighetsområde | u_i ≥ 0, k > 0 |
| Antaganden | Okorrelerade bidrag med känslighetskoefficient 1 och samma enhet. Korrelerade bidrag eller andra modellsamband kräver full GUM-metod. |
| Källa | JCGM 100:2008 Evaluation of measurement data – Guide to the expression of uncertainty in measurement (GUM), avsnitt 5.1.2 ekv. (10) med känslighetskoefficienter 1, samt avsnitt 6.2.1 ekv. (18) U = k·u_c |
| Verifieringsstatus | Metoden kontrollräknad i självtestet (3–4–5); modellvalet är användarens ansvar. |
| Granskning | Kontrollerat. k = 2 motsvarar ca 95 % endast för normalfördelning. |
| Kalkylator | `comb_unc` |
| Tester som anropar kalkylatorn | 1 |

#### Mätserie – nyckeltal — `series` (v1.1)

| | |
|---|---|
| Uttryck | `x̄ , s , x_RMS , x_topp , x_pp` |
| Typ | Allmän fysikalisk formel |
| Variabler | x̄: Medelvärde [enhet]; s: Standardavvikelse [enhet] |
| Giltighetsområde | n ≥ 1 |
| Antaganden | Se de enskilda formlerna. Skilj på förskjutning, hastighet och acceleration. |
| Källa | Se respektive formel (medel och s enligt GUM 4.2; RMS, topp och topp-till-topp enligt matematisk definition) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. |
| Kalkylator | `series` |
| Tester som anropar kalkylatorn | 2 |

### Luftstötvåg och ljud

#### Nivå (dB) från tryck — `spl_p` (v1.1)

| | |
|---|---|
| Uttryck | `L = 20 · log_10((p)/(p_0))` |
| Typ | Allmän fysikalisk formel |
| Variabler | L: Nivå [dB re 20 µPa]; p: Tryck (RMS eller topp enligt definition) [Pa]; p_0: Referenstryck i luft [20 µPa] |
| Giltighetsområde | p > 0 |
| Antaganden | Ljudtrycksnivå definieras med RMS-ljudtryck och referens 20 µPa i luft. Används topptryck (vanligt vid luftstötvåg) blir resultatet en topptrycksnivå – redovisa alltid vilken. Ange frekvens- och tidsvägning. BergPro anger inga gränsvärden. |
| Källa | IEC 60050-801 International Electrotechnical Vocabulary – Acoustics and electroacoustics, IEV 801-22-07 (ljudtrycksnivå, referens 20 µPa i luft) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Definition kontrollerad mot IEV 801-22-07. |
| Kalkylator | `spl_p` |
| Tester som anropar kalkylatorn | 4 |

#### Tryck från nivå (dB) — `p_spl` (v1.1)

| | |
|---|---|
| Uttryck | `p = p_0 · 10^L/20` |
| Typ | Allmän fysikalisk formel |
| Variabler | p: Tryck [Pa]; L: Nivå [dB re 20 µPa]; p_0: Referenstryck [20 µPa] |
| Giltighetsområde | – |
| Antaganden | Referenstryck 20 µPa (luft). Inversen ger samma sorts tryck (RMS eller topp) som nivån avsåg. |
| Källa | IEC 60050-801 International Electrotechnical Vocabulary – Acoustics and electroacoustics, IEV 801-22-07 (ljudtrycksnivå, referens 20 µPa i luft) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat (inversa par i självtestet). |
| Kalkylator | `p_spl` |
| Tester som anropar kalkylatorn | 2 |

#### Summering av nivåer (dB) — `sum_levels` (v1.1)

| | |
|---|---|
| Uttryck | `L_tot = 10 · log_10( Σ 10^L_i/10 )` |
| Typ | Allmän fysikalisk formel |
| Variabler | L_tot: Summanivå [dB]; L_i: Nivå för källa i [dB] |
| Giltighetsområde | – |
| Antaganden | Gäller endast okorrelerade (inkoherenta) bidrag och nivåer baserade på RMS-tryck, med samma referens och vägning. Gäller INTE för topptrycksnivåer (t.ex. luftstötvåg) – toppvärden kan inte adderas energetiskt. |
| Källa | Följer av definitionen av ljudtrycksnivå (IEC 60050-801 International Electrotechnical Vocabulary – Acoustics and electroacoustics, IEV 801-22-07 (ljudtrycksnivå, referens 20 µPa i luft)): energetisk summering av medelkvadrattryck |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Tillägg: summering av topptrycksnivåer är inte giltig – dokumenterat och visas som varning. |
| Kalkylator | `sum_levels` |
| Tester som anropar kalkylatorn | 4 |

#### Ljudhastighet i luft — `c_sound` (v1.1)

| | |
|---|---|
| Uttryck | `c = 343,2 · √((T + 273,15)/(293,15))` |
| Typ | Kontrollerad mot källa (ej fackgranskad) |
| Variabler | c: Ljudhastighet [m/s]; T: Lufttemperatur [°C] |
| Giltighetsområde | ca −20 °C till +50 °C (giltighetsområde angivet för ISO 9613-1 formel A.5) |
| Antaganden | Torr luft vid normalt atmosfärstryck. Fukt ger en liten ökning (< 1 %); vind ändrar den effektiva hastigheten i vindens riktning. |
| Källa | ISO 9613-1:1993 Acoustics – Attenuation of sound during propagation outdoors – Part 1, bilaga A, formel A.5 (kontrollerad via sekundärkälla: pyfar, speed_of_sound_simple) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Ändrat: tidigare 331,3·√(1 + T/273,15) ersatt med standardens formel (skillnad < 0,02 m/s). Varning utanför giltighetsområdet. |
| Kalkylator | `c_sound` |
| Tester som anropar kalkylatorn | 6 |

#### Avstånd från gångtid — `dist_delay` (v1.1)

| | |
|---|---|
| Uttryck | `d = c · t` |
| Typ | Allmän fysikalisk formel |
| Variabler | d: Avstånd [m]; c: Ljudhastighet [m/s]; t: Gångtid [s] |
| Giltighetsområde | c, t > 0 |
| Antaganden | Konstant ljudhastighet (jämn temperatur och vind). Mätosäkerhet i c ger osäkerhet i d. |
| Källa | ISO 80000-3:2019 Storheter och enheter – Del 3: Rum och tid (hastighet = sträcka/tid) |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Kontrollerat. Förifyllt c = 343 m/s borttaget – ange c för aktuell temperatur. |
| Kalkylator | `dist_delay` |
| Tester som anropar kalkylatorn | 1 |

### Kostnader

#### Total kostnad — `total_cost` (v1.1)

| | |
|---|---|
| Uttryck | `C_tot = Σ C_i` |
| Typ | Projektspecifik modell |
| Variabler | C_tot: Total kostnad [kr]; C_i: Kostnadspost i [kr] |
| Giltighetsområde | – |
| Antaganden | Alla poster i samma valuta, samma moms-princip. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `total_cost` |
| Tester som anropar kalkylatorn | 1 |

#### Kostnad per borrmeter — `cost_m` (v1.1)

| | |
|---|---|
| Uttryck | `C_m = (C_tot)/(L_tot)` |
| Typ | Projektspecifik modell |
| Variabler | C_m: Kostnad per meter [kr/m]; C_tot: Total kostnad [kr]; L_tot: Borrad längd [m] |
| Giltighetsområde | L > 0 |
| Antaganden | Kostnadsposter och längd ska avse samma omfattning. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `cost_m` |
| Tester som anropar kalkylatorn | 2 |

#### Kostnad per kubikmeter — `cost_v` (v1.1)

| | |
|---|---|
| Uttryck | `C_V = (C_totalt)/(V)` |
| Typ | Projektspecifik modell |
| Variabler | C_V: Kostnad per m³ [kr/m³]; C_totalt: Total kostnad [kr]; V: Volym [m³] |
| Giltighetsområde | V > 0 |
| Antaganden | Ange om volymen är fast eller lös volym. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `cost_v` |
| Tester som anropar kalkylatorn | 1 |

#### Kostnad per arbetstimme — `cost_h` (v1.1)

| | |
|---|---|
| Uttryck | `C_h = (C_tot)/(t)` |
| Typ | Projektspecifik modell |
| Variabler | C_h: Kostnad per timme [kr/h]; C_tot: Total kostnad [kr]; t: Arbetstid [h] |
| Giltighetsområde | t > 0 |
| Antaganden | Samma tidsdefinition som i produktionsuppföljningen. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `cost_h` |
| Tester som anropar kalkylatorn | 1 |

#### Budgetavvikelse — `budget_dev` (v1.1)

| | |
|---|---|
| Uttryck | `Δ = C_utfall − C_budget` |
| Typ | Projektspecifik modell |
| Variabler | Δ: Budgetavvikelse (positiv = över budget) [kr]; C_utfall: Faktisk kostnad [kr]; C_budget: Budget [kr] |
| Giltighetsområde | – |
| Antaganden | Teckenkonvention: positiv avvikelse = överskriden budget. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `budget_dev` |
| Tester som anropar kalkylatorn | 2 |

#### Procentuell budgetavvikelse — `budget_pct` (v1.1)

| | |
|---|---|
| Uttryck | `δ = (C_utfall − C_budget)/(C_budget) · 100 %` |
| Typ | Projektspecifik modell |
| Variabler | δ: Avvikelse i procent [%]; C_utfall: Faktisk kostnad [kr]; C_budget: Budget [kr] |
| Giltighetsområde | Budget > 0 |
| Antaganden | Teckenkonvention: positiv = över budget. |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `budget_pct` |
| Tester som anropar kalkylatorn | 3 |

#### Bränslekostnad — `fuel_cost` (v1.1)

| | |
|---|---|
| Uttryck | `C_bränsle = V_bränsle · p` |
| Typ | Projektspecifik modell |
| Variabler | C_bränsle: Bränslekostnad [kr]; V_bränsle: Förbrukad mängd [l]; p: Pris per liter [kr/l] |
| Giltighetsområde | V ≥ 0, p ≥ 0 |
| Antaganden | Priset anges av användaren (inkl./exkl. moms enligt projektets princip). |
| Källa | Projektets egen nyckeltalsdefinition (ingen extern standard) |
| Verifieringsstatus | Nyckeltalsdefinition – kontrollräknad i självtestet; beror på projektets redovisningsprinciper. |
| Granskning | Nyckeltal – kontrollräknat. |
| Kalkylator | `fuel_cost` |
| Tester som anropar kalkylatorn | 1 |

### Enhetsomvandling

#### Enhetsomvandling — `units_conv` (v1.1)

| | |
|---|---|
| Uttryck | `x_ny = x · (k_från)/(k_till)` |
| Typ | Allmän fysikalisk formel |
| Variabler | k: Omräkningsfaktor till SI-enhet [–] |
| Giltighetsområde | – |
| Antaganden | Faktorerna är exakta definitioner där sådana finns. Kalori avser termokemisk kalori (4,184 J). Förväxla inte massa (kg) och kraft (N, kgf) eller tryck och energi. |
| Källa | Thompson, A. & Taylor, B.N. (2008). Guide for the Use of the International System of Units (SI). NIST Special Publication 811, bilaga B; BIPM (2019) The International System of Units (SI), 9th ed. |
| Verifieringsstatus | Definition/samband kontrollräknat med kända värden i appens självtest. |
| Granskning | Ändrat: kcal/h räknades med internationell kalori (1,163 W) medan kcal använde termokemisk – nu konsekvent termokemisk (4184/3600 W). Alla faktorer kontrolleras mot en oberoende referenstabell i självtestet. |
| Kalkylator | – |
| Tester som anropar kalkylatorn | 0 |

### Egna modeller (ej verifierade)

#### v = K / Bᵃ · lᵇ (egen modell, ej verifierad) — `blast_v` (v1.0)

| | |
|---|---|
| Uttryck | `v = (K)/(B^a) · l^b` |
| Typ | Ej verifierad (egen/okänd källa) |
| Variabler | v: Hastighet enligt anteckningen (”hastigheten på bergmassan”) – storheten är inte fastställd [m/s]; K: Bergartskonstant, anges av användaren eller väljs per bergart enligt anteckningen (gnejs 22, granit 25, kvartsit 27, skiffer 18, alunskiffer 15) [enhet enligt källan (gäller för B i m, l i kg/m)]; B: Försättning [m]; l: Laddningskoncentration [kg/m]; a: Exponent för B (anteckningen: 1,17) [–]; b: Exponent för l (anteckningen: 0,39) [–] |
| Giltighetsområde | B > 0, l > 0, K > 0. Giltighetsområdet är okänt – ange det från din källa i kalkylatorn. |
| Antaganden | Anteckningens exempel säger ”λ 40 %” och ”40 % av B = 1,6” med B = 2 m. 40 % av 2 m är 0,8 m, inte 1,6 m. Tolkningen ändrar t med en faktor 2 och har inte avgjorts – ange därför λ själv, i procent av B eller direkt i meter. Vilken fysikalisk storhet v är har inte fastställts. Bergmassans/försättningens rörelsehastighet, partikelhastighet (vibration) och vågutbredningshastighet är olika storheter. K gäller bara för de enheter modellen har tagits fram för – enligt anteckningen B i meter och l i kg/m. Därför är B och l låsta till de enheterna. Exponenterna 1,17 och 0,39 är avlästa från en handskriven anteckning. |
| Källa | Användarens egna handskrivna anteckningar (daterade 2024-12-27). Ingen fackkälla angiven. |
| Verifieringsstatus | EJ VERIFIERAD. Kontrollerat: v räknat med anteckningens exempelindata återger anteckningens eget exempelvärde för v, och t räknas som kvoten λ/v. Anteckningens λ-exempel är inkonsekvent och har inte avgjorts. Modellens fysikaliska innebörd, enheter och giltighetsområde är inte belagda i någon fackkälla. Kräver granskning av behörig person innan resultat används. |
| Granskning | EJ VERIFIERAD. Endast aritmetiken kontrollerad. Oberoende säkerhetsgranskning 2026-10-14: enheter låsta (B i m, l i kg/m), precisionen begränsad till 3 siffror och statusen följer med resultatet i kopior, listor och rapporter. |
| Kalkylator | `blast_model` |
| Tester som anropar kalkylatorn | 17 |

#### Kvot t = λ / v (egen modell – inte ett tändintervall) — `blast_t` (v1.0)

| | |
|---|---|
| Uttryck | `t = (λ)/(v)` |
| Typ | Ej verifierad (egen/okänd källa) |
| Variabler | t: Kvot λ/v enligt anteckningen (”reell tid”) – inte ett tändintervall [s]; λ: Önskad förflyttning före nästa rad, anges av användaren i % av B eller i m [m]; v: Hastighet enligt modellen ovan [m/s] |
| Giltighetsområde | v > 0, λ > 0. |
| Antaganden | Anteckningens exempel säger ”λ 40 %” och ”40 % av B = 1,6” med B = 2 m. 40 % av 2 m är 0,8 m, inte 1,6 m. Tolkningen ändrar t med en faktor 2 och har inte avgjorts – ange därför λ själv, i procent av B eller direkt i meter. Vilken fysikalisk storhet v är har inte fastställts. Bergmassans/försättningens rörelsehastighet, partikelhastighet (vibration) och vågutbredningshastighet är olika storheter. BergPro avrundar inte till tändarsteg och ger inga förslag på tändsekvens. |
| Källa | Användarens egna handskrivna anteckningar (daterade 2024-12-27). Ingen fackkälla angiven. |
| Verifieringsstatus | EJ VERIFIERAD. Kontrollerat: v räknat med anteckningens exempelindata återger anteckningens eget exempelvärde för v, och t räknas som kvoten λ/v. Anteckningens λ-exempel är inkonsekvent och har inte avgjorts. Modellens fysikaliska innebörd, enheter och giltighetsområde är inte belagda i någon fackkälla. Kräver granskning av behörig person innan resultat används. |
| Granskning | EJ VERIFIERAD. Endast kvoten kontrollerad. Anteckningens λ-exempel är inkonsekvent (40 % av 2 m = 0,8 m, inte 1,6 m) och avgörs inte av appen. Säkerhetsgranskning 2026-10-14: t benämns inte fördröjning, söks inte på tändsekvens och anges som ”inte ett tändintervall”. |
| Kalkylator | `blast_model` |
| Tester som anropar kalkylatorn | 17 |

