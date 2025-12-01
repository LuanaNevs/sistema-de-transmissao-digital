import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

class SistemaComunicacao:
    def __init__(self):
        self.logs = []  # Inicializa a lista de logs
        self.criar_pastas()  # Cria as pastas para logs e gráficos
        
    def criar_pastas(self):
        # Cria as pastas de logs e gráficos, se não existirem
        if not os.path.exists('logs'):
            os.makedirs('logs')
        if not os.path.exists('graphs'):
            os.makedirs('graphs')    
    
    def log(self, mensagem):
        # Adiciona a mensagem ao log com timestamp e exibe na tela
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {mensagem}"
        self.logs.append(log_msg)
        print(log_msg)  # Exibe o log imediatamente na tela
    
    def ascii_para_binario(self, texto):
        # Converte o texto ASCII para uma string binária
        binario = ''.join(format(ord(char), '08b') for char in texto)
        self.log(f"Texto '{texto}' convertido para {len(binario)} bits")
        return binario
    
    def manchester_encode(self, binario):
        # Codifica os dados usando a codificação Manchester
        codificado = ''.join('01' if bit == '0' else '10' for bit in binario)
        self.log(f"Manchester encoding: {len(binario)} bits -> {len(codificado)} bits")
        return codificado
    
    def manchester_decode(self, codificado):
        # Decodifica os dados usando a codificação Manchester
        decodificado = ''
        for i in range(0, len(codificado), 2):
            if i+1 < len(codificado):
                par = codificado[i:i+2]
                if par == '01':
                    decodificado += '0'
                elif par == '10':
                    decodificado += '1'
                else:
                    decodificado += '0'  # Erro, assume 0
        return decodificado
    
    def bpsk_modular(self, binario):
        # Modula os dados usando BPSK (Binary Phase Shift Keying)
        return np.array([1 if bit == '1' else -1 for bit in binario])
    
    def qpsk_modular(self, binario):
        # Modula os dados usando QPSK (Quadrature Phase Shift Keying), mapeando dois bits para cada símbolo.
        if len(binario) % 2 != 0:
            binario += '0'  # Garante que o número de bits seja par
        
        simbolos = []
        for i in range(0, len(binario), 2):
            b1 = binario[i]     # primeiro bit
            b2 = binario[i+1]   # segundo bit
            
            I = 1 if b1 == '0' else -1
            Q = 1 if b2 == '0' else -1
            
            simbolos.append([I, Q])
        
        return np.array(simbolos)
    
    def adicionar_ruido_awgn(self, sinal, snr_db):
        # Adiciona ruído AWGN (Additive White Gaussian Noise) ao sinal.
        # SNR é dado em dB.
        snr_linear = 10 ** (snr_db / 10)
        
        if len(sinal.shape) == 1:
            potencia_sinal = np.mean(sinal ** 2)
        else:
            potencia_sinal = np.mean(np.sum(sinal ** 2, axis=1))
        
        # Calcula potência do ruído
        potencia_ruido = potencia_sinal / snr_linear
        desvio_ruido = np.sqrt(potencia_ruido / 2)
        
        # Gera e adiciona o ruído
        ruido = np.random.normal(0, desvio_ruido, sinal.shape)
        return sinal + ruido
    
    def bpsk_demodular(self, sinal_ruidoso):
        # Demodula o sinal BPSK (Binary Phase Shift Keying)
        return ''.join('1' if s > 0 else '0' for s in sinal_ruidoso)
    
    def qpsk_demodular(self, sinal_ruidoso):
        # Demodula o sinal QPSK (Quadrature Phase Shift Keying)
        bits = ''
        for simbolo in sinal_ruidoso:
            i, q = simbolo
            bit1 = '0' if i > 0 else '1'
            bit2 = '0' if q > 0 else '1'
            bits += bit1 + bit2
        return bits
    
    def calcular_ber(self, original, recebido):
        # Calcula a Taxa de Erro de Bits (BER) comparando os sinais original e recebido
        min_len = min(len(original), len(recebido))
        erros = sum(1 for i in range(min_len) if original[i] != recebido[i])
        return erros / min_len if min_len > 0 else 0
    
    def simular(self, mensagem, tipo_modulacao, snr_min, snr_max, snr_passo):
        # Simula a transmissão de uma mensagem com diferentes valores de SNR.
        self.logs = []  # Limpa logs anteriores
        self.log("="*60)
        self.log("INICIANDO SIMULAÇÃO")
        self.log("="*60)
        self.log(f"Mensagem: '{mensagem}'")
        self.log(f"Modulação: {tipo_modulacao}")
        self.log(f"SNR: {snr_min} a {snr_max} dB (passo {snr_passo})")
        self.log("") 

        # 1. Converter mensagem para binário
        self.log("ETAPA 1: Conversão ASCII -> Binário")
        binario_original = self.ascii_para_binario(mensagem)
        self.log(f"Primeiros 40 bits: {binario_original[:40]}...")
        self.log("")

        # 2. Codificar usando Manchester
        self.log("ETAPA 2: Codificação Manchester")
        binario_codificado = self.manchester_encode(binario_original)
        self.log(f"Primeiros 40 bits codificados: {binario_codificado[:40]}...")
        self.log("")

        # 3. Simulação com diferentes valores de SNR
        self.log("ETAPA 3: Simulação com diferentes SNRs")
        snr_valores = []
        ber_valores = []
        
        for snr in range(snr_min, snr_max + 1, snr_passo):
            self.log(f"\n--- Testando SNR = {snr} dB ---")
            
            # Modulação
            if tipo_modulacao == 'BPSK':
                sinal_modulado = self.bpsk_modular(binario_codificado)
                self.log(f"BPSK: {len(sinal_modulado)} símbolos modulados")
            else:  # QPSK
                sinal_modulado = self.qpsk_modular(binario_codificado)
                self.log(f"QPSK: {len(sinal_modulado)} símbolos modulados")
            
            # Adicionar ruído AWGN
            sinal_ruidoso = self.adicionar_ruido_awgn(sinal_modulado, snr)
            self.log(f"Ruído AWGN adicionado (SNR={snr} dB)")
            
            # Demodulação
            if tipo_modulacao == 'BPSK':
                binario_demodulado = self.bpsk_demodular(sinal_ruidoso)
            else:
                binario_demodulado = self.qpsk_demodular(sinal_ruidoso)
            
            # Decodificação Manchester
            binario_recebido = self.manchester_decode(binario_demodulado)
            self.log(f"Demodulação e decodificação concluídas")
            
            # Calcular BER
            ber = self.calcular_ber(binario_original, binario_recebido)
            self.log(f"BER = {ber:.6f} ({int(ber*len(binario_original))} erros em {len(binario_original)} bits)")
            
            snr_valores.append(snr)
            ber_valores.append(ber)
        
        self.log("\n" + "="*60)
        self.log("SIMULAÇÃO CONCLUÍDA")
        self.log("="*60)
        
        return snr_valores, ber_valores, binario_original, binario_codificado, sinal_modulado
    
    def plotar_resultados(self, snr_valores, ber_valores, tipo_modulacao, mensagem, sinal_modulado, snr_min, snr_max, snr_passo):
        # Plota os resultados da simulação, incluindo o gráfico de BER vs SNR e outros gráficos
        
        # Gerar nome base para os arquivos de gráficos
        horario = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_base = f"{mensagem}_SNR_{snr_min}_{snr_max}_{snr_passo}_{tipo_modulacao}_{horario}"

        # Plotar o gráfico BER vs SNR
        plt.figure(figsize=(10, 6))
        ber_plot = [max(b, 1e-7) for b in ber_valores]
        
        if max(ber_plot) > 1e-6:
            plt.semilogy(snr_valores, ber_plot, 'o-', linewidth=2, markersize=8, label=tipo_modulacao, color='#6366f1')
            plt.ylabel('BER (Taxa de Erro de Bits) - Escala Log', fontsize=12)
        else:
            plt.plot(snr_valores, ber_valores, 'o-', linewidth=2, markersize=8, label=tipo_modulacao, color='#6366f1')
            plt.ylabel('BER (Taxa de Erro de Bits)', fontsize=12)
        
        plt.grid(True, alpha=0.3)
        plt.xlabel('SNR (dB)', fontsize=12)
        plt.title(f'Desempenho BER vs SNR\nMensagem: "{mensagem}" | Codificação: Manchester | Modulação: {tipo_modulacao}', fontsize=12, fontweight='bold')
        plt.legend(fontsize=10)
        
        # Salvar gráfico BER vs SNR
        plt.savefig(f"graphs/BER_vs_SNR_{nome_base}.png")
        plt.show()
        plt.close()

        # Plotar amostragem do sinal
        plt.figure(figsize=(10, 6))
        t = np.linspace(0, len(sinal_modulado) / 100, len(sinal_modulado))
        plt.plot(t, sinal_modulado, label='Sinal Amostrado', color='b')
        plt.xlabel('Tempo [s]')
        plt.ylabel('Amplitude')
        plt.title('Amostragem do Sinal')
        plt.grid(True)

        # Salvar gráfico de amostragem
        plt.savefig(f"graphs/Amostragem_do_Sinal_{nome_base}.png")
        plt.show()
        plt.close()

        # Plotar a constelação de modulação
        if tipo_modulacao == 'BPSK':
            plt.figure(figsize=(6, 6))
            plt.scatter(sinal_modulado, np.zeros_like(sinal_modulado), label='Constelação BPSK', color='r')
            plt.xlim(-1.5, 1.5)
            plt.ylim(-1.5, 1.5)
            plt.xlabel('I')
            plt.ylabel('Q')
            plt.title('Constelação BPSK')
            plt.grid(True)
            
            # Salvar gráfico de constelação BPSK
            plt.savefig(f"graphs/Constelacao_BPSK_{nome_base}.png")
            plt.show()
            plt.close()

        elif tipo_modulacao == 'QPSK':
            plt.figure(figsize=(6, 6))
            plt.scatter(sinal_modulado[:, 0], sinal_modulado[:, 1], label='Constelação QPSK', color='g')
            plt.xlim(-1.5, 1.5)
            plt.ylim(-1.5, 1.5)
            plt.xlabel('I')
            plt.ylabel('Q')
            plt.title('Constelação QPSK')
            plt.grid(True)
            
            # Salvar gráfico de constelação QPSK
            plt.savefig(f"graphs/Constelacao_QPSK_{nome_base}.png")
            plt.show()
            plt.close()

        # Plotar quantização do sinal
        quantizacao = np.sign(sinal_modulado)  # Quantização simples
        plt.figure(figsize=(10, 6))
        plt.plot(t, sinal_modulado, label='Sinal Original', color='b')
        plt.step(t, quantizacao, label='Sinal Quantizado', color='r', where='post')
        plt.xlabel('Tempo [s]')
        plt.ylabel('Amplitude')
        plt.title('Quantização do Sinal')
        plt.grid(True)
        plt.legend()
        
        # Salvar gráfico de quantização
        plt.savefig(f"graphs/Quantizacao_{nome_base}.png")
        plt.show()
        plt.close()

        # Plotar duração do sinal no tempo
        plt.figure(figsize=(10, 6))
        plt.plot(t, sinal_modulado, label='Sinal no Tempo', color='b')
        plt.xlabel('Tempo [s]')
        plt.ylabel('Amplitude')
        plt.title('Duração do Sinal no Tempo')
        plt.grid(True)
        
        # Salvar gráfico de duração do sinal
        plt.savefig(f"graphs/Duracao_do_Sinal_{nome_base}.png")
        plt.show()
        plt.close()

    def salvar_logs(self):
        # Salva os logs da simulação em um arquivo de texto na pasta 'logs'
        nome_arquivo = f'logs/log_simulacao_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.logs))
        print(f"Log salvo em: {nome_arquivo}")

