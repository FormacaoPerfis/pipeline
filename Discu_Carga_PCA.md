# Material Suplementar — Cargas dos Componentes Principais (PCA)

Este documento complementa o artigo *"Segmentação de perfis de participação em formações continuadas por clusterização a partir de microdados educacionais do SGF e Moodle"*, disponibilizando as tabelas completas de cargas dos componentes principais (PCA) referenciadas no texto.

## Tabela A — Cargas dos Componentes Principais (PCA) - Rota B (Engajamento Validado)

O modelo PCA da Rota B submete 8 variáveis padronizadas (Z-Score) ao PCA com critério de retenção de 95% da variância acumulada, resultando em 7 componentes principais retidos (PC1 a PC7).

| Variável | PC1 | PC2 | PC3 | PC4 | PC5 | PC6 | PC7 |
|---|---|---|---|---|---|---|---|
| Idade | -0,000 | 0,300 | 0,307 | 0,517 | 0,673 | -0,309 | -0,014 |
| Escolaridade_Ordinal | -0,072 | 0,562 | 0,297 | -0,034 | -0,007 | 0,767 | -0,019 |
| qtd_tentativas | -0,223 | 0,127 | -0,115 | 0,748 | -0,597 | -0,040 | 0,051 |
| progresso_kdd | **0,631** | 0,219 | -0,226 | 0,058 | -0,033 | 0,013 | 0,007 |
| nota_final_kdd | **0,638** | 0,142 | -0,240 | 0,132 | -0,040 | 0,030 | -0,011 |
| minutos_totais_log1p | **0,268** | -0,453 | 0,463 | 0,167 | -0,031 | 0,203 | 0,663 |
| dias_permanencia_log1p | **0,262** | -0,193 | 0,614 | 0,029 | -0,271 | -0,089 | -0,660 |
| dias_duracao_curso | 0,023 | 0,517 | 0,324 | -0,350 | -0,338 | -0,514 | 0,350 |

**Fonte:** Elaborado pelos autores (2026), extraído fielmente de [`05_modelagem_rota_B_VF_artigo.ipynb`](05_modelagem_rota_B_VF_artigo.ipynb).  
**Nota:** Valores indicam a correlação linear entre as variáveis originais e os componentes principais retidos. Em negrito estão destacadas as variáveis com forte projeção no PC1 (dimensão de desempenho educacional).

---

## Tabela B — Cargas dos Componentes Principais (PCA) - Rota A (Rede Global)

O modelo PCA da Rota A submete 7 variáveis padronizadas (Z-Score) ao PCA com critério de retenção de 95% da variância acumulada, resultando em 5 componentes principais retidos (PC1 a PC5).

| Variável | PC1 | PC2 | PC3 | PC4 | PC5 |
|---|---|---|---|---|---|
| Idade | 0,023 | -0,001 | 0,733 | -0,011 | -0,680 |
| Escolaridade_Ordinal | -0,081 | -0,181 | 0,667 | 0,032 | 0,716 |
| qtd_tentativas | 0,002 | -0,111 | -0,028 | 0,992 | -0,045 |
| nota_final_kdd | **0,542** | -0,447 | -0,039 | -0,050 | -0,022 |
| progresso_kdd | **0,538** | -0,455 | -0,030 | -0,056 | -0,012 |
| minutos_totais_log1p | **0,459** | 0,519 | 0,060 | 0,066 | 0,077 |
| dias_permanencia_log1p | **0,445** | 0,528 | 0,106 | 0,063 | 0,129 |

**Fonte:** Elaborado pelos autores (2026), extraído fielmente de [`06_modelagem_rota_A_VF_artigo.ipynb`](06_modelagem_rota_A_VF_artigo.ipynb).  
**Nota:** Valores indicam a correlação linear entre as variáveis originais e os componentes principais retidos. Em negrito estão destacadas as variáveis de maior projeção no PC1.
