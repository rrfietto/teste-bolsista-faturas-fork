# Desenvolva aqui sua atividade

# - O número da instalação
# - Mês ao qual a fatura é referente
# - Tarifa cheia (com impostos)
# - Valor A Pagar para a distribuidora
# - Somatório das componentes de energia injetada

import pdfplumber
import re
import pandas as pd

pdf = pdfplumber.open("./fatura_cpfl.pdf");

page = pdf.pages[0];

text = page.extract_text();

matched_instalacao = re.search(r'www\.cpfl\.com\.br\s+(\d+)', text).group(1);
# print(matched_instalacao);

matched_mes_fatura = re.search(r'INSTALAÇÃO\s+([A-Z]{3}/\d{4})', text).group(1);
# print(matched_mes_fatura);


matched_tarifa = re.findall(r'Energia Ativa Fornecida - .*?kWh\s+(\d+,\d+)', text);

tarifa_cheia = 0;
for tarifa in matched_tarifa:
    tarifa = tarifa.replace(",", ".")
    tarifa_cheia += float(tarifa);

matched_valor_pagar_destribuidora = re.search(r'Total Distribuidora\s+(\d+,\d+)', text).group(1);
matched_valor_pagar_destribuidora = matched_valor_pagar_destribuidora.replace(",", ".")
# print(matched_valor_pagar_destribuidora);

matched_componentes = re.findall(r'Energ Atv Inj.*?kWh\s+\d+,\d+\s+(\d+,\d+)-', text);

soma = 0;

for componente in matched_componentes:
    componente = componente.replace(",", ".")
    soma += float(componente);

soma = round(soma, 2);
soma *= -1;
# print(soma);

df = pd.DataFrame({
    "Campo": [
        "Instalação",
        "Referência",
        "Tarifa cheia (com impostos)",
        "Valor da distribuidora",
        "Somatório de energia injetada"
    ],
    "Valor": [
        matched_instalacao,
        matched_mes_fatura,
        tarifa_cheia,
        matched_valor_pagar_destribuidora,
        soma
    ]
})

print(df)
    

