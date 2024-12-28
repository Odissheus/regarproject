import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

export default function DashboardTrasparenza() {
  const [documentiRecenti, setDocumentiRecenti] = useState([]);
  const [queryChat, setQueryChat] = useState('');
  const [rispostaChat, setRispostaChat] = useState('');
  const [caricamento, setCaricamento] = useState(false);

  useEffect(() => {
    caricaDocumentiRecenti();
  }, []);

  const caricaDocumentiRecenti = async () => {
    try {
      const response = await fetch('/api/documenti-recenti');
      const data = await response.json();
      setDocumentiRecenti(data);
    } catch (error) {
      console.error('Errore caricamento documenti:', error);
    }
  };

  const inviaQuery = async () => {
    if (!queryChat.trim()) return;
    
    setCaricamento(true);
    try {
      const response = await fetch('/api/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: queryChat })
      });
      const data = await response.json();
      setRispostaChat(data.risposta);
    } catch (error) {
      console.error('Errore query chatbot:', error);
      setRispostaChat('Mi dispiace, si è verificato un errore. Riprova più tardi.');
    } finally {
      setCaricamento(false);
    }
  };

  return (
    <div className="p-4 max-w-6xl mx-auto">
      {/* Documenti Recenti */}
      <div className="mb-8 bg-white rounded-lg shadow p-4">
        <h2 className="text-xl font-bold mb-4">Documenti Correlati Recenti</h2>
        <div className="space-y-2">
          {documentiRecenti.map((doc, index) => (
            <div key={index} className="p-3 bg-gray-50 rounded">
              <p className="font-semibold">{doc.titolo}</p>
              <p className="text-sm text-gray-600">{doc.data}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Chatbot */}
      <div className="bg-white rounded-lg shadow p-4">
        <h2 className="text-xl font-bold mb-4">Assistente Liste di Trasparenza</h2>
        <div className="space-y-4">
          <div className="flex gap-2">
            <input
              type="text"
              value={queryChat}
              onChange={(e) => setQueryChat(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && inviaQuery()}
              placeholder="Fai una domanda sulle liste di trasparenza..."
              className="flex-1 p-2 border border-gray-300 rounded"
            />
            <button
              onClick={inviaQuery}
              disabled={caricamento}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-blue-300"
            >
              {caricamento ? 'Caricamento...' : 'Invia'}
            </button>
          </div>
          
          {rispostaChat && (
            <div className="p-4 bg-gray-50 rounded">
              <p className="whitespace-pre-line">{rispostaChat}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}