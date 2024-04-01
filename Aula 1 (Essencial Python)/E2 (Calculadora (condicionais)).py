numero1 = int(input("Digite um número: "))
numero2 = int(input("Digite outro número: "))

operacao = int(input("Digite 1 para somar, 2 para subtrair, 3 para multiplicar e 4 para dividir: "))

if operacao == 1:
    resultado = numero1 + numero2
    print(resultado)

elif operacao == 2:
    resultado = numero1 - numero2
    print(resultado)

elif operacao == 3:
    resultado = numero1 * numero2
    print(resultado)

elif operacao == 4:
    resultado = numero1 / numero2
    print(resultado)
else:
    print("Operação inválida")

# > < >= <= == !=
