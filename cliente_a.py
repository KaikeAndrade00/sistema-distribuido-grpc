import sys
import grpc

import agendamento_pb2
import agendamento_pb2_grpc

def testar_agendamento(server_ip, usuario, medico, data_hora, especialidade):
    endereco = f"{server_ip}:50051"
    print(f"\n[CLIENTE A] Conectando via gRPC em: {endereco}...")

    with grpc.insecure_channel(endereco) as channel:
        stub = agendamento_pb2_grpc.AgendaServiceStub(channel)

        req = agendamento_pb2.AgendamentoRequest(
            usuario_id=usuario,
            medico_id=medico,
            data_hora=data_hora,
            especialidade=especialidade
        )

        try:
            resposta = stub.CriarAgendamento(req)
            print("[CLIENTE A] Resposta recebida com sucesso:")
            print(f"  - Status Sucesso: {resposta.sucesso}")
            print(f"  - ID do Agendamento: {resposta.agendamento_id}")
            print(f"  - Mensagem do Servidor: {resposta.mensagem}")
        except grpc.RpcError as e:
            print(f"[CLIENTE A] Erro de comunicação gRPC: {e.code()} - {e.details()}")

if __name__ == "__main__":
    # Se passar um IP no terminal (ex: python3 cliente_a.py 34.x.x.x), usa ele. Senão, usa localhost.
    alvo = sys.argv[1] if len(sys.argv) > 1 else "localhost"

    print("=====================================================")
    print(f"Iniciando testes com destino: {alvo}")
    print("=====================================================")

    print("\n--- CASO 1: Agendamento inicial válido ---")
    testar_agendamento(
        server_ip=alvo,
        usuario="paciente-joao-01",
        medico="dr-carlos-10",
        data_hora="2026-11-20T10:00:00Z",
        especialidade="Cardiologia"
    )

    print("\n--- CASO 2: Tentativa de agendamento no MESMO horário (deve ser recusado) ---")
    testar_agendamento(
        server_ip=alvo,
        usuario="paciente-maria-02",
        medico="dr-carlos-10",
        data_hora="2026-11-20T10:00:00Z",
        especialidade="Cardiologia"
    )
