# Dados sintéticos do pipeline

Os arquivos `00_inscricoes_anonimizadas.parquet` e `00_resultados_anonimizados.parquet` da raiz do repositório são **inteiramente sintéticos**, gerados por [`gerar_dados_sinteticos.py`](gerar_dados_sinteticos.py).

## Como foram gerados

| Elemento | Origem |
|---|---|
| Pessoas, datas de nascimento, datas/horas de inscrição, acessos, tempo de tela, nota, progresso, IDs | **Sorteados** de distribuições paramétricas (semente fixa `2026`) |
| Cursos (código, nome, carga horária), municípios do ES e SRE de cada município | Vocabulário institucional em [`vocabulario_institucional.json`](vocabulario_institucional.json) |
| Frequências de sexo, escolaridade, cargo, função e tipo de instituição | Frequências agregadas no mesmo JSON |
| Proporções estruturais | Estatísticas agregadas publicadas no artigo e nos notebooks (tabela abaixo) |

Nenhuma linha, chave, data ou timestamp foi copiada da base real: todo valor individual é sorteado pelo script, e a única entrada externa é o JSON, que contém apenas vocabulário institucional e frequências agregadas, sem dados pessoais.

Para regenerar os arquivos (o resultado é idêntico com a mesma semente):

```bash
python dados_sinteticos/gerar_dados_sinteticos.py --saida .
```

## Validação

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

**Execução.** Os notebooks 01 a 08 deste repositório rodam em sequência **sem erros** com estes arquivos: ABT com 2.364 inscrições, Rota A com 4 clusters e Rota B com 303 casos.

## Limitações

- Os dados **não reproduzem os resultados numéricos do artigo** (191.412 inscrições, percentuais das personas, IEEP). Servem para executar e inspecionar o código, não para inferência.
- A estrutura de clusters obtida é diferente da publicada. Como os notebooks 05, 07 e 08 atribuem os nomes das personas pelo número do cluster, os rótulos podem sair trocados. Isso é uma limitação do código, não dos dados.
- Os arquivos mantêm os nomes `*_anonimizadas.parquet` só por compatibilidade com os notebooks; o conteúdo é sintético.
