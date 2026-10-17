// Nalle Blaster – betalserver (Cloudflare Worker)
//
// Två adresser:
//   POST /checkout  { pack }        -> skapar en Stripe-betalning och svarar med { url } dit spelaren skickas
//   POST /claim     { session_id }  -> kollar hos Stripe att köpet är betalt och svarar med { gems }
//
// Varje köp kan bara hämtas en gång: när diamanterna lämnats ut märks betalningen
// med metadata "claimed" hos Stripe, så ingen databas behövs.
// Den hemliga Stripe-nyckeln ligger som hemlighet i Cloudflare (STRIPE_SECRET_KEY), aldrig i koden.

// Priser i ören (1000 = 10 kr). Ändra här om du vill ha andra paket.
// Paketnamnen (p100 osv.) måste vara samma som i spelets PAY_PACKS.
const PACKS = {
  p100: { gems: 100, ore: 1000, name: '100 diamanter' },
  p300: { gems: 300, ore: 2500, name: '300 diamanter' },
  p1000: { gems: 1000, ore: 6900, name: '1000 diamanter' },
};

export default {
  async fetch(req, env) {
    const gameUrl = env.GAME_URL;
    const cors = {
      'Access-Control-Allow-Origin': new URL(gameUrl).origin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Vary': 'Origin',
    };
    const json = (obj, status = 200) =>
      new Response(JSON.stringify(obj), { status, headers: { ...cors, 'Content-Type': 'application/json' } });

    if (req.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (req.method !== 'POST') return json({ ok: true, service: 'nalle-blaster-betalning' });
    if (!env.STRIPE_SECRET_KEY) return json({ error: 'not_configured' }, 503);

    const path = new URL(req.url).pathname;
    let body = {};
    try { body = await req.json(); } catch (e) { /* tom eller trasig body */ }

    if (path === '/checkout') {
      const pack = PACKS[body.pack];
      if (!pack) return json({ error: 'bad_pack' }, 400);
      const f = new URLSearchParams();
      f.set('mode', 'payment');
      f.set('locale', 'sv');
      f.set('line_items[0][quantity]', '1');
      f.set('line_items[0][price_data][currency]', 'sek');
      f.set('line_items[0][price_data][unit_amount]', String(pack.ore));
      f.set('line_items[0][price_data][product_data][name]', 'Nalle Blaster: ' + pack.name);
      f.set('metadata[pack]', body.pack);
      f.set('payment_intent_data[metadata][pack]', body.pack);
      f.set('success_url', gameUrl + '?kop={CHECKOUT_SESSION_ID}');
      f.set('cancel_url', gameUrl);
      const s = await stripe(env, 'POST', '/v1/checkout/sessions', f);
      if (!s.url) return json({ error: 'stripe', detail: s.error && s.error.message }, 502);
      return json({ url: s.url });
    }

    if (path === '/claim') {
      const id = String(body.session_id || '');
      if (!/^cs_[A-Za-z0-9_]+$/.test(id)) return json({ error: 'bad_session' }, 400);
      const s = await stripe(env, 'GET', '/v1/checkout/sessions/' + id);
      if (s.error) return json({ error: 'not_found' }, 404);
      if (s.payment_status !== 'paid') return json({ error: 'not_paid' }, 402);
      const pack = PACKS[s.metadata && s.metadata.pack];
      if (!pack || !s.payment_intent) return json({ error: 'bad_pack' }, 400);
      const pi = await stripe(env, 'GET', '/v1/payment_intents/' + s.payment_intent);
      if (pi.error) return json({ error: 'not_found' }, 404);
      if (pi.metadata && pi.metadata.claimed) return json({ error: 'already_claimed' }, 409);
      const mark = new URLSearchParams();
      mark.set('metadata[claimed]', new Date().toISOString());
      const marked = await stripe(env, 'POST', '/v1/payment_intents/' + s.payment_intent, mark);
      if (marked.error) return json({ error: 'stripe' }, 502);
      return json({ gems: pack.gems });
    }

    return json({ error: 'not_found' }, 404);
  },
};

async function stripe(env, method, path, form) {
  const res = await fetch('https://api.stripe.com' + path, {
    method,
    headers: {
      Authorization: 'Bearer ' + env.STRIPE_SECRET_KEY,
      ...(form ? { 'Content-Type': 'application/x-www-form-urlencoded' } : {}),
    },
    body: form ? form.toString() : undefined,
  });
  return res.json();
}
