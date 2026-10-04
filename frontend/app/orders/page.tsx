"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { ArrowRight } from "lucide-react";
import { api, Footer, Header } from "../../components";

export default function OrdersPage() {
  const [orders, setOrders] = useState<any[]>([]);
  const [error, setError] = useState("");
  useEffect(() => {
    if (!localStorage.getItem("recoflow_token")) {
      setError("Sign in to view your orders.");
      return;
    }
    api("/api/v1/orders").then(setOrders).catch((err) => setError(err instanceof Error ? err.message : "Unable to load orders."));
  }, []);
  return <><Header /><main className="mx-auto max-w-5xl px-5 py-12 lg:px-8"><div className="eyebrow">Your account</div><h1 className="mt-3 text-4xl font-black">Order history.</h1>{error ? <p className="mt-8 rounded-xl bg-red-500/10 p-4 text-red-200">{error}</p> : <div className="mt-10 space-y-3">{orders.length ? orders.map((order) => <Link key={order.id} href={`/orders/${order.id}`} className="glass flex items-center justify-between rounded-2xl p-5 transition hover:border-blue-200/30"><div><p className="font-bold">Order #{order.id}</p><p className="mt-1 text-sm text-white/40">{new Date(order.created_at).toLocaleString()} · {order.status}</p></div><div className="flex items-center gap-4"><span className="font-bold">₹{Number(order.total_amount).toLocaleString("en-IN")}</span><ArrowRight size={16} className="text-white/40" /></div></Link>) : <p className="mt-10 text-white/45">No orders yet.</p>}</div>}</main><Footer /></>;
}
