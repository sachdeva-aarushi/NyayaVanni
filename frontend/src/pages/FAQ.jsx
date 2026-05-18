import React from "react";
import { useNavigate } from "react-router-dom";

export default function FAQ() {
  const navigate = useNavigate();

  const faqs = [
    { q: "What file formats are supported?", a: "PDF, PNG, and JPG are supported." },
    { q: "Is NyayaVanni legal advice?", a: "No. It provides simplified explanations. Consult a lawyer for critical decisions." },
    { q: "How does it work?", a: "We extract text and use AI to summarize, detect risks, and answer questions." },
    { q: "Is my data secure?", a: "We follow standard security practices, but no system is fully risk-free." },
  ];

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 px-6 py-10">
      <div className="max-w-4xl mx-auto">
        <button onClick={() => navigate(-1)} className="text-slate-300 hover:text-white transition mb-6">
          ← Back
        </button>

        <h1 className="text-4xl font-extrabold">FAQ</h1>
        <p className="text-slate-400 mt-3">Common questions about NyayaVanni.</p>

        <div className="mt-8 space-y-4">
          {faqs.map((item, idx) => (
            <details key={idx} className="rounded-xl border border-slate-700/50 bg-slate-950/40 p-5">
              <summary className="cursor-pointer list-none flex items-center justify-between gap-4">
                <span className="font-semibold text-white">{item.q}</span>
                <span className="text-slate-400">+</span>
              </summary>
              <p className="mt-3 text-slate-400 leading-relaxed">{item.a}</p>
            </details>
          ))}
        </div>
      </div>
    </div>
  );
}