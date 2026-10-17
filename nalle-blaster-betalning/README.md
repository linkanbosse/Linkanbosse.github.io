# Nalle Blaster – betalserver

Spelet ligger i `nalle-blaster/` och publiceras på https://linkanbosse.github.io/nalle-blaster/ av den vanliga Pages-uppladdningen.

Den här mappen är en liten server som tar betalt för diamanter via **Stripe** och körs gratis på **Cloudflare Workers**. Den laddas upp automatiskt av jobbet `.github/workflows/nalle-blaster-betalning.yml`, som också skriver in serverns adress i `nalle-blaster/config.js`. Tills dess är köpknapparna i spelet avstängda.

## Så fungerar ett köp

1. Spelaren trycker på ett paket i Butiken.
2. Servern skapar en betalning hos Stripe och spelaren skickas till Stripes betalsida.
3. Efter betalningen skickas spelaren tillbaka till spelet.
4. Spelet frågar servern om köpet. Servern kollar hos Stripe att det är betalt och ger diamanterna. Varje köp kan bara hämtas en gång.

Pengarna hamnar på ditt Stripe-konto och betalas ut till ditt bankkonto.

## Kostnad

- GitHub Pages och Cloudflare Workers: gratis (Cloudflare tillåter 100 000 anrop om dagen gratis).
- Stripe: ingen månadsavgift, bara en avgift per köp. Se aktuella priser på stripe.com/se/pricing.

## Engångsinställning (cirka 20 minuter)

Stripe kräver att kontoägaren är minst 18 år. Är du yngre behöver en förälder skapa kontot.

### 1. Stripe
1. Skapa ett konto på https://dashboard.stripe.com/register och fyll i uppgifterna Stripe ber om för att kunna ta emot betalningar.
2. Gå till **Developers → API keys** och kopiera **Secret key**.
   - Börja gärna med testnyckeln (`sk_test_...`). Då kan du testköpa med kortnumret `4242 4242 4242 4242`, valfritt framtida datum och valfri CVC, utan riktiga pengar.
   - Byt till den riktiga nyckeln (`sk_live_...`) när allt fungerar.

### 2. Cloudflare
1. Skapa ett gratiskonto på https://dash.cloudflare.com/sign-up.
2. Öppna **Workers & Pages** en gång och välj ett namn för din `workers.dev`-adress om du blir tillfrågad.
3. Kopiera ditt **Account ID** (står i högerspalten på översiktssidan för Workers & Pages).
4. Gå till **My Profile → API Tokens → Create Token**, välj mallen **Edit Cloudflare Workers**, och skapa token. Kopiera den.

### 3. GitHub
I det här repot: **Settings → Secrets and variables → Actions → New repository secret**. Lägg till tre hemligheter:

| Namn | Värde |
|---|---|
| `STRIPE_SECRET_KEY` | Stripe-nyckeln från steg 1 |
| `CLOUDFLARE_ACCOUNT_ID` | Account ID från steg 2 |
| `CLOUDFLARE_API_TOKEN` | Token från steg 2 |

### 4. Starta
Gå till **Actions → Nalle Blaster – betalserver → Run workflow**. När jobbet är klart (cirka en minut) är köpen igång i spelet.

Byter du Stripe-nyckel senare: uppdatera hemligheten och kör jobbet igen.

## Ändra paket och priser

Priserna står på två ställen och måste stämma överens:
- `nalle-blaster-betalning/src/index.js` → `PACKS` (pris i ören, 1000 = 10 kr)
- `nalle-blaster/index.html` → `PAY_PACKS` (texten som visas i spelet)

## Bra att veta

- Försäljningen räknas som inkomst och ska tas upp i deklarationen. Säljer du regelbundet kan det räknas som näringsverksamhet; kolla med Skatteverket.
- Diamanterna sparas i spelarens webbläsare. Rensar spelaren webbläsaren försvinner de, precis som resten av spelet.
- Stripes betalsida skickar kvitto till köparen. Återbetalningar gör du i Stripe under **Payments**.
