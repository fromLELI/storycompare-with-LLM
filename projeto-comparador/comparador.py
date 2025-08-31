import os
from github import Github, GithubIntegration
from dotenv import load_dotenv, find_dotenv
import groq

# Carregar variáveis de ambiente
_ = load_dotenv(find_dotenv())

client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

APP_ID = os.getenv("GITHUB_APP_ID")
INSTALLATION_ID = os.getenv("GITHUB_INSTALLATION_ID")
PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")

with open(PRIVATE_KEY_PATH, "r") as f:
    private_key = f.read()

git_integration = GithubIntegration(APP_ID, private_key)
access_token = git_integration.get_access_token(INSTALLATION_ID).token
g = Github(access_token)


def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_code_from_repo(repo_name, extensions=('.py', '.js', '.java')):
    repo = g.get_repo(repo_name)
    contents = repo.get_contents("")
    code_data = []

    while contents:
        file = contents.pop(0)
        if file.type == "dir":
            contents.extend(repo.get_contents(file.path))
        elif file.path.endswith(extensions):
            snippet = file.decoded_content.decode(errors="ignore")
            numbered = "\n".join([f"{i+1}: {line}" for i, line in enumerate(snippet.splitlines())])
            code_data.append(f"### {file.path}\n{numbered}")
    return "\n\n".join(code_data)


def compare_with_llm(prompt_base, requisitos, codigo):
    final_prompt = f"""
    {prompt_base}

    === DOCUMENTO DE REQUISITOS ===
    {requisitos}

    === CÓDIGO DO REPOSITÓRIO (com numeração de linhas) ===
    {codigo}
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": final_prompt}],
        model="llama-3.2-90b-vision-preview",
    )

    return chat_completion.choices[0].message.content


def proxima_versao(pasta_resultados, nome_base):
    """
    Descobre automaticamente a próxima versão: v1, v2, v3...
    """
    versao = 1
    while True:
        pasta = os.path.join(pasta_resultados, f"{nome_base}_v{versao}")
        if not os.path.exists(pasta):
            return versao, pasta
        versao += 1


def salvar_resposta(resposta, requisitos_file):
    nome_base = os.path.splitext(os.path.basename(requisitos_file))[0]

    # Criar pasta principal de resultados
    pasta_resultados = "resultados"
    os.makedirs(pasta_resultados, exist_ok=True)

    # Descobrir a próxima versão disponível
    versao, pasta_saida = proxima_versao(pasta_resultados, nome_base)
    os.makedirs(pasta_saida, exist_ok=True)

    partes = resposta.split("====")
    for parte in partes:
        if "RELATÓRIO COMPARATIVO" in parte:
            with open(os.path.join(pasta_saida, "relatorio.md"), "w", encoding="utf-8") as f:
                f.write(parte.replace("RELATÓRIO COMPARATIVO", "").strip())
        elif "CÓDIGO ATUALIZADO" in parte:
            with open(os.path.join(pasta_saida, "codigo_atualizado.py"), "w", encoding="utf-8") as f:
                f.write(parte.replace("CÓDIGO ATUALIZADO", "").strip())
        elif "RESUMO EXECUTIVO" in parte:
            with open(os.path.join(pasta_saida, "resumo_executivo.txt"), "w", encoding="utf-8") as f:
                f.write(parte.replace("RESUMO EXECUTIVO", "").strip())

    print(f"📂 Resultados salvos em: {pasta_saida}/ (versão v{versao})")


if __name__ == "__main__":
    requisitos_file = "requisitos.txt"
    prompt_base = load_file("prompt_base.txt")
    requisitos = load_file(requisitos_file)
    codigo = extract_code_from_repo("org/repo")  # ajuste para seu repositório

    resultado = compare_with_llm(prompt_base, requisitos, codigo)

    print("\n📊 RESULTADO COMPLETO:\n")
    print(resultado)

    salvar_resposta(resultado, requisitos_file)
