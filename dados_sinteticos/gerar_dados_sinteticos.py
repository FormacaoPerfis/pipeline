"""Gerador de dados sinteticos para o pipeline KDD (SBIE 2026).

Gera os dois arquivos de entrada do pipeline:
    00_inscricoes_anonimizadas.parquet  (SGF)
    00_resultados_anonimizados.parquet  (Moodle)

Principios
----------
1. Nenhum registro, chave, data ou timestamp e copiado da base real. Todo valor individual
   (pessoa, data de nascimento, data/hora de inscricao, acessos, tempo, nota, progresso) e
   SORTEADO de distribuicoes parametricas com semente fixa.
2. A unica entrada externa e `vocabulario_institucional.json`: lista de cursos (codigo, nome,
   carga horaria), municipios do ES com a SRE correspondente e frequencias agregadas de
   categorias (sexo, escolaridade, cargo, funcao, tipo de instituicao). Nao ha dado pessoal.
3. Os parametros estruturais reproduzem estatisticas AGREGADAS publicadas no artigo e nos
   notebooks (ex.: 56% de nota ausente; ~65% "logs de atividade ausentes"; ~64% das inscricoes
   com registro no Moodle; ~2,4 inscricoes por pessoa; tentativas concentradas em 1 e 4),
   para que o pipeline execute e produza estruturas qualitativamente semelhantes.
4. Os dados NAO reproduzem os resultados numericos do artigo e nao devem ser usados para
   inferencia substantiva: servem apenas para executar e inspecionar o codigo.

Uso:  python gerar_dados_sinteticos.py [--n-pessoas 2100] [--semente 2026] [--saida .]
"""
import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent

# ---------------------------------------------------------------- parametros agregados
P_SEM_MOODLE = 0.36            # inscricoes sem registro no Moodle (real: ~36%)
P_ORFAOS_MOODLE = 0.02         # registros Moodle sem inscricao correspondente no SGF
P_DUP_INSCRICAO = 0.005        # linhas duplicadas no SGF (testa o Golden Record do NB03)
P_STATUS = {                   # status_geral entre registros Moodle
    'Nunca acessou a formação': 0.17,
    'Acessou (logs de atividade ausentes)': 0.65,
    'Acessou (com logs de atividade)': 0.18,
}
P_NOTA_AUSENTE = {             # calibrado para ~56% de nota ausente no total
    'Nunca acessou a formação': 0.97,
    'Acessou (logs de atividade ausentes)': 0.54,
    'Acessou (com logs de atividade)': 0.25,
}
TENTATIVAS = ([1, 2, 4, 8], [0.95, 0.006, 0.042, 0.002])  # linhas Moodle por inscricao
P_NULO_SRE, P_NULO_MUN, P_NULO_FUNCIONAL = 0.08, 0.04, 0.016
P_LOGS_EXPURGADOS = 0.10       # primeiro_acesso com aviso de expurgo de logs
P_SEM_TERMINO = 0.006
DIAS = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
TURNOS = ['Madrugada', 'Manhã', 'Tarde', 'Noite']
P_TURNOS = [0.03, 0.37, 0.38, 0.22]
P_DIAS = [0.19, 0.18, 0.19, 0.17, 0.14, 0.05, 0.08]


def escolher(rng, dist, n):
    chaves = list(dist.keys())
    p = np.array(list(dist.values()), dtype=float)
    return rng.choice(chaves, size=n, p=p / p.sum())


def novo_id(rng, prefixo, n, usados):
    ids = []
    while len(ids) < n:
        c = f"{prefixo}{rng.integers(0, 16**8):08X}"
        if c not in usados:
            usados.add(c)
            ids.append(c)
    return ids


def ano_do_curso(codigo, rng):
    m = re.search(r'_(20\d{2})_', codigo)
    return int(m.group(1)) if m else int(rng.integers(2022, 2025))


