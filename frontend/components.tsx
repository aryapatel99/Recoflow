"use client";

import Link from "next/link";
import {
  ArrowRight,
  Check,
  ChevronDown,
  Heart,
  Menu,
  Minus,
  Plus,
  Search,
  ShoppingBag,
  Sparkles,
  Star,
  Trash2,
  UserRound,
  X,
} from "lucide-react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { Float, MeshDistortMaterial, Sphere } from "@react-three/drei";
import { createContext, useContext, useEffect, useMemo, useRef, useState } from "react";
import { motion } from "framer-motion";

const configuredApiUrl = process.env.NEXT_PUBLIC_API_URL;
if (process.env.NODE_ENV === "production" && !configuredApiUrl) {
  throw new Error("NEXT_PUBLIC_API_URL must be configured for production builds.");
}

export const API = configuredApiUrl || "http://127.0.0.1:8000";
const BROWSER_API_PREFIX = "/api/backend";

export async function api(path: string, options: RequestInit = {}) {
  const token = typeof window !== "undefined" ? localStorage.getItem("recoflow_token") : null;
  const headers = new Headers(options.headers);
  let body = options.body;
  if (body && path === "/api/v1/events" && typeof body === "string") {
    const event = JSON.parse(body);
    if (!event.event_id) {
      event.event_id = typeof crypto !== "undefined" && crypto.randomUUID
        ? crypto.randomUUID()
        : `web-${Date.now()}-${Math.random().toString(16).slice(2)}`;
    }
    body = JSON.stringify(event);
  }
  if (body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", "Bearer " + token);
const baseUrl = typeof window === "undefined" ? API : BROWSER_API_PREFIX;
const response = await fetch(`${baseUrl}${path}`, { ...options, body, headers, cache: "no-store" });
  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {}
    throw new Error(message);
  }
  return response.json();
}

type AppContextType = {
  user: any;
  authHydrated: boolean;
  setUser: React.Dispatch<React.SetStateAction<any>>;
  cart: any[];
  wishlist: number[];
  toast: string | null;
  showToast: (message: string) => void;
  addToCart: (product: any) => void;
  removeFromCart: (id: number) => void;
  clearCart: () => void;
  toggleWishlist: (id: number) => void;
  logout: () => void;
};

const AppContext = createContext<AppContextType | null>(null);

