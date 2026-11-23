"""Funções compartilhadas pelos notebooks 09-15 da análise de tuberculose (SINAN).

Centraliza: caminhos, dicionários de códigos do SINAN-TB, população anual do IBGE,
e funções estatísticas (Fisher com OR e IC 95%, Bonferroni, taxa por 100 mil com IC).
"""
from pathlib import Path
import glob

import numpy as np
import pandas as pd
from scipy import stats

# ----------------------------------------------------------------------------
# Caminhos (relativos à pasta notebooks/)
# ----------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parents[1]
DATA = RAIZ / 'data'
RAW = DATA / 'raw'
EXTERNAL = DATA / 'external'
PROCESSED = DATA / 'processed'
FIGURAS = RAIZ / 'reports' / 'figuras'

ANOS = list(range(2014, 2025))

# ----------------------------------------------------------------------------
# Municípios de interesse (código IBGE de 6 dígitos, como no SINAN)
# ----------------------------------------------------------------------------
COD_ILHEUS = '291360'
COD_ITABUNA = '291480'
CIDADES = {
    '291360': 'Ilhéus',
    '291480': 'Itabuna',
    '293330': 'Vitória da Conquista',  # corrigido: o notebook 07 usava 291950
    '291080': 'Feira de Santana',
    '292740': 'Salvador',
    '261160': 'Recife',
    '280030': 'Aracaju',
    '330455': 'Rio de Janeiro',
    '355030': 'São Paulo',
    '410690': 'Curitiba',
}
GRUPO_CIDADE = {
    'Ilhéus': 'Sul da Bahia (litoral)', 'Itabuna': 'Sul da Bahia (litoral)',
    'Vitória da Conquista': 'Interior da Bahia', 'Feira de Santana': 'Interior da Bahia',
    'Salvador': 'Capitais', 'Recife': 'Capitais', 'Aracaju': 'Capitais',
    'Rio de Janeiro': 'Capitais', 'São Paulo': 'Capitais', 'Curitiba': 'Capitais',
}
CORES_CIDADE = {'Ilhéus': '#2b6cb0', 'Itabuna': '#c05621'}

# ----------------------------------------------------------------------------
# Dicionários de códigos da ficha de tuberculose do SINAN
# ----------------------------------------------------------------------------
MAPA_SEXO = {'M': 'Masculino', 'F': 'Feminino', 'I': 'Ignorado'}
MAPA_RACA = {'1': 'Branca', '2': 'Preta', '3': 'Amarela', '4': 'Parda', '5': 'Indígena', '9': 'Ignorado'}
MAPA_ENTRADA = {'1': 'Caso novo', '2': 'Recidiva', '3': 'Reingresso após abandono',
                '4': 'Não sabe', '5': 'Transferência', '6': 'Pós-óbito'}
MAPA_FORMA = {'1': 'Pulmonar', '2': 'Extrapulmonar', '3': 'Pulmonar + extrapulmonar'}
MAPA_DESFECHO = {'1': 'Cura', '2': 'Abandono', '3': 'Óbito por TB', '4': 'Óbito por outras causas',
                 '5': 'Transferência', '6': 'Mudança de diagnóstico', '7': 'TB-DR',
                 '8': 'Mudança de esquema', '9': 'Falência', '10': 'Abandono primário'}
MAPA_ESCOL = {'0': 'Analfabeto', '1': '1ª-4ª série incompleta', '2': '4ª série completa',
              '3': '5ª-8ª série incompleta', '4': 'Fundamental completo', '5': 'Médio incompleto',
              '6': 'Médio completo', '7': 'Superior incompleto', '8': 'Superior completo',
              '9': 'Ignorado', '10': 'Não se aplica'}
ESCOL_GRUPO = {'0': 'Baixa', '1': 'Baixa', '2': 'Baixa', '3': 'Baixa',
               '4': 'Média/Alta', '5': 'Média/Alta', '6': 'Média/Alta', '7': 'Média/Alta', '8': 'Média/Alta'}