def gerar(n_pessoas=2100, semente=2026, saida=Path('.')):
    rng = np.random.default_rng(semente)
    voc = json.loads((AQUI / 'vocabulario_institucional.json').read_text(encoding='utf-8'))
    usados = set()

    # ------------------------------------------------------------ calendario dos cursos
    cursos = pd.DataFrame(voc['cursos'])
    cal = {}
    for c in cursos.itertuples():
        ano = ano_do_curso(c.codigo, rng)
        inicio = datetime(ano, 1, 1) + timedelta(days=int(rng.integers(20, 300)))
        duracao = int(rng.choice([30, 45, 60, 90, 120], p=[0.25, 0.2, 0.3, 0.15, 0.1]))
        cal[c.codigo] = (inicio, inicio + timedelta(days=duracao))
    p_curso = cursos['peso'].to_numpy(float)
    p_curso /= p_curso.sum()

    # ------------------------------------------------------------ pessoas
    mun = pd.DataFrame(voc['municipios'])
    pes = pd.DataFrame({'id_discente_anonimo': novo_id(rng, 'DISC_SINT_', n_pessoas, usados)})
    pes['Sexo'] = escolher(rng, voc['sexo'], n_pessoas)
    idade = np.clip(rng.normal(43, 9, n_pessoas), 20, 70)
    nasc = [datetime(2025, 6, 30) - timedelta(days=float(a * 365.25)) for a in idade]
    pes['data_nascimento'] = [d.strftime('%d/%m/%Y') for d in nasc]
    pes['Escolaridade'] = escolher(rng, voc['escolaridade'], n_pessoas)
    pes['Cargo'] = escolher(rng, voc['cargo'], n_pessoas)
    pes['Funcao'] = [escolher(rng, voc['funcao_por_cargo'].get(c, {'PROFESSOR': 1.0}), 1)[0] for c in pes['Cargo']]
    pes['Tipo_Instituicao'] = escolher(rng, voc['tipo_instituicao'], n_pessoas)
    idx_m = rng.choice(len(mun), size=n_pessoas, p=mun['peso'] / mun['peso'].sum())
    pes['Municipio'] = mun['municipio'].to_numpy()[idx_m]
    pes['SRE'] = mun['sre'].to_numpy()[idx_m]
    # engajamento latente da pessoa (induz correlacao entre inscricoes do mesmo cursista)
    pes['engaj'] = rng.normal(0, 1, n_pessoas)

    # ------------------------------------------------------------ inscricoes (SGF)
    n_insc_pessoa = 1 + np.minimum(rng.poisson(1.4, n_pessoas), 7)
    linhas = []
    for p, k in zip(pes.itertuples(index=False), n_insc_pessoa):
        cods = rng.choice(cursos['codigo'], size=k, replace=False, p=p_curso)
        for cod in cods:
            linhas.append((p.id_discente_anonimo, cod))
    ins = pd.DataFrame(linhas, columns=['id_discente_anonimo', 'Nome_Breve'])
    ins = ins.merge(pes, on='id_discente_anonimo', how='left')
    ins = ins.merge(cursos.rename(columns={'codigo': 'Nome_Breve', 'nome': 'Nome_Formacao'})[
        ['Nome_Breve', 'Nome_Formacao', 'carga_horaria']], on='Nome_Breve', how='left')
    n = len(ins)
    ins['id_inscricoes'] = novo_id(rng, 'INSC_SINT_', n, usados)
    # carga horaria: valor do curso com outliers raros de digitacao (testa a winsorizacao do NB03)
    outl = rng.random(n) < 0.01
    ins.loc[outl, 'carga_horaria'] = ins.loc[outl, 'carga_horaria'] * rng.integers(5, 12, outl.sum())
    # data/hora de inscricao: ate 25 dias antes do inicio do curso, com milissegundos
    dh = []
    for cod in ins['Nome_Breve']:
        ini = cal[cod][0]
        t = ini - timedelta(days=float(rng.uniform(0, 25)), seconds=float(rng.uniform(0, 86400)))
        dh.append(t.strftime('%d/%m/%Y %H:%M:%S.') + f"{int(rng.integers(0, 1000)):03d}")
    ins['datahora_inscricao'] = dh
    # ausencias (padroes do SGF)
    ins.loc[rng.random(n) < P_NULO_SRE, 'SRE'] = None
    ins.loc[rng.random(n) < P_NULO_MUN, 'Municipio'] = None
    nf = rng.random(n) < P_NULO_FUNCIONAL
    ins.loc[nf, ['Cargo', 'Funcao', 'Tipo_Instituicao']] = None

    # ------------------------------------------------------------ resultados (Moodle)
    com_moodle = ins[rng.random(n) >= P_SEM_MOODLE].copy()
    m = len(com_moodle)
    status = rng.choice(list(P_STATUS), size=m, p=list(P_STATUS.values()))
    eng = com_moodle['engaj'].to_numpy() + rng.normal(0, 0.8, m)
    reg = []
    for row, st, e in zip(com_moodle.itertuples(index=False), status, eng):
        ini, fim = cal[row.Nome_Breve]
        dur = (fim - ini).days
        r = {
            'id_inscricoes': row.id_inscricoes,
            'nome_do_curso': row.Nome_Formacao,
            'nome_curto_do_curso': row.Nome_Breve,
            'data_inicio_formacao': ini.strftime('%Y-%m-%d'),
            'data_termino_formacao': 'Sem data de término' if rng.random() < P_SEM_TERMINO else fim.strftime('%Y-%m-%d'),
            'status_geral': st,
            'id_discente_anonimo': row.id_discente_anonimo,
        }
        r['id_resultados'] = f"{row.Nome_Breve}_{row.id_discente_anonimo}"
        # nota e progresso
        sem_nota = rng.random() < P_NOTA_AUSENTE[st]
        bom = rng.random() < 1 / (1 + np.exp(-(1.6 + 1.2 * e)))  # P(alto desempenho) ~ 0,8
        if st == 'Nunca acessou a formação':
            prog = 0.0
        elif bom:
            prog = 100.0 if rng.random() < 0.9 else float(rng.uniform(60, 100))
        else:
            prog = float(rng.uniform(5, 90))
        if sem_nota:
            nota = np.nan
        elif bom:
            nota = float(np.clip(100 - rng.gamma(1.6, 5.5), 60, 100))
        else:
            nota = float(np.clip(rng.normal(32, 18), 0, 85))
        r['progresso_na_formacao'] = f"{prog:.2f}%"
        r['nota_final_na_formacao'] = nota
        # acessos e tempo de tela
        if st == 'Nunca acessou a formação':
            r.update(primeiro_acesso='N/A (sem logs)', ultimo_acesso='Nunca acessou',
                     tempo_total_de_acesso='Cálculo indisponível', periodo_de_maior_acesso='Cálculo indisponível')
        else:
            t1 = ini + timedelta(days=float(rng.uniform(0, max(dur * 0.3, 1))), seconds=float(rng.uniform(0, 86400)))
            perm = float(np.clip(rng.gamma(1.3, 9 + 6 * max(e, -1)), 0, dur + 20))
            t2 = t1 + timedelta(days=perm, seconds=float(rng.uniform(0, 3600)))
            r['ultimo_acesso'] = t2.strftime('%Y-%m-%d %H:%M:%S')
            if st == 'Acessou (com logs de atividade)':
                p1 = t1.strftime('%Y-%m-%d %H:%M:%S')
                if rng.random() < P_LOGS_EXPURGADOS:
                    p1 += ' (logs anteriores podem ter sido expurgados)'
                r['primeiro_acesso'] = p1
                minutos = float(np.exp(rng.normal(6.2 + 0.45 * e + (0.5 if bom else 0), 0.9)))
                h, resto = divmod(int(minutos * 60), 3600)
                mi, s = divmod(resto, 60)
                r['tempo_total_de_acesso'] = f"{h}h {mi:02d}m {s}s"
                r['periodo_de_maior_acesso'] = f"{rng.choice(DIAS, p=P_DIAS)} ({rng.choice(TURNOS, p=P_TURNOS)})"
            else:
                r.update(primeiro_acesso='N/A (sem logs)', tempo_total_de_acesso='Cálculo indisponível',
                         periodo_de_maior_acesso='Cálculo indisponível')
        reg.append(r)
    res = pd.DataFrame(reg)

    # tentativas: linhas repetidas por inscricao (re-extracoes do Moodle)
    k = rng.choice(TENTATIVAS[0], size=len(res), p=TENTATIVAS[1])
    res = res.loc[res.index.repeat(k)].reset_index(drop=True)
    # orfaos: registros Moodle sem inscricao no SGF
    n_orf = int(P_ORFAOS_MOODLE * len(res))
    orf = res.sample(n_orf, random_state=semente).copy()
    orf['id_inscricoes'] = novo_id(rng, 'INSC_SINT_', n_orf, usados)
    res = pd.concat([res, orf], ignore_index=True).sample(frac=1, random_state=semente).reset_index(drop=True)

    # duplicatas no SGF (Golden Record)
    dup = ins.sample(int(P_DUP_INSCRICAO * n), random_state=semente)
    ins = pd.concat([ins, dup], ignore_index=True).sample(frac=1, random_state=semente + 1).reset_index(drop=True)

    col_ins = ['id_inscricoes', 'Nome_Breve', 'Nome_Formacao', 'carga_horaria', 'datahora_inscricao', 'Sexo',
               'data_nascimento', 'Escolaridade', 'Municipio', 'Cargo', 'Funcao', 'Tipo_Instituicao', 'SRE',
               'id_discente_anonimo']
    col_res = ['id_inscricoes', 'id_resultados', 'nome_do_curso', 'nome_curto_do_curso', 'data_inicio_formacao',
               'data_termino_formacao', 'status_geral', 'progresso_na_formacao', 'nota_final_na_formacao',
               'primeiro_acesso', 'ultimo_acesso', 'tempo_total_de_acesso', 'periodo_de_maior_acesso',
               'id_discente_anonimo']
    ins = ins[col_ins].astype({'carga_horaria': 'int64'})
    res = res[col_res]
    saida = Path(saida)
    ins.to_parquet(saida / '00_inscricoes_anonimizadas.parquet', index=False)
    res.to_parquet(saida / '00_resultados_anonimizados.parquet', index=False)
    print(f"inscricoes: {len(ins):,} linhas | pessoas: {n_pessoas:,} | resultados: {len(res):,} linhas")
    return ins, res


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--n-pessoas', type=int, default=2100)
    ap.add_argument('--semente', type=int, default=2026)
    ap.add_argument('--saida', default=str(AQUI))
    a = ap.parse_args()
    gerar(a.n_pessoas, a.semente, a.saida)
