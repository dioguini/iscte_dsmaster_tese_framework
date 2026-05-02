# Appendix Table of Contents

- [Appendix Table of Contents](#appendix-table-of-contents)
- [Appendix F - Management and Politics Layer Document Template (author proposal)](#appendix-f---management-and-politics-layer-document-template-author-proposal)
  - [Management and Politics Layer Document Template](#management-and-politics-layer-document-template)
    - [Gestão e Políticas da Qualidade de Dados](#gestão-e-políticas-da-qualidade-de-dados)
      - [Identificação - Ownership do Processo](#identificação--ownership-do-processo)
      - [Histórico de versões](#histórico-de-versões)
      - [Objetivo](#objetivo)
      - [Scope](#scope)
      - [Documentação Técnica dos Sensores (High Level)](#documentação-técnica-dos-sensores-high-level)
      - [Regras de Aquisição de Dados](#regras-de-aquisição-de-dados)
      - [Especificação de Roles](#especificação-de-roles)
      - [Pontos de Controlo](#pontos-de-controlo)
      - [Políticas de Avaliação da Qualidade de Dados](#políticas-de-avaliação-da-qualidade-de-dados)
      - [Ciclo de Melhoria Contínua (Continuous Improvement Cycle)](#ciclo-de-melhoria-contínua-continuous-improvement-cycle)


# Appendix F - Management and Politics Layer Document Template (author proposal)

## Management and Politics Layer Document Template
### Gestão e Políticas da Qualidade de Dados
___

####  Identificação - Ownership do Processo

**Responsável:** _\<Nome do Responsável>_

**Versão:** _\<Versão>_

**Data:** _\<Data de criação/alteração do documento>_

**Estado do Documento:** _\<Em elaboração / Validada / Em revisão>_

**Acesso e Versionamento:** _\<Breve descrição>_

**Localização definitiva:** _\<Diretoria onde este ficheiro se encontra guardado>_

**Política de revisão:** _\<Descrição da política de Revisão>_

**Acesso para consulta:** _\<Nível de acesso>_

**Acesso para edição:** _\<Nível de restrição>_
___

#### Histórico de versões
| Versão   | Data   | Alterações principais    | Autor                    |
|:---------|:-------|:-------------------------|:-------------------------|
| _\<Versão>_ | _\<Data>_ | _\<Resumos das alterações>_ | _\<Nome/Id do utilizador>_  |
___

#### Objetivo
_\<Descrição do objetivo do documento>_

___

#### Scope
| Campo | Descrição                                                |
| :--- |:---------------------------------------------------------|
| Dados incluídos | _\<Dados de sensores de um instrumento>_                 |
| Tipos de dados | _\<Tipos de dados observados>_                           |
| Execução | _\<Modo de execução da framework de qualidade de dados>_ |

___

#### Documentação Técnica dos Sensores (High Level)
- **Sensor do fio de prumo**

    | Campo | Descrição                                                                                                                                 |
    | :--- |:------------------------------------------------------------------------------------------------------------------------------------------|
    | Fabricante | _\<Identificação do Fabricante do sensor do tipo X>_                                                                                      |
    | Modelo | _\<Identificação do modelo do sensor do tipo X>_                                                                                          |
    | Documentação técnica | _\<Diretório da documentação técnica do sensor do tipo X>_                                                                                |
    | Variáveis medidas | _\<Variável 1 - Significado da variável 1>_<br>_\<Variável 2 - Significado da variável 3>_<br>_\<Variável 3 - Significado da variável 3>_ |

___

#### Regras de Aquisição de Dados
- **Regras de aquisição de dados provenientes do sensor do tipo X**

    | Campo | Descrição                                                                              |
    | :--- |:---------------------------------------------------------------------------------------|
    | Modo de aquisição | _\<Modo de aquisição de dados>_                                                        |
    | Frequência e cadência de aquisição | _\<Frequência de leitura de dados do sensor do tipo X>_                                 |
    | Protocolos e padrões de comunicação | _\<Identificação dos padrões e protocolos de leitura de dados do sensor do tipo X>_     |
    | Verificações automáticas na origem | _\<Identificação das verificações de dados efetuadas no/pelo próprio sensor do tipo X>_ |

___

#### Especificação de Roles
| Função | Responsabilidade | Frequência de revisão / avaliação/implementação | Utilizador                                      |
| :--- | :--- | :--- |:------------------------------------------------|
| Data Owner | Aprovação de políticas e thresholds de validação de dados | _\<Frequência temporal de revisão das políticas e thresholds de validação de dados>_ | _\<Identificação do(s) Data Owners>_           |
| Data Owner | Avaliação e definição de Data Quality checks a serem implementados | _\<Frequência temporal da revisão e avaliação e definição de Data Quality checks a serem implementados>_ | _\<Identificação do(s) Data Owners>_            |
| Data Steward | Monitorização da conformidade dos dados | _\<Frequência temporal da revisão da revisão da monitorização da conformidade dos dados>_ | _\<Identificação do(s) Data Steward>_           |
| Engenheiro Dados | Implementação dos Data Quality checks e validações de thresholds | _\<Frequência temporal da revisão da implementação dos Data Quality checks e validações de thresholds>_ | _\<Identificação do(s) Engenheiro(s) de Dados>_ |
| Analista de Dados | Validação de outputs e respetivas interpretações físicas | _\<Frequência temporal da revisão da validação de outputs e respetivas interpretações físicas>_ | _\<Identificação do(s) Analista(s) de Dados>_   |
___

#### Pontos de Controlo
- **Sensor do tipo X**

    | Campo | Descrição                                                                                                    |
    | :--- |:-------------------------------------------------------------------------------------------------------------|
    | Pontos de Execução de DQ Checks | _\<Identificação dos pontos de implementação da avaliação da qualidade de dados no ciclo de vida dos dados>_ |

___

#### Políticas de Avaliação da Qualidade de Dados
- **Sensor do tipo X**

    - _\<Dimensão de Qualidade>_ - Objetivo da avaliação da qualidade de dados para esta dimensão da qualidade na organização
___

#### Ciclo de Melhoria Contínua (Continuous Improvement Cycle) 
- **Sensor do tipo X**

  - Etapas

    | Etapa | Descrição                                                                                                                                    |
    | :--- |:---------------------------------------------------------------------------------------------------------------------------------------------|
    | Definição | _\<Descrição da etapa inicial>_                                                                                                              |
    | Execução dos DQ Checks | _\<Descrição da etapa de Execução dos DQ Checks>_                                                                                            |
    | Avaliação dos DQ Checks | _\<Descrição da etapa de Avaliação dos DQ Checks>_                                                                                           |
    | Análise | _\<Descrição da etapa de Anaálise dos outputs produzidos nas etapas de Execução e Avaliação dos DQ Checks>_                                  |
    | Observabilidade | _\<Descrição da etapa de observação dos detalhes produzidos na etapa de DQ Checks>_                                                          |
    | Ação | _\<Descrição das ações futuras a tomar (sejam elas corretivas, preventivas ou outras) após a análise dos outputs produzidos pela framework>_ |
    | Revisão | _\<Descrição da etapa de Revisão de revisão das políticas, DQ Checks, thresholds e fluxos de dados >_                                        |
    

- Ferramentas
 
    | Campo | Descrição |
    | :--- | :--- |
    | Ferramentas de suporte | _\<Identificação das diferentes ferramentas de suporte que serão utilizadas na Framework de Qualidade de Dados>_ |
