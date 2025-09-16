#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from main import SistemaSimulacaoInvestimentos, TipoTaxa

class SimuladorGUI:
    def __init__(self):
        self.sistema = SistemaSimulacaoInvestimentos()
        self.simulacao_atual = None

        # Janela principal
        self.root = Tk()
        self.root.title("Sistema de Simulação de Investimentos")
        self.root.geometry("1000x750")
        self.root.configure(bg='white')

        self.criar_interface()

    def criar_interface(self):
        # Frame principal
        main_frame = Frame(self.root, bg='white', padx=30, pady=20)
        main_frame.pack(fill=BOTH, expand=True)

        # Título
        title_label = Label(main_frame, text="Sistema de Simulação de Investimentos",
                           font=('Arial', 20, 'bold'), bg='white', fg='black')
        title_label.pack(pady=(0, 30))

        # Frame de entrada
        input_frame = LabelFrame(main_frame, text="Nova Simulação",
                                font=('Arial', 14, 'bold'), bg='white', fg='black',
                                padx=30, pady=20, relief=RIDGE, bd=2)
        input_frame.pack(fill=X, pady=(0, 20))

        # Grade de campos
        Label(input_frame, text="Nome:", font=('Arial', 12, 'bold'), bg='white', fg='black').grid(row=0, column=0, sticky=W, pady=8)
        self.entry_nome = Entry(input_frame, font=('Arial', 12), width=50, bg='lightyellow', fg='black', bd=2, relief=SOLID)
        self.entry_nome.grid(row=0, column=1, pady=8, padx=(20, 0), sticky=W+E)

        Label(input_frame, text="Aporte Inicial (R$):", font=('Arial', 12, 'bold'), bg='white', fg='black').grid(row=1, column=0, sticky=W, pady=8)
        self.entry_aporte_inicial = Entry(input_frame, font=('Arial', 12), width=25, bg='lightyellow', fg='black', bd=2, relief=SOLID)
        self.entry_aporte_inicial.grid(row=1, column=1, pady=8, padx=(20, 0), sticky=W)

        Label(input_frame, text="Aporte Mensal (R$):", font=('Arial', 12, 'bold'), bg='white', fg='black').grid(row=2, column=0, sticky=W, pady=8)
        self.entry_aporte_mensal = Entry(input_frame, font=('Arial', 12), width=25, bg='lightyellow', fg='black', bd=2, relief=SOLID)
        self.entry_aporte_mensal.grid(row=2, column=1, pady=8, padx=(20, 0), sticky=W)

        Label(input_frame, text="Prazo (meses):", font=('Arial', 12, 'bold'), bg='white', fg='black').grid(row=3, column=0, sticky=W, pady=8)
        self.entry_prazo = Entry(input_frame, font=('Arial', 12), width=20, bg='lightyellow', fg='black', bd=2, relief=SOLID)
        self.entry_prazo.grid(row=3, column=1, pady=8, padx=(20, 0), sticky=W)

        Label(input_frame, text="Taxa Mensal (%):", font=('Arial', 12, 'bold'), bg='white', fg='black').grid(row=4, column=0, sticky=W, pady=8)
        self.entry_taxa = Entry(input_frame, font=('Arial', 12), width=20, bg='lightyellow', fg='black', bd=2, relief=SOLID)
        self.entry_taxa.grid(row=4, column=1, pady=8, padx=(20, 0), sticky=W)

        # Configurar expansão da coluna
        input_frame.columnconfigure(1, weight=1)

        # Frame de botões
        button_frame = Frame(main_frame, bg='white')
        button_frame.pack(pady=20)

        Button(button_frame, text="CALCULAR", command=self.calcular_simulacao,
               bg='green', fg='black', font=('Arial', 12, 'bold'),
               padx=30, pady=12, cursor='hand2', relief=RAISED, bd=3).pack(side=LEFT, padx=8)

        Button(button_frame, text="LIMPAR", command=self.limpar_campos,
               bg='orange', fg='black', font=('Arial', 12, 'bold'),
               padx=30, pady=12, cursor='hand2', relief=RAISED, bd=3).pack(side=LEFT, padx=8)


        # Frame de resultados
        result_frame = LabelFrame(main_frame, text="Resultados",
                                 font=('Arial', 14, 'bold'), bg='white', fg='black',
                                 padx=20, pady=15, relief=RIDGE, bd=2)
        result_frame.pack(fill=BOTH, expand=True, pady=(20, 0))

        # Área de texto com scrollbar
        text_frame = Frame(result_frame, bg='white')
        text_frame.pack(fill=BOTH, expand=True)

        self.text_resultados = Text(text_frame, font=('Courier New', 11),
                                   bg='black', fg='lime',
                                   wrap=WORD, padx=15, pady=15, bd=2, relief=SUNKEN)

        scrollbar = Scrollbar(text_frame, orient=VERTICAL, command=self.text_resultados.yview,
                             bg='gray', relief=RAISED, bd=2)
        self.text_resultados.configure(yscrollcommand=scrollbar.set)

        self.text_resultados.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Mensagem inicial
        self.text_resultados.insert(END, "=== SISTEMA DE SIMULAÇÃO DE INVESTIMENTOS ===\n\n")
        self.text_resultados.insert(END, "INSTRUÇÕES:\n")
        self.text_resultados.insert(END, "1. Preencha todos os campos acima\n")
        self.text_resultados.insert(END, "2. Clique em CALCULAR para simular\n")
        self.text_resultados.insert(END, "3. Analise os resultados\n\n")
        self.text_resultados.insert(END, "FUNCIONALIDADES:\n")
        self.text_resultados.insert(END, "• CALCULAR: Simula o investimento\n")
        self.text_resultados.insert(END, "• LIMPAR: Apaga todos os campos\n")
        self.text_resultados.insert(END, "Pronto para começar!\n")

    def limpar_campos(self):
        """Limpa todos os campos"""
        self.entry_nome.delete(0, END)
        self.entry_aporte_inicial.delete(0, END)
        self.entry_aporte_mensal.delete(0, END)
        self.entry_prazo.delete(0, END)
        self.entry_taxa.delete(0, END)
        self.text_resultados.delete(1.0, END)
        self.simulacao_atual = None

        # Mensagem inicial
        self.text_resultados.insert(END, "CAMPOS LIMPOS!\n\n")
        self.text_resultados.insert(END, "Sistema pronto para nova simulação.\n")
        self.text_resultados.insert(END, "Preencha os campos e clique CALCULAR.\n")

    def validar_campos(self):
        """Valida e retorna os dados dos campos"""
        try:
            nome = self.entry_nome.get().strip()
            if not nome:
                raise ValueError("Nome é obrigatório!")

            aporte_inicial = float(self.entry_aporte_inicial.get())
            if aporte_inicial <= 0:
                raise ValueError("Aporte inicial deve ser maior que zero!")

            aporte_mensal = float(self.entry_aporte_mensal.get()) if self.entry_aporte_mensal.get() else 0.0
            if aporte_mensal < 0:
                raise ValueError("Aporte mensal não pode ser negativo!")

            prazo = int(self.entry_prazo.get())
            if prazo < 1 or prazo > 360:
                raise ValueError("Prazo deve estar entre 1 e 360 meses!")

            taxa = float(self.entry_taxa.get())
            if taxa < 0 or taxa > 100:
                raise ValueError("Taxa deve estar entre 0% e 100%!")

            return nome, aporte_inicial, aporte_mensal, prazo, taxa

        except ValueError as e:
            raise e

    def calcular_simulacao(self):
        """Calcula a simulação"""
        try:
            # Validar campos
            nome, aporte_inicial, aporte_mensal, prazo, taxa = self.validar_campos()

            # Criar simulação
            id_sim = self.sistema.criar_simulacao(nome)

            # Configurar parâmetros
            sucesso, erros = self.sistema.configurar_simulacao(
                id_sim,
                aporte_inicial=aporte_inicial,
                aporte_mensal=aporte_mensal,
                prazo_meses=prazo,
                tipo_taxa=TipoTaxa.FIXA,
                taxa_fixa=taxa
            )

            if not sucesso:
                messagebox.showerror("ERRO NA CONFIGURAÇÃO", "\n".join(erros))
                return

            # Calcular
            sucesso, erros = self.sistema.calcular_simulacao(id_sim)
            if not sucesso:
                messagebox.showerror("ERRO NO CÁLCULO", "\n".join(erros))
                return

            # Obter e exibir resultados
            resultados = self.sistema.obter_resultados(id_sim)
            if resultados:
                self.simulacao_atual = id_sim
                self.exibir_resultados(nome, resultados, aporte_inicial, aporte_mensal, prazo, taxa)
                messagebox.showinfo("SUCESSO", "Simulação calculada com sucesso!")
            else:
                messagebox.showerror("ERRO", "Falha ao obter resultados da simulação")

        except ValueError as e:
            messagebox.showerror("ERRO DE VALIDAÇÃO", str(e))
        except Exception as e:
            messagebox.showerror("ERRO INESPERADO", f"Erro: {str(e)}")

    def exibir_resultados(self, nome, resultados, aporte_inicial=0, aporte_mensal=0, prazo=0, taxa=0):
        """Exibe os resultados na área de texto"""
        self.text_resultados.delete(1.0, END)

        metricas = resultados['metricas_finais']

        # Cabeçalho
        texto = "=" * 70 + "\n"
        texto += f"RESULTADO DA SIMULAÇÃO: {nome.upper()}\n"
        texto += "=" * 70 + "\n\n"

        # Resumo financeiro
        texto += "RESUMO FINANCEIRO:\n"
        texto += "-" * 30 + "\n"
        texto += f"Saldo Final:       R$ {metricas['saldo_final']:>18,.2f}\n"
        texto += f"Total Investido:   R$ {metricas['total_investido']:>18,.2f}\n"
        texto += f"Total de Juros:    R$ {metricas['juros_acumulados']:>18,.2f}\n"
        texto += f"Rentabilidade:        {metricas['rentabilidade_total']:>18.2f}%\n\n"

        # Parâmetros
        texto += "PARÂMETROS UTILIZADOS:\n"
        texto += "-" * 25 + "\n"
        texto += f"Aporte Inicial:    R$ {aporte_inicial:>18,.2f}\n"
        texto += f"Aporte Mensal:     R$ {aporte_mensal:>18,.2f}\n"
        texto += f"Prazo:                {prazo:>18} meses\n"
        texto += f"Taxa Mensal:          {taxa:>18.2f}%\n\n"

        # Detalhes dos últimos meses
        texto += "EVOLUÇÃO DOS ÚLTIMOS 15 MESES:\n"
        texto += "-" * 45 + "\n"
        texto += f"{'Mês':>4} | {'Aporte':>12} | {'Saldo Final':>18}\n"
        texto += "-" * 45 + "\n"

        for resultado in resultados['resultados_mensais'][-15:]:
            texto += f"{resultado['mes']:>4} | R$ {resultado['aporte_mes']:>8,.2f} | R$ {resultado['saldo_final']:>14,.2f}\n"

        # Informações adicionais
        texto += "\n" + "=" * 70 + "\n"
        texto += f"Simulação completa com {len(resultados['resultados_mensais'])} meses.\n"
        texto += "Simulação calculada com sucesso!\n"
        texto += "=" * 70 + "\n"

        self.text_resultados.insert(1.0, texto)


    def executar(self):
        """Executa a aplicação"""
        self.root.mainloop()

if __name__ == '__main__':
    app = SimuladorGUI()
    app.executar()