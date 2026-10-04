"use client";

import Link from "next/link";
import {
  ArrowRight,
  ChevronRight,
  ShieldCheck,
  Sparkles,
  Zap,
} from "lucide-react";
import { motion } from "framer-motion";
import { useEffect, useState } from "react";

import {
  api,
  Footer,
  Header,
  Hero3D,
  ProductCard,
  useApp,
} from "../components";

export default function Home() {
  const [
    recommendations,
    setRecommendations,
  ] = useState<any[]>([]);
  const [products, setProducts] = useState<any[]>([]);
  const { user, authHydrated } = useApp();

  useEffect(() => {
    if (authHydrated && user) {
      api("/api/v1/recommendations/hybrid?limit=8").then((data) => setRecommendations(data.items || [])).catch(() => {});
    }
    api("/api/v1/products").then((data) => setProducts(Array.isArray(data) ? data : data.items || [])).catch(() => {});
  }, [authHydrated, user]);

  return (
    <>
      <Header />

      <main>
        <section className="relative min-h-[710px] overflow-hidden border-b border-white/5">
          <div className="grid-background absolute inset-0" />

          <Hero3D />

          <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_50%,transparent,rgba(7,9,13,.58)_40%,#07090d_82%)]" />
          <div className="pointer-events-none absolute right-[9%] top-[24%] hidden rounded-2xl border border-white/10 bg-[#101728]/75 p-3 shadow-2xl backdrop-blur-xl lg:block">
            <p className="text-[10px] uppercase tracking-[.16em] text-blue-200/70">Live signal</p>
            <p className="mt-1 text-sm font-semibold text-white/85">Your next find is forming</p>
          </div>
          <div className="pointer-events-none absolute bottom-[24%] right-[15%] hidden rounded-2xl border border-white/10 bg-[#101728]/75 p-3 shadow-2xl backdrop-blur-xl lg:block">
            <div className="flex items-center gap-2"><span className="h-2 w-2 rounded-full bg-emerald-300 shadow-[0_0_12px_rgba(110,231,183,.7)]" /><span className="text-xs text-white/65">Ranking in real time</span></div>
          </div>

          <div className="relative mx-auto flex min-h-[690px] max-w-7xl items-center px-5 lg:px-8">
            <div className="max-w-2xl pt-6">
              <motion.div
                initial={{
                  opacity: 0,
                  y: 20,
                }}
                animate={{
                  opacity: 1,
                  y: 0,
                }}
                className="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-200/15 bg-blue-300/[.06] px-3 py-1.5 text-xs text-blue-100/75"
              >
                <Sparkles size={13} className="text-blue-300" />
                AI-powered shopping
              </motion.div>

              <motion.h1
                initial={{
                  opacity: 0,
                  y: 25,
                }}
                animate={{
                  opacity: 1,
                  y: 0,
                }}
                className="max-w-2xl text-5xl font-black leading-[.96] tracking-[-.06em] md:text-[82px]"
              >
                Shopping that learns{" "}
                <span className="gradient-text">
                  what you want.
                </span>
              </motion.h1>

              <p className="mt-7 max-w-xl text-base leading-7 text-white/45 md:text-lg">
                A personal shopping layer that learns what you love, filters the noise, and brings your next great find closer.
              </p>

              <div className="mt-9 flex flex-wrap gap-3">
                <Link
                  href="/shop"
                  className="button-primary group"
                >
                  Explore products

                  <ArrowRight
                    size={16}
                    className="transition group-hover:translate-x-1"
                  />
                </Link>

                <Link
                  href="#how"
                  className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[.03] px-6 py-3.5 text-sm font-semibold transition hover:border-white/20 hover:bg-white/[.07]"
                >
                  See recommendations
                </Link>
              </div>
            </div>
          </div>
        </section>

        {products.length > 0 && (
          <section className="mx-auto max-w-7xl px-5 pb-10 pt-16 lg:px-8">
            <div className="flex items-end justify-between gap-4">
              <div><p className="eyebrow">Explore the signal</p><h2 className="mt-3 text-3xl font-bold tracking-tight">Find your next category</h2></div>
              <Link href="/shop" className="hidden items-center gap-1 text-sm text-white/50 transition hover:text-white sm:flex">Shop all <ChevronRight size={16} /></Link>
            </div>
            <div className="mt-7 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
              {Array.from(new Set(products.map((product) => product.category?.name || product.brand).filter(Boolean))).slice(0, 4).map((category: string, index) => (
                <Link key={category} href={`/shop?q=${encodeURIComponent(category)}`} className={`category-card category-card-${index} group relative min-h-40 overflow-hidden rounded-3xl border border-white/10 p-6`}>
                  <span className="relative z-10 text-xs uppercase tracking-[.2em] text-white/45">Explore</span>
                  <span className="relative z-10 mt-3 block text-xl font-bold">{category}</span>
                  <ArrowRight size={17} className="relative z-10 mt-8 text-white/40 transition group-hover:translate-x-1 group-hover:text-white" />
                  <span className="category-orb" />
                </Link>
              ))}
            </div>
          </section>
        )}

        {products.length > 0 && (
          <section className="mx-auto max-w-7xl px-5 pb-4 pt-16 lg:px-8">
            <div className="flex items-end justify-between gap-4">
              <div><p className="eyebrow">Start somewhere</p><h2 className="mt-3 text-3xl font-bold tracking-tight">Discover your next thing</h2></div>
              <Link href="/shop" className="hidden items-center gap-1 text-sm text-white/50 transition hover:text-white sm:flex">Browse all <ChevronRight size={16} /></Link>
            </div>
            <div className="mt-7 grid grid-cols-2 gap-3 sm:grid-cols-4">
              {Array.from(new Set(products.map((product) => product.brand).filter(Boolean))).slice(0, 4).map((brand: string) => (
                <Link key={brand} href={`/shop?q=${encodeURIComponent(brand)}`} className="group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-white/[.08] to-white/[.02] p-5 transition hover:-translate-y-1 hover:border-blue-200/30">
                  <span className="text-sm text-white/55">Explore</span><span className="mt-2 block text-lg font-semibold group-hover:text-blue-100">{brand}</span><ArrowRight size={15} className="mt-6 text-white/30 transition group-hover:translate-x-1 group-hover:text-blue-200" />
                </Link>
              ))}
            </div>
          </section>
        )}

        {products.length > 0 && (
          <section className="mx-auto max-w-7xl px-5 py-20 lg:px-8">
            <div className="mb-8 flex items-end justify-between gap-4"><div><p className="eyebrow">Fresh in the catalog</p><h2 className="mt-3 text-3xl font-bold tracking-tight">Trending now</h2></div><Link href="/shop" className="hidden items-center gap-1 text-sm text-white/50 transition hover:text-white sm:flex">See the edit <ChevronRight size={16} /></Link></div>
            <div className="grid grid-cols-2 gap-x-4 gap-y-10 sm:grid-cols-3 lg:grid-cols-4">
              {products.filter((product) => product.images?.length).slice(0, 4).map((product) => <ProductCard key={product.id} product={product} />)}
            </div>
          </section>
        )}

        <section className="mx-auto max-w-7xl px-5 py-20 lg:px-8">
          <div className="mb-8 flex items-end justify-between gap-4"><div><p className="eyebrow">RecoFlow intelligence</p><h2 className="mt-3 text-3xl font-bold tracking-tight md:text-4xl">Picked for you</h2><p className="mt-3 max-w-lg text-sm text-white/40">Recommendations adapt to the products you explore, save, and add to your bag.</p></div><Link href="/shop" className="hidden items-center gap-1 text-sm text-white/50 transition hover:text-white sm:flex">View all <ChevronRight size={16} /></Link></div>

          {recommendations.length ? (
            <div className="grid grid-cols-2 gap-x-4 gap-y-10 sm:grid-cols-3 lg:grid-cols-4">
              {recommendations.map(
                (item) => (
                  <ProductCard
                    key={item.product_id}
                    product={item}
                    recommendation
                  />
                )
              )}
            </div>
          ) : (
            <div className="empty-state">
              Sign in and interact with
              products to unlock personalized
              recommendations.
            </div>
          )}
        </section>

        <section id="how" className="mx-auto max-w-7xl px-5 py-20 lg:px-8">
          <div className="glass relative overflow-hidden rounded-[34px] p-7 sm:p-10">
            <div className="absolute inset-0 opacity-60 [background:radial-gradient(circle_at_80%_20%,rgba(116,138,255,.18),transparent_34%),radial-gradient(circle_at_10%_90%,rgba(168,115,255,.12),transparent_30%)]" />
            <div className="relative"><p className="eyebrow">How RecoFlow learns</p><h2 className="mt-3 max-w-xl text-3xl font-bold tracking-tight md:text-4xl">Every interaction becomes a better next step.</h2><div className="mt-10 grid gap-3 md:grid-cols-5">{["You", "Interactions", "Behavior signals", "Ranking engine", "Recommendations"].map((step, index) => <div key={step} className="flow-node relative rounded-2xl border border-white/10 bg-black/20 p-4 text-sm font-semibold text-white/80"><span className="mb-4 block text-xs text-blue-200/60">0{index + 1}</span>{step}{index < 4 && <span className="flow-line hidden md:block" />}</div>)}</div></div>
          </div>
        </section>

        <section id="about" className="mx-auto max-w-7xl px-5 pb-20 pt-2 lg:px-8">
          <div className="grid gap-4 md:grid-cols-3">
            <div className="glass rounded-3xl p-6"><p className="eyebrow">The signal</p><p className="mt-4 text-2xl font-bold">Less scrolling.<br /><span className="text-white/40">More finding.</span></p></div>
            <div className="glass rounded-3xl p-6"><p className="eyebrow">Built around you</p><p className="mt-4 text-sm leading-6 text-white/45">Every view, click, and save makes the next recommendation a little more intentional.</p></div>
            <div className="glass rounded-3xl p-6"><p className="eyebrow">Always evolving</p><p className="mt-4 text-sm leading-6 text-white/45">Your taste changes. RecoFlow adapts in real time without losing the joy of discovery.</p></div>
          </div>
        </section>

        <section
          id="how"
          className="border-y border-white/5 bg-white/[.015]"
        >
          <div className="mx-auto max-w-7xl px-5 py-20 lg:px-8">
            <div className="mb-10 max-w-xl"><p className="eyebrow">The RecoFlow method</p><h2 className="mt-3 text-3xl font-bold tracking-tight md:text-4xl">It gets better with every <span className="gradient-text">signal.</span></h2></div>
            <div className="grid gap-5 md:grid-cols-3">
            <Feature
              icon={<Sparkles />}
              title="Learns your taste"
            />

            <Feature
              icon={<Zap />}
              title="Ranks in real time"
            />

            <Feature
              icon={<ShieldCheck />}
              title="Secure by design"
            />
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </>
  );
}

function Feature({
  icon,
  title,
}: {
  icon: React.ReactNode;
  title: string;
}) {
  return (
    <motion.div
      whileHover={{
        y: -5,
      }}
      className="glass rounded-3xl p-7"
    >
      <div className="mb-5 text-blue-300">
        {icon}
      </div>

      <h3 className="text-lg font-bold">
        {title}
      </h3>

      <p className="mt-2 text-sm leading-6 text-white/40">
        Behavior signals flow through the
        RecoFlow recommendation engine to
        improve what you see next.
      </p>
    </motion.div>
  );
}