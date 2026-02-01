"""
生成示例案例脚本
"""
import sys
import json
from pathlib import Path

# 添加 echuu 模块到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from echuu import EchuuLiveEngine


def generate_example(name: str, persona: str, background: str, topic: str, language: str = "zh"):
    """生成一个示例案例"""
    print(f"\n{'='*60}")
    print(f"生成案例: {name} - {topic}")
    print(f"语言: {language}")
    print(f"{'='*60}\n")
    
    engine = EchuuLiveEngine()
    
    try:
        # 设置角色和话题
        engine.setup(
            name=name,
            persona=persona,
            topic=topic,
            background=background,
            language=language
        )
        
        # 生成表演（不播放音频，不保存音频）
        results = []
        for step in engine.run(max_steps=10, play_audio=False, save_audio=False):
            results.append({
                "step": step.get("step", 0),
                "stage": step.get("stage", ""),
                "speech": step.get("speech", ""),
                "action": step.get("action", "continue"),
                "emotion_break": step.get("emotion_break"),
                "disfluencies": step.get("disfluencies", []),
            })
        
        return {
            "character": {
                "name": name,
                "persona": persona,
                "background": background,
            },
            "topic": topic,
            "language": language,
            "script": results,
        }
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """生成所有示例案例"""
    output_dir = Path(__file__).parent.parent / "output" / "examples"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    examples = [
        {
            "name": "小梅",
            "persona": "温柔治愈型，喜欢分享生活细节",
            "background": "大学生，喜欢在食堂吃饭，经常遇到有趣的人和事",
            "topic": "食堂打饭遇到的有趣故事",
            "language": "zh",
            "filename": "example_chinese_canteen.json"
        },
        {
            "name": "さくら",
            "persona": "オタク系VTuber、アニメとゲームが大好き",
            "background": "秋葉原によく行く、コレクション好き",
            "topic": "秋葉原でグッズを買いに行ったら同好の士に出会った話",
            "language": "ja",
            "filename": "example_japanese_akihabara.json"
        },
        {
            "name": "Luna",
            "persona": "Energetic content creator, loves dancing and sharing life",
            "background": "Social media influencer, posts dance videos regularly",
            "topic": "Complaining about platform algorithm limiting my dance video because of weird camera angle",
            "language": "en",
            "filename": "example_english_dance_video.json"
        }
    ]
    
    print("🚀 开始生成示例案例...\n")
    
    for example_config in examples:
        result = generate_example(
            name=example_config["name"],
            persona=example_config["persona"],
            background=example_config["background"],
            topic=example_config["topic"],
            language=example_config["language"]
        )
        
        if result:
            output_file = output_dir / example_config["filename"]
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"✅ 已保存: {output_file}")
        else:
            print(f"❌ 生成失败: {example_config['filename']}")
    
    print(f"\n{'='*60}")
    print("✅ 所有案例生成完成！")
    print(f"📁 输出目录: {output_dir}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
