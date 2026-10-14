# Arquivo: api.py
import time
from fastapi import FastAPI, Request
from datetime import datetime
import random

app = FastAPI(title="Forzy Sensor API")

# Banco de dados em memória para os logs de observabilidade e dados do sensor
logs_observabilidade = []

historico_mock = [
    {"timestamp": "2026-10-14T10:00:00", "valor": 45.2, "status": "Normal"},
    {"timestamp": "2026-10-14T10:05:00", "valor": 46.1, "status": "Normal"},
    {"timestamp": "2026-10-14T10:10:00", "valor": 55.4, "status": "Alerta"},
]

# MIDDLEWARE DE OBSERVABILIDADE
@app.middleware("http")
async def registrar_observabilidade(request: Request, call_next):
    start_time = time.time()
    
    # Processa a requisição
    response = await call_next(request)
    
    # Calcula a latência em milissegundos
    process_time = (time.time() - start_time) * 1000
    
    # Captura os headers exigidos pelo Front-end/Governança
    session_id = request.headers.get("X-Session-Id", "N/A")
    feature = request.headers.get("X-Feature", "N/A")
    
    # Só registra rotas da nossa API (ignora rotas internas do FastAPI como /docs)
    if "/v1/" in request.url.path:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "endpoint": request.url.path,
            "metodo": request.method,
            "session_id": session_id,
            "feature": feature,
            "latencia_ms": round(process_time, 2),
            "status_code": response.status_code
        }
        logs_observabilidade.append(log_entry)
        
    return response

# ENDPOINTS
@app.get("/v1/sensores/{tag}/leitura-atual")
def get_leitura_atual(tag: str):
    # Simula um atraso aleatório para teste de latência
    time.sleep(random.uniform(0.1, 0.5))
    return {
        "tag": tag,
        "leitura": round(random.uniform(40.0, 60.0), 2),
        "severidade": "Normal" if random.random() > 0.2 else "Alerta"
    }

@app.get("/v1/sensores/{tag}/historico")
def get_historico(tag: str):
    time.sleep(random.uniform(0.2, 0.6))
    return {"tag": tag, "historico": historico_mock}

@app.get("/v1/observabilidade")
def get_observabilidade():
    return {"total_registros": len(logs_observabilidade), "logs": logs_observabilidade}