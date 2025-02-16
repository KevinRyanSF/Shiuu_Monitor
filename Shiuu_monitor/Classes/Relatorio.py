from datetime import datetime
from fpdf import FPDF


class Relatorio:
    def __init__(self):
        from FacadeSingleton.FacadeSingletonManager import FacadeManager
        self.__facade = FacadeManager()

    def gerar_historico(self):
        # Solicita as datas ao usuário
        data_init = input("Digite a data inicial (Ex.: dd-mm-yyyy): ")
        data_end = input("Digite a data final (Ex.: dd-mm-yyyy): ")

        # Converte as datas para datetime.date
        try:
            data_init = datetime.strptime(data_init, "%d-%m-%Y").date()
            data_end = datetime.strptime(data_end, "%d-%m-%Y").date()
        except ValueError:
            print("Formato de data inválido. Use dd-mm-yyyy.")
            return

        # Busca todas as medições no banco de dados
        medicoes = self.__facade.db.fetch_all("medicoes")

        # Ordena medições por ambiente
        sorted_medicoes = sorted(medicoes, key=lambda amb: amb["nome_ambiente"])

        # Dicionário para agrupar medições por ambiente
        ambientes_relatorio = {}

        for medicao in sorted_medicoes:
            # Converte o campo 'data' (ISO 8601) para datetime
            try:
                timestamp_dt = datetime.fromisoformat(medicao["data"])  # Use fromisoformat() para string ISO 8601
            except ValueError as e:
                print(f"Erro ao converter timestamp: {e}")
                continue

            timestamp_data = timestamp_dt.date()  # Apenas a data para filtro
            timestamp_hora = timestamp_dt.strftime("%H:%M:%S")  # Apenas a hora para exibir

            # Filtra medições dentro do intervalo de datas
            if data_init <= timestamp_data <= data_end:
                ambiente_nome = medicao["nome_ambiente"]
                registro = f"{timestamp_data.strftime('%d/%m/%Y')} {timestamp_hora} - Valor: {medicao['valor']}dB"

                if ambiente_nome not in ambientes_relatorio:
                    ambientes_relatorio[ambiente_nome] = []

                ambientes_relatorio[ambiente_nome].append(registro)

        # Exibe o relatório formatado
        if not ambientes_relatorio:
            print("Nenhuma medição encontrada no período especificado.")
            return

        print("\n=== RELATÓRIO DE MEDIÇÕES ===")
        for ambiente, registros in ambientes_relatorio.items():
            print(f"\n🔹 Ambiente: {ambiente}")
            for registro in registros:
                print(registro)

        while True:
            pdf = input("Deseja gerar pdf? [y/n]: ").lower()
            if pdf == "y":
                break
            elif pdf == "n":
                return 0
            else:
                print("Digite uma opção válida.")

        # Verifica se há dados para gerar o relatório
        if not ambientes_relatorio:
            print("Nenhuma medição encontrada no período especificado.")
            return

        # Criando o PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)

        # Título do documento
        pdf.cell(200, 10, "Relatório de Medições", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, f"Período: {data_init.strftime('%d/%m/%Y')} a {data_end.strftime('%d/%m/%Y')}", ln=True,
                 align="C")
        pdf.ln(10)

        # Adicionando os dados ao PDF
        for ambiente, registros in ambientes_relatorio.items():
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, f"Ambiente: {ambiente}", ln=True)
            pdf.ln(5)

            pdf.set_font("Arial", "", 12)
            for registro in registros:
                pdf.multi_cell(0, 8, registro)
            pdf.ln(10)

        # Salvar PDF
        nome_arquivo = f"relatorio_{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.pdf"
        pdf.output(nome_arquivo)

        print(f"Relatório gerado com sucesso: {nome_arquivo}")