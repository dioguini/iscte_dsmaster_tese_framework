# Appendix Table of Contents

- [Appendix Table of Contents](#appendix-table-of-contents)
- [Appendix G - Management and Politics Layer Document Proposal](#appendix-g---management-and-politics-layer-document-proposal)
  - [Management and Politics Layer Document Proposal](#management-and-politics-layer-document-proposal)
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

# Appendix G - Management and Politics Layer Document Proposal


## Management and Politics Layer Document Proposal
### Gestão e Políticas da Qualidade de Dados
___

####  Identificação - Ownership do Processo
**Responsável**: Utilizador_1

**Versão**: v1.0

**Data**: 31/10/2025

**Estado do Documento**: Validado

**Acesso e Versionamento**: Geral para toda a organização

**Localização definitiva**: Diretoria principal da equipa de Qualidade de Dados

**Política de revisão**: Revisão anual ou com alterações estruturais sempre que necessário

**Acesso para consulta**: Público dentro da organização

**Acesso para edição**: Restrito
___

#### Histórico de versões
| Versão | Data | Alterações principais | Autor |
| :--- | :--- | :--- | :--- |
| 1.0 | 31/10/2025 | Criação inicial | Utilzador |

___

#### Objetivo
Este documento visa descrever os princípios, regras, papéis, processos e fluxos que asseguram a qualidade dos dados desde a sua aquisição nos diferentes tipos de sensores, até à sua disponibilização para os analistas. Este documento é iterativo, suportando o ciclo de melhoria contínua da qualidade de dados para os diferentes sensores utilizados.
A framweork deverá apresentar uma clara separação de responsabilidades entre utilizadores e/ou equipas e entre componentes, facilitando a manutenção e escalabilidade. Uma estrutura modular possibilita a integração futura de novos sensores, adaptando-se a diferentes contextos e requisitos técnicos. Os outputs são organizados de forma estruturada, por tipo de sensor, timestamp da execução, módulo de execução, e cada output deverá conter sempre que aplicável a dimensão de qualidade de dados, id do sensor e modo de leitura e uma nomenclatura standard, por forma a garantir a rastreabilidade e facilidade de análise para qualquer analista de dados, devendo ainda conter uma componente de logging, que regista todas as etapas do processo de execução, contribuindo essencialmente para diagnóstico de eventuais falhas e também de fácil entendimento para o end user de todos os passos executados.

___

#### Scope
| Campo | Descrição |
| :--- | :--- |
| Dados incluídos | Dados de sensores de um instrumento |
| Tipos de dados | Série Temporal de observações |
| Execução | Parametrizável, capaz de se adaptar aos modos de leitura e automático/manual, permitindo ainda que seja dada a possibilidade de escolher o ano de avaliação dos dados.<br><br>Capacidade de produzir relatórios de Profiling para análise rápida e inicial dos dados.<br><br>Avaliar métricas para dimensões de qualidade de dados e avaliação dos valores com thresholds.<br><br>Permitir uma capacidade interpretativa dos resultados através da produção de gráficos, para ajuda na tomada de decisão<br><br>Permitir a exportação dos registos avalidados |


___

#### Documentação Técnica dos Sensores (High Level)
- **Sensor do fio de prumo**
    
    | Campo | Descrição                                                                                                                                                                                                                                                                                                                              |
    | :--- |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | Fabricante | N/A                                                                                                                                                                                                                                                                                                                                    |
    | Modelo | N/A                                                                                                                                                                                                                                                                                                                                    |
    | Documentação técnica | N/A                                                                                                                                                                                                                                                                                                                                    |
    | Variáveis medidas | **ANO** - Ano de leitura<br>**MES** - Mês de leitura<br>**DIA** - Dia de leitura<br>**HORA** - Hora de leitura<br>**MINUTO** - Minuto de leitura<br>**DESLOCRADIALABS** - Valor absoluto do Deslocamento Radial da posição observada do fio de prumo<br>**DESLOCTANGABS** - Valor absoluto do Deslocamento Tangencial da posição observada do fio de prumo |
    | Limites operacionais e de precisão | N/A                                                                                                                                                                                                                                                                                                                                    |

___

#### Regras de Aquisição de Dados
- **Regras de aquisição de dados provenientes do sensor Fio de Prumo**
    
    | Campo | Descrição |
    | :--- | :--- |
    | Modo de aquisição | Automático |
    | Frequência e cadência de aquisição | 1 leitura / hora |
    | Protocolos e padrões de comunicação | N/A |
    | Verificações automáticas na origem | Não |
    
    | Campo | Descrição |
    | :--- | :--- |
    | Modo de aquisição | Manual |
    | Frequência e cadência de aquisição | É esperado mas não garantida uma leitura a cada 15 dias |
    | Protocolos e padrões de comunicação | Leitura Manual |
    | Verificações automáticas na origem | Não |

___

#### Especificação de Roles
| Função | Responsabilidade | Frequência de revisão / avaliação/implementação | Utilizador |
| :--- | :--- | :--- | :--- |
| Data Owner | Aprovação de políticas e thresholds de validação de dados | Anual | Utilizador1 |
| Data Owner | Avaliação e definição de Data Quality checks a serem implementados | Anual | Utilizador2 |
| Data Steward | Monitorização da conformidade dos dados | Anual | Utilizador3 |
| Engenheiro Dados | Implementação dos Data Quality checks e validações de thresholds | Quando aplicável | Utilizador4 |
| Analista de Dados | Validação de outputs e respetivas interpretações físicas | Quando aplicável | Utilizador5 |
___

#### Pontos de Controlo
- **Sensor do fio de prumo**

    | Campo | Descrição |
    | :--- | :--- |
    | Pontos de Execução de DQ Checks | Fase de Aquisição dos dados dos sensores- Sim<br>Dados armazenados - Não<br>Transformação de dados - Não |

___

#### Políticas de Avaliação da Qualidade de Dados
- **Sensor do fio de prumo**

  - _**Completeness**_ - Medir a qualidade dos dados ao nível da completude para cada variável dos ficheiros de leitura (automático e manual) para os dados de deslocamento do fio de prumo.

  - _**Timeliness**_ - Medir a qualidade dos dados do fio de prumo ao nível temporal, sendo para tal necessário implementar métricas onde se identifiquem intervalos de aquisição de dados, densidade temporal por forma a verificar se a quantidade de registos vão de encontro ao que está definido.


___

#### Ciclo de Melhoria Contínua (Continuous Improvement Cycle) 
- **Sensor do fio de prumo**
  - Etapas

    | Etapa | Descrição |
    | :--- | :--- |
    | Definição | Definição de DQ Checks e Thresholds manuais no ficheiro de configuração |
    | Execução dos DQ Checks | Execução do processo de avaliação da qualidade de dados, através da avaliação definidas e implementadas na framework. |
    | Avaliação dos DQ Checks | Execução do Threhsold Validator por forma a monitorizar os resultados produzidos pelos DQ Checks |
    | Análise | Produção de gráficos a partir dos resultados de DQ Checks e Threshold Validator. Interpretação e análise crítica dos resultados |
    | Observabilidade | Análise dos registos detalhados que foram avaliados durante o processo de avaliação de qualidade de dados |
    | Ação | Aplicar medidas corretivas tendo por base os outputs da framework |
    | Revisão | Revisão das políticas, DQ Checks, thresholds e fluxos de dados |

  - Ferramentas

    | Campo | Descrição |
    | :--- | :--- |
    | Ferramentas de suporte | Framework Data Quality implementada em Python:<br>Logs<br>Gráficos produzidos pelos DQ Checks<br>Gráficos produzidos pelo Threhsold Validator<br>Relatório detalhados dos registos avaliados<br>Ficheiros .csv |




