## HashBench — Argon2id vs bcrypt

Aplicativo simples em Streamlit para comparar o tempo de hash entre Argon2id e bcrypt.

## Descrição

Este projeto contém um protótipo educativo que mede o custo de processamento (tempo) de duas funções de derivação de senha: Argon2id (memory-hard) e bcrypt. É destinado a fins de estudo e demonstração.

## Finalidade

O trabalho foi desenvolvido como estudo para o Conince XIII da Faculdade Eduvel — Avaré.

## Requisitos

- Python 3.8+ (recomendado)
- Bibliotecas: `streamlit`, `bcrypt`, `argon2-cffi`, `matplotlib`

## Instalação rápida

1. Crie um ambiente virtual (recomendado) e ative-o.
2. Instale dependências:

```bash
pip install streamlit bcrypt argon2-cffi matplotlib
```

## Como executar

Execute o app com o Streamlit:

```bash
streamlit run main.py
```

## Notas importantes

- O parâmetro `memory_cost` do Argon2 é expresso em KB; valores muito altos podem causar erros de memória em máquinas com pouca RAM (especialmente no Windows). Se ocorrer `HashingError` ou "out of memory", reduza o valor máximo no slider no `main.py`.
- Este projeto é um protótipo educacional — não use os parâmetros mostrados em produção sem avaliação prévia.

## Contato

Projeto desenvolvido por estudantes para o Conince XIII — Faculdade Eduvele (Avaré).

- [Sr. Me. Renan Supremo](https://github.com/Renan-RodriguesDEV)
- [Pedro](https://linkedin.com/in/pedro-henrique-8a78a137a)
- [Mariani](https://github.com/Mariani-D)
