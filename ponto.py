

if __name__ == '__main__':
    menu = """
##########################
    BATIDA DE PONTO Menu

    Opções:
    1 - Bater Ponto Diário
    2 - Inserir Ponto
    3 - Comprovante de hoje

    0 - Sair
    """
    while 1:
        print(menu)     
        op = input("Digite a opção desejada:\n")

        res, mss = validacao(op, 0, 3)
        if res == -1:
            print(mss)
            continue

        manneger = p.PontoBD()

        if op == '1':
            retorno = manneger.ponto()
            if retorno == -1:
                if manneger.batida.hour < 12:
                    tipo = 'entrada'
                else: tipo = 'saida'
                print(f'Ponto de {tipo} já registrado')
            else: print('Ponto Registrado com Sucesso!!!')
            manneger.horas()
        elif op == '2':
            data = input('Digite a data (formato AAAA-MM-DD):\n')
            hora = input('Digite a hora (formato HH:MM):\n')
            while 1:
                tipo = input('Digite 1 para entrada e 2 para saida:\n')               
                res, mss = validacao(tipo, 1, 2)
                if res == -1:
                    print(mss)
                    continue
                break
            if tipo == '1':
                tipo = 'entrada'
            else: tipo = 'saida'

            ret = manneger.inserPonto(data, hora, tipo)
            if ret == -1:
                print(f'Ponto de {tipo} já marcado!')
            else:
                print('Ponto inserido com sucesso!')
            manneger.horas()    

        elif op == '3':
            data_comp = dt.date.today()
            select = f"""
            select data, hora, tipo from ponto
            where data = '{data_comp}'
            """
            dados = manneger.getQuery(select)
            print()
            print('Dia        Hora  Tipo')
            for i in range(len(dados['data'])):
                print(dados['data'][i], dados['hora'][i], dados['tipo'][i])
        
        elif test == '0':
            sys.exit(0)