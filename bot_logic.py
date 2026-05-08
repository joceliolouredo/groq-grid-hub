import os
import json
from groq import Groq
from dotenv import load_dotenv
import requests
import time

load_dotenv()

class TradingBot:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.pionex_key = os.getenv("PIONEX_API_KEY")
        self.pionex_secret = os.getenv("PIONEX_API_SECRET")
        self.config = self.load_config()

    def load_config(self):
        with open('config.json', 'r') as f:
            return json.load(f)

    def save_config(self, new_config):
        self.config = new_config
        with open('config.json', 'w') as f:
            json.dump(new_config, f, indent=4)

    def get_ai_suggestion(self):
        """Usa a Groq para analisar o mercado e sugerir a grade"""
        try:
            prompt = f"O par atual é {self.config['symbol']}. Analise a tendência de curto prazo e sugira um limite superior e inferior para um Grid Trading. Responda apenas em formato JSON: {{'upper': valor, 'lower': valor, 'reason': 'motivo'}}"
            
            completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-70b-8192",
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Erro AI: {e}"

    def execute_pionex_trade(self, side, amount, price):
        """Simulação de execução na Pionex (Substitua pelas chamadas reais da API Pionex)"""
        # Aqui você usaria requests.post para a API da Pionex com assinatura HMAC
        print(f"Executando {side} de {amount} no preço {price} via Pionex...")
        return True

    def check_health(self):
        """Verifica se as chaves de API estão funcionando"""
        health = {"pionex": "🔴", "groq": "🔴"}
        try:
            # Testa Groq
            self.groq_client.models.list()
            health["groq"] = "🟢"
        except: pass
        
        try:
            # Testa Pionex (Simulado: verifique se a chave existe)
            if self.pionex_key and self.pionex_secret:
                health["pionex"] = "🟢"
        except: pass
        
        return health