MAPA_BACILO = {'1': 'Positiva', '2': 'Negativa', '3': 'Não realizada', '4': 'Não se aplica'}
MAPA_CULTURA = {'1': 'Positiva', '2': 'Negativa', '3': 'Em andamento', '4': 'Não realizada'}
MAPA_TRM = {'1': 'Detectável sensível à rifampicina', '2': 'Detectável resistente à rifampicina',
            '3': 'Não detectável', '4': 'Inconclusivo', '5': 'Não realizado'}
MAPA_HIV = {'1': 'Positivo', '2': 'Negativo', '3': 'Em andamento', '4': 'Não realizado'}
# TPUNINOT segue a tabela de tipos de estabelecimento do CNES
MAPA_TIPO_UNIDADE = {'1': 'Posto de saúde', '2': 'Centro de saúde / UBS', '4': 'Policlínica',
                     '5': 'Hospital geral', '7': 'Hospital especializado', '15': 'Unidade mista',
                     '20': 'Pronto-socorro geral', '21': 'Pronto-socorro especializado',
                     '22': 'Consultório isolado', '36': 'Clínica / centro de especialidade',
                     '39': 'Unidade de apoio diagnose e terapia', '50': 'Unidade de vigilância em saúde',
                     '62': 'Hospital-dia', '68': 'Central de gestão em saúde', '70': 'CAPS',
                     '71': 'Centro de apoio à saúde da família', '73': 'Pronto atendimento (UPA)'}
SIM_NAO = {'1': 1.0, '2': 0.0}  # 9 (ignorado), 0 e vazio viram NaN

COMORBIDADES = {
    'AGRAVALCOO': 'alcoolismo', 'AGRAVDROGA': 'drogas_ilicitas', 'AGRAVTABAC': 'tabagismo',
    'AGRAVDIABE': 'diabetes', 'AGRAVAIDS': 'aids', 'AGRAVDOENC': 'doenca_mental',
    'POP_RUA': 'situacao_rua', 'POP_LIBER': 'privado_liberdade', 'POP_SAUDE': 'profissional_saude',
    'POP_IMIG': 'imigrante', 'BENEF_GOV': 'beneficiario_governo', 'TRATSUP_AT': 'tdo',
}


def limpa(serie):
    """Remove espaços e transforma texto vazio em NaN (o SINAN grava brancos como ' ')."""
    s = serie.astype(object).where(serie.notna()).astype(str).str.strip()
    return s.where(~s.isin(['', 'nan', 'NaN', 'None', '<NA>']), np.nan)


def sem_zero_esquerda(serie):
    """'01' -> '1', '10' -> '10'."""
    s = limpa(serie)
    return s.str.lstrip('0').mask(lambda x: x == '', '0')


def arquivos_brutos():
    arqs = sorted(glob.glob(str(RAW / '**' / 'TUBEBR*.csv'), recursive=True))
    if not arqs:
        raise FileNotFoundError('Nenhum TUBEBR*.csv encontrado em data/raw/')
    return arqs


# ----------------------------------------------------------------------------
# População (estimativas IBGE / Censo 2022) — ver notebook 09
# ----------------------------------------------------------------------------
def carrega_populacao():
    caminho = EXTERNAL / 'populacao_municipios_2014_2024.csv'
    pop = pd.read_csv(caminho, dtype={'cod6': str})
    return pop


def pop_cidade_ano(pop, cod6, ano):
    v = pop.loc[(pop['cod6'] == cod6) & (pop['ano'] == ano), 'populacao']
    return float(v.iloc[0]) if len(v) else np.nan


# ----------------------------------------------------------------------------
# Estatística
# ----------------------------------------------------------------------------
def ic_proporcao(k, n, alpha=0.05):
    """IC de Wilson para uma proporção, em %."""
    if n == 0:
        return (np.nan, np.nan)
    z = stats.norm.ppf(1 - alpha / 2)
    p = k / n
    den = 1 + z ** 2 / n
    centro = (p + z ** 2 / (2 * n)) / den
    meia = z * np.sqrt(p * (1 - p) / n + z ** 2 / (4 * n ** 2)) / den
    return (100 * (centro - meia), 100 * (centro + meia))


