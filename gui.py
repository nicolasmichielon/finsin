"""
INTERFACE GRÁFICA DO SINFIN
Trabalho de Análise e Projeto de Sistemas
Curso: Sistemas de Informação - UFSC
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from main import SistemaSimulacaoInvestimentos, TipoTaxa

class InterfaceSimulador:
    """Interface gráfica unificada do sistema"""

    def __init__(self):
        self.sistema = SistemaSimulacaoInvestimentos()
        self.simulacao_atual = None

        # Janela principal
        self.root = tk.Tk()
        self.root.title("Sistema de Simulação de Investimentos - SIN/UFSC")
        self.root.geometry("1000x750")

        # Configurar tema moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Definir cores do tema minimalista
        self.cores = {
            'bg_principal': '#fafafa',
            'bg_secundario': '#ffffff',
            'bg_destaque': '#f8f9fa',
            'texto_principal': '#2c3e50',
            'texto_secundario': '#7f8c8d',
            'accent_principal': '#6c757d',
            'border': '#dee2e6'
        }

        self.root.configure(bg=self.cores['bg_principal'])
        self.configurar_tema()
        self.criar_interface()

    def configurar_tema(self):
        """Configura o tema visual da aplicação"""
        # Configurar estilos ttk
        self.style.configure('Titulo.TLabel',
                            font=('Segoe UI', 14, 'bold'),
                            background=self.cores['bg_secundario'],
                            foreground=self.cores['texto_principal'])

        self.style.configure('Accent.TButton',
                            background=self.cores['accent_principal'],
                            foreground='white',
                            font=('Segoe UI', 10, 'bold'))

        self.style.configure('Outline.TButton',
                            background=self.cores['bg_secundario'],
                            foreground=self.cores['accent_principal'],
                            font=('Segoe UI', 10),
                            relief='solid',
                            borderwidth=1)

    def criar_interface(self):
        """Cria a interface gráfica unificada"""

        # Título principal
        titulo = tk.Label(self.root, text="Sistema de Simulação de Investimentos",
                      font=('Segoe UI', 18, 'bold'),
                      bg=self.cores['bg_principal'],
                      fg=self.cores['texto_principal'])
        titulo.pack(pady=(20, 10))

        # Subtítulo
        subtitulo = tk.Label(self.root, text="Trabalho de Engenharia de Software - SIN/UFSC",
                         font=('Segoe UI', 12),
                         bg=self.cores['bg_principal'],
                         fg=self.cores['texto_secundario'])
        subtitulo.pack(pady=(0, 20))

        # Container principal centralizado
        container = tk.Frame(self.root, bg=self.cores['bg_principal'])
        container.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        # Seção de configuração
        config_section = tk.Frame(container, bg=self.cores['bg_secundario'],
                                relief=tk.FLAT, bd=1, highlightbackground=self.cores['border'],
                                highlightthickness=1)
        config_section.pack(fill=tk.X, pady=(0, 20))

        # Seção de resultados
        results_section = tk.Frame(container, bg=self.cores['bg_secundario'],
                                 relief=tk.FLAT, bd=1, highlightbackground=self.cores['border'],
                                 highlightthickness=1)
        results_section.pack(fill=tk.BOTH, expand=True)

        self.criar_secao_configuracao(config_section)
        self.criar_secao_resultados(results_section)


    def criar_secao_configuracao(self, parent):
        """Cria seção de configuração da simulação"""

        # Título da seção
        ttk.Label(parent, text="Configuração da Simulação", style='Titulo.TLabel').pack(pady=(20, 15))

        # Container para formulário
        form_container = tk.Frame(parent, bg=self.cores['bg_secundario'])
        form_container.pack(fill=tk.X, padx=30, pady=(0, 20))

        # Nome da simulação
        nome_frame = tk.Frame(form_container, bg=self.cores['bg_secundario'])
        nome_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(nome_frame, text="Nome da Simulação:").pack(anchor=tk.W)
        self.entry_nome = ttk.Entry(nome_frame, width=40, font=('Segoe UI', 11))
        self.entry_nome.pack(fill=tk.X, pady=(5, 0))

        # Parâmetros em grid
        params_frame = tk.Frame(form_container, bg=self.cores['bg_secundario'])
        params_frame.pack(fill=tk.X, pady=(0, 20))

        # Primeira linha
        ttk.Label(params_frame, text="Aporte Inicial (R$):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_aporte_inicial = ttk.Entry(params_frame, width=15, font=('Segoe UI', 11))
        self.entry_aporte_inicial.grid(row=0, column=1, padx=(10, 30), pady=5, sticky=tk.W)

        ttk.Label(params_frame, text="Aporte Mensal (R$):").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.entry_aporte_mensal = ttk.Entry(params_frame, width=15, font=('Segoe UI', 11))
        self.entry_aporte_mensal.grid(row=0, column=3, padx=(10, 0), pady=5, sticky=tk.W)

        # Segunda linha
        ttk.Label(params_frame, text="Prazo (meses):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_prazo = ttk.Entry(params_frame, width=15, font=('Segoe UI', 11))
        self.entry_prazo.grid(row=1, column=1, padx=(10, 30), pady=5, sticky=tk.W)

        ttk.Label(params_frame, text="Taxa Mensal (%):").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.entry_taxa = ttk.Entry(params_frame, width=15, font=('Segoe UI', 11))
        self.entry_taxa.grid(row=1, column=3, padx=(10, 0), pady=5, sticky=tk.W)

        # Botões de ação
        actions_frame = tk.Frame(form_container, bg=self.cores['bg_secundario'])
        actions_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(actions_frame, text="Calcular Simulação", command=self.calcular_simulacao,
                  style='Accent.TButton', cursor='hand2').pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(actions_frame, text="Limpar", command=self.limpar_campos,
                  style='Outline.TButton', cursor='hand2').pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(actions_frame, text="Salvar Arquivo", command=self.salvar_simulacao,
                  style='Outline.TButton', cursor='hand2').pack(side=tk.RIGHT, padx=(0, 10))

        ttk.Button(actions_frame, text="Carregar Arquivo", command=self.carregar_simulacao,
                  style='Outline.TButton', cursor='hand2').pack(side=tk.RIGHT)


    def criar_secao_resultados(self, parent):
        """Cria seção de resultados da simulação"""

        # Título da seção
        ttk.Label(parent, text="Resultados da Simulação", style='Titulo.TLabel').pack(pady=(20, 15))

        # Área de resultados
        result_container = tk.Frame(parent, bg=self.cores['bg_secundario'])
        result_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))

        self.text_resultados = tk.Text(result_container, font=('Courier New', 11),
                                     bg=self.cores['bg_destaque'],
                                     fg=self.cores['texto_principal'],
                                     wrap=tk.WORD,
                                     relief=tk.FLAT,
                                     highlightbackground=self.cores['border'],
                                     highlightthickness=1,
                                     insertbackground=self.cores['texto_principal'],
                                     selectbackground=self.cores['accent_principal'])

        scrollbar_results = ttk.Scrollbar(result_container, orient=tk.VERTICAL, command=self.text_resultados.yview)
        self.text_resultados.configure(yscrollcommand=scrollbar_results.set)

        self.text_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_results.pack(side=tk.RIGHT, fill=tk.Y)

        # Mensagem inicial
        self.text_resultados.insert(tk.END, "=== SISTEMA DE SIMULAÇÃO DE INVESTIMENTOS ===\n\n")
        self.text_resultados.insert(tk.END, "Preencha os campos acima e clique em 'Calcular Simulação'\n")
        self.text_resultados.insert(tk.END, "para ver os resultados da análise financeira.\n\n")
        self.text_resultados.insert(tk.END, "Os cálculos e projections aparecerão aqui...")



    # Métodos de controle
    def criar_simulacao_automatica(self):
        """Cria simulação automaticamente quando necessário"""
        nome = self.entry_nome.get().strip()
        if not nome:
            nome = "Simulação " + str(len(self.sistema.gerenciador.simulacoes) + 1)
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, nome)

        try:
            if not self.simulacao_atual:
                id_simulacao = self.sistema.criar_simulacao(nome)
                self.simulacao_atual = id_simulacao
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar simulação: {str(e)}")
            return False
        return True

    def validar_campos(self):
        """Valida se os campos estão preenchidos corretamente"""
        try:
            if not self.entry_aporte_inicial.get().strip():
                messagebox.showerror("Erro", "Aporte inicial é obrigatório!")
                return False

            aporte_inicial = float(self.entry_aporte_inicial.get())
            if aporte_inicial <= 0:
                messagebox.showerror("Erro", "Aporte inicial deve ser maior que zero!")
                return False

            if not self.entry_prazo.get().strip():
                messagebox.showerror("Erro", "Prazo é obrigatório!")
                return False

            prazo = int(self.entry_prazo.get())
            if prazo <= 0:
                messagebox.showerror("Erro", "Prazo deve ser maior que zero!")
                return False

            if not self.entry_taxa.get().strip():
                messagebox.showerror("Erro", "Taxa mensal é obrigatória!")
                return False

            taxa = float(self.entry_taxa.get())
            if taxa < 0:
                messagebox.showerror("Erro", "Taxa não pode ser negativa!")
                return False

            return True

        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos nos campos!")
            return False

    def aplicar_parametros(self):
        """Aplica parâmetros da interface na simulação"""
        try:
            parametros = {}

            # Nome
            nome = self.entry_nome.get().strip()
            if nome:
                self.sistema.editar_nome_simulacao(self.simulacao_atual, nome)

            # Parâmetros financeiros
            parametros['aporte_inicial'] = float(self.entry_aporte_inicial.get())
            parametros['prazo_meses'] = int(self.entry_prazo.get())
            parametros['tipo_taxa'] = TipoTaxa.FIXA
            parametros['taxa_fixa'] = float(self.entry_taxa.get())

            if self.entry_aporte_mensal.get().strip():
                parametros['aporte_mensal'] = float(self.entry_aporte_mensal.get())
            else:
                parametros['aporte_mensal'] = 0.0

            # Aplica configurações
            sucesso, erros = self.sistema.configurar_simulacao(self.simulacao_atual, **parametros)
            if not sucesso:
                raise Exception("\n".join(erros))

        except Exception as e:
            raise Exception(f"Erro ao aplicar parâmetros: {str(e)}")

    def carregar_dados_simulacao(self, id_simulacao):
        """Carrega dados da simulação nos campos"""
        simulacao = self.sistema.gerenciador.obter_simulacao(id_simulacao)
        if not simulacao:
            return

        # Limpa campos
        self.limpar_campos()

        # Preenche informações
        self.entry_nome.insert(0, simulacao.nome)
        self.entry_aporte_inicial.insert(0, str(simulacao.aporte_inicial))
        self.entry_aporte_mensal.insert(0, str(simulacao.aporte_mensal or 0))
        self.entry_prazo.insert(0, str(simulacao.prazo_meses))

        if simulacao.tipo_taxa == TipoTaxa.FIXA and simulacao.taxa_fixa:
            self.entry_taxa.insert(0, str(simulacao.taxa_fixa))

    def calcular_simulacao(self):
        """Calcula e exibe resultados da simulação"""
        # Validar campos
        if not self.validar_campos():
            return

        # Criar simulação automaticamente se necessário
        if not self.criar_simulacao_automatica():
            return

        self.text_resultados.delete(1.0, tk.END)
        self.text_resultados.insert(tk.END, "Calculando simulação...\n\n")
        self.text_resultados.update()

        try:
            # Aplicar parâmetros
            self.aplicar_parametros()

            # Executar cálculo
            resultado = self.sistema.testar_simulacao(self.simulacao_atual)

            if resultado['sucesso']:
                self.exibir_resultados(resultado)
            else:
                self.text_resultados.insert(tk.END, "ERRO NO CÁLCULO:\n")
                for erro in resultado['erros']:
                    self.text_resultados.insert(tk.END, f"- {erro}\n")

        except Exception as e:
            self.text_resultados.insert(tk.END, f"ERRO INESPERADO: {str(e)}\n")

    def exibir_resultados(self, resultado):
        """Exibe resultados na área de texto"""
        self.text_resultados.delete(1.0, tk.END)

        sim_info = resultado['simulacao']
        resultados = resultado['resultados']

        texto = "=" * 60 + "\n"
        texto += f"RESULTADOS - {sim_info['nome'].upper()}\n"
        texto += "=" * 60 + "\n\n"

        texto += "RESUMO FINANCEIRO:\n"
        texto += "-" * 20 + "\n"
        texto += f"Saldo Final:      R$ {resultados['saldo_final']:>15,.2f}\n"
        texto += f"Total Investido:  R$ {resultados['total_investido']:>15,.2f}\n"
        texto += f"Juros Acumulados: R$ {resultados['juros_acumulados']:>15,.2f}\n"
        texto += f"Rentabilidade:       {resultados['rentabilidade_percentual']:>15.2f}%\n"
        texto += f"Prazo:               {resultados['total_meses']:>15} meses\n\n"

        ganho_liquido = resultados['saldo_final'] - resultados['total_investido']
        texto += f"Ganho líquido: R$ {ganho_liquido:,.2f}\n"

        if resultados['total_meses'] > 0:
            ganho_mensal_medio = ganho_liquido / resultados['total_meses']
            texto += f"Ganho médio mensal: R$ {ganho_mensal_medio:,.2f}\n"

        texto += "\n" + "=" * 60 + "\n"

        self.text_resultados.insert(tk.END, texto)

    def salvar_simulacao(self):
        """Salva simulação atual em arquivo"""
        if not self.simulacao_atual:
            messagebox.showwarning("Aviso", "Nenhuma simulação selecionada para salvar!")
            return

        arquivo = filedialog.asksaveasfilename(
            title="Salvar simulação",
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json")]
        )

        if arquivo:
            sucesso, msg = self.sistema.salvar_simulacao(self.simulacao_atual, arquivo)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
            else:
                messagebox.showerror("Erro", msg)

    def carregar_simulacao(self):
        """Carrega simulação de arquivo"""
        arquivo = filedialog.askopenfilename(
            title="Carregar simulação",
            filetypes=[("Arquivos JSON", "*.json")]
        )

        if arquivo:
            sucesso, resultado = self.sistema.carregar_simulacao(arquivo)
            if sucesso:
                self.simulacao_atual = resultado
                self.carregar_dados_simulacao(resultado)
                messagebox.showinfo("Sucesso", f"Simulação carregada com ID: {resultado}")
            else:
                messagebox.showerror("Erro", resultado)


    def limpar_campos(self):
        """Limpa campos de configuração"""
        self.entry_nome.delete(0, tk.END)
        self.entry_aporte_inicial.delete(0, tk.END)
        self.entry_aporte_mensal.delete(0, tk.END)
        self.entry_prazo.delete(0, tk.END)
        self.entry_taxa.delete(0, tk.END)


    def executar(self):
        """Executa a aplicação"""
        # Inicialização concluída

        # Inicia interface
        self.root.mainloop()

# Execução da aplicação
if __name__ == '__main__':
    app = InterfaceSimulador()
    app.executar()