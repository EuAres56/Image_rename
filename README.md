# Renomeador de Imagens OCR

Aplicação desktop com interface web (via Flask) para renomear imagens com base no texto extraído por OCR. O sistema usa a API OCR.Space para reconhecimento óptico de caracteres e renomeia arquivos de imagem conforme o horário detectado no texto das fotos.

---

## Funcionalidades

- Seleção de pasta local com imagens (.jpg, .jpeg, .png)
- Processamento automático das imagens para extração do texto via OCR
- Renomeação dos arquivos baseando-se em padrões de horário encontrados no texto
- Indicação visual do progresso do processamento via barra de progresso
- Logs de erro para facilitar o debug
- Interface web simples e responsiva com Bootstrap
- Seleção da pasta via janela nativa do sistema operacional (Tkinter)

---

## Tecnologias

- Python 3.x
- Flask
- Pillow (PIL)
- Tkinter (para seleção da pasta)
- API OCR.Space
- Bootstrap 5 (frontend)
- JSON para logs e configurações

---

## Como usar

### Pré-requisitos

- Python 3.8 ou superior
- Instalar dependências:

```bash
pip install -r requirements.txt

## Video de uso e explicação do projeto
YouTube:
