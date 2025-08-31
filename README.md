# LEGACY.exe (storycompare-with-LLM)

# 🚀 Guia de Configuração — Sistema Comparador de Requisitos x Repositório

Este guia explica como configurar e rodar o **Sistema Comparador** que utiliza:
- **Groq API** → para comparação inteligente via LLM
- **GitHub App** → para acessar repositórios com permissão *read-only*

---

## 📂 Estrutura Final do Projeto

```
/projeto-comparador
  ├── comparador.py
  ├── requisitos.txt
  ├── prompt_base.txt
  ├── requirements.txt
  ├── SETUP.md
  ├── .env
  ├── .gitignore
  └── keys/
      └── github_app.pem
```

---

## 1. Configurar a Groq API

1. Acesse [Groq Console](https://console.groq.com/).
2. Vá em **API Keys → Generate New Key**.
3. Copie a chave gerada.
4. No `.env`, adicione:
   ```ini
   GROQ_API_KEY=sua_chave_groq_aqui
   ```

---

## 2. Criar um GitHub App

1. Vá em [GitHub → Settings → Developer settings → GitHub Apps](https://github.com/settings/apps).
2. Clique em **New GitHub App**.
3. Configure:
   - **App name**: `comparador-ti`
   - **Repository permissions → Contents: Read-only**
   - Instale apenas nos repositórios desejados.
4. Clique em **Create GitHub App**.

---

## 3. Obter credenciais do App

- **App ID**: aparece na página do App (Ex.: `123456`).
- **Installation ID**: aparece na URL quando instala o App:
  ```
  https://github.com/organizations/<org>/settings/installations/<id>
  ```
- **Private key (.pem)**:
  - Vá em **Private keys → Generate private key**
  - Baixe o arquivo `.pem`
  - Salve em `projeto-comparador/keys/github_app.pem`

---

## 4. Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```ini
GROQ_API_KEY=sua_chave_groq_aqui
GITHUB_APP_ID=123456
GITHUB_INSTALLATION_ID=987654
GITHUB_PRIVATE_KEY_PATH=./keys/github_app.pem
```

---

## 5. Instalar dependências

No terminal, dentro do projeto:

```bash
pip install -r requirements.txt
```

---

## 6. Executar o sistema

```bash
python comparador.py
```

O sistema irá:
- Ler `requisitos.txt`
- Extrair código do repositório GitHub
- Comparar via Groq LLM
- Salvar os resultados em uma pasta versionada, exemplo:

```
requisitos_abc_v1/
   ├── relatorio.md
   ├── codigo_atualizado.py
   └── resumo_executivo.txt
```

---

## ✅ Pronto!

Agora você tem o sistema configurado e pode rodar sempre que houver novos requisitos.