export function Providers({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<any>(null);
  const [cart, setCart] = useState<any[]>([]);
  const [wishlist, setWishlist] = useState<number[]>([]);
  const [toast, setToast] = useState<string | null>(null);
  const [hydrated, setHydrated] = useState(false);
  const [authHydrated, setAuthHydrated] = useState(false);

  useEffect(() => {
    try {
      const savedCart = localStorage.getItem("recoflow_cart");
      const savedWishlist = localStorage.getItem("recoflow_wishlist");
      if (savedCart) setCart(JSON.parse(savedCart));
      if (savedWishlist) setWishlist(JSON.parse(savedWishlist));
    } catch {}
    const token = localStorage.getItem("recoflow_token");
    if (token) {
      api("/auth/me")
        .then(async (authenticatedUser) => {
          setUser(authenticatedUser);
          const [serverCart, serverWishlist] = await Promise.all([
            api("/api/v1/cart"),
            api("/api/v1/wishlist"),
          ]);
          setCart((serverCart.items || []).map((item: any) => ({
            ...item.product,
            id: item.product_id,
            quantity: item.quantity,
          })));
          setWishlist((serverWishlist.items || []).map((item: any) => item.product_id));
        })
        .catch(() => localStorage.removeItem("recoflow_token"));
    }
    setHydrated(true);
    setAuthHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    localStorage.setItem("recoflow_cart", JSON.stringify(cart));
    localStorage.setItem("recoflow_wishlist", JSON.stringify(wishlist));
  }, [cart, hydrated, wishlist]);

  function addToCart(product: any) {
    const id = Number(product.id ?? product.product_id);
    setCart((current) => {
      const existing = current.find((item) => Number(item.id ?? item.product_id) === id);
      const quantity = existing ? existing.quantity + 1 : 1;
      if (user) {
        api("/api/v1/cart/items", {
          method: "POST",
          body: JSON.stringify({ product_id: id, quantity }),
        }).catch(() => showToast("Could not sync your bag."));
      }
      if (existing) {
        return current.map((item) =>
          Number(item.id ?? item.product_id) === id ? { ...item, quantity: item.quantity + 1 } : item,
        );
      }
      return [...current, { ...product, id, quantity: 1 }];
    });
  }

  function removeFromCart(id: number) {
    setCart((current) => {
      const existing = current.find((item) => Number(item.id ?? item.product_id) === id);
      const quantity = existing ? existing.quantity - 1 : 0;
      if (user) {
        const request = quantity > 0
          ? api("/api/v1/cart/items", { method: "POST", body: JSON.stringify({ product_id: id, quantity }) })
          : api(`/api/v1/cart/items/${id}`, { method: "DELETE" });
        request.catch(() => showToast("Could not sync your bag."));
      }
      return current
        .map((item) => Number(item.id ?? item.product_id) === id ? { ...item, quantity: item.quantity - 1 } : item)
        .filter((item) => item.quantity > 0);
    });
  }

  function clearCart() {
    setCart([]);
  }

  function toggleWishlist(id: number) {
    const removing = wishlist.includes(id);
    setWishlist((current) => removing ? current.filter((item) => item !== id) : [...current, id]);
    if (user) {
      const request = removing
        ? api(`/api/v1/wishlist/items/${id}`, { method: "DELETE" })
        : api("/api/v1/wishlist/items", { method: "POST", body: JSON.stringify({ product_id: id }) });
      request.catch(() => showToast("Could not sync your wishlist."));
    }
    setToast(removing ? "Removed from wishlist" : "Saved to wishlist");
    window.setTimeout(() => setToast(null), 2200);
  }

  function showToast(message: string) {
    setToast(message);
    window.setTimeout(() => setToast(null), 2200);
  }

  function logout() {
    localStorage.removeItem("recoflow_token");
    setUser(null);
    setCart([]);
    setWishlist([]);
  }

  return (
    <AppContext.Provider value={{ user, authHydrated, setUser, cart, wishlist, toast, showToast, addToCart, removeFromCart, clearCart, toggleWishlist, logout }}>
      {children}
      {toast && <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="toast"><Check size={16} /> {toast}</motion.div>}
    </AppContext.Provider>
  );
}

export function useApp() {
  const value = useContext(AppContext);
  if (!value) throw new Error("useApp must be used inside Providers");
  return value;
}

export function Header() {
  const { user, cart, wishlist, logout } = useApp();
  const [query, setQuery] = useState("");
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const cartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  function search(event: React.FormEvent) {
    event.preventDefault();
    if (query.trim()) window.location.href = `/shop?q=${encodeURIComponent(query.trim())}`;
  }

  return (
    <header className={`sticky top-0 z-50 border-b border-white/[.08] bg-[#07090d]/80 backdrop-blur-2xl transition-all duration-300 ${scrolled ? "shadow-[0_14px_50px_rgba(0,0,0,.28)]" : ""}`}>
      <div className={`mx-auto flex max-w-7xl items-center gap-4 px-5 transition-all duration-300 lg:px-8 ${scrolled ? "h-[62px]" : "h-[76px]"}`}>
        <Link href="/" className="group flex shrink-0 items-center gap-2 text-xl font-black tracking-[-.05em]">
          <span className="brand-mark"><Sparkles size={14} /></span>
          <span><span className="gradient-text">Reco</span>Flow</span>
        </Link>
        <nav className="hidden items-center gap-7 text-sm text-white/55 md:flex">
          <Link className="nav-link" href="/shop">Shop</Link>
          <Link className="nav-link" href="/#how">How it works</Link>
          <Link className="nav-link" href="/#about">Our approach</Link>
        </nav>
        <form onSubmit={search} className="ml-auto hidden max-w-md flex-1 md:block">
          <div className="glass flex h-11 items-center rounded-full px-4 transition focus-within:border-blue-300/40">
            <Search size={16} className="text-white/35" />
            <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search your next favorite..." className="ml-3 w-full bg-transparent text-sm outline-none placeholder:text-white/30" />
          </div>
        </form>
        <div className="flex items-center gap-1">
          <Link href="/wishlist" className="icon-button relative"><Heart size={18} /><span className="sr-only">Wishlist</span>{wishlist.length > 0 && <i>{wishlist.length}</i>}</Link>
          <Link href="/cart" className="icon-button relative"><ShoppingBag size={19} /><span className="sr-only">Cart</span>{cartCount > 0 && <i>{cartCount}</i>}</Link>
          {user ? <button onClick={logout} className="icon-button hidden sm:inline-flex" title="Sign out"><UserRound size={18} /></button> : <Link href="/login" className="hidden rounded-full bg-white px-4 py-2.5 text-xs font-bold text-black transition hover:bg-blue-100 sm:inline-flex">Sign in</Link>}
          <button onClick={() => setMobileOpen(!mobileOpen)} className="icon-button md:hidden">{mobileOpen ? <X size={20} /> : <Menu size={20} />}</button>
        </div>
      </div>
      {mobileOpen && (
        <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className="border-t border-white/[.08] px-5 py-4 md:hidden">
          <form onSubmit={search} className="mb-4 flex h-11 items-center rounded-xl border border-white/10 bg-white/[.04] px-3"><Search size={16} className="text-white/35" /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search products..." className="ml-3 w-full bg-transparent text-sm outline-none" /></form>
          <div className="grid gap-1 text-sm text-white/70"><Link onClick={() => setMobileOpen(false)} className="rounded-lg px-3 py-3 hover:bg-white/5" href="/shop">Shop all</Link><Link onClick={() => setMobileOpen(false)} className="rounded-lg px-3 py-3 hover:bg-white/5" href="/#how">How it works</Link><Link onClick={() => setMobileOpen(false)} className="rounded-lg px-3 py-3 hover:bg-white/5" href="/wishlist">Wishlist</Link>{!user && <Link onClick={() => setMobileOpen(false)} className="rounded-lg px-3 py-3 text-blue-200 hover:bg-white/5" href="/login">Sign in</Link>}</div>
        </motion.div>
      )}
    </header>
  );
}

function Orb() {
  const ref = useRef<any>(null);
  useFrame((state) => {
    if (!ref.current) return;
    ref.current.rotation.x = state.clock.elapsedTime * 0.12;
    ref.current.rotation.y = state.clock.elapsedTime * 0.16;
  });
  return <Float speed={1.5} rotationIntensity={0.4} floatIntensity={0.8}><Sphere ref={ref} args={[1.7, 64, 64]}><MeshDistortMaterial color="#718dff" metalness={0.65} roughness={0.16} distort={0.32} speed={1.6} /></Sphere></Float>;
}

function SceneParticles() {
  const points = useMemo(() => {
    const values = new Float32Array(180 * 3);
    for (let index = 0; index < values.length; index += 3) {
      const radius = 2.4 + Math.random() * 1.8;
      const angle = Math.random() * Math.PI * 2;
      values[index] = Math.cos(angle) * radius;
      values[index + 1] = (Math.random() - 0.5) * 3;
      values[index + 2] = Math.sin(angle) * radius;
    }
    return values;
  }, []);
  const ref = useRef<any>(null);
  useFrame((_, delta) => {
    if (ref.current) ref.current.rotation.y += delta * 0.025;
  });
  return (
    <points ref={ref}>
      <bufferGeometry><bufferAttribute attach="attributes-position" args={[points, 3]} /></bufferGeometry>
      <pointsMaterial color="#9db9ff" size={0.018} transparent opacity={0.55} sizeAttenuation />
    </points>
  );
}

function ParallaxRig({ reducedMotion }: { reducedMotion: boolean }) {
  const ref = useRef<any>(null);
  const { camera } = useThree();
  useFrame((state) => {
    if (!ref.current) return;
    const targetX = reducedMotion ? 0 : state.pointer.x * 0.22;
    const targetY = reducedMotion ? 0 : state.pointer.y * 0.12;
    ref.current.rotation.y += (targetX - ref.current.rotation.y) * 0.035;
    ref.current.rotation.x += (-targetY - ref.current.rotation.x) * 0.035;
    camera.position.x += (targetX * 0.28 - camera.position.x) * 0.025;
    camera.position.y += (targetY * 0.18 - camera.position.y) * 0.025;
    camera.lookAt(0, 0, 0);
  });
  return (
    <group ref={ref}>
      <SceneParticles />
      <Float speed={1.1} rotationIntensity={0.25} floatIntensity={0.55}>
        <mesh rotation={[0.4, 0.2, 0.1]} position={[2.05, 0.55, -0.25]}>
          <torusGeometry args={[0.78, 0.018, 16, 80]} />
          <meshBasicMaterial color="#93c5fd" transparent opacity={0.72} />
        </mesh>
      </Float>
      <Float speed={0.8} rotationIntensity={0.2} floatIntensity={0.45}>
        <mesh position={[-1.95, -0.65, -0.35]} rotation={[0.5, 0.4, 0.2]}>
          <octahedronGeometry args={[0.38, 0]} />
          <meshStandardMaterial color="#9d8cff" metalness={0.8} roughness={0.2} emissive="#4338ca" emissiveIntensity={0.4} />
        </mesh>
      </Float>
      <Orb />
    </group>
  );
}

export function Hero3D() {
  const [reducedMotion, setReducedMotion] = useState(false);
  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setReducedMotion(media.matches);
    update();
    media.addEventListener("change", update);
    return () => media.removeEventListener("change", update);
  }, []);
  return <div className="hero-orb absolute inset-0"><Canvas dpr={[1, 1.5]} camera={{ position: [0, 0, 5], fov: 45 }}><ambientLight intensity={0.8} /><directionalLight position={[3, 4, 5]} intensity={2.4} color="#d9e2ff" /><pointLight position={[3, 1, 2]} intensity={7} color="#6f8cff" /><pointLight position={[-3, -2, 2]} intensity={6} color="#a18cff" /><ParallaxRig reducedMotion={reducedMotion} /></Canvas></div>;
}

