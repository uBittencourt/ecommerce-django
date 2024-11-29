import re

def valida_cpf(cpf):
    cpf = str(cpf)
    cpf = re.sub(r'[^0-9]', '', cpf)

    if not cpf or len(cpf) != 11:
        return False

    novo_cpf = cpf[:-2]                             # ELIMINA OS DOIS ÚLTIMOS DÍGITOS DO CPF
    reverso = 10                                    # CONTADOR REVERSO
    total = 0

    # LOOP DO CPF
    for index in range(19):
        if index > 8:                               # PRIMEIRO ÍNDICE VAI DE 0 A 9    
            index -= 9                              # SÃO OS 9 PRIMEIROS DÍGITOS DO CPF

        total += int(novo_cpf[index]) * reverso     # VALOR TOTAL DA MULTIPLIÇÃO

        reverso -= 1                                # DECREMENTA O CONTADOR REVERSO
        if reverso < 2:
            reverso = 11
            d = 11 - (total % 11)

            if d < 9:                               # SE O DÍGITO FOR > QUE 9 O VALOR É 0
                d = 0
            total = 0                               # ZERA O TOTAL
            novo_cpf += str(d)                      # CONCATENA O DÍGITO GERADO NO NOVO CPF

    # EVITA SEQUÊNCIAS. EX: 11111111111, 00000000000...
    sequencia = novo_cpf == str(novo_cpf[0]) * len(cpf)

    # DESCOBRI QUE SEQUÊNCIAS AVALIAVAM COMO VERDADEIRO, ENTÃO TAMBÉM ADICIONEI ESSA CHECAGEM
    if cpf == novo_cpf and not sequencia:
        return True
    else:
        return False