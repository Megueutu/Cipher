# Roadmap — Password Security & Applied Cryptography (CLI Project)

> Projeto de estudo assíncrono para dev júnior migrando para cybersecurity, com foco em hashing, criptografia aplicada e análise de senhas.

---

## Objetivo do projeto

Construir uma ferramenta CLI que demonstre, na prática, por que certas escolhas criptográficas são seguras (ou não) — cobrindo geração, análise, hashing e quebra de senhas. O valor do projeto não está em "ter um hash funcionando", mas em **documentar o raciocínio de segurança** por trás de cada decisão.

---

## Fase 0 — Preparação teórica (antes de codar)

**Estudar:**
- Diferença entre **encoding, encryption e hashing** (erro comum até entre devs)
- O que torna um hash "criptográfico" (determinismo, avalanche effect, resistência a colisão)
- Conceito de **entropia** aplicado a senhas
- O que é **salt** e por que ele existe (proteção contra rainbow tables)
- Diferença entre hash rápido (SHA-256) e hash lento/memory-hard (bcrypt, scrypt, Argon2) — e por que isso importa pra senha especificamente

**Entregável desta fase:** um `THEORY.md` ou seção no README com esses conceitos escritos com suas próprias palavras (isso já é prova de entendimento pra quem for avaliar o repo).

---

## Fase 1 — Gerador de senha segura (`password_generator.py`)

**O que implementar:**
- Geração de senha usando `secrets` (CSPRNG) — nunca `random`
- Opções configuráveis: tamanho, uso de símbolos/números/maiúsculas
- Cálculo de entropia da senha gerada (mostrar ao usuário)

**O que aprender fazendo:**
- Diferença entre PRNG comum e CSPRNG — por que `random.choice()` é previsível e inadequado pra segurança
- Como calcular entropia: `log2(tamanho_do_alfabeto ^ comprimento)`

**Pegadinha pra documentar no README:** gerar uma versão "insegura" de propósito usando `random`, e comparar a previsibilidade dela com a versão `secrets` — visualmente mostra o problema.

---

## Fase 2 — Analisador de força de senha (`password_analyzer.py`)

**O que implementar:**
- Score de força baseado em entropia (não só em "tem símbolo? tem número?")
- Checagem contra wordlist de senhas vazadas (ex: rockyou.txt — arquivo público, comum em labs de segurança)
- Detecção de padrões previsíveis (substituição leet, sequências tipo `12345`, repetição de caracteres)

**O que aprender fazendo:**
- Por que "senhas fortes por regra" (1 maiúscula, 1 número, 1 símbolo) não é o mesmo que senha com boa entropia
- Como listas de senhas vazadas viram a primeira linha de ataque real (dictionary attack)

---

## Fase 3 — Hash "ingênuo" implementado/aplicado (`naive_hash.py`)

**O que implementar:**
- Hash de senha usando SHA-256 puro (sem salt, sem custo computacional)
- Opcional avançado: implementar o algoritmo SHA-256 do zero (bom exercício, mas não obrigatório — usar `hashlib` já é aceitável aqui, o ponto é o *uso ingênuo*, não a reimplementação do algoritmo)

**O que aprender fazendo:**
- Por que hash rápido é uma característica ótima para checksums, mas péssima para senhas
- Como a ausência de salt permite ataques de rainbow table

---

## Fase 4 — Hash real de produção (`secure_hash.py`)

**O que implementar:**
- Uso de `bcrypt` (ou `argon2-cffi`) como deveria ser feito em produção
- Comparação de tempo de hash entre SHA-256 puro e bcrypt (mostrar que a lentidão é proposital)

**O que aprender fazendo:**
- O conceito de **work factor / cost factor** e como ele se ajusta ao poder computacional ao longo do tempo
- Por que "memory-hard" (Argon2) é a evolução sobre bcrypt (resistência a ataques com GPU/ASIC)

> ⚠️ Não implemente bcrypt/Argon2 do zero — são algoritmos com muitos detalhes sutis de segurança. Use a lib real e foque em **entender e comparar**, não reinventar.

---

## Fase 5 — Demonstração de quebra de hash (`crack_demo.py`)

**O que implementar:**
- Brute-force contra os hashes SHA-256 gerados na Fase 3 (com tempo cronometrado)
- Dictionary attack usando a wordlist da Fase 2
- Mesmo ataque contra o hash bcrypt da Fase 4 (mostrando que leva ordens de magnitude mais tempo)

**O que aprender fazendo:**
- Como medir e comunicar "tempo até quebra" de forma que faça sentido pra alguém não técnico (segundos vs séculos)
- Isso vira o "resultado final" mais impactante do projeto — o gráfico comparativo

**Entregável:** tabela ou gráfico no README comparando tempo de crack: SHA-256 sem salt vs SHA-256 com salt vs bcrypt vs Argon2.

---

## Fase 6 — CLI e polimento (`main.py`)

**O que implementar:**
- Interface via `argparse` unificando todos os módulos (`--generate`, `--analyze`, `--hash`, `--crack`)
- Output formatado com `rich` ou `colorama` (tabelas, cores — dá um "acabamento" sem precisar de GUI)

**O que aprender fazendo:**
- Boas práticas de design de CLI (help text claro, flags consistentes) — habilidade transferível pra qualquer ferramenta de security que você for construir depois

---

## Fase 7 — Documentação final

**O que produzir:**
- `README.md` em inglês (público-alvo: vagas internacionais/remotas), com:
  - Contexto/motivação do projeto
  - Tabela de resultados comparativos (Fase 5)
  - Explicação teórica resumida de cada conceito aplicado
  - Prints do terminal em uso
- Opcional: `README.pt-BR.md` linkado no topo, se quiser alcançar também o público nacional

---

## Estrutura final sugerida do repositório

```
password-security-lab/
├── README.md
├── README.pt-BR.md          (opcional)
├── THEORY.md
├── src/
│   ├── password_generator.py
│   ├── password_analyzer.py
│   ├── naive_hash.py
│   ├── secure_hash.py
│   ├── crack_demo.py
│   └── main.py
├── data/
│   └── wordlist_sample.txt   (subset pequeno, não subir rockyou.txt inteiro)
├── results/
│   └── crack_time_comparison.png
└── requirements.txt
```

---

## Conexão com o projeto de cloud (contexto geral)

Esse projeto é independente, mas reforça diretamente conceitos que você vai usar na Fase 2-3 do roadmap de cloud security:
- **IAM e secrets management** (AWS Secrets Manager, KMS) fazem sentido muito mais rápido depois que você entende *por que* hashing/criptografia de senha importa por dentro
- Ao documentar "hash rápido vs lento", você já está pensando em termos de **ameaça e mitigação** — o mesmo raciocínio usado em auditoria de IAM policy

---

## Checklist rápido de entrega

- [ ] Gerador de senha com CSPRNG
- [ ] Analisador de força com entropia + wordlist check
- [ ] Hash ingênuo (SHA-256 puro)
- [ ] Hash seguro (bcrypt/Argon2)
- [ ] Demo de quebra com tempo comparado
- [ ] CLI unificado
- [ ] README em inglês + THEORY.md
- [ ] Gráfico/tabela comparativa nos resultados