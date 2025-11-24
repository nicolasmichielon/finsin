"""
SISTEMA DE SIMULAÇÃO DE INVESTIMENTOS
Trabalho de Análise e Projeto de Sistemas
Curso: Sistemas de Informação - UFSC

Membros da Equipe:
- Nick D: Implementou UC01 - Configurar Simulação
- Nick C: Implementou UC02 - Calcular Simulação
- Nick J: Implementou UC03 - Gerenciar Simulações
"""

import json
import math
import csv
from datetime import datetime
from typing import List, Dict, Optional, Any
from enum import Enum
from dataclasses import dataclass, asdict

try:
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    MATPLOTLIB_DISPONIVEL = True
except ImportError:
    MATPLOTLIB_DISPONIVEL = False
    Figure = Any  # Fallback quando matplotlib não está disponível
    print("Aviso: matplotlib não está instalado. Funcionalidade de gráficos desabilitada.")

# ============================================================================
# ENUMS E ESTRUTURAS BÁSICAS
# ============================================================================

class TipoTaxa(Enum):
    """Define os tipos de taxa de retorno disponíveis"""
    FIXA = "fixa"
    VARIAVEL = "variavel"

@dataclass
class ResultadoMensal:
    """Representa o resultado financeiro de um mês da simulação"""
    mes: int
    aporte_mes: float
    total_investido: float
    juros_mes: float
    juros_acumulados: float
    saldo_final: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class HistoricoModificacao:
    """Representa uma modificação feita na simulação"""
    timestamp: datetime
    campo_alterado: str
    valor_antigo: Any
    valor_novo: Any

    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'campo_alterado': self.campo_alterado,
            'valor_antigo': str(self.valor_antigo),
            'valor_novo': str(self.valor_novo)
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HistoricoModificacao':
        return cls(
            timestamp=datetime.fromisoformat(data['timestamp']),
            campo_alterado=data['campo_alterado'],
            valor_antigo=data['valor_antigo'],
            valor_novo=data['valor_novo']
        )

# ============================================================================
# CLASSE PRINCIPAL - SIMULAÇÃO
# ============================================================================

@dataclass
class Simulacao:
    """
    Classe que representa uma simulação de investimento
    Contém todos os parâmetros e resultados da simulação
    """
    id: str
    nome: str
    aporte_inicial: float
    aporte_mensal: float
    prazo_meses: int
    tipo_taxa: TipoTaxa
    taxa_fixa: Optional[float] = None
    taxas_variaveis: Optional[List[float]] = None
    resultados: List[ResultadoMensal] = None
    data_criacao: datetime = None
    data_modificacao: datetime = None
    historico: List[HistoricoModificacao] = None

    def __post_init__(self):
        """Inicializa campos padrão"""
        if self.resultados is None:
            self.resultados = []
        if self.data_criacao is None:
            self.data_criacao = datetime.now()
        if self.data_modificacao is None:
            self.data_modificacao = datetime.now()
        if self.historico is None:
            self.historico = []

    def validar(self) -> tuple[bool, List[str]]:
        """Valida os dados da simulação"""
        erros = []

        # Validação básica dos campos obrigatórios
        if not self.nome or not self.nome.strip():
            erros.append("Nome da simulação é obrigatório")

        if self.aporte_inicial is None or self.aporte_inicial <= 0:
            erros.append("Aporte inicial deve ser maior que R$ 0,00")

        if self.prazo_meses is None or self.prazo_meses < 1 or self.prazo_meses > 360:
            erros.append("Prazo deve estar entre 1 e 360 meses")

        # Validação da taxa
        if self.tipo_taxa == TipoTaxa.FIXA:
            if self.taxa_fixa is None or self.taxa_fixa < 0 or self.taxa_fixa > 100:
                erros.append("Taxa fixa deve estar entre 0% e 100%")
        elif self.tipo_taxa == TipoTaxa.VARIAVEL:
            if not self.taxas_variaveis or len(self.taxas_variaveis) == 0:
                erros.append("Taxas variáveis são obrigatórias")
            elif len(self.taxas_variaveis) != self.prazo_meses:
                erros.append(f"Número de taxas ({len(self.taxas_variaveis)}) deve ser igual ao prazo ({self.prazo_meses})")
            elif any(taxa < 0 or taxa > 100 for taxa in self.taxas_variaveis):
                erros.append("Todas as taxas devem estar entre 0% e 100%")

        return len(erros) == 0, erros

    def to_dict(self) -> Dict[str, Any]:
        """Converte simulação para dicionário (para salvar em JSON)"""
        data = asdict(self)
        data['tipo_taxa'] = self.tipo_taxa.value
        data['data_criacao'] = self.data_criacao.isoformat() if self.data_criacao else None
        data['data_modificacao'] = self.data_modificacao.isoformat() if self.data_modificacao else None
        if self.historico:
            data['historico'] = [h.to_dict() for h in self.historico]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Simulacao':
        """Cria simulação a partir de dicionário (para carregar de JSON)"""
        if data.get('data_criacao'):
            data['data_criacao'] = datetime.fromisoformat(data['data_criacao'])
        if data.get('data_modificacao'):
            data['data_modificacao'] = datetime.fromisoformat(data['data_modificacao'])

        data['tipo_taxa'] = TipoTaxa(data['tipo_taxa'])

        if data.get('resultados'):
            data['resultados'] = [ResultadoMensal(**r) for r in data['resultados']]

        if data.get('historico'):
            data['historico'] = [HistoricoModificacao.from_dict(h) for h in data['historico']]

        return cls(**data)

