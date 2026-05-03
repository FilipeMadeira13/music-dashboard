# 🎵 Music Dashboard

> Dashboard interativo para explorar dados musicais com a API do Last.fm — artistas, álbuns, faixas e muito mais.

---

## 📌 Visão Geral

O **Music Dashboard** é uma aplicação web construída com **Streamlit** que consome a API do Last.fm para exibir métricas e visualizações musicais de forma intuitiva. O projeto é dividido em três painéis independentes:

| Painel | Arquivo | Descrição |
|---|---|---|
| 🎵 Top Álbuns | `pages/Top_albums.py` | Exibe os principais álbuns de um artista com informações de faixas e ouvintes |
| 🎧 Top Faixas | `pages/Top_tracks.py` | Lista as principais faixas de um artista com métricas de desempenho |
| 🔗 Artistas Similares | `Similar_artists.py` | Mostra artistas semelhantes ao pesquisado com pontuação de similaridade |

---

## ✨ Funcionalidades

- 🔍 Consulta de álbuns e faixas em tempo real via API do Last.fm
- 📊 Visualizações interativas com tabelas e gráficos
- 📥 Exportação de dados para CSV diretamente pela interface
- ⚡ Cache de resultados para reduzir chamadas repetidas à API
- 🔄 Enriquecimento de álbuns com consultas paralelas otimizadas
- ✅ Validação de dados e tratamento de erros em pontos críticos

---

## 🗂️ Estrutura do Projeto

```
music-dashboard/
├── api/
│   └── lastfm_client.py        # Cliente HTTP do Last.fm e processamento de dados
├── pages/
│   ├── Top_albums.py           # Dashboard de álbuns
│   └── Top_tracks.py           # Dashboard de faixas
├── ui/
│   └── notifications.py        # Feedback visual para download de arquivos
├── utils/
│   └── utils.py                # Funções utilitárias de conversão e formatação
├── Similar_artists.py          # Relatório de artistas similares
├── config.py                   # Carregamento de variáveis de ambiente e configuração da API
├── requirements.txt            # Dependências do projeto
└── .env                        # Chave da API (não versionar)
```

---

## ⚙️ Instalação

### Pré-requisitos

- Python **3.11+**
- `pip` instalado
- Conta e API Key do [Last.fm](https://www.last.fm/api/account/create)

### Passo a passo

**1. Clone o repositório**

```bash
git clone https://github.com/seu-usuario/music-dashboard.git
cd music-dashboard
```

**2. Crie e ative um ambiente virtual**

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python -m venv .venv
source .venv/bin/activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt streamlit
```

**4. Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto:

```env
API_KEY=sua_api_key_do_lastfm_aqui
```

> ⚠️ **Atenção:** nunca versione o arquivo `.env`. Certifique-se de que ele está listado no `.gitignore`.

---

## 🚀 Como Usar

Execute cada painel individualmente com o Streamlit:

```bash
# Dashboard de álbuns
streamlit run pages/Top_albums.py

# Dashboard de faixas
streamlit run pages/Top_tracks.py

# Relatório de artistas similares
streamlit run Similar_artists.py
```

Acesse a aplicação no navegador em `http://localhost:8501`.

---

## 🛣️ Melhorias Futuras

- [ ] Adicionar testes automatizados para as funções de processamento de dados
- [ ] Criar uma página inicial unificada com navegação entre os painéis
- [ ] Aplicar estilo visual customizado com temas Streamlit
- [ ] Suporte a múltiplos idiomas (i18n)
- [ ] Implementar autenticação de usuário com OAuth do Last.fm

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request*.

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).