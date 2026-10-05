"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowRight, LoaderCircle } from "lucide-react";
import { api, Footer, Header, useApp } from "../../components";

export default function CheckoutPage() {
  const { cart, clearCart, user, authHydrated } = useApp();
  const [form, setForm] = useState({ full_name: "", line1: "", city: "", state: "", postal_code: "", country: "India" });
  const [shipping, setShipping] = useState("standard");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const total = cart.reduce((sum, item) => sum + Number(item.price || 0) * item.quantity, 0);

  async function placeOrder(event: React.FormEvent) {
    event.preventDefault();
    if (!cart.length) return;
    setBusy(true);
    setError("");
    try {
      const order = await api("/api/v1/orders", {
        method: "POST",
        body: JSON.stringify({
          items: cart.map((item) => ({ product_id: Number(item.id ?? item.product_id), quantity: item.quantity })),
          delivery_address: form,
          shipping_method: shipping,
          idempotency_key: crypto.randomUUID(),
        }),
      });
      clearCart();
      window.location.href = `/checkout/success?order=${order.id}`;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to place order.");
    } finally {
      setBusy(false);
    }
  }

  if (!authHydrated) return <><Header /><main className="mx-auto max-w-3xl px-5 py-20 text-center">Loading checkout…</main><Footer /></>;
  if (!user) return <><Header /><main className="mx-auto max-w-3xl px-5 py-20 text-center"><h1 className="text-3xl font-black">Sign in to checkout</h1><p className="mt-3 text-white/45">Your order is protected and linked to your account.</p><Link href="/login" className="button-primary mt-7">Continue to sign in <ArrowRight size={16} /></Link></main><Footer /></>;
  if (!cart.length) return <><Header /><main className="mx-auto max-w-3xl px-5 py-20 text-center"><h1 className="text-3xl font-black">Your bag is empty</h1><Link href="/shop" className="button-primary mt-7">Explore products <ArrowRight size={16} /></Link></main><Footer /></>;
  return <><Header /><main className="mx-auto max-w-6xl px-5 py-12 lg:px-8"><div className="eyebrow">Checkout</div><h1 className="mt-3 text-4xl font-black">Almost yours.</h1><form onSubmit={placeOrder} className="mt-10 grid gap-6 lg:grid-cols-[1fr_340px]"><div className="space-y-6"><section className="glass rounded-3xl p-6"><h2 className="text-xl font-bold">Delivery information</h2><div className="mt-5 grid gap-4 sm:grid-cols-2">{[["full_name", "Full name"], ["line1", "Address"], ["city", "City"], ["state", "State"], ["postal_code", "Postal code"]].map(([key, label]) => <label key={key} className="text-sm text-white/60">{label}<input required value={form[key as keyof typeof form]} onChange={(e) => setForm({ ...form, [key]: e.target.value })} className="mt-2 w-full rounded-xl border border-white/10 bg-white/[.03] p-3 text-white outline-none focus:border-blue-300/50" /></label>)}</div></section><section className="glass rounded-3xl p-6"><h2 className="text-xl font-bold">Shipping method</h2><div className="mt-5 grid gap-3 sm:grid-cols-2">{[["standard", "Standard · 3–5 days"], ["express", "Express · 1–2 days"]].map(([value, label]) => <label key={value} className="rounded-xl border border-white/10 p-4 text-sm"><input type="radio" name="shipping" value={value} checked={shipping === value} onChange={(e) => setShipping(e.target.value)} className="mr-3" />{label}</label>)}</div></section><section className="glass rounded-3xl p-6"><h2 className="text-xl font-bold">Demo payment</h2><p className="mt-2 text-sm text-white/45">No payment is processed. Placing this order records a demo purchase.</p></section></div><aside className="glass h-fit rounded-3xl p-6"><h2 className="font-bold">Order review</h2><div className="mt-5 space-y-3 text-sm text-white/60">{cart.map((item) => <div key={item.id} className="flex justify-between gap-3"><span>{item.title} × {item.quantity}</span><span>₹{(Number(item.price || 0) * item.quantity).toLocaleString("en-IN")}</span></div>)}</div><div className="my-5 flex justify-between border-t border-white/10 pt-5 text-lg font-bold"><span>Total</span><span>₹{total.toLocaleString("en-IN")}</span></div>{error && <p className="mb-4 rounded-xl bg-red-500/10 p-3 text-sm text-red-200">{error}</p>}<button disabled={busy} className="button-primary w-full justify-center disabled:opacity-50">{busy ? <LoaderCircle className="animate-spin" size={16} /> : <ArrowRight size={16} />} Place order</button></aside></form></main><Footer /></>;
}
