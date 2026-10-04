"use client";

import { useEffect, useMemo, useState } from "react";
import {
  Footer,
  Header,
  ProductCard,
  api,
  useApp,
} from "../../components";
import Link from "next/link";
import { ArrowRight, Heart, Sparkles } from "lucide-react";

export default function Wishlist() {
  const { wishlist } = useApp();
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api("/api/v1/products")
      .then((data) => setProducts(Array.isArray(data) ? data : data.items || []))
      .catch(() => setProducts([]))
      .finally(() => setLoading(false));
  }, []);

  const savedProducts = useMemo(
    () => products.filter((product) => wishlist.includes(Number(product.id ?? product.product_id))),
    [products, wishlist],
  );

  return (
    <>
      <Header />

      <main className="mx-auto max-w-4xl px-5 py-20 text-center lg:py-28">
        <div className="brand-mark mx-auto"><Heart size={15} fill="currentColor" /></div>
        <p className="eyebrow mt-6">
          Saved
        </p>

        <h1 className="mt-3 text-4xl font-black tracking-tight md:text-5xl">
          Wishlist
        </h1>

        <p className="mt-3 text-sm text-blue-100/60">{wishlist.length} {wishlist.length === 1 ? "saved item" : "saved items"}</p>

        <p className="mx-auto mt-4 max-w-xl text-sm leading-7 text-white/40">
          Save the pieces you keep coming back to. Your favorites live here, ready whenever inspiration strikes.
        </p>
        {loading ? (
          <div className="mt-10 grid grid-cols-2 gap-4 text-left sm:grid-cols-3">
            {[1, 2, 3].map((item) => <div key={item} className="aspect-[4/5] animate-pulse rounded-[22px] bg-white/[.05]" />)}
          </div>
        ) : savedProducts.length ? (
          <div className="mt-10 grid grid-cols-2 gap-x-4 gap-y-10 text-left sm:grid-cols-3">
            {savedProducts.map((product) => <ProductCard key={product.id ?? product.product_id} product={product} />)}
          </div>
        ) : (
          <div className="empty-state mx-auto mt-10 max-w-xl">
            <Sparkles size={24} className="mx-auto text-blue-200" />
            <p className="mt-4 text-sm text-white/50">Your saved collection is waiting for its first favorite.</p>
            <Link href="/shop" className="button-primary mt-6">Find something to love <ArrowRight size={15} /></Link>
          </div>
        )}
      </main>

      <Footer />
    </>
  );
}