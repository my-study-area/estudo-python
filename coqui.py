import os
from datetime import datetime
from PyPDF2 import PdfReader
from TTS.api import TTS

# 📄 Nome do arquivo PDF
# pdf_file = "seja-uma-maquina-de-aprender.pdf"
pdf_file = "blink-deveficiente-domain-driven-design-as-partes-que-realmente-importam.pdf"

# 📁 Caminho absoluto (mesma pasta do script)
base_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(base_dir, pdf_file)

# 🕒 Gerar timestamp
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

# 🎧 Nome do arquivo de saída
output_file = pdf_file.replace(".pdf", f"-{timestamp}.wav")
output_path = os.path.join(base_dir, output_file)

# 📖 Ler PDF
reader = PdfReader(pdf_path)
texto = ""

for pagina in reader.pages:
    conteudo = pagina.extract_text()
    if conteudo:
        texto += conteudo + "\n"

# 🧹 Limpeza básica
texto = texto.replace("\n", " ").strip()

print('texto gerado: {texto}')
# ✂️ Dividir texto (evita erro em textos grandes)
def dividir_texto(texto, max_chars=5000):
    return [texto[i:i+max_chars] for i in range(0, len(texto), max_chars)]

partes = dividir_texto(texto)

# 🧠 Carregar modelo Coqui (português)
tts = TTS(model_name="tts_models/pt/cv/vits", progress_bar=True)

# 🔊 Gerar áudio por partes
arquivos_temp = []

for i, parte in enumerate(partes):
    temp_file = os.path.join(base_dir, f"temp_{i}.wav")
    tts.tts_to_file(text=parte, file_path=temp_file)
    arquivos_temp.append(temp_file)

# 🔗 Juntar áudios
import wave


print('criando arquivo de audio ...')
with wave.open(output_path, 'wb') as output:
    with wave.open(arquivos_temp[0], 'rb') as first:
        output.setparams(first.getparams())

    for arquivo in arquivos_temp:
        with wave.open(arquivo, 'rb') as w:
            output.writeframes(w.readframes(w.getnframes()))

print('limpando temporários ...')
# 🧹 Limpar temporários
for arquivo in arquivos_temp:
    os.remove(arquivo)

print(f"✅ Áudio gerado: {output_path}")
