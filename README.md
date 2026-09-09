# Trabalho de Sistemas Distribuídos - Etapa 1

Comunicação gRPC interna entre dois microsserviços rodando na GCP.

- **Microsserviço A (Cliente):** `cliente_a.py`
- **Microsserviço B (Servidor):** `servidor_b.py`
- **Contrato Protobuf:** `agendamento.proto`

## Como Executar
1. `pip install -r requirements.txt`
2. `python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. agendamento.proto`
3. `python3 servidor_b.py`
4. `python3 cliente_a.py <IP_DO_SERVIDOR>`


### . Cliente A - Modo Interativo (CLI)
Permite entrada dinâmica de dados com validação de horário e catálogo de profissionais:
```bash
python cliente_interativo.py <IP_DO_SERVIDOR>`
