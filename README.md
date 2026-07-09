# Caixa360 (revisado)

## ⚠️ Antes de tudo: rotacione a senha do banco

`database/database.py` tinha usuário e senha do Postgres/Supabase escritos direto no
código. Considere essa credencial comprometida e troque-a no painel do Supabase, mesmo
com as correções abaixo. A senha agora vem de `DB_PASSWORD` (variável de ambiente ou
`st.secrets`) — veja `.env.example`.

## Nova funcionalidade: editar e excluir lançamentos

Agora dá pra editar ou excluir um lançamento pelo mesmo campo de comando em texto livre
que já existia para registrar entrada/saída:

- `"excluir registro 12"`, `"deletar lançamento 7"`, `"apagar 5"`
- `"editar registro 12 valor 300"`, `"alterar registro 12 categoria salario"`

**Exclusão pede confirmação**: o comando de excluir não apaga na hora — ele mostra o
lançamento encontrado e só exclui de fato se você clicar em "Sim, excluir". Isso evita
apagar algo por causa de uma interpretação errada do texto.

**Saldo é recalculado automaticamente** depois de qualquer edição ou exclusão. Como o
saldo de cada linha é acumulado (guarda o total até aquele ponto), editar ou excluir um
lançamento no meio da lista deixaria todos os saldos seguintes errados se não fossem
recalculados — isso agora é feito em `repo/caixa360_repo.py::_recalcular_saldos`.

Toda edição/exclusão é sempre filtrada por `usuario_id`, então um usuário nunca
consegue mexer no lançamento de outro.

## Bugs corrigidos

- **`services/entrada_dados.py`**: fazia `import datetime` (o módulo) mas chamava
  `datetime.now()` (método que só existe na classe `datetime.datetime`). Isso só não
  quebrava porque `from services.tratamento_comandos import *` era importado depois e
  reexportava o nome `datetime` da classe — um **import circular escondido**
  (`entrada_dados` importava de `tratamento_comandos`, que importa `get_dados` de volta
  de `entrada_dados`). Removido o import circular e corrigido para
  `datetime.datetime.now()` explícito.
- **`app.py`**: no branch de login sem troca de senha obrigatória, havia
  `nome_usuario = resultado[1]` — mas `resultado[1]` é o booleano `trocar_senha`, não o
  nome do usuário, e essa variável nunca era usada depois. Código morto e mal nomeado,
  removido.
- **`pages/trocar_senha.py`**: quando a senha vinha vazia, o código fazia
  `AttributeError("...")` sem dar `raise` — ou seja, criava o objeto de erro e
  descartava, sem nenhum efeito, retornando `None`. Corrigido para de fato retornar a
  lista de erros. Também removido um `import sqlite3` morto (o banco é Postgres) e a
  lógica de update de senha agora reaproveita `repo.usuarios_repo.atualizar_senha` em
  vez de duplicar a query ali dentro.
- **Ordem de checagem de comandos**: `eh_movimentacao_rapida` (usada para
  "200 mercado" virar um depósito rápido) era checada antes de qualquer outra coisa.
  Um comando de exclusão de 2 palavras como `"excluir 5"` caía nesse atalho e virava um
  **depósito de R$ 5** por engano. Exclusão e edição agora são checadas primeiro.
- **Gráficos quebravam sem dados**: `grafico_entrada_saida()` e `grafico_pizza()`
  tentavam atribuir 7 nomes de coluna a um DataFrame vazio quando o usuário não tinha
  nenhum lançamento ainda. Agora mostram uma mensagem em vez de quebrar.
- Conexões que não fechavam em caso de erro (sem `try/finally`) em vários pontos do
  `repo/`.
- `trocar_senha: int` no model, mas `BOOLEAN` no banco; `data: datetime` (o módulo) em
  vez de `datetime.datetime` no model de extrato.
- `app.py` rodava `criar_tabela_extrato()` / `criar_tabela_usuarios()` a cada
  refresh de página. Agora roda uma vez por processo (`st.cache_resource`).
- `requirements.txt` tinha `moviepy` e `faster-whisper`, sem nenhuma referência a eles
  em nenhum arquivo do projeto — removidos (comentário deixado caso seja pra uma
  feature de voz futura).
- Removidos `st.write` de debug ("Valor:", "Operação:", "Categoria:") que apareciam
  pro usuário final ao processar qualquer movimentação.

## Rodando localmente

```bash
pip install -r requirements.txt
export DB_PASSWORD="sua_senha_nova"
streamlit run app.py
```

## Estrutura

```
app.py                        # login + inicialização do banco
config.py                      # lê credenciais de env vars / st.secrets
pages/menu.py                  # tela principal (comando em texto + confirmação de exclusão)
pages/trocar_senha.py           # troca de senha obrigatória no primeiro login
database/database.py            # conexão com o Postgres
models/                          # dataclasses Usuario e Caixa360
repo/                             # funções que falam com o banco (CRUD completo de extrato)
services/
  auth.py                          # usuario_id da sessão
  seguranca_senha.py                # checagem de senha com bcrypt
  entrada_dados.py                   # grava entrada/saída
  editar_excluir.py                  # NOVO: interpreta comandos de editar/excluir
  consultar_extrato.py                # extrato e gráficos
  tratamento_comandos.py               # roteia o texto digitado pro serviço certo
sql/                                    # strings SQL
utils/                                   # config de página e saudação
```