def taxa_100k(casos, pop, alpha=0.05):
    """Taxa por 100 mil com IC exato de Poisson."""
    if not pop or np.isnan(pop):
        return (np.nan, np.nan, np.nan)
    lo = stats.chi2.ppf(alpha / 2, 2 * casos) / 2 if casos > 0 else 0.0
    hi = stats.chi2.ppf(1 - alpha / 2, 2 * (casos + 1)) / 2
    return (casos / pop * 1e5, lo / pop * 1e5, hi / pop * 1e5)


def fisher_2x2(a, b, c, d):
    """Tabela [[a, b], [c, d]] (linha = grupo, coluna = evento sim/não).

    Retorna OR, IC 95% (Woolf, com correção de 0,5 se houver zero) e p do teste exato de Fisher.
    """
    _, p = stats.fisher_exact([[a, b], [c, d]])
    aa, bb, cc, dd = (x + 0.5 for x in (a, b, c, d)) if min(a, b, c, d) == 0 else (a, b, c, d)
    or_ = (aa * dd) / (bb * cc)
    se = np.sqrt(1 / aa + 1 / bb + 1 / cc + 1 / dd)
    return or_, np.exp(np.log(or_) - 1.96 * se), np.exp(np.log(or_) + 1.96 * se), p


def compara_grupos(df, grupo_col, evento_col, grupo_a, grupo_b):
    """Compara a proporção de evento (0/1) entre dois grupos com Fisher. NaN é excluído."""
    sub = df[df[grupo_col].isin([grupo_a, grupo_b]) & df[evento_col].notna()]
    ga = sub[sub[grupo_col] == grupo_a][evento_col]
    gb = sub[sub[grupo_col] == grupo_b][evento_col]
    a, b = int(ga.sum()), int((1 - ga).sum())
    c, d = int(gb.sum()), int((1 - gb).sum())
    or_, lo, hi, p = fisher_2x2(a, b, c, d)
    return {
        f'n {grupo_a}': a + b, f'% {grupo_a}': 100 * a / (a + b) if a + b else np.nan,
        f'n {grupo_b}': c + d, f'% {grupo_b}': 100 * c / (c + d) if c + d else np.nan,
        'OR': or_, 'IC95% inf': lo, 'IC95% sup': hi, 'p (Fisher)': p,
    }


def bonferroni(pvals):
    from statsmodels.stats.multitest import multipletests
    return multipletests(pvals, method='bonferroni')[1]


def fmt_p(p):
    return '<0,001' if p < 0.001 else f'{p:.3f}'.replace('.', ',')


def salva_fig(fig, nome):
    FIGURAS.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURAS / f'{nome}.png', dpi=150, bbox_inches='tight')


# ----------------------------------------------------------------------------
# Carregamento da base analítica (gerada no notebook 09)
# ----------------------------------------------------------------------------
COLS_COD = ['uf_not', 'mun_not', 'uf_res', 'mun_res', 'mun_trat']
COLS_DATA = ['dt_notific', 'dt_diag', 'dt_inic_tr', 'dt_encerra', 'dt_digita']


def carrega_base():
    df = pd.read_csv(PROCESSED / 'tb_base_analitica.csv.gz', dtype={c: str for c in COLS_COD},
                     parse_dates=COLS_DATA, low_memory=False)
    ordem_espera = ['Mesmo dia', '1-7 dias', '8-15 dias', '16-30 dias', 'Mais de 30 dias']
    df['espera_tratamento'] = pd.Categorical(df['espera_tratamento'], categories=ordem_espera, ordered=True)
    rotulos = [f'{i}-{i+4}' for i in range(0, 80, 5)] + ['80+']
    df['faixa_etaria'] = pd.Categorical(df['faixa_etaria'], categories=rotulos, ordered=True)
    return df


def residentes_ii(df, anos=(2014, 2024)):
    """Registros de residentes de Ilhéus e Itabuna diagnosticados no período."""
    m = df['mun_res'].isin([COD_ILHEUS, COD_ITABUNA]) & df['ano_diag'].between(*anos)
    out = df[m].copy()
    out['cidade'] = out['cidade_res']
    return out


def estilo():
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_theme(style='whitegrid', font_scale=1.0)
    plt.rcParams.update({'figure.dpi': 110, 'axes.titleweight': 'bold', 'axes.titlesize': 12,
                         'axes.spines.top': False, 'axes.spines.right': False})