export function ProductCard({ product, recommendation = false }: { product: any; recommendation?: boolean }) {
  const { addToCart, wishlist, toggleWishlist, showToast, user } = useApp();
  const id = Number(product.id ?? product.product_id);
  const saved = wishlist.includes(id);
  const [imageFailed, setImageFailed] = useState(false);
  async function event(eventType: string) {
    if (!user) return;
    try { await api("/api/v1/events", { method: "POST", body: JSON.stringify({ event_type: eventType, product_id: id, metadata: { source: "web_ui" } }) }); } catch {}
  }
  return (
    <motion.article initial={{ opacity: 0, y: 15 }} whileInView={{ opacity: 1, y: 0 }} whileHover={{ y: -7, rotateX: 1.5, rotateY: -1.5 }} viewport={{ once: true, margin: "-30px" }} transition={{ type: "spring", stiffness: 260, damping: 22 }} className="group [perspective:1000px]">
      <div className="product-shine relative aspect-[4/5] overflow-hidden rounded-[22px] border border-white/[.08] bg-gradient-to-br from-[#1a2234] to-[#0d1118] shadow-2xl shadow-black/20">
        <Link href={`/product/${id}`} onClick={() => event("product_click")} className="block h-full">
          {product.images?.[0] && !imageFailed ? <img src={product.images[0]} alt={product.title || ""} onError={() => setImageFailed(true)} className="h-full w-full object-cover transition duration-700 group-hover:scale-110" /> : <div className="flex h-full items-center justify-center text-5xl text-white/10">◈</div>}
          <div className="absolute inset-x-0 bottom-0 h-1/2 bg-gradient-to-t from-black/55 to-transparent" />
        </Link>
        <button onClick={() => toggleWishlist(id)} className={`absolute right-3 top-3 rounded-full border p-2.5 backdrop-blur-xl transition ${saved ? "border-pink-300/30 bg-pink-400/15 text-pink-200" : "border-white/10 bg-black/30 text-white/70 hover:bg-white/15 hover:text-white"}`}><Heart size={15} fill={saved ? "currentColor" : "none"} /></button>
        {recommendation && <span className="absolute bottom-3 left-3 rounded-full border border-blue-200/15 bg-[#111a32]/80 px-2.5 py-1.5 text-[10px] font-semibold text-blue-100 backdrop-blur-xl"><Sparkles size={10} className="mr-1 inline" /> Picked for you</span>}
      </div>
      <div className="pt-3.5">
        <div className="flex items-start gap-2"><Link href={`/product/${id}`} className="line-clamp-2 flex-1 text-[14px] font-semibold leading-5 text-white/90 transition hover:text-blue-200">{product.title}</Link><button onClick={() => { addToCart(product); showToast("Added to bag"); event("add_to_cart"); }} className="quick-add" title="Add to cart"><ShoppingBag size={14} /></button></div>
        <div className="mt-2.5 flex items-center justify-between"><b className="text-base">₹{Number(product.price || 0).toLocaleString("en-IN")}</b>{product.rating ? <span className="flex items-center gap-1 text-xs text-amber-200/75"><Star size={12} fill="currentColor" /> {Number(product.rating).toFixed(1)}</span> : <span className="text-xs text-white/30">New arrival</span>}</div>
      </div>
    </motion.article>
  );
}

