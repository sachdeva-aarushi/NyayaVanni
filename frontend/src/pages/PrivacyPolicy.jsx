import React from "react";
import { useNavigate } from "react-router-dom";

export default function PrivacyPolicy() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 px-6 py-10">
      <div className="max-w-4xl mx-auto">
        <button onClick={() => navigate(-1)} className="text-slate-300 hover:text-white transition mb-6">
          ← Back
        </button>

        <h1 className="text-4xl font-extrabold">Privacy Policy</h1>
        <p className="text-slate-400 mt-3">
          This page explains how NyayaVanni handles uploaded documents and user data.
        </p>

        <div className="mt-8 space-y-6 text-slate-300 leading-relaxed">
          <section>
            <h2 className="text-xl font-bold text-white">1. Data We Process</h2>
            <p className="mt-2">Uploaded documents and chat prompts are used to generate summaries and responses.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-white">2. Storage</h2>
            <p className="mt-2">Depending on configuration, documents may be processed temporarily or stored for history features.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-white">3. Security</h2>
            <p className="mt-2">We use standard security practices, but no system is 100% secure.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-white">4. Contact</h2>
            <p className="mt-2">Questions? Email: <span className="text-nyaya-400">support@nyayavanni.com</span></p>
          </section>
        </div>
      </div>
    </div>
  );
}