# ============================================================================
# UC01 - CONFIGURAR SIMULAÇÃO (IMPLEMENTADO POR Nick D)
# ============================================================================

class ConfiguradorSimulacao:
    """
    UC01 - Permite ao usuário configurar simulações
    IMPLEMENTADO POR: Nick D
    """

    def __init__(self):
        self.simulacoes: Dict[str, Simulacao] = {}
        self._proximo_id = 1

    def _gerar_id(self) -> str:
        """Gera ID único para nova simulação"""
        id_simulacao = f"SIM{self._proximo_id:04d}"
        self._proximo_id += 1
        return id_simulacao

    def criar_simulacao(self, nome: str) -> str:
        """
        UC01 - Cria uma nova simulação

        Args:
            nome: Nome da simulação

        Returns:
            ID da simulação criada
        """
        if not nome or not nome.strip():
            raise ValueError("Nome da simulação é obrigatório")

        # Cria nova simulação com valores padrão
        simulacao = Simulacao(
            id=self._gerar_id(),
            nome=nome.strip(),
            aporte_inicial=1000.0,  # Valor padrão
            aporte_mensal=0.0,
            prazo_meses=12,
            tipo_taxa=TipoTaxa.FIXA,
            taxa_fixa=1.0
        )

        # Armazena a simulação
        self.simulacoes[simulacao.id] = simulacao

        print(f"[UC01] Simulação '{nome}' criada com ID: {simulacao.id} - Nick D")
        return simulacao.id

    def configurar_parametros(self, id_simulacao: str, **novos_parametros) -> tuple[bool, List[str]]:
        """
        UC01 - Configura os parâmetros de uma simulação

        Args:
            id_simulacao: ID da simulação a configurar
            **novos_parametros: Novos valores dos parâmetros

        Returns:
            Tupla (sucesso, lista_de_erros)
        """
        # Verifica se simulação existe
        simulacao = self.obter_simulacao(id_simulacao)
        if not simulacao:
            erro = f"Simulação {id_simulacao} não encontrada"
            print(f"[UC01] {erro}")
            return False, [erro]

        print(f"[UC01] Configurando simulação: {simulacao.nome} - Nick D")

        # Aplica as mudanças nos parâmetros
        parametros_alterados = []
        timestamp = datetime.now()

        for campo, novo_valor in novos_parametros.items():
            if hasattr(simulacao, campo):
                valor_antigo = getattr(simulacao, campo)
                if valor_antigo != novo_valor:
                    setattr(simulacao, campo, novo_valor)
                    parametros_alterados.append(f"{campo}: {valor_antigo} → {novo_valor}")

                    modificacao = HistoricoModificacao(
                        timestamp=timestamp,
                        campo_alterado=campo,
                        valor_antigo=valor_antigo,
                        valor_novo=novo_valor
                    )
                    simulacao.historico.append(modificacao)

        # Atualiza data de modificação
        simulacao.data_modificacao = timestamp

        # Limpa resultados antigos pois parâmetros mudaram
        simulacao.resultados = []

        # Valida a simulação após as mudanças
        valida, erros = simulacao.validar()

        if valida:
            print(f"[UC01] Parâmetros configurados com sucesso - Nick D:")
            for param in parametros_alterados:
                print(f"[UC01]   - {param}")
            return True, []
        else:
            print(f"[UC01] Erros na validação após configuração:")
            for erro in erros:
                print(f"[UC01]   - {erro}")
            return False, erros

    def editar_nome(self, id_simulacao: str, novo_nome: str) -> tuple[bool, str]:
        """
        UC01 - Edita apenas o nome da simulação

        Args:
            id_simulacao: ID da simulação
            novo_nome: Novo nome

        Returns:
            Tupla (sucesso, mensagem)
        """
        simulacao = self.obter_simulacao(id_simulacao)
        if not simulacao:
            return False, f"Simulação {id_simulacao} não encontrada"

        if not novo_nome or not novo_nome.strip():
            return False, "Nome não pode estar vazio"

        nome_antigo = simulacao.nome
        timestamp = datetime.now()

        if nome_antigo != novo_nome.strip():
            simulacao.nome = novo_nome.strip()
            simulacao.data_modificacao = timestamp

            modificacao = HistoricoModificacao(
                timestamp=timestamp,
                campo_alterado='nome',
                valor_antigo=nome_antigo,
                valor_novo=novo_nome.strip()
            )
            simulacao.historico.append(modificacao)

        print(f"[UC01] Nome alterado: '{nome_antigo}' → '{novo_nome.strip()}' - Nick D")
        return True, f"Nome alterado de '{nome_antigo}' para '{novo_nome.strip()}'"

    def listar_simulacoes(self) -> List[Dict[str, Any]]:
        """Retorna lista de simulações com informações básicas"""
        return [
            {
                'id': s.id,
                'nome': s.nome,
                'prazo_meses': s.prazo_meses,
                'data_criacao': s.data_criacao.strftime('%d/%m/%Y %H:%M'),
                'calculada': len(s.resultados) > 0
            }
            for s in self.simulacoes.values()
        ]

    def obter_simulacao(self, id_simulacao: str) -> Optional[Simulacao]:
        """Obtém simulação por ID"""
        return self.simulacoes.get(id_simulacao)

    def obter_historico(self, id_simulacao: str) -> Optional[List[HistoricoModificacao]]:
        """Obtém histórico de modificações de uma simulação"""
        simulacao = self.obter_simulacao(id_simulacao)
        if simulacao:
            return simulacao.historico
        return None

    def adicionar_simulacao(self, simulacao: Simulacao) -> None:
        """Adiciona uma simulação ao dicionário"""
        self.simulacoes[simulacao.id] = simulacao

    def excluir_simulacao(self, id_simulacao: str) -> tuple[bool, str]:
        """
        UC01 - Exclui uma simulação

        Args:
            id_simulacao: ID da simulação a excluir

        Returns:
            Tupla (sucesso, mensagem)
        """
        if id_simulacao not in self.simulacoes:
            return False, f"Simulação {id_simulacao} não encontrada"

        nome = self.simulacoes[id_simulacao].nome
        del self.simulacoes[id_simulacao]

        print(f"[UC01] Simulação '{nome}' ({id_simulacao}) excluída - Nick D")
        return True, f"Simulação '{nome}' excluída com sucesso"

