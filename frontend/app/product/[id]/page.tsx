"use client";

import {
  useEffect,
  useState,
} from "react";

import { useParams } from "next/navigation";

import Link from "next/link";

import {
  ArrowRight,
  ChevronRight,
  Check,
  Heart,
  Minus,
  Plus,
  ShoppingBag,
  Sparkles,
  Star,
} from "lucide-react";

import {
  api,
  Footer,
  Header,
  ProductCard,
  useApp,
} from "../../../components";

export default function ProductPage() {
  const params =
    useParams<{
      id: string;
    }>();

  const {
    addToCart,
    wishlist,
    toggleWishlist,
    user,
    authHydrated,
  } = useApp();

  const [product, setProduct] =
    useState<any>(null);
  const [loadError, setLoadError] = useState(false);
  const [recentlyViewed, setRecentlyViewed] = useState<any[]>([]);
  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(false);
  const [activeImage, setActiveImage] = useState(0);
  const [imageFailed, setImageFailed] = useState(false);

  const [
    recommendations,
    setRecommendations,
  ] = useState<any[]>([]);

  useEffect(() => {
    const id =
      Number(params.id);

    if (!Number.isInteger(id) || id <= 0) {
      setLoadError(true);
      return;
    }

    api(`/api/v1/products/${id}`)
      .then((data) => {
        setProduct(data);
        try {
          const current = JSON.parse(localStorage.getItem("recoflow_recently_viewed") || "[]");
          const next = [data, ...current.filter((item: any) => Number(item.id ?? item.product_id) !== id)].slice(0, 4);
          localStorage.setItem("recoflow_recently_viewed", JSON.stringify(next));
          setRecentlyViewed(next.slice(1));
        } catch {}
      })
      .catch(() => setLoadError(true));

    if (authHydrated && user) {
      api("/api/v1/recommendations/hybrid?limit=6")
        .then((data) => setRecommendations(data.items || []))
        .catch(() => {});

      api("/api/v1/events", {
        method: "POST",
        body: JSON.stringify({
          event_type: "product_view",
          product_id: id,
          metadata: { source: "product_page" },
        }),
      }).catch(() => {});
    }
  }, [authHydrated, params.id, user]);

  useEffect(() => {
    setImageFailed(false);
  }, [product?.id]);

  if (!product && loadError) {
    return <><Header /><main className="mx-auto max-w-xl px-5 py-28 text-center"><div className="brand-mark mx-auto">!</div><h1 className="mt-5 text-3xl font-black">Product unavailable</h1><p className="mt-3 text-sm leading-6 text-white/45">We could not load this product right now. Try another discovery path.</p><Link href="/shop" className="button-primary mt-7">Back to shop <ArrowRight size={16} /></Link></main><Footer /></>;
  }

  if (!product) {
    return (
      <>
        <Header />

        <main className="py-32 text-center text-white/40">
          Loading product…
        </main>
        <Footer />
      </>
    );
  }

  const id = Number(
    product.id ??
      product.product_id
  );

  function add() {
    for (let i = 0; i < quantity; i++) addToCart(product);
    setAdded(true);
    window.setTimeout(() => setAdded(false), 1800);

    api(
      "/api/v1/events",
      {
        method: "POST",
        body: JSON.stringify({
          event_type:
            "add_to_cart",
          product_id: id,
          metadata: {
            source:
              "product_page",
          },
        }),
      }
    ).catch(() => {});
  }

  return (
    <>
      <Header />

      <main className="mx-auto max-w-7xl px-5 py-10 lg:px-8">
        <div className="flex items-center gap-2 text-sm text-white/40">
          <Link href="/shop" className="transition hover:text-white">Shop</Link>
          <ChevronRight size={14} />
          <span className="line-clamp-1 text-white/65">{product.title}</span>
        </div>

        <div className="mt-8 grid gap-12 lg:grid-cols-[1.05fr_.95fr]">
          <div>
            <div className="product-shine aspect-square overflow-hidden rounded-[30px] border border-white/[.08] bg-white/5 shadow-2xl shadow-black/30">
            {product.images?.[activeImage] && !imageFailed ? (
              <img
                src={product.images[activeImage]}
                alt={product.title || ""}
                onError={() => setImageFailed(true)}
                className="h-full w-full object-cover transition duration-700 hover:scale-105"
              />
            ) : (
              <div className="flex h-full items-center justify-center text-7xl text-white/10">
                ◈
              </div>
            )}
            </div>
            {product.images?.length > 1 && (
              <div className="mt-4 flex gap-3 overflow-x-auto">
                {product.images.map((image: string, index: number) => (
                  <button key={image} onClick={() => { setActiveImage(index); setImageFailed(false); }} className={`h-20 w-16 shrink-0 overflow-hidden rounded-xl border transition ${activeImage === index ? "border-blue-200/70" : "border-white/10 opacity-60 hover:opacity-100"}`}>
                    <img src={image} alt="" className="h-full w-full object-cover" />
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="flex flex-col justify-center">
            <p className="eyebrow">
              {product.brand ||
                "RecoFlow selection"}
            </p>

            <h1 className="mt-3 text-4xl font-black tracking-[-.04em] md:text-6xl">
              {product.title}
            </h1>

            <div className="mt-5 flex items-center gap-4 text-sm text-white/40">
              {product.rating && (
                <span className="flex items-center gap-1 text-amber-200/80">
                  <Star
                    size={14}
                    className="mr-1 inline"
                    fill="currentColor"
                  />

                  {Number(
                    product.rating
                  ).toFixed(1)}
                </span>
              )}

              <span className="border-l border-white/10 pl-4">
                {Number(
                  product.review_count ||
                    0
                ).toLocaleString()}{" "}
                reviews
              </span>
            </div>

            <div className="my-7 text-4xl font-black tracking-tight">
              ₹
              {Number(
                product.price || 0
              ).toLocaleString(
                "en-IN"
              )}
            </div>

            <p className="max-w-xl text-sm leading-7 text-white/45">
              {product.description ||
                "A product selected for the RecoFlow catalog."}
            </p>

            <div className="mt-8 flex flex-wrap gap-3">
              <div className="flex items-center gap-3 rounded-full border border-white/10 px-3 py-2.5">
                <button onClick={() => setQuantity(Math.max(1, quantity - 1))} className="p-1 text-white/50 hover:text-white"><Minus size={15} /></button>
                <span className="min-w-5 text-center text-sm">{quantity}</span>
                <button onClick={() => setQuantity(quantity + 1)} className="p-1 text-white/50 hover:text-white"><Plus size={15} /></button>
              </div>
              <button
                onClick={add}
                className="button-primary flex-1 justify-center"
              >
                {added ? <><Check size={17} /> Added to bag</> : <><ShoppingBag size={17} /> Add to cart</>}
              </button>

              <button onClick={() => toggleWishlist(id)} className={`rounded-full border px-5 transition ${wishlist.includes(id) ? "border-pink-300/30 bg-pink-300/10 text-pink-200" : "border-white/10 text-white/70 hover:bg-white/10"}`}>
                <Heart size={19} fill={wishlist.includes(id) ? "currentColor" : "none"} />
              </button>
            </div>

            <div className="mt-6 rounded-2xl border border-blue-200/10 bg-blue-300/[.04] p-4 text-xs leading-5 text-white/45">
              <Sparkles
                size={13}
                className="mr-1 inline text-blue-300"
              />
              Recommendations adapt to
              your interactions.
            </div>
            <div className="mt-7 grid grid-cols-2 gap-3 border-t border-white/10 pt-6 text-xs text-white/45">
              <div><span className="block text-white/25">Brand</span><span className="mt-1 block text-white/70">{product.brand || "RecoFlow selection"}</span></div>
              <div><span className="block text-white/25">Reviews</span><span className="mt-1 block text-white/70">{Number(product.review_count || 0).toLocaleString("en-IN")}</span></div>
              <div><span className="block text-white/25">Availability</span><span className="mt-1 block text-emerald-200/80">In catalog</span></div>
              <div><span className="block text-white/25">Personalization</span><span className="mt-1 block text-white/70">Adaptive picks</span></div>
            </div>
          </div>
        </div>

        {recommendations.length >
          0 && (
          <section className="mt-20 border-t border-white/10 pt-12">
            <p className="eyebrow">
              Personalized
            </p>

            <h2 className="mt-2 mb-7 text-3xl font-bold">
              You may also like
            </h2>

            <div className="grid grid-cols-2 gap-x-4 gap-y-9 sm:grid-cols-3 lg:grid-cols-6">
              {recommendations.map(
                (item) => (
                  <ProductCard
                    key={
                      item.product_id
                    }
                    product={item}
                    recommendation
                  />
                )
              )}
              {recentlyViewed.length > 0 && (
                <section className="mt-20 border-t border-white/10 pt-12">
                  <p className="eyebrow">Your trail</p>
                  <h2 className="mt-2 mb-7 text-3xl font-bold">Recently viewed</h2>
                  <div className="grid grid-cols-2 gap-x-4 gap-y-9 sm:grid-cols-4">
                    {recentlyViewed.map((item) => <ProductCard key={item.id ?? item.product_id} product={item} />)}
                  </div>
                </section>
              )}
            </div>
          </section>
        )}
      </main>

      <Footer />
    </>
  );
}