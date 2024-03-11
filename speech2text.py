import whisper
import os
from tqdm import tqdm
whisper_model = None
transcribe_kwargs: dict[str, Optional[str]] = {
    'model': 'tiny',
    'prompt': '以下是普通话的句子。'
    'language': None,
    # 'language': 'zh',
}
def load_whisper(model="tiny"):
    global whisper_model
    whisper_model = whisper.load_model(model)
    print("Whisper模型："+model)

def run_analysis(filename, **transcribe_kwargs):
    global whisper_model
    print("正在加载Whisper模型...")
    # 读取列表中的音频文件
    audio_list = os.listdir(f"audio/slice/{filename}")
    print("加载Whisper模型成功！")
    # 创建outputs文件夹
    os.makedirs("outputs", exist_ok=True)
    print("正在转换文本...")

    i = 1
    for fn in audio_list:
        print(f"正在转换第{i}/{len(audio_list)}个音频...")
        # 识别音频
        transcribe_kwargs["initial_prompt"] = transcribe_kwargs.get("prompt", "以下是普通话的句子。")
        transcribe_kwargs.pop("model", None)
        transcribe_kwargs.pop("prompt", None)
        
        result = whisper_model.transcribe(f"audio/slice/{filename}/{fn}", **transcribe_kwargs)
        print("".join([i["text"] for i in result["segments"] if i is not None]))

        with open(f"outputs/{filename}.txt", "a", encoding="utf-8") as f:
            f.write("".join([i["text"] for i in result["segments"] if i is not None]))
            f.write("\n")
    

# run_analysis("20231125133459")