export function Footer() {
  return <footer className="mt-24 border-t border-white/[.08] px-5 py-12 lg:px-8"><div className="mx-auto grid max-w-7xl gap-10 md:grid-cols-[1.5fr_1fr_1fr_1fr]"><div><Link href="/" className="text-xl font-black"><span className="gradient-text">Reco</span>Flow</Link><p className="mt-4 max-w-xs text-sm leading-6 text-white/35">A smarter way to discover products that feel made for you.</p></div><div><p className="footer-label">Explore</p><div className="mt-4 grid gap-3 text-sm text-white/45"><Link href="/shop">Shop all</Link><Link href="/wishlist">Wishlist</Link><Link href="/cart">Your cart</Link></div></div><div><p className="footer-label">RecoFlow</p><div className="mt-4 grid gap-3 text-sm text-white/45"><Link href="/#how">How it works</Link><Link href="/#about">Our approach</Link></div></div><div><p className="footer-label">Stay in the loop</p><p className="mt-4 text-sm leading-6 text-white/40">Personalized picks, thoughtfully delivered.</p></div></div><div className="mx-auto mt-12 flex max-w-7xl flex-col gap-2 border-t border-white/[.08] pt-5 text-xs text-white/25 sm:flex-row sm:justify-between"><span>© {new Date().getFullYear()} RecoFlow</span><span>Personalized shopping, engineered.</span></div></footer>;
}