# ============================================================================
# UC02 - CALCULAR SIMULAÇÃO (IMPLEMENTADO POR Nick C)
# ============================================================================

class CalculadoraSimulacao:
    """
    UC02 - Permite ao usuário calcular simulações
    IMPLEMENTADO POR: Nick C
    """

    def __init__(self, configurador: ConfiguradorSimulacao):
        self.configurador = configurador

    def calcular_simulacao(self, id_simulacao: str) -> tuple[bool, List[str]]:
        """
        UC02 - Calcula a projeção completa da simulação

        Args:
            id_simulacao: ID da simulação a calcular

        Returns:
            Tupla (sucesso, lista_de_erros)
        """
        # Obtém a simulação
        simulacao = self.configurador.obter_simulacao(id_simulacao)
        if not simulacao:
            erro = f"Simulação {id_simulacao} não encontrada"
            print(f"[UC02] {erro}")
            return False, [erro]

        print(f"[UC02] Iniciando cálculo da simulação: {simulacao.nome} - Nick C")

        # Valida antes de calcular
        valida, erros = simulacao.validar()
        if not valida:
            print(f"[UC02] Simulação inválida, não é possível calcular")
            return False, erros

        try:
            # Executa o cálculo mês a mês
            resultados = self._calcular_projecao_mensal(simulacao)

            # Salva os resultados na simulação
            simulacao.resultados = resultados
            simulacao.data_modificacao = datetime.now()

            print(f"[UC02] Cálculo concluído: {len(resultados)} meses processados - Nick C")
            return True, []

        except Exception as e:
            erro_msg = f"Erro durante o cálculo: {str(e)}"
            print(f"[UC02] {erro_msg}")
            return False, [erro_msg]

    def _calcular_projecao_mensal(self, simulacao: Simulacao) -> List[ResultadoMensal]:
        """
        Método interno que executa o cálculo mês a mês
        Aplica juros compostos e aportes mensais
        """
        resultados = []
        saldo_atual = simulacao.aporte_inicial
        total_investido = simulacao.aporte_inicial
        juros_acumulados = 0.0

        print(f"[UC02] Calculando {simulacao.prazo_meses} meses... - Nick C")

        for mes in range(1, simulacao.prazo_meses + 1):
            # Determina a taxa do mês
            if simulacao.tipo_taxa == TipoTaxa.FIXA:
                taxa_mes_decimal = simulacao.taxa_fixa / 100
            else:
                taxa_mes_decimal = simulacao.taxas_variaveis[mes - 1] / 100

            # Calcula juros sobre o saldo atual
            juros_mes = saldo_atual * taxa_mes_decimal
            saldo_atual += juros_mes
            juros_acumulados += juros_mes

            # Aplica aporte mensal
            aporte_mes = simulacao.aporte_mensal if simulacao.aporte_mensal else 0.0
            saldo_atual += aporte_mes
            total_investido += aporte_mes

            # Cria resultado do mês
            resultado = ResultadoMensal(
                mes=mes,
                aporte_mes=aporte_mes,
                total_investido=total_investido,
                juros_mes=juros_mes,
                juros_acumulados=juros_acumulados,
                saldo_final=saldo_atual
            )

            resultados.append(resultado)

        return resultados

    def testar_simulacao(self, id_simulacao: str) -> Dict[str, Any]:
        """
        UC02 - Testa a simulação e retorna resumo dos resultados

        Args:
            id_simulacao: ID da simulação a testar

        Returns:
            Dicionário com resultados do teste
        """
        print(f"[UC02] Testando simulação {id_simulacao} - Nick C")

        # Calcula a simulação
        sucesso, erros = self.calcular_simulacao(id_simulacao)

        if not sucesso:
            return {
                'sucesso': False,
                'erros': erros,
                'resultados': None
            }

        # Obtém os resultados
        simulacao = self.configurador.obter_simulacao(id_simulacao)
        if not simulacao or not simulacao.resultados:
            return {
                'sucesso': False,
                'erros': ['Falha ao obter resultados'],
                'resultados': None
            }

        # Prepara resumo dos resultados
        ultimo_resultado = simulacao.resultados[-1]

        resumo = {
            'sucesso': True,
            'erros': [],
            'simulacao': {
                'id': simulacao.id,
                'nome': simulacao.nome,
                'prazo_meses': simulacao.prazo_meses
            },
            'resultados': {
                'saldo_final': ultimo_resultado.saldo_final,
                'total_investido': ultimo_resultado.total_investido,
                'juros_acumulados': ultimo_resultado.juros_acumulados,
                'rentabilidade_percentual': round(((ultimo_resultado.saldo_final / ultimo_resultado.total_investido - 1) * 100), 2),
                'total_meses': len(simulacao.resultados)
            }
        }

        print(f"[UC02] Teste concluído - Saldo final: R$ {ultimo_resultado.saldo_final:,.2f} - Nick C")

        return resumo

