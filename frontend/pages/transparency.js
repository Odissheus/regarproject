import { useState, useEffect } from 'react';

export default function Transparency() {
  const [liste, setListe] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const res = await fetch('https://regar-backend.onrender.com/prezzi-rimborso');
      const data = await res.json();
      setListe(data);
    }
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6">Liste di Trasparenza</h1>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full">
          <thead>
            <tr className="bg-gray-50">
              <th className="px-6 py-3 text-left">Principio Attivo</th>
              <th className="px-6 py-3 text-left">Nome Commerciale</th>
              <th className="px-6 py-3 text-left">Prezzo</th>
              <th className="px-6 py-3 text-left">Data Aggiornamento</th>
            </tr>
          </thead>
          <tbody>
            {liste.map((lista) => (
              <tr key={lista.id} className="border-t border-gray-200">
                <td className="px-6 py-4">{lista.principio_attivo}</td>
                <td className="px-6 py-4">{lista.nome_commerciale}</td>
                <td className="px-6 py-4">€{lista.prezzo}</td>
                <td className="px-6 py-4">{lista.data_aggiornamento}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}