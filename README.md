```markdown
# Sistema de Identificação de Fake News

## Objetivos

Neste projeto, apresentamos os objetivos gerais e específicos do sistema. Os objetivos gerais fornecem uma visão ampla, enquanto os objetivos específicos detalham as etapas e metas de desenvolvimento.

### Objetivo Geral

Desenvolver um sistema de identificação de notícias falsas veiculadas em idioma português, utilizando técnicas de mineração de texto, e criar uma Interface de Programação de Aplicações (API) para facilitar o uso do modelo.

### Objetivos Específicos

a) Analisar e realizar todas as etapas de mineração de texto;
b) Desenvolver cinco modelos utilizando técnicas de aprendizado de máquina e redes neurais, comparando-os para selecionar o melhor classificador;
c) Implantar o projeto no ambiente Amazon Web Services (AWS);
d) Gerar uma API em ambiente AWS, via API Gateway, para consumo do modelo.

---

## Estrutura do Projeto

O repositório é composto pelos seguintes arquivos principais:

- **`deploy.py`**: Contém o script de implantação do sistema no ambiente AWS, incluindo a criação e configuração da API para consumo do modelo.
- **`modelagem.ipynb`**: Notebook com as etapas de mineração de texto, treinamento e comparação dos modelos desenvolvidos.
- **`Fake.br-corpus`**: Dataset utilizado para o treinamento e validação dos modelos, composto por notícias reais e falsas em português.

---

## Instruções de Uso

1. **Clonar o Repositório:**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Configurar Ambiente Virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Executar o Notebook:**
   Abra o arquivo `modelagem.ipynb` em um ambiente Jupyter Notebook e execute as células para realizar o treinamento e validação dos modelos.

4. **Implantação do Sistema:**
   Utilize o arquivo `deploy.py` para configurar e implantar o modelo em um ambiente AWS.
   ```bash
   python deploy.py
   ```

---