# ============================================================================
# UC03 - GERENCIAR SIMULAÇÕES (IMPLEMENTADO POR Nick J)
# ============================================================================

class GerenciadorSimulacoes:
    """
    UC03 - Permite ao usuário gerenciar simulações (salvar/carregar)
    IMPLEMENTADO POR: Nick J
    """

    def __init__(self, configurador: ConfiguradorSimulacao):
        self.configurador = configurador

    def salvar_simulacao(self, id_simulacao: str, caminho_arquivo: str) -> tuple[bool, str]:
        """
        UC03 - Salva simulação em arquivo JSON

        Args:
            id_simulacao: ID da simulação
            caminho_arquivo: Caminho onde salvar

        Returns:
            Tupla (sucesso, mensagem)
        """
        if id_simulacao not in self.configurador.simulacoes:
            return False, f"Simulação {id_simulacao} não encontrada"

        try:
            simulacao = self.configurador.obter_simulacao(id_simulacao)

            # Converte para dicionário e salva
            with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
                json.dump(simulacao.to_dict(), arquivo, ensure_ascii=False, indent=2)

            print(f"[UC03] Simulação {id_simulacao} salva em: {caminho_arquivo} - Nick J")
            return True, f"Simulação salva com sucesso em {caminho_arquivo}"

        except Exception as e:
            erro_msg = f"Erro ao salvar arquivo: {str(e)}"
            print(f"[UC03] {erro_msg}")
            return False, erro_msg

    def carregar_simulacao(self, caminho_arquivo: str) -> tuple[bool, str]:
        """
        UC03 - Carrega simulação de arquivo JSON

        Args:
            caminho_arquivo: Caminho do arquivo

        Returns:
            Tupla (sucesso, id_simulacao_ou_erro)
        """
        try:
            # Lê arquivo JSON
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)

            # Cria simulação a partir dos dados
            simulacao = Simulacao.from_dict(dados)

            # Adiciona ao configurador
            self.configurador.adicionar_simulacao(simulacao)

            # Atualiza contador de IDs
            try:
                num_id = int(simulacao.id[3:])  # Remove "SIM"
                if num_id >= self.configurador._proximo_id:
                    self.configurador._proximo_id = num_id + 1
            except:
                pass

            print(f"[UC03] Simulação carregada: {simulacao.id} - {simulacao.nome} - Nick J")
            return True, simulacao.id

        except Exception as e:
            erro_msg = f"Erro ao carregar arquivo: {str(e)}"
            print(f"[UC03] {erro_msg}")
            return False, erro_msg

