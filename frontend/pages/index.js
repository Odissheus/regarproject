import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100">
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">RegAr.AI</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link href="/pricing">
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <h2 className="text-2xl font-semibold mb-4">Prezzi e Rimborsi</h2>
              <p>Consulta i prezzi e le informazioni sui rimborsi dei farmaci</p>
            </div>
          </Link>
          <Link href="/transparency">
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <h2 className="text-2xl font-semibold mb-4">Liste di Trasparenza</h2>
              <p>Accedi alle liste di trasparenza aggiornate</p>
            </div>
          </Link>
        </div>
      </main>
    </div>
  );
}