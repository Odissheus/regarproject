import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchNews() {
      try {
        const response = await fetch('https://regar-backend.onrender.com/aifa-news');
        const data = await response.json();
        setNews(data);
        setLoading(false);
      } catch (error) {
        console.error('Errore nel recupero delle news:', error);
        setLoading(false);
      }
    }
    
    fetchNews();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-blue-800">RegAr.AI</h1>
          <Link to="/chatbot" className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition duration-200">
            Accedi al Chatbot
          </Link>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <section>
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">Ultime News AIFA</h2>
          
          {loading ? (
            <div className="flex justify-center">
              <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
            </div>
          ) : news.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {news.map((item) => (
                <div key={item.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition duration-200">
                  <div className="p-6">
                    <p className="text-sm text-gray-500 mb-2">{new Date(item.date).toLocaleDateString('it-IT')}</p>
                    <h3 className="text-xl font-semibold mb-3 text-gray-800">{item.title}</h3>
                    <p className="text-gray-600 mb-4">{item.summary}</p>
                    <a 
                      href={item.link} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 font-medium"
                    >
                      Leggi di più →
                    </a>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-gray-600">Nessuna news disponibile al momento. Riprova più tardi.</p>
          )}
        </section>
      </main>
      
      <footer className="bg-gray-800 text-white py-8 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center">© 2025 RegAr.AI - Informazioni AIFA sempre aggiornate</p>
        </div>
      </footer>
    </div>
  );
}