# ============================================================================
# UC04 - EXPORTAR SIMULAÇÃO PARA CSV
# ============================================================================

class ExportadorSimulacao:
    """
    UC04 - Permite exportar simulações para formato CSV
    """

    def __init__(self, configurador: ConfiguradorSimulacao):
        self.configurador = configurador

    def exportar_csv(self, id_simulacao: str, caminho_arquivo: str) -> tuple[bool, str]:
        """
        UC04 - Exporta simulação para arquivo CSV

        Args:
            id_simulacao: ID da simulação
            caminho_arquivo: Caminho onde salvar

        Returns:
            Tupla (sucesso, mensagem)
        """
        if id_simulacao not in self.configurador.simulacoes:
            return False, f"Simulação {id_simulacao} não encontrada"

        try:
            simulacao = self.configurador.simulacoes[id_simulacao]

            with open(caminho_arquivo, 'w', encoding='utf-8', newline='') as arquivo:
                writer = csv.writer(arquivo)

                # Cabeçalho com informações da simulação
                writer.writerow(['INFORMAÇÕES DA SIMULAÇÃO'])
                writer.writerow(['ID', simulacao.id])
                writer.writerow(['Nome', simulacao.nome])
                writer.writerow(['Aporte Inicial (R$)', f'{simulacao.aporte_inicial:.2f}'])
                writer.writerow(['Aporte Mensal (R$)', f'{simulacao.aporte_mensal:.2f}'])
                writer.writerow(['Prazo (meses)', simulacao.prazo_meses])
                writer.writerow(['Tipo de Taxa', simulacao.tipo_taxa.value])

                if simulacao.tipo_taxa == TipoTaxa.FIXA:
                    writer.writerow(['Taxa Fixa (%)', f'{simulacao.taxa_fixa:.2f}'])
                else:
                    writer.writerow(['Taxas Variáveis (%)', ', '.join(f'{t:.2f}' for t in simulacao.taxas_variaveis)])

                writer.writerow(['Data de Criação', simulacao.data_criacao.strftime('%d/%m/%Y %H:%M:%S')])
                writer.writerow(['Data de Modificação', simulacao.data_modificacao.strftime('%d/%m/%Y %H:%M:%S')])
                writer.writerow([])

                # Resultados mensais
                if simulacao.resultados:
                    writer.writerow(['RESULTADOS MENSAIS'])
                    writer.writerow(['Mês', 'Aporte do Mês (R$)', 'Total Investido (R$)',
                                   'Juros do Mês (R$)', 'Juros Acumulados (R$)', 'Saldo Final (R$)'])

                    for resultado in simulacao.resultados:
                        writer.writerow([
                            resultado.mes,
                            f'{resultado.aporte_mes:.2f}',
                            f'{resultado.total_investido:.2f}',
                            f'{resultado.juros_mes:.2f}',
                            f'{resultado.juros_acumulados:.2f}',
                            f'{resultado.saldo_final:.2f}'
                        ])

                    # Resumo final
                    ultimo = simulacao.resultados[-1]
                    writer.writerow([])
                    writer.writerow(['RESUMO FINAL'])
                    writer.writerow(['Saldo Final (R$)', f'{ultimo.saldo_final:.2f}'])
                    writer.writerow(['Total Investido (R$)', f'{ultimo.total_investido:.2f}'])
                    writer.writerow(['Juros Acumulados (R$)', f'{ultimo.juros_acumulados:.2f}'])
                    rentabilidade = ((ultimo.saldo_final / ultimo.total_investido - 1) * 100)
                    writer.writerow(['Rentabilidade (%)', f'{rentabilidade:.2f}'])
                else:
                    writer.writerow(['Simulação ainda não foi calculada'])

            print(f"[UC04] Simulação {id_simulacao} exportada para CSV: {caminho_arquivo}")
            return True, f"Simulação exportada com sucesso para {caminho_arquivo}"

        except Exception as e:
            erro_msg = f"Erro ao exportar CSV: {str(e)}"
            print(f"[UC04] {erro_msg}")
            return False, erro_msg

