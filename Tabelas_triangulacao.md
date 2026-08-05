# Material Suplementar — Triangulação de Métricas de Validação Interna

Este documento complementa o artigo *"Segmentação de perfis de participação em formações continuadas por clusterização a partir de microdados educacionais do SGF e Moodle"*, disponibilizando as tabelas completas de triangulação de métricas de validação interna (varredura sistemática de k = 2 a 8) referenciadas no texto.

## Tabela A — Triangulação de Métricas de Validação Interna para a Rota B (espaço PCA)

| k | Silhueta (Máx) | Calinski-Harabasz (Máx) | Davies-Bouldin (Mín) |
|---|---|---|---|
| **2** | **0,3770** | 8645,0 | 1,2835 |
| 3 | 0,2508 | 8723,6 | 1,5491 |
| 4 | 0,2609 | 9480,3 | 1,2464 |
| 5 | 0,2600 | 10258,1 | 1,1792 |
| 6 | 0,2785 | **10573,0** | **1,1275** |
| 7 | 0,2694 | 10278,8 | 1,1583 |
| 8 | 0,2443 | 9783,5 | 1,1727 |

**Fonte:** Elaborado pelos autores (2026).
**Nota:** Valores de Silhueta e Calinski-Harabasz buscam maximização; Davies-Bouldin busca minimização. A linha em destaque (k = 2) indica a solução adotada, com melhor Silhueta; a linha k = 6 indica o segundo polo de otimização (melhor Calinski-Harabasz e Davies-Bouldin), descartado por fragmentar excessivamente os perfis (ver discussão na Seção de Resultados).

---

## Tabela B — Triangulação de Métricas de Validação Interna - Rota A (Espaço PCA)

| k | Silhueta (Máx) | Calinski-Harabasz (Máx) | Davies-Bouldin (Mín) |
|---|---|---|---|
| 2 | 0,3518 | 76250,3 | 1,2567 |
| 3 | 0,4260 | 93384,3 | 0,9776 |
| **4** | **0,4533** | **111918,7** | **0,7790** |
| 5 | 0,3793 | 103583,3 | 0,9205 |
| 6 | 0,3308 | 100063,5 | 1,0401 |
| 7 | 0,3701 | 96454,7 | 0,9198 |
| 8 | 0,3358 | 95212,2 | 1,0702 |

**Fonte:** Elaborado pelos autores (2026).
**Nota:** A linha destacada em negrito (k = 4) indica o desempenho ótimo simultâneo nas três métricas, convergindo como a solução adotada para a Rota A.
