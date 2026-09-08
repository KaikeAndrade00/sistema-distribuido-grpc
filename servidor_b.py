from concurrent import futures
import uuid
import grpc

import agendamento_pb2
import agendamento_pb2_grpc

class AgendaService(agendamento_pb2_grpc.AgendaServiceServicer):
    def __init__(self):
        # Dicionário ou set em memória para armazenar compromissos marcados
        # Formato da chave: "medico_id:data_hora"
        self.horarios_ocupados = set()

    def CriarAgendamento(self, request, context):
        chave_horario = f"{request.medico_id}:{request.data_hora}"
        print(f"\n[SERVIDOR B] >>> Requisição recebida:")
        print(f"  - Paciente: {request.usuario_id}")
        print(f"  - Médico: {request.medico_id} ({request.especialidade})")
        print(f"  - Horário: {request.data_hora}")

        # Validação de conflito de agenda
        if chave_horario in self.horarios_ocupados:
            print("[SERVIDOR B] [RECUSADO] Horário indisponível!")
            return agendamento_pb2.AgendamentoResponse(
                sucesso=False,
                agendamento_id="",
                mensagem=f"O médico {request.medico_id} já possui agendamento em {request.data_hora}."
            )

        # Confirmar reserva
        self.horarios_ocupados.add(chave_horario)
        id_gerado = str(uuid.uuid4())
        print(f"[SERVIDOR B] [APROVADO] Agendamento criado com ID: {id_gerado}")

        return agendamento_pb2.AgendamentoResponse(
            sucesso=True,
            agendamento_id=id_gerado,
            mensagem="Agendamento confirmado com sucesso!"
        )

def serve():
    # Inicializa o servidor com pool de threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    agendamento_pb2_grpc.add_AgendaServiceServicer_to_server(AgendaService(), server)
    
    # Escuta em 0.0.0.0 (todas as interfaces) na porta 50051
    server.add_insecure_port("[::]:50051")
    print("=====================================================")
    print(">>> Servidor gRPC (Microsserviço B) ATIVO na porta 50051")
    print(">>> Aguardando requisições RPC...")
    print("=====================================================")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
