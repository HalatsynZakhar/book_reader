from gtts import gTTS
from gtts.tokenizer import pre_processors
tts = gTTS(""""“This changes everything,” said Dickie. “That thing evens the odds.” Graves was as excited about the gun as Rob was, that much anyone could see.""")
tts.save('hello.mp3')
playsound('hello.mp3')