export function CartPage() {
  const { cart, addToCart, removeFromCart, showToast } = useApp();
  const total = cart.reduce((sum, item) => sum + Number(item.price || 0) * item.quantity, 0);
  return <><Header /><main className="mx-auto max-w-6xl px-5 py-12 lg:px-8"><div className="eyebrow">Your bag</div><h1 className="mt-3 text-4xl font-black tracking-tight md:text-5xl">Make it yours.</h1><p className="mt-3 text-white/40">Review your picks before they find their way to you.</p>{!cart.length ? <div className="empty-state mt-12"><ShoppingBag size={28} className="mx-auto text-blue-200" /><h2 className="mt-4 text-xl font-bold">Your bag is waiting</h2><p className="mt-2 text-sm text-white/40">Add something you love and it will appear here.</p><Link href="/shop" className="button-primary mt-7">Explore products <ArrowRight size={16} /></Link></div> : <div className="mt-10 grid gap-6 lg:grid-cols-[1fr_340px]"><div className="space-y-3">{cart.map((item) => { const id = Number(item.id ?? item.product_id); return <div key={id} className="glass flex gap-4 rounded-2xl p-4"><div className="h-28 w-24 shrink-0 overflow-hidden rounded-xl bg-white/5">{item.images?.[0] ? <img src={item.images[0]} alt="" className="h-full w-full object-cover" /> : <div className="flex h-full items-center justify-center text-white/10">◈</div>}</div><div className="flex flex-1 flex-col"><Link href={`/product/${id}`} className="font-semibold hover:text-blue-200">{item.title}</Link><p className="mt-2 text-sm text-white/45">{item.brand || "RecoFlow selection"}</p><p className="mt-auto pt-3 font-bold">₹{Number(item.price || 0).toLocaleString("en-IN")}</p></div><div className="flex flex-col items-end justify-between"><button onClick={() => { for (let i = 0; i < item.quantity; i++) removeFromCart(id); showToast("Removed from bag"); }} className="text-white/25 transition hover:text-red-300"><Trash2 size={16} /></button><div className="flex items-center gap-3 rounded-full border border-white/10 px-2 py-1 text-sm"><button onClick={() => removeFromCart(id)} className="p-1 text-white/55 hover:text-white"><Minus size={13} /></button>{item.quantity}<button onClick={() => addToCart(item)} className="p-1 text-white/55 hover:text-white"><Plus size={13} /></button></div></div></div>; })}<Link href="/shop" className="mt-5 inline-flex items-center gap-2 text-sm text-white/50 hover:text-white"><ArrowRight size={15} className="rotate-180" /> Continue shopping</Link></div><aside className="glass h-fit rounded-3xl p-6"><h2 className="font-bold">Order summary</h2><div className="my-5 flex justify-between border-t border-white/10 pt-5 text-lg font-bold"><span>Subtotal</span><span>₹{total.toLocaleString("en-IN")}</span></div><Link href="/checkout" className="button-primary w-full justify-center">Continue to checkout <ArrowRight size={16} /></Link><p className="mt-4 text-center text-xs text-white/30">Demo payment · No charge will be made</p></aside></div>}</main><Footer /></>;
}
