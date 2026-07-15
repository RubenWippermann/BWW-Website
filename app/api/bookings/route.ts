import { env } from "cloudflare:workers";
import { getDb } from "../../../db";
import { bookings } from "../../../db/schema";

type BookingPayload = {
  course?: string; name?: string; organization?: string; email?: string; phone?: string;
  preferredDate?: string; participants?: string | number; location?: string; message?: string;
  consent?: string; website?: string;
};

function clean(value: unknown, max = 500) { return String(value ?? "").trim().slice(0, max); }

export async function POST(request: Request) {
  try {
    const payload = (await request.json()) as BookingPayload;
    if (payload.website) return Response.json({ error: "Ungültige Anfrage." }, { status: 400 });

    const course = clean(payload.course, 160);
    const name = clean(payload.name, 120);
    const email = clean(payload.email, 180).toLowerCase();
    const participants = Math.max(1, Math.min(100, Number(payload.participants) || 1));
    if (!course || !name || !email.includes("@") || payload.consent !== "accepted") {
      return Response.json({ error: "Bitte füllen Sie alle Pflichtfelder aus und bestätigen Sie den Datenschutz." }, { status: 400 });
    }

    const reference = `BWW-${new Date().getFullYear()}-${crypto.randomUUID().slice(0, 8).toUpperCase()}`;
    const values = {
      reference, course, name, email, participants,
      organization: clean(payload.organization, 160), phone: clean(payload.phone, 60),
      preferredDate: clean(payload.preferredDate, 30), location: clean(payload.location, 180),
      message: clean(payload.message, 2000),
    };
    const db = getDb();
    const [booking] = await db.insert(bookings).values(values).returning({ id: bookings.id, reference: bookings.reference });

    const runtime = env as unknown as { SOFTWARE_WIPPERMANN_WEBHOOK_URL?: string; SOFTWARE_WIPPERMANN_API_KEY?: string };
    if (runtime.SOFTWARE_WIPPERMANN_WEBHOOK_URL) {
      try {
        await fetch(runtime.SOFTWARE_WIPPERMANN_WEBHOOK_URL, {
          method: "POST",
          headers: { "content-type": "application/json", ...(runtime.SOFTWARE_WIPPERMANN_API_KEY ? { authorization: `Bearer ${runtime.SOFTWARE_WIPPERMANN_API_KEY}` } : {}) },
          body: JSON.stringify({ source: "bww-website", ...values }),
        });
      } catch { /* Die Anfrage bleibt sicher in D1 gespeichert. */ }
    }

    return Response.json({ booking }, { status: 201 });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unbekannter Fehler";
    return Response.json({ error: message.includes("no such table") ? "Die Buchungsdatenbank wird noch eingerichtet. Bitte senden Sie Ihre Anfrage vorübergehend per E-Mail." : "Die Anfrage konnte nicht gespeichert werden. Bitte versuchen Sie es erneut." }, { status: 500 });
  }
}
