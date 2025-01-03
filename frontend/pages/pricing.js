import { useState, useEffect } from 'react';

export default function Pricing() {
  const [prezzi, setPrezzi] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const res = await fetch('http://localhost:8000/prezzi-rimborso');
      const data = await res.json();
      setPrezzi(data);
    }
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6">Prezzi e Rimborsi</h1>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full">
          <thead>
            <tr className="bg-gray-50">
              <th className="px-6 py-3 text-left">Data</th>
              <th className="px-6 py-3 text-left">Titolo</th>
              <th className="px-6 py-3 text-left">Link</th>
            </tr>
          </thead>
          <tbody>
            {prezzi.map((prezzo) => (
              <tr key={prezzo.id} className="border-t border-gray-200">
                <td className="px-6 py-4">{prezzo.data}</td>
                <td className="px-6 py-4">{prezzo.titolo}</td>
                <td className="px-6 py-4">
                  <a href={prezzo.link} className="text-blue-600 hover:underline">
                    Dettagli
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}