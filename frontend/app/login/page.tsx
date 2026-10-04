"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Check, Eye, EyeOff, Sparkles } from "lucide-react";

import {
  api,
  Header,
  useApp,
} from "../../components";

export default function Login() {
  const router =
    useRouter();

  const {
    setUser,
  } = useApp();

  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");

  const [error, setError] =
    useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  async function submit(
    event: React.FormEvent
  ) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const data =
        await api(
          "/auth/login",
          {
            method: "POST",
            body: JSON.stringify({
              email,
              password,
            }),
          }
        );

      localStorage.setItem(
        "recoflow_token",
        data.access_token
      );

      const user =
        await api(
          "/auth/me"
        );

      setUser(user);

      router.push("/");
    } catch (error: any) {
      setError(
        error.message ||
          "Unable to sign in."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Header />

      <main className="mx-auto grid min-h-[calc(100vh-76px)] max-w-5xl items-center gap-10 px-5 py-12 lg:grid-cols-[1.1fr_.9fr]">
        <div className="hidden overflow-hidden rounded-[30px] border border-white/10 bg-gradient-to-br from-[#151d38] via-[#0e1426] to-[#0b0d14] p-10 lg:block">
          <div className="brand-mark"><Sparkles size={14} /></div>
          <p className="eyebrow mt-10">Welcome to personal</p>
          <h2 className="mt-4 max-w-lg text-5xl font-black tracking-tight">Less noise.<br /><span className="gradient-text">Better finds.</span></h2>
          <p className="mt-5 max-w-md text-sm leading-7 text-white/45">Your RecoFlow account keeps your shopping signal close, so every visit starts a little smarter.</p>
          <div className="mt-10 flex items-center gap-3 text-sm text-white/55"><Check size={16} className="text-blue-200" /> Personalized discovery that evolves with you</div>
        </div>
        <form
          onSubmit={submit}
          className="glass w-full rounded-[28px] p-8 shadow-2xl shadow-black/20 sm:p-10"
        >
          <div className="brand-mark mb-6"><Sparkles size={14} /></div>
          <p className="eyebrow">
            Welcome back
          </p>

          <h1 className="mt-3 text-4xl font-black tracking-tight">
            Sign in
          </h1>

          <label className="mt-6 block text-sm text-white/55">
            Email

            <input
              required
              type="email"
              value={email}
              onChange={(event) =>
                setEmail(
                  event.target.value
                )
              }
              className="mt-2 w-full rounded-xl border border-white/10 bg-white/[.03] p-3.5 outline-none transition focus:border-blue-300/50"
            />
          </label>

          <label className="mt-4 block text-sm text-white/55">
            Password

            <div className="relative">
              <input
                required
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="mt-2 w-full rounded-xl border border-white/10 bg-white/[.03] p-3.5 pr-11 outline-none transition focus:border-blue-300/50"
              />
              <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-white/35 hover:text-white">{showPassword ? <EyeOff size={17} /> : <Eye size={17} />}</button>
            </div>
          </label>

          {error && (
            <div className="mt-4 text-sm text-red-300">
              <p>{error}</p>
            </div>
          )}

          <button disabled={loading} className="button-primary mt-6 w-full justify-center disabled:opacity-60">
            {loading ? "Signing in…" : "Sign in"}
          </button>

          <p className="mt-5 text-center text-sm text-white/40">
            Need an account?{" "}
            <Link
              href="/register"
              className="text-white"
            >
              Create one
            </Link>
          </p>
        </form>
      </main>
    </>
  );
}