# Nalle Blaster – grafik

- `bear_source_chatgpt.png` – originalbilden på pixelbjörnen, skapad av spelets ägare med ChatGPT.
- `bear_sheet.png` – samma björn rensad och packad till spriteark (612×511, genomskinlig bakgrund, 64 färger).
  Rader: stå (4), gå (6), spring (6), attack (6), skadad (3), glädje (2), svimma (6). Varje ruta är 102×73 px, fötterna vid (35, 68).
- `bear_sheet.json` – rutstorlek, ankarpunkt och animationer.

Spelet (`../index.html`) har arket inbakat som data-URI, så filerna här behövs inte för att spelet ska fungera.

## 3D-björnen (standard)

- `bear_backpack.glb` – 3D-modellen, skapad av spelets ägare med ChatGPT (73 delar, inga animationer).
- `bake_backpack_bear.py` + `render3d.py` – animerar delarna (ben, armar, huvud, kropp) och renderar 33 bilder
  med cel-skuggning och kontur. Körs med `python3 bake_backpack_bear.py` (numpy, Pillow, scipy).
- `bear3d_sheet.png` – färgark (768×896, celler 128×128, samma rader som pixelbjörnen).
- `bear3d_mask.png` – mask för björnfärger: röd = päls, grön = mage/nos, blå = armar/ben/öron.
- `bear3d_sheet.json` – ankare (fötter), framtass för vapnet och huvudets topp.

I spelet väljer man stil under Inställningar → Björnstil.
