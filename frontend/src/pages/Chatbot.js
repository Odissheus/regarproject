import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';

export default function Chatbot() {
  const [messages, setMessages] = useState([
    { 
      type: 'bot', 
      content: `Ciao! Sono l'assistente virtuale di RegAr.AI, specializzato nel sito AIFA.
      
Come posso aiutarti?
      
Puoi chiedermi informazioni su:
- Ultime news e aggiornamenti AIFA
- Dove trovare specifici documenti o sezioni
- Farmaci equivalenti e prezzi
- Procedure di farmacovigilanza
- Normative e regolamenti`
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestedQuestions, setSuggestedQuestions] = useState([
    'Quali sono le ultime news di AIFA?',
    'Come posso trovare i farmaci equivalenti?',
    'Dove trovo informazioni sui prezzi dei farmaci?',
    'Come segnalare una reazione avversa?'
  ]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    
    // Aggiungi il messaggio dell'utente
    setMessages(prev => [...prev, { type: 'user', content: input }]);
    const userQuery = input;
    setInput('');
    setLoading(true);
    
    try {
      // Chiamata all'API del backend
      const response = await fetch('https://regar-backend.onrender.com/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userQuery }),
      });
      
      const data = await response.json();
      
      // Aggiungi la risposta del bot
      setMessages(prev => [...prev, { 
        type: 'bot', 
        content: data.response,
        links: data.links || [] // Collegamenti ipertestuali rilevanti
      }]);
      
      // Aggiorna suggerimenti basati sulla conversazione
      if (data.suggestions) {
        setSuggestedQuestions(data.suggestions);
      }
    } catch (error) {
      console.error('Errore nella richiesta al chatbot:', error);
      setMessages(prev => [...prev, { 
        type: 'bot', 
        content: 'Mi dispiace, si è verificato un errore. Puoi provare a riformulare la domanda o visitare direttamente il sito AIFA: https://www.aifa.gov.it/' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };
  
  const handleSuggestedQuestion = (question) => {
    setInput(question);
  };

  // Funzione per formattare i messaggi con link cliccabili
  const formatMessage = (content) => {
    // Cerca URL in formato markdown [testo](url)
    const markdownLinkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
    
    // Cerca URL semplici http:// o https://
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    
    // Prima sostituisci i link in formato markdown
    let formattedContent = content.replace(markdownLinkRegex, '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:underline">$1</a>');
    
    // Poi sostituisci gli URL semplici
    formattedContent = formattedContent.replace(urlRegex, (url) => {
      // Evita di sostituire URL già in tag <a>
      if (url.startsWith('https://') && !url.startsWith('https://<a')) {
        return `<a href="${url}" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:underline">${url}</a>`;
      }
      return url;
    });
    
    // Dividi in paragrafi
    const paragraphs = formattedContent.split('\n\n');
    
    return (
      <>
        {paragraphs.map((paragraph, idx) => (
          <p key={idx} className="mb-2" dangerouslySetInnerHTML={{ __html: paragraph }} />
        ))}
      </>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex flex-col">
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <Link to="/" className="text-3xl font-bold text-blue-800">RegAr.AI</Link>
          <span className="text-gray-600">Assistente AIFA</span>
        </div>
      </header>
      
      <main className="flex-1 max-w-5xl w-full mx-auto p-4 flex flex-col">
        <div className="bg-white rounded-lg shadow-lg flex-1 flex flex-col overflow-hidden border border-gray-200">
          <div className="p-4 bg-blue-700 text-white flex justify-between items-center">
            <h2 className="text-xl font-semibold">Assistente AIFA</h2>
            <span className="text-sm bg-blue-600 px-2 py-1 rounded">Powered by RegAr.AI</span>
          </div>
          
          <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
            <div className="space-y-4">
              {messages.map((msg, index) => (
                <div 
                  key={index} 
                  className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div 
                    className={`max-w-3/4 p-4 rounded-lg shadow-sm ${
                      msg.type === 'user' 
                        ? 'bg-blue-600 text-white rounded-br-none' 
                        : 'bg-white text-gray-800 rounded-bl-none border border-gray-200'
                    }`}
                  >
                    {msg.type === 'user' ? msg.content : formatMessage(msg.content)}
                    
                    {msg.links && msg.links.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-gray-200">
                        <p className="text-sm font-medium">Link utili:</p>
                        <ul className="list-disc pl-5 text-sm">
                          {msg.links.map((link, i) => (
                            <li key={i}>
                              <a 
                                href={link.url} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-blue-600 hover:underline"
                              >
                                {link.text}
                              </a>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="bg-white p-4 rounded-lg rounded-bl-none border border-gray-200 shadow-sm">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce delay-75"></div>
                      <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce delay-150"></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef}></div>
            </div>
          </div>
          
          {/* Domande suggerite */}
          {suggestedQuestions.length > 0 && (
            <div className="p-3 bg-gray-100 border-t border-gray-200">
              <p className="text-xs text-gray-500 mb-2">Domande suggerite:</p>
              <div className="flex flex-wrap gap-2">
                {suggestedQuestions.map((question, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSuggestedQuestion(question)}
                    className="bg-white text-blue-700 text-sm px-3 py-1 rounded-full border border-blue-300 hover:bg-blue-50 transition-colors duration-200"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}
          
          <div className="p-4 border-t border-gray-200 bg-white">
            <div className="flex space-x-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Scrivi un messaggio..."
                className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button 
                onClick={handleSend}
                disabled={loading || !input.trim()}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition duration-200 disabled:opacity-50"
              >
                Invia
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}