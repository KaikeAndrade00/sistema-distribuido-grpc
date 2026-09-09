import sys
from datetime import datetime
import grpc

import agendamento_pb2
import agendamento_pb2_grpc

CATALOGO_MEDICOS = {
    "1": {"id": "dr-roberto-cardio", "nome": "Dr. Roberto Costa", "especialidade": "Cardiologia"},
    "2": {"id": "dra-juliana-dermato", "nome": "Dra. Juliana Mendes", "especialidade": "Dermatologia"},
    "3": {"id": "dr-alberto-oftalmo", "nome": "Dr. Alberto Ramos", "especialidade": "Oftalmologia"},
}

def obter_texto_obrigatorio(rotulo):
    while True:
        valor = input(rotulo).strip()
        if valor:
            return valor
        print("  [!] Este campo não pode ficar vazio. Tente novamente.")

def selecionar_medico():
    print("\n--- Selecione o Médico ---")
    for chave, dados in CATALOGO_MEDICOS.items():
        print(f"[{chave}] {dados['nome']} ({dados['especialidade']})")
    print("[4] Outro médico (digitação manual)")

    while True:
        opcao = input("Escolha uma opção (1-4): ").strip()
        if opcao in CATALOGO_MEDICOS:
            medico = CATALOGO_MEDICOS[opcao]
            return medico["id"], medico["especialidade"]
        elif opcao == "4":
            med_id = obter_texto_obrigatorio("Digite o ID do médico (ex: dr-carlos): ")
            esp = obter_texto_obrigatorio("Digite a especialidade: ")
            return med_id, esp
        print("  [!] Opção inválida. Escolha entre 1 e 4.")

def obter_data_hora():
    exemplo = "2026-11-20 14:30"
    while True:
        entrada = input(f"Data e Horário (AAAA-MM-DD HH:MM) [Ex: {exemplo}]: ").strip()
        try:
            dt = datetime.strptime(entrada, "%Y-%m-%d %H:%M")
            # Correção: segundos fixos em :00Z sem o caractere inválido %
            return dt.strftime("%Y-%m-%dT%H:%M:00Z")
        except ValueError:
            print("  [!] Formato inválido! Use exatamente o formato AAAA-MM-DD HH:MM.")

def solicitar_agendamento(stub, usuario, medico, data_hora, especialidade):
    req = agendamento_pb2.AgendamentoRequest(
        usuario_id=usuario,
        medico_id=medico,
        data_hora=data_hora,
        especialidade=especialidade
    )

    try:
        resposta = stub.CriarAgendamento(req)
        print("\n================ RESPOSTA gRPC ================")
        print(f"Status Sucesso : {resposta.sucesso}")
        print(f"ID Agendamento : {resposta.agendamento_id if resposta.agendamento_id else 'Nenhum'}")
        print(f"Mensagem       : {resposta.mensagem}")
        print("===============================================\n")
    except grpc.RpcError as e:
        print(f"\n[ERRO gRPC] Código: {e.code()} - {e.details()}\n")

def main():
    alvo = sys.argv[1] if len(sys.argv) > 1 else input("IP Externo da VM no GCP: ").strip()
    endereco = f"{alvo}:50051"

    print(f"\nEstabelecendo canal gRPC com: {endereco}")

    with grpc.insecure_channel(endereco) as channel:
        stub = agendamento_pb2_grpc.AgendaServiceStub(channel)

        while True:
            print("\n================ NOVO AGENDAMENTO ================")
            usuario = obter_texto_obrigatorio("Nome/ID do Paciente: ")
            medico_id, especialidade = selecionar_medico()
            data_hora = obter_data_hora()

            print(f"\n>> Enviando RPC para {medico_id} ({especialidade}) às {data_hora}...")
            solicitar_agendamento(stub, usuario, medico_id, data_hora, especialidade)

            opcao = input("Deseja realizar outro agendamento? (s/n): ").strip().lower()
            if opcao != 's':
                print("\nEncerrando cliente gRPC.")
                break

if __name__ == "__main__":
    main()
