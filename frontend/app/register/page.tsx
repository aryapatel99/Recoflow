"use client";

import { useState } from "react";
import Link from "next/link";
import { Check, Eye, EyeOff, Sparkles } from "lucide-react";

import {
  api,
  Header,
} from "../../components";

export default function Register() {
  const [form, setForm] =
    useState({
      email: "",
      password: "",
      first_name: "",
      last_name: "",
    });

  const [error, setError] =
    useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [success, setSuccess] = useState(false);

  const passwordScore = [
    form.password.length >= 8,
    /[A-Z]/.test(form.password),
    /\d/.test(form.password),
  ].filter(Boolean).length;

  async function submit(
    event: React.FormEvent
  ) {
    event.preventDefault();

    setError("");
    if (form.password.length < 8) {
      setError("Use at least 8 characters for your password.");
      return;
    }
    setLoading(true);

    try {
      await api(
        "/auth/register",
        {
          method: "POST",
          body: JSON.stringify({
            email: form.email,
            password: form.password,
            full_name: `${form.first_name} ${form.last_name}`.trim(),
          }),
        }
      );

      setSuccess(true);
    } catch (error: any) {
      setError(
        error.message ||
          "Unable to create account."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Header />

      <main className="mx-auto grid min-h-[calc(100vh-76px)] max-w-5xl items-center gap-10 px-5 py-12 lg:grid-cols-[.9fr_1.1fr]">
        <div className="hidden rounded-[30px] border border-white/10 bg-gradient-to-br from-[#151d38] via-[#0e1426] to-[#0b0d14] p-10 lg:block">
          <div className="brand-mark"><Sparkles size={14} /></div>
          <p className="eyebrow mt-10">A better way to browse</p>
          <h2 className="mt-4 text-4xl font-black tracking-tight">Your taste is the beginning of the journey.</h2>
          <p className="mt-5 text-sm leading-7 text-white/45">RecoFlow learns from the products you explore, save, and add to your bag to make discovery feel more personal over time.</p>
          <div className="mt-10 space-y-4 text-sm text-white/60"><p><Check size={15} className="mr-2 inline text-blue-200" />Your feed evolves with you</p><p><Check size={15} className="mr-2 inline text-blue-200" />No noisy generic recommendations</p><p><Check size={15} className="mr-2 inline text-blue-200" />Built around your real interactions</p></div>
        </div>
        <form
          onSubmit={submit}
          className="glass w-full rounded-[28px] p-8 shadow-2xl shadow-black/20 sm:p-10"
        >
          <div className="brand-mark mb-6"><Sparkles size={14} /></div>
          <p className="eyebrow">
            Get started
          </p>

          <h1 className="mt-3 text-4xl font-black tracking-tight">
            Create account
          </h1>

          <div className="grid grid-cols-2 gap-3">
            <input
              required
              placeholder="First name"
              value={form.first_name}
              onChange={(event) =>
                setForm({
                  ...form,
                  first_name:
                    event.target.value,
                })
              }
              className="mt-6 rounded-xl border border-white/10 bg-white/[.03] p-3.5 outline-none transition focus:border-blue-300/50"
            />

            <input
              required
              placeholder="Last name"
              value={form.last_name}
              onChange={(event) =>
                setForm({
                  ...form,
                  last_name:
                    event.target.value,
                })
              }
              className="mt-6 rounded-xl border border-white/10 bg-white/[.03] p-3.5 outline-none transition focus:border-blue-300/50"
            />
          </div>

          <input
            required
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={(event) =>
              setForm({
                ...form,
                email:
                  event.target.value,
              })
            }
            className="mt-4 w-full rounded-xl border border-white/10 bg-white/[.03] p-3.5 outline-none transition focus:border-blue-300/50"
          />

          <div className="relative mt-4">
            <input
              required
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={form.password}
              onChange={(event) => setForm({ ...form, password: event.target.value })}
              className="w-full rounded-xl border border-white/10 bg-white/[.03] p-3.5 pr-11 outline-none transition focus:border-blue-300/50"
            />
            <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3 top-1/2 -translate-y-1/2 text-white/35 hover:text-white">{showPassword ? <EyeOff size={17} /> : <Eye size={17} />}</button>
          </div>
          <div className="mt-3 flex items-center gap-2">
            {[1, 2, 3].map((level) => <span key={level} className={`h-1 flex-1 rounded-full ${passwordScore >= level ? passwordScore === 1 ? "bg-amber-300" : passwordScore === 2 ? "bg-blue-300" : "bg-emerald-300" : "bg-white/10"}`} />)}
          </div>
          <p className="mt-2 text-xs text-white/30">{form.password ? `${passwordScore}/3 password checks passed` : "Use 8+ characters, a capital letter, and a number."}</p>

          {success ? (
            <div className="mt-5 rounded-xl border border-emerald-300/20 bg-emerald-300/10 p-3 text-sm text-emerald-200">
              <p>Account created. You can sign in now.</p>
              <Link href="/login" className="mt-2 inline-block text-white underline">
                Continue to sign in
              </Link>
            </div>
          ) : error && (
            <p className="mt-4 text-sm text-red-300">
              {error}
            </p>
          )}

          <button disabled={loading || success} className="button-primary mt-6 w-full justify-center disabled:cursor-not-allowed disabled:opacity-60">
            {loading ? "Creating your account…" : success ? "Account created" : "Create account"}
          </button>

          <p className="mt-5 text-center text-sm text-white/40">
            Already registered?{" "}
            <Link
              href="/login"
              className="text-white"
            >
              Sign in
            </Link>
          </p>
        </form>
      </main>
    </>
  );
}