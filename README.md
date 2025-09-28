# FIAP-IAparaDevs-Fase5-Hackaton

## 1. Visão Geral
A IA-STRIDE é uma ferramenta desenvolvida em Python que utiliza inteligência artificial para analisar diagramas de arquitetura de software, independentemente do provedor de nuvem. Ela realiza uma análise de vulnerabilidades baseada na metodologia STRIDE, sugere correções e, ao final, gera um relatório detalhado em PDF. Adicionalmente, a ferramenta produz um diagrama atualizado em formato Mermaid com as correções sugeridas e um arquivo Terraform para a criação da infraestrutura correspondente.

## 2. Metodologia STRIDE
- A ferramenta utiliza o método de modelagem de ameaças STRIDE para categorizar e analisar vulnerabilidades. Cada sigla representa um tipo de ameaça potencial:

    - Spoofing (Representação): Vulnerabilidades relacionadas à falsificação de identidade.

    - Tampering (Violação): Vulnerabilidades relacionadas à adulteração de dados.

    - Repudiation (Não Repúdio): Vulnerabilidades que permitem a negação de ações realizadas.

    - Information Disclosure (Divulgação de Informação): Vulnerabilidades que levam à exposição indevida de dados.

    - Denial of Service (Negação de Serviço): Vulnerabilidades que causam a indisponibilidade do serviço.

    - Elevation of Privilege (Elevação de Privilégio): Vulnerabilidades que permitem o acesso a privilégios não autorizados.

## 3. Fluxo de Execução
- Entrada do Desenho de Arquitetura: A IA-STRIDE aceita um desenho de arquitetura em formato de imagem ou texto (dependendo da implementação). A IA interpreta a estrutura, componentes e fluxos de dados do desenho.

     - Análise de Vulnerabilidade (STRIDE): Com base na interpretação da arquitetura, a IA aplica a metodologia STRIDE para identificar ameaças potenciais em cada componente e interação.

     - Sugestão de Correções: Após a análise, a ferramenta sugere correções específicas para mitigar as vulnerabilidades encontradas.

     - Geração do Relatório PDF: Um relatório completo é gerado em formato PDF, contendo a análise, as vulnerabilidades identificadas e as correções propostas.

     - Criação do Diagrama Mermaid: Um novo diagrama, formatado em Mermaid, é criado para refletir a arquitetura com as correções sugeridas, facilitando a visualização e documentação.

     - Geração do Terraform: O código Terraform é gerado automaticamente, permitindo a criação e o gerenciamento da infraestrutura corrigida em qualquer provedor de nuvem.

## 4. Arquivos



- **requirements.txt**: Documento que descreve todas as libs e verões usadas no projeto

## 5. Como usar
- Instalação: Instale as dependências com o seguinte comando, utilizando o arquivo requirements.txt:

```<bash>

pip install -r requirements.txt
Use o código com cuidado.
```

- Configuração: Configure as variáveis de ambiente necessárias em um arquivo .env (chaves de API, etc.).

- Execução: Inicie o servidor FastAPI (ou a CLI, dependendo da interface implementada) para começar a análise.

- Saídas Geradas
    - Relatório PDF: Um documento detalhado com a análise de segurança da arquitetura, um diagrama Mermaid e o código Terraformpara provisionar a infraestrutura em um provedor de nuvem de sua escolha.