# ============================================================================
# UC05 - VISUALIZAR GRÁFICOS
# ============================================================================

class GeradorGraficos:
    """
    UC05 - Permite visualizar gráficos das simulações
    """

    def __init__(self, configurador: ConfiguradorSimulacao):
        self.configurador = configurador

    def criar_figura_evolucao(self, id_simulacao: str) -> Optional[Figure]:
        """
        Cria figura com gráfico de evolução do saldo

        Args:
            id_simulacao: ID da simulação

        Returns:
            Figure do matplotlib ou None se erro
        """
        if not MATPLOTLIB_DISPONIVEL:
            return None

        simulacao = self.configurador.obter_simulacao(id_simulacao)
        if not simulacao or not simulacao.resultados:
            return None

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        fig.suptitle(f'Evolução do Investimento - {simulacao.nome}', fontsize=14, fontweight='bold')

        meses = [r.mes for r in simulacao.resultados]
        saldo = [r.saldo_final for r in simulacao.resultados]
        investido = [r.total_investido for r in simulacao.resultados]
        juros = [r.juros_acumulados for r in simulacao.resultados]

        # Gráfico 1: Evolução do Saldo
        ax1.plot(meses, saldo, 'b-', linewidth=2, label='Saldo Final')
        ax1.plot(meses, investido, 'g--', linewidth=2, label='Total Investido')
        ax1.fill_between(meses, investido, saldo, alpha=0.3, color='green')
        ax1.set_xlabel('Mês')
        ax1.set_ylabel('Valor (R$)')
        ax1.set_title('Evolução do Saldo Final')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Gráfico 2: Juros Acumulados
        ax2.plot(meses, juros, 'r-', linewidth=2, label='Juros Acumulados')
        ax2.fill_between(meses, 0, juros, alpha=0.3, color='red')
        ax2.set_xlabel('Mês')
        ax2.set_ylabel('Valor (R$)')
        ax2.set_title('Juros Acumulados')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        return fig

    def criar_figura_composicao(self, id_simulacao: str) -> Optional[Figure]:
        """
        Cria figura com gráfico de composição (pizza)

        Args:
            id_simulacao: ID da simulação

        Returns:
            Figure do matplotlib ou None se erro
        """
        if not MATPLOTLIB_DISPONIVEL:
            return None

        simulacao = self.configurador.obter_simulacao(id_simulacao)
        if not simulacao or not simulacao.resultados:
            return None

        ultimo = simulacao.resultados[-1]

        fig, ax = plt.subplots(figsize=(8, 8))
        fig.suptitle(f'Composição do Saldo Final - {simulacao.nome}', fontsize=14, fontweight='bold')

        valores = [ultimo.total_investido, ultimo.juros_acumulados]
        labels = ['Total Investido', 'Juros Acumulados']
        colors = ['#4CAF50', '#FF9800']
        explode = (0.05, 0.05)

        ax.pie(valores, labels=labels, colors=colors, autopct='%1.1f%%',
               startangle=90, explode=explode, shadow=True)
        ax.axis('equal')

        # Adiciona legenda com valores
        legenda_texto = [
            f'Total Investido: R$ {ultimo.total_investido:,.2f}',
            f'Juros Acumulados: R$ {ultimo.juros_acumulados:,.2f}',
            f'Saldo Final: R$ {ultimo.saldo_final:,.2f}'
        ]
        ax.text(0, -1.3, '\n'.join(legenda_texto), ha='center', fontsize=10)

        return fig

