import os
from datetime import datetime
import re
import fitz  # PyMuPDF
from TTS.api import TTS
import wave

# 📄 Nome do arquivo PDF
pdf_file = "blink-deveficiente-domain-driven-design-as-partes-que-realmente-importam.pdf"

# 📁 Caminho base (mesma pasta do script)
base_dir = os.path.dirname(os.path.abspath(__file__))
pdf_path = os.path.join(base_dir, pdf_file)

# 🕒 Timestamp
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

# 🎧 Nome do arquivo de saída
output_file = pdf_file.replace(".pdf", f"-{timestamp}.wav")
output_path = os.path.join(base_dir, output_file)

# 📖 Função para extrair texto com PyMuPDF
def extrair_texto_pdf(caminho_pdf):
    texto = ""
    doc = fitz.open(caminho_pdf)
    
    for pagina in doc:
        texto += pagina.get_text() + "\n"
        print(texto)
        print('=======')
    
    doc.close()
    return texto

# 🧹 Limpeza do texto
def limpar_texto(texto):
    texto = re.sub(r'\S+@\S+', '', texto)
    texto = re.sub(r'IP:\s*\d+\.\d+\.\d+\.\d+', '', texto)
    texto = re.sub(r'Adriano Avelino.*', '', texto)
    texto = re.sub(r'\.{2,}', '.', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

# ✂️ Dividir texto
def dividir_texto(texto, max_chars=4000):
    return [texto[i:i+max_chars] for i in range(0, len(texto), max_chars)]

# 🚀 Execução
texto = extrair_texto_pdf(pdf_path)
texto = limpar_texto(texto)
partes = dividir_texto(texto)

# 🧠 Modelo multilíngue (melhor pt-BR)
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

arquivos_temp = []

print("🔊 Gerando áudio...")

speaker_wav = os.path.join(base_dir, "voz-br.wav")

for i, parte in enumerate(partes):
    temp_file = os.path.join(base_dir, f"temp_{i}.wav")
    
    tts.tts_to_file(
        text=parte,
        file_path=temp_file,
        language="pt",
        speaker_wav=speaker_wav
    )
    
    arquivos_temp.append(temp_file)
    print(f"Parte {i+1}/{len(partes)} concluída")

# 🔗 Juntar áudios
with wave.open(output_path, 'wb') as output:
    with wave.open(arquivos_temp[0], 'rb') as first:
        output.setparams(first.getparams())

    for arquivo in arquivos_temp:
        with wave.open(arquivo, 'rb') as w:
            output.writeframes(w.readframes(w.getnframes()))

# 🧹 Limpar arquivos temporários
for arquivo in arquivos_temp:
    os.remove(arquivo)

print(f"\n✅ Áudio final gerado:")
print(output_path)
