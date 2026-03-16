# Sistema de Controle de EPI 🦺

Este é um **sistema de gerenciamento de Equipamentos de Proteção Individual (EPI)** feito em **Python** com **Streamlit**.  

Permite cadastrar funcionários, cadastrar EPIs, registrar entregas com assinatura digital, gerar fichas em PDF, acompanhar histórico e alertas de vencimento.

---

## 📌 Funcionalidades

- Cadastro de **Funcionários** com status (Ativo / Desligado)
- Cadastro de **EPIs** com validade e fabricante
- Registro de **entrega de EPIs** com:
  - Seleção de funcionário e EPI
  - Data de entrega
  - Assinatura digital do funcionário
  - Geração de ficha em PDF
- **Dashboard** com métricas e gráficos
- Filtros por funcionário e data
- Histórico de entregas em tabela
- Alertas de vencimento próximos ou vencidos

---

## 🛠 Tecnologias utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Pillow](https://python-pillow.org/)
- [streamlit-drawable-canvas](https://github.com/andfanilo/streamlit-drawable-canvas)
- SQLite (banco de dados local)

---

## ⚙️ Como executar o projeto

1. Clone este repositório:

```bash
git clone https://github.com/SEUUSUARIO/controle_epi.git
cd controle_epi