# Função principal do menu
def menu_principal():
    # Interface de linha de comando para o menu principal
    while True:
        # Limpar tela (funciona no Windows e Linux/Mac)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("="*60)
        print("SISTEMA DE COMUNICAÇÃO DIGITAL")
        print("Trabalho II - Redes de Computadores")
        print("="*60)
        print()
        
        sistema = SistemaComunicacao()
        
        # Configurações da simulação
        mensagem = input("Digite a mensagem ASCII (padrão: HELLO): ").strip()
        if not mensagem:
            mensagem = "HELLO"
        
        print("\nEscolha a modulação:")
        print("1 - BPSK (Binary Phase Shift Keying)")
        print("2 - QPSK (Quadrature Phase Shift Keying)")
        escolha = input("Opção (1 ou 2): ").strip()
        tipo_modulacao = 'QPSK' if escolha == '2' else 'BPSK'
        
        print("\nConfiguração do SNR (Signal-to-Noise Ratio):")
        snr_min = int(input("SNR mínimo em dB (padrão: 0): ") or "0")
        snr_max = int(input("SNR máximo em dB (padrão: 10): ") or "10")
        snr_passo = int(input("Passo do SNR em dB (padrão: 2): ") or "2")
        
        print("\n" + "="*60)
        print("INICIANDO SIMULAÇÃO...")
        print("="*60 + "\n")
        
        # Executar simulação
        snr_vals, ber_vals, bin_orig, bin_cod, sinal_modulado = sistema.simular(
            mensagem, tipo_modulacao, snr_min, snr_max, snr_passo
        )
        
        # Mostrar estatísticas finais
        print("\n" + "="*60)
        print("ESTATÍSTICAS FINAIS")
        print("="*60)
        print(f"Mensagem original: '{mensagem}'")
        print(f"Bits originais: {len(bin_orig)}")
        print(f"Bits após Manchester: {len(bin_cod)} (dobro) ")
        print(f"Modulação: {tipo_modulacao}")
        print(f"Codificação de canal: Manchester")
        print(f"Tipo de ruído: AWGN (Additive White Gaussian Noise)")
        print()
        print(f"Melhor BER: {min(ber_vals):.6f} (SNR = {snr_vals[ber_vals.index(min(ber_vals))]} dB)")
        print(f"Pior BER: {max(ber_vals):.6f} (SNR = {snr_vals[ber_vals.index(max(ber_vals))]} dB)")
        print("="*60)
        
        # Salvar logs
        sistema.salvar_logs()
        
        # Plotar resultados
        print("\nGerando gráfico...")
        sistema.plotar_resultados(snr_vals, ber_vals, tipo_modulacao, mensagem, sinal_modulado, snr_min, snr_max, snr_passo)
        
        print("\n" + "="*60)
        print("Simulação concluída com sucesso!")
        print("="*60)
        
        # Perguntar se deseja realizar outra simulação
        print("\nDeseja realizar outra simulação?")
        print("1 - Sim, nova simulação")
        print("2 - Não, sair do programa")
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao != '1':
            print("\n" + "="*60)
            print("Encerrado o Sistema de Transmissão Digital!")
            print("="*60)
            break
        
        print("\n\nIniciando nova simulação...\n")
        input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    menu_principal()
