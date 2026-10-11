import io
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS

app = FastAPI(
    title="Ultimate Text-to-Speech API",
    description="Convert text to speech with stable language and speed options."
)

# تفعيل الـ CORS لمنع أخطاء المتصفح
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/text-to-speech", summary="Convert Text to MP3 Audio")
async def text_to_speech(
    text: str = Query(..., description="The text you want to convert into speech"),
    lang: str = Query("ar", description="Language code: 'ar' for Arabic, 'en' for English"),
    speed: str = Query("normal", description="Choose speed: 'normal' (عادي) or 'slow' (بطيء)")
):
    if not text.strip():
        raise HTTPException(
            status_code=400, 
            detail="The text parameter cannot be empty."
        )

    try:
        # تحديد ما إذا كان الصوت بطيئاً أم عادياً مباشرة عبر gTTS
        is_slow = True if speed.lower() == "slow" else False
        
        # توليد الصوت بشكل مستقر وآمن تماماً
        tts = gTTS(text=text, lang=lang, slow=is_slow)
        
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return StreamingResponse(
            audio_buffer,
            media_type="audio/mpeg",
            headers={"Content-Disposition": 'attachment; filename="speech_output.mp3"'}
        )

    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate speech. Error: {str(err)}"
        )