# Segmentação de Perfis de Participação em Formações Continuadas (SBIE 2026)

Este repositório contém o pipeline completo de *Knowledge Discovery in Databases* (KDD) desenvolvido para o artigo **"Segmentação de perfis de participação em formações continuadas por clusterização a partir de microdados educacionais do SGF e Moodle"**, aceito e publicado no **Simpósio Brasileiro de Informática na Educação (SBIE) 2026**.

## ⚖️ Ética e Proteção de Dados (LGPD)

A pesquisa foi devidamente autorizada pela **Secretaria da Educação do Espírito Santo (SEDU/ES)** e aprovada pelo **Comitê de Ética em Pesquisa (CEP) do IFES**, sob o Certificado de Apresentação para Apreciação Ética (**CAAE: 94696925.5.0000.5072**). 

Em cumprimento à LGPD, os microdados originais não são disponibilizados. Os arquivos `00_inscricoes_anonimizadas.parquet` (5.010 linhas) e `00_resultados_anonimizados.parquet` (3.739 linhas) são **inteiramente sintéticos**, gerados por [`dados_sinteticos/gerar_dados_sinteticos.py`](dados_sinteticos/gerar_dados_sinteticos.py) a partir de distribuições paramétricas e de frequências agregadas, sem reutilizar nenhum registro, chave ou data da base real. Eles reproduzem a estrutura e proporções gerais da base (ex.: 56% de notas ausentes, ~82% de tempo de acesso indisponível, ~64% de casamento SGF × Moodle), mas **não reproduzem os resultados numéricos do artigo** e servem apenas para executar o pipeline.

Para regenerar os arquivos (resultado idêntico com a semente fixa `2026`):

```bash
python dados_sinteticos/gerar_dados_sinteticos.py --saida .
```

**Limitações dos dados sintéticos**
* Não reproduzem os resultados numéricos do artigo (191.412 inscrições, percentuais das personas, IEEP). Servem para executar e inspecionar o código, não para inferência.
* A estrutura de clusters obtida difere da publicada. Como os notebooks 05, 07 e 08 atribuem os nomes das personas pelo número do cluster, os rótulos podem sair trocados. É uma limitação do código, não dos dados.
* Os arquivos mantêm o sufixo `_anonimizadas`/`_anonimizados` apenas por compatibilidade com os notebooks; o conteúdo é sintético.
* As saídas salvas nos notebooks correspondem à execução com a base original e aos valores relatados no artigo. Nelas, identificadores individuais aparecem mascarados (`MASCARADO_NNNNNN`) e datas/horas de amostras aparecem agregadas por mês.

Detalhes do método e da validação (fidelidade estrutural e testes de privacidade): [`dados_sinteticos/README_DADOS_SINTETICOS.md`](dados_sinteticos/README_DADOS_SINTETICOS.md).

---

## 📁 Estrutura do Repositório e Instalação Local

Os dados sintéticos, o gerador e os notebooks já estão organizados na raiz do repositório, prontos para execução sequencial:

```text
pipeline/
├── 00_inscricoes_anonimizadas.parquet     # Dataset sintético de inscrições (SGF)
├── 00_resultados_anonimizados.parquet     # Dataset sintético de resultados (Moodle)
├── 01_analise_exploratoria_inscricoes.ipynb
├── 02_analise_exploratoria_resultados.ipynb
├── 03_limpeza_inscricoes.ipynb
├── 04_limpeza_resultados_merge.ipynb
├── 05_modelagem_rota_B_VF_artigo.ipynb
├── 06_modelagem_rota_A_VF_artigo.ipynb
├── 07_analise_geoespacial_rota_B_VF_artigo.ipynb
├── 08_tabelas_descritivas_estatistica_rotas_B_A_VF_artigo.ipynb
├── Discu_Carga_PCA.md                     # Material Suplementar: Cargas do PCA (Rotas A e B)
├── Tabelas_triangulacao.md                # Material Suplementar: Triangulação de Métricas (k=2 a 8)
├── artigo_SBIE2026.pdf                     # Artigo publicado no SBIE 2026 (PDF)
├── dados_sinteticos/
│   ├── gerar_dados_sinteticos.py          # Gerador dos dois arquivos 00_*.parquet
│   ├── vocabulario_institucional.json     # Cursos, municípios/SRE e frequências agregadas
│   └── README_DADOS_SINTETICOS.md         # Método e validação dos dados sintéticos
├── requirements.txt                       # Dependências do projeto
├── .gitignore                             # Regras de exclusão do Git
├── LICENSE                                # MIT (código) + CC BY 4.0 (dados e textos)
└── README.md
```

### 💻 Instalação em Ambiente Local

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/FormacaoPerfis/pipeline.git
   cd pipeline
   ```

2. **Crie e ative um ambiente virtual (Python 3.9+):**
   ```bash
   # Windows (PowerShell):
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # Linux / macOS:
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie o Jupyter ou abra no VS Code:**
   ```bash
   jupyter lab
   ```

> [!NOTE]
> Todos os notebooks possuem detecção automática de ambiente, funcionando perfeitamente de forma nativa tanto em ambientes locais (VS Code, Jupyter) quanto no Google Colab, criando automaticamente os diretórios de saída (`dados_output/`).

---

## 🚀 Guia de Execução e Saídas Detalhadas (Pipeline KDD)

A execução deve seguir rigorosamente a ordem numérica, pois os artefatos gerados em uma etapa são dependências diretas da etapa seguinte.