# ============================================================================
# UC06 - COMPARAR SIMULAÇÕES
# ============================================================================

class ComparadorSimulacoes:
    """
    UC06 - Permite comparar múltiplas simulações
    """

    def __init__(self, configurador: ConfiguradorSimulacao):
        self.configurador = configurador

    def comparar(self, lista_ids: List[str]) -> Optional[Dict[str, Any]]:
        """
        Compara múltiplas simulações

        Args:
            lista_ids: Lista de IDs das simulações a comparar

        Returns:
            Dicionário com dados comparativos ou None se erro
        """
        if not lista_ids or len(lista_ids) < 2:
            return None

        comparacao = {
            'simulacoes': [],
            'total_simulacoes': len(lista_ids)
        }

        for id_sim in lista_ids:
            simulacao = self.configurador.obter_simulacao(id_sim)
            if not simulacao:
                continue

            dados_sim = {
                'id': simulacao.id,
                'nome': simulacao.nome,
                'aporte_inicial': simulacao.aporte_inicial,
                'aporte_mensal': simulacao.aporte_mensal,
                'prazo_meses': simulacao.prazo_meses,
                'tipo_taxa': simulacao.tipo_taxa.value
            }

            if simulacao.resultados:
                ultimo = simulacao.resultados[-1]
                dados_sim.update({
                    'saldo_final': ultimo.saldo_final,
                    'total_investido': ultimo.total_investido,
                    'juros_acumulados': ultimo.juros_acumulados,
                    'rentabilidade': ((ultimo.saldo_final / ultimo.total_investido - 1) * 100),
                    'calculada': True
                })
            else:
                dados_sim.update({
                    'saldo_final': 0,
                    'total_investido': 0,
                    'juros_acumulados': 0,
                    'rentabilidade': 0,
                    'calculada': False
                })

            comparacao['simulacoes'].append(dados_sim)

        return comparacao

    def criar_grafico_comparacao(self, lista_ids: List[str]) -> Optional[Figure]:
        """
        Cria gráfico comparativo entre simulações

        Args:
            lista_ids: Lista de IDs das simulações

        Returns:
            Figure do matplotlib ou None
        """
        if not MATPLOTLIB_DISPONIVEL:
            return None

        comparacao = self.comparar(lista_ids)
        if not comparacao:
            return None

        # Filtra apenas simulações calculadas
        sims_calculadas = [s for s in comparacao['simulacoes'] if s['calculada']]
        if len(sims_calculadas) < 2:
            return None

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Comparação de Simulações', fontsize=14, fontweight='bold')

        nomes = [s['nome'] for s in sims_calculadas]
        saldos = [s['saldo_final'] for s in sims_calculadas]
        rentabilidades = [s['rentabilidade'] for s in sims_calculadas]

        # Gráfico 1: Saldo Final
        cores = plt.cm.viridis([i/len(sims_calculadas) for i in range(len(sims_calculadas))])
        ax1.bar(nomes, saldos, color=cores)
        ax1.set_title('Saldo Final')
        ax1.set_ylabel('Valor (R$)')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3, axis='y')

        # Gráfico 2: Rentabilidade
        ax2.bar(nomes, rentabilidades, color=cores)
        ax2.set_title('Rentabilidade (%)')
        ax2.set_ylabel('Percentual (%)')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        return fig

# ============================================================================
# SISTEMA PRINCIPAL - INTEGRAÇÃO DOS CASOS DE USO
# ============================================================================

