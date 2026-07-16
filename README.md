# 🎓 Sistema de Gestão Acadêmica (Student & Course Manager)

## Link para [video no YouTube](https://youtu.be/x7kWesKeEDM?is=y_IIgToTQSJXKwcr)

Um sistema simplificado de gestão acadêmica desenvolvido em **Python** utilizando o framework **Flask**. O projeto foi estruturado seguindo princípios de **Clean Architecture** (Arquitetura Limpa) e **DDD (Domain-Driven Design)**, garantindo desacoplamento entre as regras de negócio, os contratos de aplicação e os detalhes de infraestrutura (persistência em arquivos CSV).

O sistema permite o cadastro de estudantes, criação e vínculo de disciplinas (cursos), além de realizar o cálculo automático de índices de desempenho acadêmico como o **GPA americano** e o **IRA brasileiro**.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Framework Web:** Flask (para entrega das views e tratamento de rotas HTTP)
* **Banco de Dados (Persistência):** Arquivos Flat-File (`.csv`) gerenciados localmente
* **Geração de Identificadores:** UUID4

---
## 🚀 Funcionalidades Principais

### 1. Gestão de Estudantes
* Cadastro de estudante com validação e limpeza automática de caracteres não numéricos do CPF/Tax ID (`student_tax_id`).
* Listagem, edição e exclusão de estudantes.
* Associação dinâmica de disciplinas (`courses`) através do ID dos cursos.

### 2. Gestão de Cursos (Disciplinas)
* Criação de disciplinas contendo carga horária (`credit_hours`) e nota (`grade`).
* Validação de segurança: Notas obrigatoriamente contidas no intervalo **0 a 10**.
* Atualização de dados cadastrais e remoção de disciplinas com atualização em cascata na lista do estudante.

### 3. Métricas de Desempenho Acadêmico
Integrado diretamente no modelo de domínio de cursos (`Course`):
* **IRA (Índice de Rendimento Acadêmico):** Média ponderada clássica utilizando a carga horária como peso e as notas no sistema brasileiro (0 a 10).
* **GPA (Grade Point Average):** Média ponderada baseada no modelo americano de pontuação (escala de 0.0 a 4.0), convertendo as faixas de notas brasileiras automaticamente para conceitos (A, B, C, D, F).

---

## 💾 Camada de Persistência (CSV Context)

A persistência do sistema é inovadora por dispensar bancos de dados complexos para fins acadêmicos. O componente `Context` atua como um gerenciador leve de arquivos texto:
* Cria de forma autônoma o diretório `db/` e os arquivos `.csv` estruturados com cabeçalho de colunas.
* Fornece operações seguras de leitura (`_reader`), escrita direta (`_appender`), além de varredura seletiva para atualizações e exclusões baseadas em ID.

---

## 🏁 Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o Python 3 instalado em sua máquina.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
    git clone git@github.com:theDevOli/gpa-calculator.git
    cd gpa-calculator
   ```
2. **Crie e ative um ambiente virtual (Opcional, mas recomendado):**

   * **No Linux/macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   * **No Windows (Prompt de Comando):**
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Instale as dependências (Flask):**
   ```bash
   pip install Flask
   ```
4. **Inicie o servidor de desenvolvimento:**
   ```bash
   python __main__.py
   ```
5. **Acesse no seu navegador:**
   Abra o endereço [http://127.0.0.1:5000](http://127.0.0.1:5000) para interagir com o painel de estudantes.

---

## 📝 Padrões de Código Utilizados

* **SOLID:** Aplicação estrita do princípio de Inversão de Dependência (Controllers dependem de contratos de aplicação; Serviços dependem de contratos de repositório).
* **Google Style Docstrings:** Todas as classes, atributos, métodos, parâmetros e retornos estão totalmente documentados no padrão de documentação do Google para Python.
* **Tipagem (Type Hints):** Utilização ativa de indicações de tipos nativos (`str`, `float`, `list`, `Optional`, `List`) para garantir clareza e facilitar o auxílio do intellisense nas IDEs.