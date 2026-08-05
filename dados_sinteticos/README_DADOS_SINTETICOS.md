# Dados sintéticos do pipeline (versão 2 — 21/10/2026)

Os arquivos `00_inscricoes_anonimizadas.parquet` e `00_resultados_anonimizados.parquet` da raiz do repositório são **inteiramente sintéticos**. Eles foram gerados por [`gerar_dados_sinteticos.py`](gerar_dados_sinteticos.py) e substituem a versão anterior, que reutilizava registros reais com chaves trocadas (problema apontado em auditoria externa).

## Como foram gerados

| Elemento | Origem |
|---|---|
| Pessoas, datas de nascimento, datas/horas de inscrição, acessos, tempo de tela, nota, progresso, IDs | **Sorteados** de distribuições paramétricas (semente fixa `2026`) |
| Cursos (código, nome, carga horária), municípios do ES e SRE de cada município | Vocabulário institucional em [`vocabulario_institucional.json`](vocabulario_institucional.json) |
| Frequências de sexo, escolaridade, cargo, função e tipo de instituição | Frequências agregadas no mesmo JSON |
| Proporções estruturais | Estatísticas agregadas publicadas no artigo e nos notebooks (tabela abaixo) |

Nenhuma linha, chave, data ou timestamp foi copiada da base real. O JSON não contém dados pessoais.

Para regenerar os arquivos (o resultado é idêntico com a mesma semente):

```bash
python dados_sinteticos/gerar_dados_sinteticos.py --saida .
```

## Validação (21/10/2026)

**Fidelidade estrutural**

| Indicador | Sintético | Referência (base real, agregado) |
|---|---|---|
| Linhas | 5.010 inscrições (2.100 pessoas) / 3.739 registros Moodle | — |
| Nota final ausente | 56,2% | 56,06% |
| "Cálculo indisponível" no tempo de acesso | 82,8% | 81,6% |
| Status: logs ausentes / com logs / nunca acessou | 65,9% / 17,2% / 16,9% | 64,8% / 18,4% / 16,9% |
| Inscrições com registro no Moodle | 63,5% | 63,9% |
| Inscrições por pessoa | 2,37 | ≈ 2,4 |
| Tentativas por inscrição (1 / 2 / 4 / 8) | 3.071 / 18 / 144 / 7 | concentradas em 1 e 4 |
| Spearman nota × progresso | 0,61 | 0,48 |

**Privacidade.** Comparação com os arquivos anteriores, que continham valores reais:
- 0 IDs coincidentes.
- 0 valores de `datahora_inscricao` coincidentes.
- 0 combinações (curso, data/hora, sexo, município, cargo) coincidentes.
- 0 combinações Moodle (curso, 1º acesso, último acesso, tempo, progresso) coincidentes.

As únicas coincidências isoladas são valores genéricos: rótulos como "Cálculo indisponível" e 79 datas de nascimento que caem no mesmo dia do calendário por acaso.

**Execução.** Os notebooks 01 a 08 do repositório público rodaram em sequência **sem erros** com estes arquivos: ABT com 2.364 inscrições, Rota A com 4 clusters e Rota B com 303 casos.

## Limitações (declarar no README)

- Os dados **não reproduzem os resultados numéricos do artigo** (191.412 inscrições, percentuais das personas, IEEP). Servem para executar e inspecionar o código, não para inferência.
- A estrutura de clusters obtida é diferente da publicada. Como os notebooks 05, 07 e 08 atribuem os nomes das personas pelo número do cluster, os rótulos podem sair trocados. Isso é um defeito conhecido do código, não dos dados.
- Os arquivos mantêm os nomes `*_anonimizadas.parquet` só por compatibilidade com os notebooks. O nome correto é "sintéticos".

## Texto sugerido para o README (substitui o parágrafo atual sobre os dados)

> Em cumprimento à LGPD, os microdados originais não são disponibilizados. Os arquivos `00_inscricoes_anonimizadas.parquet` (5.010 linhas) e `00_resultados_anonimizados.parquet` (3.739 linhas) são **inteiramente sintéticos**, gerados por `dados_sinteticos/gerar_dados_sinteticos.py` a partir de distribuições paramétricas e de frequências agregadas, sem reutilizar nenhum registro, chave ou data da base real. Eles reproduzem a estrutura e proporções gerais da base (ex.: 56% de notas ausentes, ~82% de tempo de acesso indisponível, ~64% de casamento SGF × Moodle), mas **não reproduzem os resultados numéricos do artigo** e servem apenas para executar o pipeline.
