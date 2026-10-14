# Forzy Digital Twin - Sensor Monitoring API

Checkpoint integrado entre as disciplinas de Front-end e Governança em IA.

## 👥 Integrantes do Grupo
* RM 564202 - Luccas Verdelli do Nascimento Alvarenga Veronezi
* RM 563286 - Rickelmy Omine
* RM 564537 - Roberto Eduardo
* RM 562316 - Geandro Dezordi 
* RM 562370 - Davi Barboza

## 🏗️ Arquitetura do Projeto
O projeto é dividido em duas camadas:
1. **Back-end (FastAPI):** Expõe os endpoints de leitura atual, histórico e observabilidade do provider de Sensores. Possui um middleware que intercepta as requisições, calculando a latência e registrando os headers de contexto (`X-Session-Id` e `X-Feature`).
2. **Front-end (Streamlit):** Interface gráfica que consome a API utilizando a biblioteca `requests`, enviando os metadados de governança em todas as interações.
