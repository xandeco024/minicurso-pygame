senha = int(input("Defina a senha: "))

senhainserida = int(input("Digite a senha: "))

while senhainserida != senha:
    print("Senha incorreta")
    senhainserida = int(input("Digite a senha: "))

print("Senha correta")