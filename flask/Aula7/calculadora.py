import math

from flask import render_template, request


def calcular():
    num1 = float(request.form.get("num1",0))
    num2 = float(request.form.get("num2",0))
    operacao = request.form["operacao"]

    if operacao == "sqrt":
        if num1 < 0:
            resultado = "Erro: número negativo"
            etapas = f"Não existe raiz real de {num1}."
        else:
            resultado = math.sqrt(num1)
            etapas = f"√{num1} = {resultado}"
    elif operacao == "bskr":
        num3 = float(request.form.get("num3",0))
        if not num2 and num3:
            resultado="Erro: dados invalidos"
            etapas="Informe o segundo ou terceiro número para esta operação."
        else:
            if num1 == 0:
                resultado="Erro: 'a' não pode ser 0"
                etapas+="O coeficiente 'a' deve ser diferente de 0."
            else:
                delta = (num2**2) - (4 * num1 * num3)
                etapas = f"Δ = {num2}² - 4 * {num1} * {num3} = {delta}\n"

                if delta < 0:
                    resultado="Sem raízes reais"
                    etapas="Como delta é < 0, não existe raizes"
                elif delta == 0:
                    x = -num2 / (2*num1)
                    resultado = x
                    etapas += f"x = -({num2}) / (2 * {num1}) = {resultado}\n"
                else:
                    x1 = (num2 + math.sqrt(delta)) / (2 * num1)
                    x2 = (-num2 + math.sqrt(delta)) / (2 * num1)
                    resultado = f"x1 = {x1} - x2 = {x2}"
                    etapas += f"x = (-({num2}) ± √{delta}) / (2 * {num1})\n"
                    etapas += f"{resultado}"
    else:
        if not num2:
            resultado="Erro: dados invalidos"
            etapas="Informe o segundo número para esta operação."

        if operacao == "+":
            resultado = num1 + num2
            etapas = f"{num1} + {num2} = {resultado}"
        elif operacao == "-":
            resultado = num1 - num2
            etapas = f"{num1} - {num2} = {resultado}"
        elif operacao == "*":
            resultado = num1 * num2
            etapas = f"{num1} * {num2} = {resultado}"
        elif operacao == "/":
            if num2 != 0:
                resultado = num1 / num2
                etapas = f"{num1} / {num2} = {resultado}"
            else:
                resultado = "Erro: Divisão por zero"
                etapas = "Não é possível dividir por zero."
        elif operacao == "**":
            resultado = num1 ** num2
            etapas = f"{num1} ** {num2} = {resultado}"
        elif operacao == "log":
            resultado = math.log(num1,num2)
            etapas = f"log{num2}({num1}) = {resultado}"
        else:
            resultado = "Operação inválida"
            etapas = "A operação selecionada é inválida."

    return render_template("calculadora.html", etapas=etapas, resultados=resultado)
