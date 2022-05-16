from googletrans import Translator
from translate import Translator as trans
translator = Translator()
source_lan = "en"
translated_to= "hi"
text="namaskar"
translated_text = translator.translate(text, src=source_lan, dest = translated_to)
res=translated_text.text
print(translated_text.text)