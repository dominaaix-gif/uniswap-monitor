#!/usr/bin/env python3
print("🚀 Script iniciado")

try:
    import requests
    print("✅ requests importado")
    import time
    print("✅ time importado")
    from datetime import datetime
    print("✅ datetime importado")
    import re
    print("✅ re importado")
    import os
    print("✅ os importado")
    
    from selenium import webdriver
    print("✅ selenium webdriver importado")
    from selenium.webdriver.chrome.options import Options
    print("✅ chrome options importado")
    from selenium.webdriver.chrome.service import Service
    print("✅ chrome service importado")
    from webdriver_manager.chrome import ChromeDriverManager
    print("✅ webdriver_manager importado")
    
except ImportError as e:
    print(f"❌ Erro de import: {e}")
    exit(1)

print("📊 Verificando variáveis de ambiente...")
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_IDS = [os.environ.get('CHAT_ID1'), os.environ.get('CHAT_ID2')]
print(f"BOT_TOKEN presente: {'✅' if BOT_TOKEN else '❌'}")
print(f"CHAT_IDS: {CHAT_IDS}")

UNISWAP_URL = "https://app.uniswap.org/positions/v3/ethereum/1091548"
print(f"URL: {UNISWAP_URL}")

def send_telegram_message(message):
    try:
        print(f"📱 Enviando mensagem: {message[:50]}...")
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        for chat_id in CHAT_IDS:
            data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
            response = requests.post(url, json=data, timeout=10)
            print(f"Telegram response: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Erro Telegram: {e}")
        return False

def setup_driver():
    try:
        print("🔧 Configurando Chrome...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        print("✅ Chrome options configuradas")
        
        print("📥 Baixando ChromeDriver...")
        service = Service(ChromeDriverManager().install())
        print("✅ ChromeDriver baixado")
        
        print("🚀 Iniciando Chrome...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ Chrome iniciado com sucesso")
        return driver
    except Exception as e:
        print(f"❌ Erro no setup_driver: {e}")
        return None

print("🎯 Iniciando execução principal...")
driver = setup_driver()

if driver:
    print("✅ Driver criado com sucesso")
    try:
        print("🌐 Acessando Uniswap...")
        driver.get(UNISWAP_URL)
        print("⏳ Aguardando página carregar...")
        time.sleep(10)
        
        page_source = driver.page_source
        print(f"📄 Página carregada: {len(page_source)} caracteres")
        
        # Teste simples de encontrar valores
        if "$" in page_source:
            print("✅ Símbolo $ encontrado na página")
        else:
            print("❌ Símbolo $ NÃO encontrado")
            
        # Enviar resultado básico
        message = f"🔧 <b>Debug Nova Pool 1091548</b>\n\nPágina carregou: {len(page_source)} chars\nContém $: {'Sim' if '$' in page_source else 'Não'}"
        send_telegram_message(message)
        
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        send_telegram_message(f"🚨 Erro: {str(e)}")
    finally:
        print("🔒 Fechando driver...")
        driver.quit()
        print("✅ Driver fechado")
else:
    print("❌ Falha ao criar driver")
    send_telegram_message("🚨 Falha ao criar Chrome driver")

print("🏁 Script finalizado")
