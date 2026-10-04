"use client";

import Link from "next/link";
import { use, useEffect, useState } from "react";
import { ArrowLeft } from "lucide-react";
import { api, Footer, Header } from "../../../components";

export default function OrderDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [order, setOrder] = useState<any>(null);
  const [error, setError] = useState("");
  useEffect(() => { api(`/api/v1/orders/${id}`).then(setOrder).catch((err) => setError(err instanceof Error ? err.message : "Unable to load order.")); }, [id]);
  return <><Header /><main className="mx-auto max-w-4xl px-5 py-12 lg:px-8"><Link href="/orders" className="inline-flex items-center gap-2 text-sm text-white/45 hover:text-white"><ArrowLeft size={15} /> Order history</Link>{error ? <p className="mt-8 rounded-xl bg-red-500/10 p-4 text-red-200">{error}</p> : order && <><div className="mt-8 flex items-end justify-between"><div><div className="eyebrow">Order details</div><h1 className="mt-3 text-4xl font-black">Order #{order.id}</h1></div><span className="rounded-full bg-blue-300/15 px-3 py-1 text-sm text-blue-100">{order.status}</span></div><div className="mt-8 grid gap-6 lg:grid-cols-2"><section className="glass rounded-3xl p-6"><h2 className="font-bold">Items</h2><div className="mt-5 space-y-4">{order.items.map((item: any) => <div key={item.id} className="flex justify-between text-sm"><span>Product #{item.product_id} × {item.quantity}</span><span>₹{Number(item.unit_price * item.quantity).toLocaleString("en-IN")}</span></div>)}</div><div className="mt-6 flex justify-between border-t border-white/10 pt-5 text-lg font-bold"><span>Total</span><span>₹{Number(order.total_amount).toLocaleString("en-IN")}</span></div></section><section className="glass rounded-3xl p-6"><h2 className="font-bold">Delivery</h2><p className="mt-4 text-sm text-white/60">{order.delivery_address.full_name}<br />{order.delivery_address.line1}<br />{order.delivery_address.city}, {order.delivery_address.state} {order.delivery_address.postal_code}<br />{order.delivery_address.country}</p><p className="mt-5 text-sm text-white/45">Shipping: {order.shipping_method}</p></section></div></>}</main><Footer /></>;
}