### Fase 1: Análise Exploratória de Dados (EDA)
* **`01_analise_exploratoria_inscricoes.ipynb`**
  * **Objetivo:** Explorar distribuição demográfica, escolaridade e eixos de atuação no SGF.
  * **Saída:** Relatórios de esparsidade e gráficos de contagem demográfica.
* **`02_analise_exploratoria_resultados.ipynb`**
  * **Objetivo:** Analisar engajamento, notas e tempo de tela no Moodle.
  * **Saída:** Gráficos de distribuição de notas e identificação de outliers de tempo.

### Fase 2: Saneamento e Engenharia de Features
* **`03_limpeza_inscricoes.ipynb`**
  * **Objetivo:** Tratamento de nulos (MNAR), consolidação de duplicatas (Golden Record), winsorização de carga horária, criação de Macro Cargos e imputação geoespacial via API do IBGE.
  * **Saída:** `03_inscricoes_tratadas.parquet`.
* **`04_limpeza_resultados_merge.ipynb`**
  * **Objetivo:** Escalonamento logarítmico de tempo, tratamento da evasão (Shadow Matrix) e o *Inner Join* definitivo entre SGF e Moodle.
  * **Saída:** `matriz_analitica_kdd_final.parquet`.

### Fase 3: Modelagem Não-Supervisionada (K-Means & PCA)
* **`05_modelagem_rota_B_VF_artigo.ipynb`**
  * **Objetivo:** Modelagem da **Rota B** (Engajamento Estrito - excluindo evasões). Otimização do K ótimo via Cotovelo e Silhueta.
  * **Saída:** Gráficos heurísticos de validação interna de clusters.
* **`06_modelagem_rota_A_VF_artigo.ipynb`**
  * **Objetivo:** Modelagem da **Rota A** (Rede Global - incluindo evasões). Aplicação de PCA (retenção de 95%), revalidação geométrica e particionamento definitivo (K=4).
  * **Saídas:** 
    * Base rotulada: `matriz_rota_a_clusterizada_final.csv`.
    * Figuras (300dpi): `rota_a_revalidacao_pca_vertical_300dpi.png`, `rota_a_painel_3d_2d_percentuais_legenda_refinado_300dpi.png`, `rota_a_boxplots_profiling_vertical_espacamento_final_300dpi.png`.
    * Código LaTeX das cargas do PCA para o artigo.

### Fase 4: Pós-Processamento e Contexto Espacial
* **`07_analise_geoespacial_rota_B_VF_artigo.ipynb`**
  * **Objetivo:** Mapeamento da distribuição territorial dos clusters encontrados, cruzando com as Superintendências Regionais de Educação (SREs).
  * **Saída:** Mapas de calor territorial e tabelas de capilaridade.
* **`08_tabelas_descritivas_estatistica_rotas_B_A_VF_artigo.ipynb`**
  * **Objetivo:** Geração das tabelas descritivas finais (medianas e notas por perfil) das Rotas B e A.
  * **Saída:** Código LaTeX das tabelas descritivas usadas no manuscrito do SBIE.

---

## 📄 Materiais Suplementares Citados no Artigo

Em atendimento às notas de rodapé da publicação no SBIE 2026, disponibilizam-se as tabelas analíticas completas que subsidiaram a discussão metodológica:

* **Tabelas de Triangulação de Métricas ($k = 2$ a $8$):**
  * Acesse: [`Tabelas_triangulacao.md`](Tabelas_triangulacao.md)
  * Contém a varredura sistemática dos coeficientes de Silhueta, Calinski-Harabasz e Davies-Bouldin para a **Rota B** (*Nota de Rodapé 2, p. 837*) e para a **Rota A** (*Nota de Rodapé 5, p. 840*).

* **Tabelas de Cargas dos Componentes Principais (PCA):**
  * Acesse: [`Discu_Carga_PCA.md`](Discu_Carga_PCA.md)
  * Contém a matriz completa de correlação linear das variáveis com os 7 componentes da **Rota B** (*Nota de Rodapé 3, p. 838*) e os 5 componentes da **Rota A** (*Nota de Rodapé 4, p. 840*).

---

## 📚 Como Citar este Trabalho

O artigo completo publicado nos Anais do SBIE 2026 está disponível diretamente no repositório:
* 📄 **[Download do Artigo em PDF](artigo_SBIE2026.pdf)**

```bibtex
@inproceedings{andrade2026segmentacao,
  title     = {Segmenta{\c{c}}{\~a}o de perfis de participa{\c{c}}{\~a}o em forma{\c{c}}{\~o}es continuadas por clusteriza{\c{c}}{\~a}o a partir de microdados educacionais do SGF e Moodle},
  author    = {Andrade, Leonardo Cruz de and Souza, Sandro Ricardo de and Carletti Neto, Almir and Sim{\~o}es, S{\'e}rgio Nery},
  booktitle = {Anais do XXXVII Simp{\'o}sio Brasileiro de Inform{\'a}tica na Educa{\c{c}}{\~a}o (SBIE 2026)},
  pages     = {832--848},
  year      = {2026},
  doi       = {10.5753/sbie.2026.27342},
  publisher = {SBC}
}
```

---

## 📜 Licença

O código (notebooks e gerador de dados) é distribuído sob a licença **MIT**. Os dados sintéticos, a documentação e os materiais suplementares estão sob **CC BY 4.0**. Veja [`LICENSE`](LICENSE).

---
*Pesquisa desenvolvida com rigor ético e metodológico para o Simpósio Brasileiro de Informática na Educação (SBIE) 2026.*