class SistemaSimulacaoInvestimentos:
    """
    Classe principal que integra todos os casos de uso
    """

    def __init__(self):
        self.gerenciador = ConfiguradorSimulacao()
        self.calculadora = CalculadoraSimulacao(self.gerenciador)
        self.arquivos = GerenciadorSimulacoes(self.gerenciador)
        self.exportador = ExportadorSimulacao(self.gerenciador)
        self.graficos = GeradorGraficos(self.gerenciador) if MATPLOTLIB_DISPONIVEL else None
        self.comparador = ComparadorSimulacoes(self.gerenciador)

        print("Sistema de Simulação de Investimentos inicializado")
        print("Casos de Uso disponíveis:")
        print("  UC01 - Configurar Simulação (Nick D)")
        print("  UC02 - Calcular Simulação (Nick C)")
        print("  UC03 - Gerenciar Simulações (Nick J)")
        print("  UC04 - Exportar para CSV")
        if MATPLOTLIB_DISPONIVEL:
            print("  UC05 - Visualizar Gráficos")
        print("  UC06 - Comparar Simulações")

    # Métodos do UC01 (Nick D)
    def criar_simulacao(self, nome: str) -> str:
        """UC01 - Criar nova simulação"""
        return self.gerenciador.criar_simulacao(nome)

    def configurar_simulacao(self, id_simulacao: str, **parametros) -> tuple[bool, List[str]]:
        """UC01 - Configurar parâmetros da simulação"""
        return self.gerenciador.configurar_parametros(id_simulacao, **parametros)

    def editar_nome_simulacao(self, id_simulacao: str, novo_nome: str) -> tuple[bool, str]:
        """UC01 - Editar nome da simulação"""
        return self.gerenciador.editar_nome(id_simulacao, novo_nome)

    def excluir_simulacao(self, id_simulacao: str) -> tuple[bool, str]:
        """UC01 - Excluir simulação"""
        return self.gerenciador.excluir_simulacao(id_simulacao)

    # Métodos do UC02 (Nick C)
    def calcular_simulacao(self, id_simulacao: str) -> tuple[bool, List[str]]:
        """UC02 - Calcular simulação"""
        return self.calculadora.calcular_simulacao(id_simulacao)

    def testar_simulacao(self, id_simulacao: str) -> Dict[str, Any]:
        """UC02 - Testar simulação completa"""
        return self.calculadora.testar_simulacao(id_simulacao)

    # Métodos do UC03 (Nick J)
    def salvar_simulacao(self, id_simulacao: str, caminho: str) -> tuple[bool, str]:
        """UC03 - Salvar simulação"""
        return self.arquivos.salvar_simulacao(id_simulacao, caminho)

    def carregar_simulacao(self, caminho: str) -> tuple[bool, str]:
        """UC03 - Carregar simulação"""
        return self.arquivos.carregar_simulacao(caminho)

    # Métodos do UC04
    def exportar_csv(self, id_simulacao: str, caminho: str) -> tuple[bool, str]:
        """UC04 - Exportar simulação para CSV"""
        return self.exportador.exportar_csv(id_simulacao, caminho)

    # Métodos auxiliares
    def listar_simulacoes(self) -> List[Dict[str, Any]]:
        """Lista todas as simulações"""
        return self.gerenciador.listar_simulacoes()

    def obter_historico(self, id_simulacao: str) -> Optional[List[HistoricoModificacao]]:
        """Obtém histórico de modificações"""
        return self.gerenciador.obter_historico(id_simulacao)

    def criar_grafico_evolucao(self, id_simulacao: str) -> Optional[Figure]:
        """UC05 - Cria gráfico de evolução"""
        if self.graficos:
            return self.graficos.criar_figura_evolucao(id_simulacao)
        return None

    def criar_grafico_composicao(self, id_simulacao: str) -> Optional[Figure]:
        """UC05 - Cria gráfico de composição"""
        if self.graficos:
            return self.graficos.criar_figura_composicao(id_simulacao)
        return None

    def comparar_simulacoes(self, lista_ids: List[str]) -> Optional[Dict[str, Any]]:
        """UC06 - Compara múltiplas simulações"""
        return self.comparador.comparar(lista_ids)

    def criar_grafico_comparacao(self, lista_ids: List[str]) -> Optional[Figure]:
        """UC06 - Cria gráfico de comparação"""
        return self.comparador.criar_grafico_comparacao(lista_ids)

# ============================================================================
# EXECUÇÃO PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    # Executa exemplo de uso
    sistema = SistemaSimulacaoInvestimentos()
