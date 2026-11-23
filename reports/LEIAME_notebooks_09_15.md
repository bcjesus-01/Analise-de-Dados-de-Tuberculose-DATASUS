# Notebooks 09 a 15 — análise de tuberculose em Ilhéus e Itabuna (2014-2024)

Pergunta: quais fatores sociodemográficos, clínicos e operacionais estão associados ao desfecho desfavorável
(abandono ou óbito) em Ilhéus e Itabuna, e quão longe as cidades estão das metas do MS/OMS?

Ordem de execução (os notebooks 00-08 não foram alterados):

| Notebook | Conteúdo |
|---|---|
| 09_base_analitica_corrigida | Lê os TUBEBR14-24 de `data/raw`, monta a base corrigida e a população anual (Censos 2010-2022) |
| 10_incidencia_e_indicadores | Incidência por 100 mil, indicadores x metas, completude e os gráficos refeitos da reunião |
| 11_testes_ilheus_itabuna | Fisher + Bonferroni, tempo até o tratamento em %, transmissão estimada |
| 12_fatores_desfecho_desfavoravel | Regressão logística (bruta e ajustada), por cidade e sensibilidade |
| 13_temporal_pandemia | Série mensal, esperado x observado na pandemia, queda de 2023 |
| 14_comparativo_cidades | 10 cidades por 100 mil, litoral x interior, mapa e IDH da Bahia, pacientes de fora, quem atende Ilhéus, números publicados |
| 15_analise_consolidada_tuberculose | Resumo executivo e respostas às perguntas da reunião |

Dependências: pandas, numpy, matplotlib, seaborn, scipy, statsmodels, scikit-learn, geopandas.
`data/processed/tb_base_analitica.csv.gz` é gerado pelo 09; os demais notebooks leem dele.
Funções comuns ficam em `src/tb_utils.py`. Figuras são salvas em `reports/figuras`.
