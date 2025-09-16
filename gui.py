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

        Button(button_frame, text="SALVAR JSON", command=self.salvar_json,
               bg='blue', fg='black', font=('Arial', 12, 'bold'),
               padx=25, pady=12, cursor='hand2', relief=RAISED, bd=3).pack(side=LEFT, padx=8)

        Button(button_frame, text="CARREGAR JSON", command=self.carregar_json,
               bg='purple', fg='black', font=('Arial', 12, 'bold'),
               padx=20, pady=12, cursor='hand2', relief=RAISED, bd=3).pack(side=LEFT, padx=8)


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
        self.text_resultados.insert(END, "• SALVAR JSON: Salva simulação em arquivo\n")
        self.text_resultados.insert(END, "• CARREGAR JSON: Carrega simulação salva\n")
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

    def salvar_json(self):
        """Salva simulação em JSON"""
        if not self.simulacao_atual:
            messagebox.showwarning("AVISO", "Nenhuma simulação calculada para salvar!")
            return

        arquivo = filedialog.asksaveasfilename(
            title="Salvar simulação como:",
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )

        if arquivo:
            try:
                sucesso, msg = self.sistema.salvar_simulacao(self.simulacao_atual, arquivo)
                if sucesso:
                    messagebox.showinfo("SUCESSO", f"Simulação salva com sucesso!\n\nArquivo: {arquivo}")
                else:
                    messagebox.showerror("ERRO", f"Falha ao salvar:\n{msg}")
            except Exception as e:
                messagebox.showerror("ERRO", f"Erro ao salvar:\n{str(e)}")

    def carregar_json(self):
        """Carrega simulação de JSON"""
        arquivo = filedialog.askopenfilename(
            title="Carregar simulação:",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )

        if arquivo:
            try:
                sucesso, resultado = self.sistema.carregar_simulacao(arquivo)
                if sucesso:
                    self.simulacao_atual = resultado

                    # Obter dados da simulação carregada
                    resultados = self.sistema.obter_resultados(self.simulacao_atual)
                    if resultados:
                        # Preencher campos da interface
                        simulacoes = self.sistema.listar_simulacoes()
                        sim_dados = next((s for s in simulacoes if s['id'] == self.simulacao_atual), None)

                        if sim_dados:
                            # Limpar campos primeiro SEM chamar limpar_campos() para não resetar a simulacao_atual
                            self.entry_nome.delete(0, END)
                            self.entry_aporte_inicial.delete(0, END)
                            self.entry_aporte_mensal.delete(0, END)
                            self.entry_prazo.delete(0, END)
                            self.entry_taxa.delete(0, END)

                            # Preencher com dados carregados
                            self.entry_nome.insert(0, sim_dados['nome'])

                            # Buscar dados da simulação no sistema
                            simulacao_obj = self.sistema.gerenciador.obter_simulacao(self.simulacao_atual)
                            if simulacao_obj:
                                # Debug - mostrar dados carregados
                                print(f"DEBUG - Dados carregados:")
                                print(f"ID: {simulacao_obj.id}")
                                print(f"Nome: {simulacao_obj.nome}")
                                print(f"Aporte inicial: {simulacao_obj.aporte_inicial}")
                                print(f"Aporte mensal: {simulacao_obj.aporte_mensal}")
                                print(f"Prazo: {simulacao_obj.prazo_meses}")
                                print(f"Taxa fixa: {simulacao_obj.taxa_fixa}")

                                self.entry_aporte_inicial.insert(0, str(simulacao_obj.aporte_inicial))

                                # Aporte mensal pode ser None
                                aporte_mensal = simulacao_obj.aporte_mensal if simulacao_obj.aporte_mensal is not None else 0
                                self.entry_aporte_mensal.insert(0, str(aporte_mensal))

                                self.entry_prazo.insert(0, str(simulacao_obj.prazo_meses))

                                # Taxa fixa pode ser None se for taxa variável
                                if simulacao_obj.taxa_fixa is not None:
                                    self.entry_taxa.insert(0, str(simulacao_obj.taxa_fixa))
                                else:
                                    self.entry_taxa.insert(0, "0")
                            else:
                                print(f"DEBUG - Simulação não encontrada: {self.simulacao_atual}")

                        # Exibir resultados carregados
                        nome_exibir = sim_dados['nome'] if sim_dados else "Simulação Carregada"

                        # Obter parâmetros para exibição
                        simulacao_obj = self.sistema.gerenciador.obter_simulacao(self.simulacao_atual)
                        if simulacao_obj:
                            # Garantir valores válidos para exibição
                            aporte_inicial = simulacao_obj.aporte_inicial if simulacao_obj.aporte_inicial is not None else 0
                            aporte_mensal = simulacao_obj.aporte_mensal if simulacao_obj.aporte_mensal is not None else 0
                            prazo_meses = simulacao_obj.prazo_meses if simulacao_obj.prazo_meses is not None else 0
                            taxa_fixa = simulacao_obj.taxa_fixa if simulacao_obj.taxa_fixa is not None else 0

                            self.exibir_resultados(
                                nome_exibir,
                                resultados,
                                aporte_inicial,
                                aporte_mensal,
                                prazo_meses,
                                taxa_fixa
                            )
                        else:
                            self.exibir_resultados(nome_exibir, resultados)
                        messagebox.showinfo("SUCESSO", f"Simulação carregada com sucesso!\n\nArquivo: {arquivo}\nID: {resultado}")
                    else:
                        messagebox.showwarning("AVISO", "Simulação carregada mas sem resultados calculados.")
                else:
                    messagebox.showerror("ERRO", f"Falha ao carregar simulação:\n{resultado}")
            except Exception as e:
                messagebox.showerror("ERRO", f"Erro ao carregar simulação:\n{str(e)}")

    def executar(self):
        """Executa a aplicação"""
        self.root.mainloop()

if __name__ == '__main__':
    app = SimuladorGUI()
    app.executar()