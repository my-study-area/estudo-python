from PyPDF2 import PdfReader
from gtts import gTTS

# Ler PDF
reader = PdfReader("seja-uma-maquina-de-aprender.pdf")
texto = ""

for pagina in reader.pages:
    texto += pagina.extract_text()
    print(texto)

# Converter para áudio
tts = gTTS(text=texto, lang='pt')
tts.save("audio2.mp3")

print("Áudio gerado com sucesso!")
