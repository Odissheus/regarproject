import unittest
from src.transparency_manager import TransparencyManager
from test_chatbot import TransparencyListChatbot
import os
import sqlite3

class TestTransparencySystem(unittest.TestCase):
    def setUp(self):
        """Prepara l'ambiente di test"""
        print("\nPreparazione test...")
        self.manager = TransparencyManager()
        self.chatbot = TransparencyListChatbot()
        
    def test_1_download_list(self):
        """Testa il download della lista di trasparenza"""
        print("\nTest download lista...")
        pdf_path = self.manager.download_latest_list()
        self.assertIsNotNone(pdf_path)
        self.assertTrue(os.path.exists(pdf_path))
        print(f"Lista scaricata: {pdf_path}")
        
    def test_2_parse_and_save(self):
        """Testa il parsing e il salvataggio dei dati"""
        print("\nTest parsing e salvataggio...")
        changes = self.manager.update()
        self.assertIsNotNone(changes)
        
        # Verifica che i dati siano nel database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM liste_trasparenza")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertGreater(count, 0)
        print(f"Salvati {count} record nel database")
        
    def test_3_chatbot_queries(self):
        """Testa diverse query al chatbot"""
        print("\nTest queries chatbot...")
        test_queries = [
            "Qual è il prezzo del paracetamolo?",
            "Mostrami le ultime modifiche",
            "Dammi le statistiche generali",
        ]
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            response = self.chatbot.process_query(query)
            print(f"Risposta: {response}")
            self.assertIsNotNone(response)
            self.assertIsInstance(response, str)
            self.assertTrue(len(response) > 0)
            
    def test_4_recent_documents(self):
        """Testa il recupero dei documenti recenti"""
        print("\nTest documenti recenti...")
        documents = self.manager.get_recent_documents()
        self.assertIsNotNone(documents)
        self.assertIsInstance(documents, list)
        print(f"Trovati {len(documents)} documenti recenti")

def run_system_test():
    print("Avvio test completo del sistema...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTransparencySystem)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    run_system_test()