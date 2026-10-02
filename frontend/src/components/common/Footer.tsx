"use client";

import React from "react";
import Link from "next/link";
import { PhoneCall, ShieldCheck, HeartHandshake, Scale, ExternalLink } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-slate-900 text-slate-300 text-xs border-t border-slate-800 mt-16 print:hidden">
      {/* Helpline banner */}
      <div className="bg-slate-950 border-b border-slate-800 px-6 py-3">
        <div className="max-w-[1700px] mx-auto flex flex-col md:flex-row items-center justify-between gap-3 text-[11px]">
          <div className="flex items-center gap-2 text-amber-400 font-semibold">
            <HeartHandshake className="w-4 h-4 text-amber-400 flex-shrink-0" />
            <span>Emergency Legal & Human Rights Helplines in Pakistan:</span>
          </div>
          <div className="flex flex-wrap items-center gap-2.5">
            <span className="bg-slate-800/90 px-3 py-1 rounded-md border border-slate-700 text-slate-200 font-mono text-[11px] flex items-center gap-1.5 shadow-xs">
              <span className="text-amber-400 font-bold">MoHR:</span> <strong>1099</strong>
            </span>
            <span className="bg-slate-800/90 px-3 py-1 rounded-md border border-slate-700 text-slate-200 font-mono text-[11px] flex items-center gap-1.5 shadow-xs">
              <span className="text-emerald-400 font-bold">Punjab Ombudsperson:</span> <strong>042-99214436</strong>
            </span>
            <span className="bg-slate-800/90 px-3 py-1 rounded-md border border-slate-700 text-slate-200 font-mono text-[11px] flex items-center gap-1.5 shadow-xs">
              <span className="text-sky-400 font-bold">Sindh Ombudsperson:</span> <strong>021-99211025</strong>
            </span>
          </div>
        </div>
      </div>

      {/* Main Footer Links */}
      <div className="max-w-[1700px] mx-auto px-6 py-10 grid grid-cols-1 md:grid-cols-4 gap-8">
        {/* Brand & Purpose */}
        <div className="space-y-3.5 md:col-span-2">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-[#0B4F6C] text-white flex items-center justify-center font-bold text-sm shadow-xs border border-primary-700">
              حق
            </div>
            <span className="font-extrabold text-white text-base tracking-tight">HaqDar (حقدار)</span>
            <span className="text-[10px] bg-emerald-950 text-emerald-300 px-2.5 py-0.5 rounded-full border border-emerald-700/60 uppercase font-semibold tracking-wide">
              HEC × PakAngels AI Hackathon
            </span>
          </div>
          <p className="text-slate-400 text-xs leading-relaxed max-w-lg">
            Autonomous multi-agent legal intelligence platform empowering dispossessed women in Pakistan to recover their lawful inheritance under Islamic Faraizi jurisprudence and the Enforcement of Women&apos;s Property Rights Act.
          </p>
          <div className="text-[11px] text-slate-300 bg-slate-950/70 p-3 rounded-lg border border-slate-800/90 leading-relaxed max-w-lg">
            ⚖️ Engineered with deterministic rational arithmetic, zero-drift Quranic closure, and fast-track Ombudsperson recovery roadmaps.
          </div>
        </div>

        {/* Platform Navigation */}
        <div className="space-y-3">
          <div className="font-bold text-slate-100 text-xs uppercase tracking-wider">Platform & Architecture</div>
          <ul className="space-y-2 text-xs text-slate-400">
            <li>
              <Link href="/about" className="hover:text-amber-300 transition-colors flex items-center gap-1.5">
                <span>About & 8-Agent Topology</span>
              </Link>
            </li>
            <li>
              <Link href="/disclaimer" className="hover:text-amber-300 transition-colors flex items-center gap-1.5">
                <span>Sharia & Statutory Authorities</span>
              </Link>
            </li>
            <li>
              <Link href="/#tree" className="hover:text-amber-300 transition-colors">
                Shajra Nasab Reconstruction
              </Link>
            </li>
            <li>
              <Link href="/#docs" className="hover:text-amber-300 transition-colors">
                PLRA Mutation Forensic Audit
              </Link>
            </li>
          </ul>
        </div>

        {/* Legal & Compliance */}
        <div className="space-y-3">
          <div className="font-bold text-slate-100 text-xs uppercase tracking-wider">Compliance & Ethics</div>
          <ul className="space-y-2 text-xs text-slate-400">
            <li>
              <Link href="/privacy" className="hover:text-amber-300 transition-colors">
                Privacy Policy & Client Data
              </Link>
            </li>
            <li>
              <Link href="/terms" className="hover:text-amber-300 transition-colors">
                Terms of Service & Usage
              </Link>
            </li>
            <li>
              <Link href="/disclaimer" className="hover:text-amber-300 transition-colors">
                PPC 498A Criminal Penalties
              </Link>
            </li>
            <li className="pt-1">
              <span className="text-[10px] text-slate-400 bg-slate-950/90 px-2 py-1 rounded border border-slate-800 inline-block">
                High Court Advocate Review Recommended
              </span>
            </li>
          </ul>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-slate-800/90 px-6 py-4 bg-slate-950">
        <div className="max-w-[1700px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] text-slate-400">
          <div>
            © {new Date().getFullYear()} HaqDar. Built for the HEC × PakAngels National AI Hackathon.
          </div>
          <div className="flex items-center gap-4 text-slate-400">
            <Link href="/privacy" className="hover:text-white transition-colors">Privacy</Link>
            <span className="text-slate-600">•</span>
            <Link href="/terms" className="hover:text-white transition-colors">Terms</Link>
            <span className="text-slate-600">•</span>
            <Link href="/disclaimer" className="hover:text-white transition-colors">Disclaimer</Link>
            <span className="text-slate-600">•</span>
            <Link href="/about" className="hover:text-white transition-colors">About</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
