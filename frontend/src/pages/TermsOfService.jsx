import React from "react";
import { useNavigate } from "react-router-dom";

export default function TermsOfService() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 px-6 py-10">
      <div className="max-w-4xl mx-auto">
        <button onClick={() => navigate(-1)} className="text-slate-300 hover:text-white transition mb-6">
          ← Back
        </button>

        <h1 className="text-4xl font-extrabold">Terms of Service</h1>
        <p className="text-slate-400 mt-3">
          By using NyayaVanni, you agree to the terms below.
        </p>

        <div className="mt-8 space-y-6 text-slate-300 leading-relaxed">
          <section>
            <h2 className="text-xl font-bold text-white">1. Not Legal Advice</h2>
            <p className="mt-2">NyayaVanni provides simplified explanations. Always consult a qualified lawyer for legal decisions.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-white">2. User Responsibilities</h2>
            <p className="mt-2">You are responsible for the documents you upload and ensuring you have rights to share them.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-white">3. Service Availability</h2>
            <p className="mt-2">The service may be updated, paused, or changed without prior notice.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-white">4. Contact</h2>
            <p className="mt-2">Email: <span className="text-nyaya-400">support@nyayavanni.com</span></p>
          </section>
        </div>
      </div>
    </div>
  );
}