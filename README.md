
# Sistema de Comunicação Digital - Executável

Este projeto contém um executável para rodar um sistema de comunicação digital, utilizando técnicas de modulação BPSK e QPSK, com codificação Manchester e ruído AWGN (Additive White Gaussian Noise). O objetivo é demonstrar o impacto dessas técnicas na taxa de erro de bits (BER) e na eficiência espectral do sistema de comunicação.

## Como executar o Executável

### Passo 1: Baixar o Executável

Se você já tem o executável, siga para o Passo 2. Caso contrário, faça o download do arquivo **SistemaTransmissaoDigital.exe** na pasta `executables/` do repositório.

### Passo 2: Executar o Executável

- **Windows**: Clique duas vezes no arquivo `SistemaTransmissaoDigital.exe` para iniciar o programa.
- **Outros sistemas operacionais**: Para sistemas Linux ou MacOS, você pode executar o executável no terminal, caso tenha gerado a versão para esses sistemas. Caso contrário, o código precisa ser executado via Python.

### Passo 3: Configurações da Simulação

O programa solicitará algumas configurações para a simulação:

1. **Mensagem**: Insira a mensagem que deseja transmitir em formato ASCII (por padrão, a mensagem será "HELLO").
2. **Tipo de Modulação**: Escolha entre:
   - **1**: BPSK (Binary Phase Shift Keying)
   - **2**: QPSK (Quadrature Phase Shift Keying)
3. **Configuração de SNR**:
   - Defina o **SNR mínimo** (em dB).
   - Defina o **SNR máximo** (em dB).
   - Defina o **passo do SNR** (em dB).

### Passo 4: Resultados

Após a execução da simulação:

- **Logs**: Os logs serão salvos automaticamente na pasta `logs/`.
- **Gráficos**: Os gráficos gerados (como o gráfico de **BER vs SNR**) serão salvos na pasta `graphs/`.

## Estrutura do Repositório

```
SistemaTransmissaoDigital/
│
├── executables/                   # Pasta para arquivos executáveis
│   └── SistemaTransmissaoDigital.exe  # Executável gerado (Windows)
│
├── logs/                          # Pasta para logs gerados durante a execução
│   └── log_simulacao_20251201.txt  # Exemplo de arquivo de log gerado
│
├── graphs/                        # Pasta para gráficos gerados
│   ├── BER_vs_SNR_Hello_20251201.png  # Gráfico de BER vs SNR
│   ├── Amostragem_do_Sinal_Hello_20251201.png  # Gráfico de amostragem do sinal
│   ├── Constelacao_BPSK_Hello_20251201.png   # Gráfico de constelação BPSK
│   └── Quantizacao_Hello_20251201.png  # Gráfico de quantização do sinal
│
└── .gitignore                     # Arquivo para excluir arquivos desnecessários (ex: arquivos temporários, ambientes virtuais)
```

## Links de Acesso
- [Apresentação no Canva](https://www.canva.com/design/DAG6HYq765g/hry7MGrFFX_h6PXtJk6Vlw/view?utm_content=DAG6HYq765g&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h5731f0eddf)
- [Video Simulação](https://drive.google.com/file/d/1ETdFXeYkCr0X-jIHK_-G_xe7oal580v2/view?usp=drive_link)
- [Gráficos e Logs](https://drive.google.com/drive/folders/1697qh9M47IgSY1b_cOrbWbME5KDrbVfL?usp=drive_link)

## Autor

- **Luana Lopes**  
  Universidade do Vale do Rio dos Sinos - Unisinos  
  Disciplina de Redes de Computadores - Internetworking, Roteamento e Transmissão
