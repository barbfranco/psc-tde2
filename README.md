# TDE 2: Programação Concorrente

**Disciplina:** Performance em Sistemas Ciberfísicos  
**Linguagem:** Python 3.10+

## Vídeo de apresentação: >>*[INSERIR LINK AQUI]*<<

## Integrantes
- **Bárbara:** Jantar dos Filósofos.
- **Julia:** testes, progresso e justiça.
- **Bruno:** contador concorrente e semáforos.
- **Ícaro:** deadlock com dois locks.

## 1: JANTAR DOS FILÓSOFOS

### Objetivo e implementação
Simular cinco filósofos compartilhando cinco garfos, demonstrando problemas de concorrência e formas de evitar deadlock.
**Versão ingênua:** cada filósofo pega um garfo e aguarda o segundo. Uma barreira sincroniza as threads para reproduzir o impasse, impedindo que os filósofos avancem.
**Versão corrigida:** os garfos são adquiridos em ordem crescente de índice, eliminando a condição de espera circular, uma das quatro condições de Coffman. Um mecanismo de senhas organiza o atendimento dos pedidos, contribuindo para a justiça entre os filósofos.

### Resultados
A versão ingênua reproduziu o deadlock. Na versão corrigida, as 11 execuções foram concluídas, com três refeições por filósofo em cada uma e sem inanição observada.
Os logs completos e a análise dos resultados estão disponíveis em `evidencias/filosofos.txt`.

### Fluxograma
![Fluxograma dos Filósofos](evidencias/fluxo-filosofos-tde2.png)

### Como executar
No terminal, a partir da raiz do repositório:
`python 1-filosofos/filosofos.py`
Selecione:
- `1` para a versão ingênua.
- `2` para a versão corrigida.

## 2: CONTADOR CONCORRENTE E SEMÁFOROS

*A completar*

## 3: DEADLOCK COM DOIS LOCKS

*A completar*