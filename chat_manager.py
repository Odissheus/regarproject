import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import sqlite3
from datetime import datetime

class ChatManager:
    def __init__(self, db_path='database.db'):
        self.tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-italian-xxl-uncased")
        self.model = AutoModelForQuestionAnswering.from_pretrained("dbmdz/bert-base-italian-xxl-uncased")
        self.db_path = db_path

    def get_context(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT principio_attivo, nome_commerciale, prezzo 
            FROM liste_trasparenza 
            ORDER BY data_aggiornamento DESC
        """)
        data = cursor.fetchall()
        conn.close()
        return "\n".join([f"{row[0]} - {row[1]}: €{row[2]}" for row in data])

    def get_response(self, query):
        try:
            context = self.get_context()
            inputs = self.tokenizer(query, context, return_tensors="pt")
            outputs = self.model(**inputs)
            
            answer_start = torch.argmax(outputs.start_logits)
            answer_end = torch.argmax(outputs.end_logits)
            
            answer = self.tokenizer.decode(inputs["input_ids"][0][answer_start:answer_end+1])
            
            self.log_chat(query, answer)
            return answer
        except Exception as e:
            print(f"Errore: {e}")
            return "Mi scusi, potrebbe riformulare la domanda?"

    def log_chat(self, query, response):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO chat_log (query, response, timestamp) 
            VALUES (?, ?, ?)
        """, (query, response, datetime.now()))
        conn.commit()
        conn.close()