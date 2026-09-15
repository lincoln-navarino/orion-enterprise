import os, re
import pandas as pd

# Texto com os dados brutos do TikTok colados pelo usuário
CSV_PATH_RAW = os.path.join("arquivos", "tiktok_pedidos_bruto.csv")

def formatar_valor(v):
    if pd.isna(v): return 0.0
    s = str(v).replace("BRL", "").replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(s)
    except:
        return 0.0

def processar_e_organizar(raw_csv_path):
    df = pd.read_csv(raw_csv_path, dtype=str)
    print(f"Total de linhas lidas: {len(df)}")
    print("Colunas:", df.columns.tolist()[:10])

    # Coluna de data
    date_col = "Created Time" if "Created Time" in df.columns else ("Paid Time" if "Paid Time" in df.columns else df.columns[0])
    
    # Converter para datetime
    df["_dt"] = pd.to_datetime(df[date_col].str.strip(), format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
    
    # Fallback para outros formatos se necessário
    if df["_dt"].isna().sum() > 0:
        df["_dt"] = df["_dt"].fillna(pd.to_datetime(df[date_col].str.strip(), errors="coerce"))

    # Mapear Ano e Mês
    meses_map = {
        1: "01-Janeiro", 2: "02-Fevereiro", 3: "03-Março", 4: "04-Abril",
        5: "05-Maio", 6: "06-Junho", 7: "07-Julho", 8: "08-Agosto",
        9: "09-Setembro", 10: "10-Outubro", 11: "11-Novembro", 12: "12-Dezembro"
    }

    df["Ano"] = df["_dt"].dt.year.fillna(2026).astype(int).astype(str)
    df["Mes_Num"] = df["_dt"].dt.month.fillna(7).astype(int)
    df["Mes_Nome"] = df["Mes_Num"].map(meses_map)

    # Agrupar e salvar nas pastas de Vendas
    for (ano, mes_nome), grp in df.groupby(["Ano", "Mes_Nome"]):
        pasta_dest = os.path.join("arquivos", "Relatórios", "Vendas", str(ano), mes_nome, "TikTok")
        os.makedirs(pasta_dest, exist_ok=True)
        
        # Salvar arquivo CSV limpo
        file_dest = os.path.join(pasta_dest, f"Pedidos_TikTok_{mes_nome}_{ano}.csv")
        # Remover colunas temporárias antes de salvar
        grp_save = grp.drop(columns=["_dt", "Ano", "Mes_Num", "Mes_Nome"])
        grp_save.to_csv(file_dest, index=False, encoding="utf-8-sig")
        print(f"✅ Salvo: {file_dest} ({len(grp_save)} pedidos)")

if __name__ == "__main__":
    if os.path.exists(CSV_PATH_RAW):
        processar_e_organizar(CSV_PATH_RAW)
