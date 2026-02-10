import pandas as pd

def apurar_vencedor(valor_real):
    try:
        df = pd.read_csv('palpites.csv')
        
        if df.empty:
            print("O arquivo de palpites está vazio.")
            return

        # Calcula a diferença absoluta entre o palpite e o valor real
        df['diferenca'] = (df['palpite'] - valor_real).abs()

        # Ordena pela menor diferença. Se houver empate na distância, 
        # o critério de desempate é quem comentou primeiro (data_postagem)
        df = df.sort_values(by=['diferenca', 'data_postagem'])

        vencedor = df.iloc[0]

        print("-" * 30)
        print(f"🏆 RESULTADO OFICIAL 🏆")
        print("-" * 30)
        print(f"Valor Real: {valor_real} feijões")
        print(f"Vencedor: @{vencedor['usuario']}")
        print(f"Palpite: {vencedor['palpite']}")
        print(f"Diferença: {vencedor['diferenca']} feijão(ões)")
        print(f"Data do palpite: {vencedor['data_postagem']}")
        print("-" * 30)

        # Opcional: Salvar o ranking dos TOP 5 em um arquivo
        df.head(5).to_csv('vencedores_top5.csv', index=False)
        print("O ranking TOP 5 foi salvo em 'vencedores_top5.csv'")

    except FileNotFoundError:
        print("Erro: O arquivo 'palpites.csv' não foi encontrado.")

if __name__ == "__main__":
    resultado = int(input("Digite a quantidade real de feijões contados: "))
    apurar_vencedor(resultado)