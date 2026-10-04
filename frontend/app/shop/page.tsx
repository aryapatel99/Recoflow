"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Search, SlidersHorizontal, X } from "lucide-react";
import { api, Footer, Header, ProductCard } from "../../components";

type Product = {
  id: number;
  external_id?: string;
  title: string;
  description?: string | null;
  price?: number | null;
  brand?: string | null;
  category_id?: number | null;
  rating?: number | null;
  review_count?: number | null;
  images?: string[] | null;
};

function ShopContent() {
  const searchParams = useSearchParams();

  const initialSearch = searchParams.get("q") || "";

  const [products, setProducts] = useState<Product[]>([]);
  const [search, setSearch] = useState(initialSearch);
  const [sort, setSort] = useState("featured");
  const [brand, setBrand] = useState("");
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const query = searchParams.get("q") || "";
    setSearch(query);
  }, [searchParams]);

  useEffect(() => {
    async function loadProducts() {
      try {
        setLoading(true);
        setError("");

        const data = await api("/api/v1/products");
        if (!data || typeof data !== "object" || !Array.isArray(data.items)) {
          throw new Error("invalid-products-response");
        }
        setProducts(data.items);
      } catch (err) {
        const reason = err instanceof Error ? err.message : "unknown";
        setError(
          reason === "network"
            ? "We couldn’t reach the product service."
            : reason === "invalid-json" || reason === "invalid-products-response"
              ? "The product service returned an unexpected response."
              : reason.startsWith("http:")
                ? `The product service returned ${reason.slice(5)}.`
                : "Products are temporarily unavailable.",
        );
      } finally {
        setLoading(false);
      }
    }

    loadProducts();
  }, []);

  const filteredProducts = useMemo(() => {
    let result = [...products];

    const query = search.trim().toLowerCase();

    if (query) {
      result = result.filter((product) => {
        const searchable = [
          product.title,
          product.description || "",
          product.brand || "",
          product.external_id || "",
        ]
          .join(" ")
          .toLowerCase();

        return searchable.includes(query);
      });
    }

    if (sort === "price-low") {
      result.sort(
        (a, b) =>
          Number(a.price || 0) -
          Number(b.price || 0)
      );
    }

    if (sort === "price-high") {
      result.sort(
        (a, b) =>
          Number(b.price || 0) -
          Number(a.price || 0)
      );
    }

    if (sort === "rating") {
      result.sort(
        (a, b) =>
          Number(b.rating || 0) -
          Number(a.rating || 0)
      );
    }

    if (sort === "reviews") {
      result.sort(
        (a, b) =>
          Number(b.review_count || 0) -
          Number(a.review_count || 0)
      );
    }

    if (brand) {
      result = result.filter((product) => product.brand === brand);
    }

    return result;
  }, [products, search, sort, brand]);

  const brands = useMemo(
    () => Array.from(new Set(products.map((product) => product.brand).filter((value): value is string => Boolean(value)))).slice(0, 6),
    [products],
  );

  return (
    <main className="min-h-screen px-4 pb-20 pt-12 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <div className="mb-10 flex flex-col justify-between gap-5 md:flex-row md:items-end">
          <div>
          <p className="eyebrow">The RecoFlow edit</p>

          <h1 className="mt-3 text-4xl font-bold tracking-[-.04em] text-white sm:text-6xl">
            Explore products
          </h1>

          <p className="mt-4 max-w-xl text-gray-400">
            Discover pieces worth keeping. Every interaction helps RecoFlow tune your next find.
          </p>
          </div>
          <p className="text-sm text-white/35">Curated for curious minds</p>
        </div>

        <div className="glass mb-8 flex flex-col gap-4 rounded-2xl p-3 sm:flex-row">
          <div className="relative flex-1">
            <Search
              size={18}
              className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"
            />

            <input
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
              placeholder="Search products..."
              className="w-full rounded-xl border border-white/10 bg-black/20 py-3 pl-11 pr-4 text-white outline-none transition focus:border-blue-300/50"
            />
          </div>

          <div className="relative">
            <SlidersHorizontal
              size={17}
              className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"
            />

            <select
              value={sort}
              onChange={(event) =>
                setSort(event.target.value)
              }
              className="w-full appearance-none rounded-xl border border-white/10 bg-black/20 py-3 pl-11 pr-10 text-white outline-none sm:w-56"
            >
              <option value="featured">
                Featured
              </option>

              <option value="price-low">
                Price: Low to High
              </option>

              <option value="price-high">
                Price: High to Low
              </option>

              <option value="rating">
                Highest Rated
              </option>

              <option value="reviews">
                Most Reviewed
              </option>
            </select>
          </div>
        </div>
        <div className="mb-8 flex items-center gap-2 overflow-x-auto pb-1">
          <button onClick={() => setFiltersOpen(!filtersOpen)} className="inline-flex shrink-0 items-center gap-2 rounded-full border border-white/10 bg-white/[.04] px-4 py-2 text-xs font-semibold text-white/70 transition hover:border-white/20 hover:text-white sm:hidden">
            <SlidersHorizontal size={14} /> Filters
          </button>
          <button onClick={() => setBrand("")} className={`shrink-0 rounded-full px-4 py-2 text-xs font-semibold transition ${!brand ? "bg-white text-black" : "border border-white/10 text-white/50 hover:text-white"}`}>All products</button>
          {brands.map((item) => <button key={item} onClick={() => setBrand(item)} className={`shrink-0 rounded-full px-4 py-2 text-xs font-semibold transition ${brand === item ? "bg-blue-200 text-[#101526]" : "border border-white/10 text-white/50 hover:text-white"}`}>{item}</button>)}
        </div>
        {filtersOpen && (
          <div className="mb-8 flex items-center justify-between rounded-2xl border border-blue-200/10 bg-blue-300/[.04] p-4 text-sm text-white/60 sm:hidden">
            <span>{brand ? `Filtering by ${brand}` : "Showing every available product"}</span>
            <button onClick={() => setFiltersOpen(false)} className="text-white/45 hover:text-white"><X size={16} /></button>
          </div>
        )}

        {loading && (
          <div className="grid grid-cols-2 gap-x-4 gap-y-10 sm:grid-cols-3 lg:grid-cols-4">
            {Array.from({ length: 8 }).map(
              (_, index) => (
                <div
                  key={index}
                  className="aspect-[4/5] animate-pulse rounded-[22px] border border-white/10 bg-gradient-to-br from-white/[.07] to-white/[.02]"
                />
              )
            )}
          </div>
        )}

        {!loading && error && (
          <div className="rounded-2xl border border-red-500/20 bg-red-500/10 p-6 text-red-300">
            {error}
          </div>
        )}

        {!loading &&
          !error &&
          filteredProducts.length === 0 && (
            <div className="empty-state">
              <h2 className="text-xl font-semibold text-white">
                No products found
              </h2>

              <p className="mt-2 text-gray-400">
                Try a different search term.
              </p>
            </div>
          )}

        {!loading &&
          !error &&
          filteredProducts.length > 0 && (
            <>
              <div className="mb-5 flex items-center justify-between">
                <p className="text-sm text-gray-400">
                  {filteredProducts.length} products
                </p>
              </div>

              <div className="grid grid-cols-2 gap-x-4 gap-y-10 sm:grid-cols-3 lg:grid-cols-4">
                {filteredProducts.map((product) => (
                  <ProductCard
                    key={product.id}
                    product={product}
                  />
                ))}
              </div>
            </>
          )}
      </div>
    </main>
  );
}

export default function ShopPage() {
  return (
    <>
      <Header />
      <Suspense
        fallback={
          <main className="min-h-screen px-4 pb-20 pt-12 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-7xl">
            <div className="h-10 w-64 animate-pulse rounded-lg bg-white/10" />

            <div className="mt-4 h-6 w-96 animate-pulse rounded-lg bg-white/10" />

            <div className="mt-10 h-14 animate-pulse rounded-2xl bg-white/10" />

            <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
              {Array.from({ length: 8 }).map(
                (_, index) => (
                  <div
                    key={index}
                    className="h-96 animate-pulse rounded-2xl bg-white/[0.04]"
                  />
                )
              )}
            </div>
          </div>
          </main>
        }
      >
        <ShopContent />
      </Suspense>
      <Footer />
    </>
  );
}