# Menu Translator 🍽️

Um aplicativo web moderno e responsivo desenvolvido em Python com Flask que extrai e traduz automaticamente textos de cardápios físicos (imagens) em diversos idiomas, como Inglês, Russo e outros. O sistema organiza pratos e valores em uma tabela limpa e fácil de ler, contando também com um modo escuro nativo e histórico local de consultas.

---

## 🚀 Funcionalidades

* **OCR Multilíngue:** Extração de textos usando `pytesseract` com suporte a múltiplos pacotes de idiomas simultâneos (`por+eng+rus`).
* **Tradução Inteligente:** Integração com a API do Google Translator através da biblioteca `deep-translator`.
* **Filtro de Preços:** Identificação automática de valores e moedas por meio de Expressões Regulares (Regex).
* **Interface Dark Mode:** Frontend limpo, moderno e responsivo estilizado com CSS puro.
* **Histórico Dinâmico:** Exibição dos últimos cardápios enviados na página inicial via Jinja2 templates.
* **Acesso Mobile:** Configurado para rodar na rede local e permitir o uso direto da câmera do celular.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** [Python 3](https://www.python.org/) / [Flask](https://flask.palletsprojects.com/)
* **Processamento de Imagem & OCR:** [Pillow (PIL)](https://python-pillow.org/) / [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
* **Tradução:** [Deep Translator](https://github.com/nidhaloff/deep-translator)
* **Frontend:** HTML5 / CSS3 (Modo Escuro) / Jinja2

---

## 🔧 Como Rodar o Projeto Localmente

### Pré-requisitos
É necessário ter o **Python 3** instalado e o motor do **Tesseract OCR** configurado no seu sistema operacional (ex: Arch Linux/CachyOS, Ubuntu, Windows).

### Passo a Passo

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/HIDEKI-SHIN/menu-traslater.git](https://github.com/HIDEKI-SHIN/menu-traslater.git)
   cd menu-traslater
