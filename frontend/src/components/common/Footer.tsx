"use client";

import React from "react";
import Link from "next/link";
import { PhoneCall, ShieldCheck, HeartHandshake, Scale, ExternalLink } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-primary-950 text-slate-300 text-xs border-t border-primary-900 mt-12 print:hidden">
      {/* Helpline banner */}
      <div className="bg-accent-950/80 border-b border-accent-900/60 px-6 py-3">
        <div className="max-w-[1700px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-2 text-[11px]">
          <div className="flex items-center gap-2 text-accent-300 font-medium">
            <HeartHandshake className="w-4 h-4 text-accent-400 flex-shrink-0" />
            <span>Emergency Legal & Human Rights Helplines in Pakistan:</span>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <span className="bg-accent-900/60 px-2 py-0.5 rounded border border-accent-700/60 text-white font-mono">
              📞 MoHR Helpline: <strong>1099</strong>
            </span>
            <span className="bg-accent-900/60 px-2 py-0.5 rounded border border-accent-700/60 text-white font-mono">
              📞 Punjab Ombudsperson: <strong>042-99214436</strong>
            </span>
            <span className="bg-accent-900/60 px-2 py-0.5 rounded border border-accent-700/60 text-white font-mono">
              📞 Sindh Ombudsperson: <strong>021-99211025</strong>
            </span>
          </div>
        </div>
      </div>

      {/* Main Footer Links */}
      <div className="max-w-[1700px] mx-auto px-6 py-8 grid grid-cols-1 md:grid-cols-4 gap-8">
        {/* Brand & Purpose */}
        <div className="space-y-3 md:col-span-2">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-primary-800 text-white flex items-center justify-center font-bold text-sm">
              حق
            </div>
            <span className="font-extrabold text-white text-base">HaqDar (حقدار)</span>
            <span className="text-[10px] bg-emerald-900/60 text-emerald-300 px-2 py-0.5 rounded border border-emerald-700/60 uppercase font-semibold">
              HEC × PakAngels AI Hackathon
            </span>
          </div>
          <p className="text-slate-400 text-xs leading-relaxed max-w-lg">
            Autonomous multi-agent legal intelligence platform empowering dispossessed women in Pakistan to recover their lawful inheritance under Islamic Faraizi jurisprudence and the Enforcement of Women&apos;s Property Rights Act.
          </p>
          <div className="text-[11px] text-slate-500">
            Engineered with deterministic rational arithmetic, zero-drift Quranic closure, and fast-track Ombudsperson recovery roadmaps.
          </div>
        </div>

        {/* Platform Navigation */}
        <div className="space-y-2.5">
          <div className="font-bold text-white text-xs uppercase tracking-wider">Platform & Architecture</div>
          <ul className="space-y-1.5 text-xs text-slate-400">
            <li>
              <Link href="/about" className="hover:text-white transition-colors flex items-center gap-1.5">
                <span>About & 8-Agent Topology</span>
              </Link>
            </li>
            <li>
              <Link href="/disclaimer" className="hover:text-white transition-colors flex items-center gap-1.5">
                <span>Sharia & Statutory Authorities</span>
              </Link>
            </li>
            <li>
              <Link href="/#tree" className="hover:text-white transition-colors">
                Shajra Nasab Reconstruction
              </Link>
            </li>
            <li>
              <Link href="/#docs" className="hover:text-white transition-colors">
                PLRA Mutation Forensic Audit
              </Link>
            </li>
          </ul>
        </div>

        {/* Legal & Compliance */}
        <div className="space-y-2.5">
          <div className="font-bold text-white text-xs uppercase tracking-wider">Compliance & Ethics</div>
          <ul className="space-y-1.5 text-xs text-slate-400">
            <li>
              <Link href="/privacy" className="hover:text-white transition-colors">
                Privacy Policy & Client Data
              </Link>
            </li>
            <li>
              <Link href="/terms" className="hover:text-white transition-colors">
                Terms of Service & Usage
              </Link>
            </li>
            <li>
              <Link href="/disclaimer" className="hover:text-white transition-colors">
                PPC 498A Criminal Penalties
              </Link>
            </li>
            <li>
              <span className="text-slate-500 text-[11px] block mt-2">
                High Court Advocate Review Recommended
              </span>
            </li>
          </ul>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-primary-900/80 px-6 py-4">
        <div className="max-w-[1700px] mx-auto flex flex-col sm:flex-row items-center justify-between gap-2 text-[11px] text-slate-500">
          <div>
            © {new Date().getFullYear()} HaqDar. Built for the HEC × PakAngels National AI Hackathon.
          </div>
          <div className="flex items-center gap-4">
            <Link href="/privacy" className="hover:text-slate-300">Privacy</Link>
            <span>•</span>
            <Link href="/terms" className="hover:text-slate-300">Terms</Link>
            <span>•</span>
            <Link href="/disclaimer" className="hover:text-slate-300">Disclaimer</Link>
            <span>•</span>
            <Link href="/about" className="hover:text-slate-300">About</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
