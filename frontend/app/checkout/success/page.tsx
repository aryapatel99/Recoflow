"use client";

import Link from "next/link";
import { Check } from "lucide-react";
import { useEffect, useState } from "react";
import { Footer, Header } from "../../../components";

export default function CheckoutSuccessPage() {
  const [orderId, setOrderId] = useState<string | null>(null);

  useEffect(() => {
    const value = new URLSearchParams(window.location.search).get("order");
    if (value && /^\d+$/.test(value)) setOrderId(value);
  }, []);

  return <><Header /><main className="mx-auto max-w-2xl px-5 py-24 text-center"><div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-blue-300/15 text-blue-200"><Check /></div><h1 className="mt-6 text-4xl font-black">Order placed.</h1><p className="mt-3 text-white/45">Your demo order is confirmed and your purchase has been recorded.</p>{orderId && <p className="mt-4 text-sm text-white/50">Order <Link className="text-blue-200 hover:text-white" href={`/orders/${orderId}`}>#{orderId}</Link></p>}<div className="mt-8 flex justify-center gap-3"><Link href="/orders" className="button-primary">View orders</Link><Link href="/shop" className="button-secondary">Continue shopping</Link></div></main><Footer /></>;
}
