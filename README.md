# 📊 Epidemiologia da Tuberculose (Ilhéus e Itabuna): Uma Abordagem de Ciência de Dados
Este projeto aplica técnicas de Ciência de Dados e Estatística Inferencial para analisar o panorama epidemiológico da Tuberculose (TB) na região de Ilhéus e Itabuna (Bahia), utilizando dados reais de saúde pública (2014-2024). O objetivo principal é identificar gargalos logísticos, mapear vulnerabilidades sociais e fornecer insights acionáveis para o aprimoramento de políticas públicas no Sistema Único de Saúde (SUS).

# 🎯 Objetivos do Projeto:
* Desenvolver um pipeline de Engenharia de Dados para extração, limpeza e consolidação de mais de uma década de registos do SINAN (Sistema de Informação de Agravos de Notificação).
* Identificar o perfil demográfico e socioeconómico de maior vulnerabilidade à doença.
* Avaliar a eficácia da política de Tratamento Diretamente Observado (TDO).
* Mapear o impacto das comorbilidades (especialmente o alcoolismo) nas taxas de abandono do tratamento.

# 📈 Principais Descobertas e Insights:

1. O Rosto da Vulnerabilidade Social

A Tuberculose na região possui um recorte social e demográfico muito bem definido. A análise revelou que a esmagadora maioria dos pacientes enquadra-se no perfil de homens adultos, autodeclarados pardos e com o ensino fundamental incompleto ou analfabetos.
Este cenário comprova que a dificuldade de acesso à educação e a vulnerabilidade laboral são determinantes sociais diretos para a contração da doença.

2. O Impacto Crítico do Alcoolismo

Ao mapear as comorbilidades, o Alcoolismo (17,4%) destacou-se como o agravante mais presente, superando a Diabetes e o HIV/AIDS. Devido à forte hepatotoxicidade da medicação para a TB, que impede o consumo de álcool durante os 6 meses de tratamento, o paciente alcoolista apresenta taxas de abandono estatisticamente superiores, exigindo um acompanhamento psicológico e social dedicado por parte do sistema de saúde.

3. O Ciclo Vicioso e a Subutilização do TDO

    Eficácia vs. Adoção: O Tratamento Diretamente Observado (TDO) demonstrou ser matematicamente eficaz na redução das taxas de abandono (de 16% para 14,4%). No entanto, menos de 8% dos pacientes (apenas 145 num universo de quase 2.000) receberam este acompanhamento supervisionado.

    O Custo do Abandono: A baixa adoção desta política gera um efeito cascata. O projeto identificou quase 500 pacientes classificados como "Recidiva" ou "Reingresso após Abandono". O sistema gasta recursos para os tratar, mas falha na cura definitiva, mantendo estas pessoas presas num ciclo de adoecimento prolongado.

4. Gargalo Logístico: O Perigo da Espera

A análise da diferença temporal entre a data do diagnóstico e o início do tratamento revelou uma logística eficiente para cerca de 80% dos casos (atendidos na primeira semana). Contudo, foi detetado um grave gargalo epidemiológico: mais de 300 pacientes esperaram mais de 1 mês para tomar a primeira dose de medicação.
Tratando-se de uma doença de transmissão aérea, cada dia de atraso representa um elevado risco biológico de proliferação da bactéria na comunidade.

5. O Impacto da Extrema Vulnerabilidade (Moradia e Situação de Rua):

Devido às regras de anonimização e sigilo médico da LGPD que impedem o mapeamento exato por bairro, o projeto utilizou a variável de "Situação de Rua" como proxy de extrema vulnerabilidade espacial e socioeconômica.
Os resultados encontrados foram alarmantes: enquanto os pacientes com moradia apresentam uma taxa de cura de 84% (roçando a meta de ouro de 85% estabelecida pela OMS), os pacientes em situação de rua veem as suas chances de cura despencarem para apenas 41,9%.
Este dado quantifica a impossibilidade prática de um indivíduo sustentar um tratamento agressivo de 6 meses sem acesso a alimentação regular, segurança e teto, evidenciando que o combate à Tuberculose não é apenas um desafio clínico, mas uma urgência intersetorial de Assistência Social e Direitos Humanos.

# 👨‍💻 Autor
Bruno Cardoso de Jesus
🎓 Graduando em Ciência da Computação | Previsão de Conclusão: 2027

🏛️ Universidade Estadual de Santa Cruz (UESC) - Bahia, Brasil
