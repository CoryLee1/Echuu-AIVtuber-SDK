# Echuu - AI VTuber 自动直播系统

一个用于生成自然、即兴感的直播内容的 Python 库，通过从真实主播切片中学习表演模式。

## 🤖 使用的 AI 模型

| 功能 | 模型 | 提供商 | 用途 |
|------|------|--------|------|
| **剧本生成** | Gemini 3 Flash/Pro | Google | 生成自然口语化的直播剧本（推荐） |
| **剧本生成** | Claude Sonnet 4 | Anthropic | 备选：高质量剧本生成 |
| **语音合成** | Qwen3 TTS Flash Realtime | 阿里云百炼 | 实时语音合成，支持多种音色 |

### 🔑 需要的 API Key

#### 推荐配置（使用 Gemini 3）

1. **Google Gemini API Key** (用于 LLM 剧本生成)
   - 获取地址: https://aistudio.google.com/apikey
   - 环境变量: `GEMINI_API_KEY`
   - 推荐模型: `gemini-3-flash-preview` (快速、高智能、性价比高)
   - 高级选项: `gemini-3-pro-preview` (最强推理能力)

2. **阿里云百炼 API Key** (用于 TTS 语音合成)
   - 获取地址: https://bailian.console.aliyun.com/?tab=model#/api-key
   - 环境变量: `DASHSCOPE_API_KEY`

#### 备选配置

**Anthropic Claude**:
- 获取地址: https://console.anthropic.com/
- 环境变量: `ANTHROPIC_API_KEY`

**OpenAI GPT-4o**:
- 环境变量: `OPENAI_API_KEY`

> 💡 也支持通义千问作为 LLM，详见 `.env.example`

## 🆕 Gemini 3 新特性

### 思考级别控制

通过 `thinking_level` 参数控制模型的推理深度：

```python
from echuu.live.llm_factory import create_llm_client

# 创建 Gemini 3 客户端
client = create_llm_client(
    provider="gemini",
    model="gemini-3-flash-preview",
    thinking_level="high"  # 推理深度
)
```

**可选级别**:
- `high` - 最大推理深度（默认，适合复杂任务）
- `low` - 最小延迟（适合简单对话）
- `medium` - 平衡（仅 Flash）
- `minimal` - 最快（仅 Flash）

### 图像生成

使用 Gemini 3 Pro Image 生成高质量图像：

```python
from echuu.live.gemini_client import GeminiClient

client = GeminiClient(model="gemini-3-pro-image-preview")

# 生成图像
image_bytes = client.generate_image(
    prompt="一个温馨的咖啡厅，有柔和的阳光",
    aspect_ratio="16:9",
    image_size="4K",
    use_search=True  # 使用 Google Search 进行有根据的生成
)
```

### 视觉理解

支持高分辨率图像分析：

```python
# 分析图像
text = client.call_with_image(
    prompt="描述这张图片的内容",
    image_data=open("photo.jpg", "rb").read(),
    media_resolution="media_resolution_high"  # 高质量分析
)
```

## 概述

Echuu 是一个完整的 AI VTuber 自动直播系统，核心目标是生成**自然、即兴、有真实感**的直播内容。系统通过分析真实主播的表演模式，学习注意力转移、话语行为、故事结构等规律，并生成具有相似自然度的内容。

### 核心特性

- 🎭 **故事内核生成**: 基于"分享欲 + 反常 + 内心戏"的故事内核模式
- 🎨 **情绪复合**: 支持复杂情绪状态的建模和表达
- 💬 **弹幕互动**: 智能评估和响应实时弹幕
- 🎪 **即兴表演**: 支持跑题、结构破坏等自然行为
- 🧠 **记忆系统**: 维护剧情点、承诺、情绪轨迹等状态
- 🎙️ **语音合成**: 集成 TTS 客户端，支持实时语音生成

## 快速开始

### 安装

```bash
pip install -r requirements.txt
```

### 基本使用

```python
from echuu import EchuuLiveEngine

# 创建引擎
engine = EchuuLiveEngine()

# 设置角色和话题
engine.setup(
    name="六螺",
    persona="爱吐槽的女主播",
    topic="关于上司的八卦",
    background="前上班族，现全职主播"
)

# 运行表演
for step in engine.run(max_steps=15, play_audio=False, save_audio=True):
    print(f"[{step['stage']}] {step['speech']}")
    if step.get('inner_monologue'):
        print(f"  💭 {step['inner_monologue']}")
```

## 🔄 Pipeline 示例：从输入到输出

下面通过一个完整示例，展示 Echuu 如何将用户输入转化为带表情标注的直播剧本。

### 用户输入

```python
engine.setup(
    name="六螺",
    persona="爱吐槽的前上班族女主播，说话直接，经常自嘲",
    topic="关于上司的超劲爆八卦",
    background="在互联网公司工作3年后辞职做全职主播"
)
```

---

### Phase -1: 故事内核分析 (StoryNucleus)

系统首先分析话题，确定故事的核心驱动力：

```
内核模式: 八卦爆料型
分享欲: "我知道一个超级劲爆的秘密，不说出来会憋死"
反常点: 身份反差 - 平时PUA别人的上司，居然被开除了
开场意图: 制造悬念，吊胃口
```

**输出**: 确定叙事框架和情绪基调

---

### Phase 0: 触发方式选择 (TriggerBank)

从触发库中选择自然的开场方式：

```
触发类型: thought_drift (思维漂移)
开场模板: "诶，你们知道吗，我突然想起来一件事..."
```

**输出**: 自然的故事入口

---

### Phase 1: 沉浸状态构建

模拟主播"边想边说"的状态：

```
我正在直播，刚才看到弹幕有人问我以前的工作，
突然想起那个天天PUA我们的前上司...
心情有点复杂，又想吐槽又觉得好笑。
准备用"你们猜怎么着"开场吊一下胃口。
```

**输出**: 第一人称沉浸视角

---

### Phase 2: 剧本生成 (ScriptGeneratorV4)

生成 8-10 个叙事单元，每个单元自动附带 PerformerCue：

```json
[
  {
    "id": "line_0",
    "text": "诶，你们知道吗，我上周发现了一件超级劲爆的事！",
    "stage": "Hook",
    "cost": 0.3,
    "cue": {
      "emotion": {"key": "happy", "intensity": 0.85},
      "gesture": {"clip": "react_surprised", "duration": 0.8},
      "look": {"target": "camera", "strength": 0.8},
      "blink": {"mode": "hold"}
    }
  },
  {
    "id": "line_1",
    "text": "就是...我前上司啊，那个天天PUA我们的人，居然...",
    "stage": "Build-up",
    "cost": 0.5,
    "cue": {
      "emotion": {"key": "neutral", "intensity": 0.6},
      "gesture": {"clip": "talk_gesture_medium", "duration": 2.0},
      "look": {"target": "down", "strength": 0.6},
      "pause": 0.3
    }
  },
  {
    "id": "line_2",
    "text": "他被公司开除了！哈哈哈哈！太解气了！",
    "stage": "Climax",
    "cost": 0.8,
    "cue": {
      "emotion": {"key": "happy", "intensity": 1.0},
      "gesture": {"clip": "react_laugh", "duration": 1.5},
      "look": {"target": "camera", "strength": 0.9},
      "blink": {"mode": "hold"},
      "beat": 0.5
    }
  },
  {
    "id": "line_3",
    "text": "好了不说了，反正就这么个事，看弹幕有人问什么...",
    "stage": "Resolution",
    "cost": 0.2,
    "cue": {
      "emotion": {"key": "relaxed", "intensity": 0.5},
      "gesture": {"clip": "idle_sway", "duration": 4.0},
      "look": {"target": "chat", "strength": 0.6}
    }
  }
]
```

---

### Phase 3: 结构破坏 (StructureBreaker)

注入真实主播的"不完美"特征：

- ❌ 删除升华结尾（"这件事让我明白..."）
- ✅ 添加跑题片段（"说到PUA，我想起之前..."）
- ✅ 数字模糊化（"500块" → "几百块吧"）
- ✅ 草草收尾（"反正就这样，下一个话题"）

---

### Phase 4: 实时表演 (PerformerV3)

逐行执行剧本，处理弹幕互动：

```
[Step 0] Hook [CONT]
  Speech: 诶，你们知道吗，我上周发现了一件超级劲爆的事！
  Cue: emotion=happy, gesture=react_surprised, look=camera

[Step 1] Build-up [CONT]
  Speech: 就是...我前上司啊，那个天天PUA我们的人，居然...
  Cue: emotion=neutral, gesture=talk_gesture_medium, look=down, pause=0.3s

[Step 2] Climax [CONT]
  Speech: 他被公司开除了！哈哈哈哈！太解气了！
  Cue: emotion=happy(1.0), gesture=react_laugh, beat=0.5s
  情绪断点: 完全破防 - 积压的不满释放

[Step 3] Resolution [TEASE]
  Danmaku: "为什么被开除？"
  Speech: 这个嘛...你们真想知道？那我下次直播详细说！好了不说了...
  Cue: emotion=relaxed, gesture=idle_sway, look=chat
```

---

### 输出：VRM 控制指令

PerformerCue 通过 VRMExpressionMapper 转换为前端可消费的指令：

```json
{
  "type": "expression",
  "blendShape": "happy",
  "weight": 1.0,
  "fadeIn": 0.15,
  "fadeOut": 0.25,
  "version": "vrm1"
}
```

前端（Unity/three-vrm）根据这些指令驱动虚拟形象的表情和动作。

---

### 完整流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户输入                                 │
│  name="六螺", persona="...", topic="关于上司的八卦"              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Phase -1: StoryNucleus                                         │
│  → 分析话题 → 确定故事模式(八卦爆料) → 提取反常点                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Phase 0: TriggerBank                                           │
│  → 选择触发类型(thought_drift) → 生成开场语                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: Immersion                                             │
│  → 构建第一人称沉浸状态 → 确定情绪基调                            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Phase 2: ScriptGeneratorV4                                     │
│  → LLM生成剧本 → 自动添加 PerformerCue (表情/动作/视线)          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ infer_emotion_from_text("太开心了！")                     │   │
│  │ → EmotionCue(key=HAPPY, intensity=1.0)                   │   │
│  │                                                           │   │
│  │ get_gesture_for_stage("Climax", "happy")                 │   │
│  │ → GestureCue(clip="react_laugh", duration=1.5)           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Phase 3: StructureBreaker                                      │
│  → 删除升华 → 注入跑题 → 模糊数字 → 真实化处理                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Phase 4: PerformerV3 + TTS                                     │
│  → 逐行执行 → 弹幕互动判断 → 语音合成                             │
│  → 输出 speech + audio + cue                                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  输出: VRM 控制指令                                              │
│  → VRMExpressionMapper 转换                                     │
│  → 发送到 Unity/three-vrm 前端                                  │
│  → 驱动虚拟形象表情、动作、视线、口型                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📚 输出案例

我们提供了三个不同语言和主题的完整案例，展示 ECHUU 的生成效果：

### 案例 1: 中文 - 食堂打饭遇到的有趣故事

**角色**: 小梅 - 温柔治愈型，喜欢分享生活细节  
**话题**: 食堂打饭遇到的有趣故事  
**文件**: [`output/examples/example_chinese_canteen.json`](output/examples/example_chinese_canteen.json)

**示例片段**:
```
[Step 1] Hook
诶我突然想起来一个事，刚才看弹幕有人说红烧肉，我就想起大学食堂...
我跟你们说，我有个同学啊，她每天中午都要排队二十分钟就为了吃到
阿姨打的红烧肉，但是她有个特别奇怪的习惯...

[Step 5] Climax
诶我说到哪了？对，原来啊，她爸爸就是我们学校后勤部门的，负责食堂
管理的！阿姨们都认识她爸爸，所以对她特别好。但是她从来没跟我们说
过这个事，我们还以为她就是单纯礼貌呢
```

### 案例 2: 日语 - 秋叶原买谷遇到同好

**角色**: さくら - オタク系VTuber、アニメとゲームが大好き  
**话题**: 秋葉原でグッズを買いに行ったら同好の士に出会った話  
**文件**: [`output/examples/example_japanese_akihabara.json`](output/examples/example_japanese_akihabara.json)

**示例片段**:
```
[Step 1] Hook
不知道为什么我突然想起以前的一个事，刚才看弹幕有人说想去秋叶原，
我就想起那次...那是什么时候来着，今年春天？还是去年？反正挺暖和的，
我排队买那个限定的亚丝娜手办，animate门口排了好长的队

[Step 4] Climax
结果她问我平时看哪个V，我就...就说了几个别的V的名字，没敢说我自己，
然后她说她最近在看一个叫さくら的VTuber，超可爱的，声音很治愈。
我当时整个人都僵住了...
```

### 案例 3: 英文 - 跳舞视频被平台限流抱怨

**角色**: Luna - Energetic content creator, loves dancing and sharing life  
**话题**: Complaining about platform algorithm limiting my dance video because of weird camera angle  
**文件**: [`output/examples/example_english_dance_video.json`](output/examples/example_english_dance_video.json)

**示例片段**:
```
[Step 1] Hook
Oh I just remembered something... 我刚才调摄像头的时候突然想起，之前
我有个舞蹈视频被限流了，就因为摄像头角度问题。我到现在都想不明白，
明明是正常的舞步，为什么算法就觉得有问题...

[Step 5] Climax
我当时气得不行，然后做了个特别幼稚的事情。我重新录了一遍，这次把
摄像头放得特别高，然后配文'这样算法满意了吗？'结果你猜怎么着？这条
居然爆了，点赞比原来那条高十倍。
```

### 查看完整案例

所有案例文件位于 `output/examples/` 目录，包含完整的：
- ✅ 角色信息（名称、人设、背景）
- ✅ 话题和语言设置
- ✅ 完整的剧本（包含所有步骤）
- ✅ 情绪断点和认知特征
- ✅ 记忆状态快照
- 🎵 **音频示例**: `example_chinese_cat_audio.mp3` (TTS 合成效果)

```bash
# 查看案例文件
cat output/examples/example_chinese_canteen.json

# 或在 Python 中加载
import json
with open("output/examples/example_chinese_canteen.json", "r", encoding="utf-8") as f:
    example = json.load(f)
    for step in example["script"]:
        print(f"[{step['stage']}] {step['speech']}")
```

### 生成自己的案例

如果你想生成自己的案例，可以使用提供的脚本：

```bash
# 运行示例生成脚本
python scripts/generate_examples.py
```

或者修改脚本中的配置来生成自定义案例：

```python
from echuu import EchuuLiveEngine
import json

engine = EchuuLiveEngine()
engine.setup(
    name="你的角色名",
    persona="角色人设",
    topic="你的话题",
    background="角色背景",
    language="zh"  # 或 "ja", "en"
)

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

# 保存结果
with open("my_example.json", "w", encoding="utf-8") as f:
    json.dump({
        "character": {
            "name": "你的角色名",
            "persona": "角色人设",
            "background": "角色背景",
        },
        "topic": "你的话题",
        "language": "zh",
        "script": results,
    }, f, ensure_ascii=False, indent=2)
```

## 架构概览

Echuu 采用模块化设计，主要分为三个层次：

```
echuu/
├── core/           # 核心组件：故事内核、情绪、触发器等
├── generators/     # 生成器：剧本生成、示例采样
└── live/           # 实时表演：引擎、表演者、弹幕处理
```

## 核心组件

### Core 模块 (`echuu.core`)

#### StoryNucleus - 故事内核生成器

生成故事的核心模式，基于"分享欲 + 反常 + 内心戏"的公式。

```python
from echuu import StoryNucleus

nucleus = StoryNucleus()
story = nucleus.generate(
    topic="关于上司的八卦",
    persona="爱吐槽的女主播"
)
```

**核心模式**:
- `slippery_slope`: 滑坡谬误（小事变大事）
- `kindness_trap`: 善良陷阱（好心没好报）
- `anger_armor`: 愤怒盔甲（用愤怒掩盖脆弱）
- `choice_cost`: 选择代价（每个选择都有代价）
- `tiny_shame`: 微小羞耻（小事的羞耻感）
- `contradiction_reveal`: 矛盾揭示（自我矛盾）

#### EmotionMixer - 情绪混合器

处理复杂情绪状态，支持情绪复合和转换。

```python
from echuu import EmotionMixer, EmotionConfig

mixer = EmotionMixer()
config = EmotionConfig(
    primary="愤怒",
    secondary="委屈",
    intensity=0.7
)
emotion = mixer.mix(config)
```

#### TriggerBank - 触发词库

管理故事开场的触发模板，支持多种开场方式。

```python
from echuu import TriggerBank

bank = TriggerBank()
trigger = bank.sample_trigger("danmaku")
```

#### DigressionDB - 跑题数据库

注入自然的跑题内容，增加即兴感。

```python
from echuu import DigressionDB

db = DigressionDB()
digression = db.sample_digression(context="工作话题")
```

#### StructureBreaker - 结构破坏器

打破完美结构，生成非闭合、非升华的结尾。

```python
from echuu import StructureBreaker

breaker = StructureBreaker()
broken_script = breaker.break_structure(script_lines)
```

#### PatternAnalyzer - 模式分析器

从标注数据中学习真实主播的表演模式。

```python
from echuu import PatternAnalyzer

with open("data/annotated_clips.json", "r", encoding="utf-8") as f:
    clips = json.load(f)

analyzer = PatternAnalyzer(clips)
patterns = analyzer.analyze_patterns()
```

#### DramaAmplifier - 戏剧放大器

控制情绪强度和戏剧张力。

```python
from echuu import DramaAmplifier

amplifier = DramaAmplifier()
amplified = amplifier.amplify(script_line, intensity=0.8)
```

#### PerformerCue - 表演标注协议

为每行台词提供可执行的表情与动作标注，供 Unity/three-vrm 等前端消费。

```python
from echuu import (
    PerformerCue, EmotionCue, GestureCue, LookCue,
    EmotionKey, LookTarget, BlinkMode,
    infer_emotion_from_text,
)

# 从文本自动推断表情
emotion = infer_emotion_from_text("太开心了！")
# -> EmotionCue(key=HAPPY, intensity=0.95)

# 创建完整的表演标注
cue = PerformerCue(
    emotion=EmotionCue(key=EmotionKey.HAPPY, intensity=0.8),
    gesture=GestureCue(clip="react_laugh", duration=1.5),
    look=LookCue(target=LookTarget.CAMERA, strength=0.8),
)

# 序列化为 JSON
print(cue.to_json())
```

**表情枚举 (EmotionKey)**:
- `NEUTRAL`, `HAPPY`, `ANGRY`, `SAD`, `RELAXED`, `SURPRISED`

**视线目标 (LookTarget)**:
- `CAMERA`, `CHAT`, `OFFSCREEN`, `DOWN`, `UP`, `LEFT`, `RIGHT`

**眨眼模式 (BlinkMode)**:
- `AUTO`, `HOLD`, `NONE`, `WINK_LEFT`, `WINK_RIGHT`

### VRM 模块 (`echuu.vrm`)

#### VRMExpressionMapper - VRM 表情映射器

将 canonical 表情枚举转换为 VRM0/VRM1 格式的 BlendShape 指令。

```python
from echuu import VRMExpressionMapper, VRMVersion, EmotionKey

# 创建 VRM1 映射器
mapper = VRMExpressionMapper(version=VRMVersion.VRM1)

# 生成 VRM 控制指令
cmd = mapper.to_vrm_command(EmotionKey.HAPPY, intensity=0.9)
# -> {
#   "type": "expression",
#   "blendShape": "happy",
#   "weight": 0.9,
#   "fadeIn": 0.2,
#   "fadeOut": 0.3,
#   "version": "vrm1"
# }
```

#### GESTURE_PRESETS - 动作预设库

提供 18 个常用手势/动作预设：

```python
from echuu import GESTURE_PRESETS, get_gesture_by_emotion, GestureCategory

# 查看所有预设
print(f"Total presets: {len(GESTURE_PRESETS)}")

# 根据情绪获取匹配的动作
gesture = get_gesture_by_emotion("happy")
print(f"Gesture: {gesture.name} - {gesture.description}")
```

**动作分类 (GestureCategory)**:
- `IDLE`: 待机动作 (idle_breathe, idle_sway, idle_look_around)
- `TALK`: 说话动作 (talk_gesture_small/medium/big, talk_point)
- `EMOTE`: 表情动作 (emote_nod, emote_shake_head, emote_tilt_head, emote_shrug)
- `REACT`: 反应动作 (react_surprised, react_laugh, react_think, react_facepalm)
- `POSE`: 姿势动作 (pose_confident, pose_shy, pose_angry)

### Generators 模块 (`echuu.generators`)

#### ScriptGeneratorV4 - 剧本生成器

整合所有核心组件的主生成器，生成完整的直播剧本。

```python
from echuu import ScriptGeneratorV4

generator = ScriptGeneratorV4(llm_client, example_sampler)
script_lines = generator.generate(
    name="六螺",
    persona="爱吐槽的女主播",
    topic="关于上司的八卦",
    background="前上班族，现全职主播"
)
```

**生成流程**:
1. Phase 0: 初始化创作环境
2. Phase 1: 生成故事内核（分享欲 + 反常 + 内心戏）
3. Phase 2: 生成完整剧本（包含跑题、结构破坏等）
4. Phase 3: 后处理和优化

#### ExampleSampler - 示例采样器

从真实切片中采样示例，用于 Few-shot 学习。

```python
from echuu import ExampleSampler

sampler = ExampleSampler("data/vtuber_raw_clips.jsonl")
examples = sampler.sample(topic="工作", count=3)
```

### Live 模块 (`echuu.live`)

#### EchuuLiveEngine - 主引擎

整合所有组件的核心引擎，提供完整的直播功能。

```python
from echuu import EchuuLiveEngine

engine = EchuuLiveEngine()
engine.setup(
    name="六螺",
    persona="爱吐槽的女主播",
    topic="关于上司的八卦"
)

for step in engine.run(max_steps=15):
    # 处理每一步的表演结果
    pass
```

#### PerformerV3 - 表演者

执行剧本，处理弹幕，生成响应。

```python
from echuu import PerformerV3

performer = PerformerV3(llm_client, tts_client, danmaku_handler)
result = performer.perform_step(state, step_index)
```

#### DanmakuHandler - 弹幕处理器

评估和处理实时弹幕，决定是否响应。

```python
from echuu import DanmakuHandler, DanmakuEvaluator

evaluator = DanmakuEvaluator()
handler = DanmakuHandler(evaluator)

decision = handler.evaluate_danmaku(
    danmaku=danmaku,
    current_state=state
)
```

**评估机制**:
- `urgency`: 弹幕的紧急程度
- `cost`: 打断当前表演的代价
- `decision_value = urgency - cost`
  - 正数 → 响应弹幕
  - 负数 → 继续剧本

#### State 类

##### PerformanceState - 表演状态

维护整个表演的状态，包括剧本、记忆、弹幕队列等。

```python
from echuu import PerformanceState

state = PerformanceState(
    name="六螺",
    persona="爱吐槽的女主播",
    topic="关于上司的八卦",
    script_lines=script_lines,
    memory=memory
)
```

##### PerformerMemory - 表演者记忆

维护剧情点、承诺、情绪轨迹等记忆状态。

```python
from echuu import PerformerMemory

memory = PerformerMemory()
memory.story_points["mentioned"].append("上司的八卦")
memory.promises.append({
    "text": "我会告诉你们细节",
    "fulfilled": False
})
```

##### Danmaku - 弹幕

弹幕数据模型。

```python
from echuu import Danmaku

danmaku = Danmaku.from_text("主播快说！", user="观众A")
```

## 高级用法

### 自定义回调

监听生成过程的各个阶段：

```python
def on_phase(msg):
    print(f"[Phase] {msg}")

engine.setup(
    name="六螺",
    persona="爱吐槽的女主播",
    topic="关于上司的八卦",
    on_phase_callback=on_phase
)
```

### 实时弹幕注入

在表演过程中动态注入弹幕：

```python
from echuu import Danmaku

# 在表演过程中
danmaku = Danmaku.from_text("真的假的？", user="观众")
engine.state.danmaku_queue.append(danmaku)
```

### 自定义角色配置

```python
character_config = {
    "catchphrases": ["对吧", "我觉得"],
    "speech_style": "casual",
    "emotion_range": [0.3, 0.9]
}

engine.setup(
    name="六螺",
    persona="爱吐槽的女主播",
    topic="关于上司的八卦",
    character_config=character_config
)
```

## 数据格式

### 标注数据格式

```json
{
  "clip_id": "clip_001",
  "skeleton": "共情→自我经历→对比→建议→升华",
  "catchphrases": ["对吧", "我觉得"],
  "segments": [
    {
      "id": "seg_01",
      "start_time": 0,
      "end_time": 35,
      "text": "...",
      "attention_focus": "self",
      "speech_act": "opine",
      "trigger": "danmaku"
    }
  ]
}
```

### 剧本格式

```python
ScriptLineV4(
    id="line_01",
    text="我刚才看到这个，突然想起一个事...",
    stage="Hook",
    interruption_cost=0.3,
    key_info=["上司的八卦"],
    emotion_config={"primary": "兴奋", "intensity": 0.7},
    # 新增：表演标注（自动生成）
    cue=PerformerCue(
        emotion=EmotionCue(key=EmotionKey.HAPPY, intensity=0.85),
        gesture=GestureCue(clip="react_surprised", duration=0.8),
        look=LookCue(target=LookTarget.CAMERA, strength=0.8),
        blink=BlinkCue(mode=BlinkMode.HOLD),
    )
)
```

**PerformerCue 自动生成**:
- `emotion`: 根据文本关键词推断（开心、生气、难过等）
- `gesture`: 根据叙事阶段和情绪匹配预设动作
- `look`: 根据上下文确定视线目标（camera/chat/down）
- `blink`: 根据标点符号调整（感叹号→hold，省略号→auto）
- `beat/pause`: 根据阶段和标点添加节拍/暂停提示

## 📤 SDK 输出接口参考

供后端工程师对接使用的完整接口文档。

### 1. `engine.run()` 每步输出 (Step Result)

调用 `engine.run()` 时，每个 yield 返回的字典包含以下字段：

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `speech` | `string` | 当前台词文本 | `"诶，你们知道吗..."` |
| `stage` | `string` | 叙事阶段 | `"Hook"`, `"Build-up"`, `"Climax"`, `"Resolution"` |
| `step` | `int` | 当前步骤索引 | `0`, `1`, `2`, ... |
| `action` | `string` | 执行动作类型 | `"continue"`, `"tease"`, `"jump"`, `"improvise"`, `"end"` |
| `line_idx` | `int` | 剧本行索引 | `0`, `1`, `2`, ... |
| `audio` | `bytes \| None` | TTS 音频二进制数据 | `b'\xff\xfb\x90...'` |
| `audio_url` | `string \| None` | 音频文件 URL（Web 模式） | `"/audio/session_123/step_0.mp3"` |
| `danmaku` | `string \| None` | 触发的弹幕文本 | `"为什么被开除？"` |
| `priority` | `float` | 弹幕优先级 (0-1) | `0.8` |
| `cost` | `float` | 打断代价 (0-1) | `0.5` |
| `relevance` | `float` | 弹幕相关度 (0-1) | `0.7` |
| `disfluencies` | `list[string]` | 认知特征标记 | `["数字模糊", "自我修正"]` |
| `emotion_break` | `dict \| None` | 情绪断点 | `{"level": 2, "trigger": "回忆"}` |
| `cue` | `dict \| None` | 表演标注 (PerformerCue) | 见下表 |
| `memory_snapshot` | `dict` | 记忆状态快照 | 见下表 |

### 2. PerformerCue 结构

`step["cue"]` 包含以下字段，用于驱动 VRM 虚拟形象：

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `emotion` | `EmotionCue \| None` | 表情标注 | 见下表 |
| `gesture` | `GestureCue \| None` | 动作标注 | 见下表 |
| `look` | `LookCue \| None` | 视线标注 | 见下表 |
| `blink` | `BlinkCue \| None` | 眨眼标注 | 见下表 |
| `lipsync` | `LipsyncCue \| None` | 口型标注（预留） | 见下表 |
| `camera` | `CameraCue \| None` | 镜头标注（可选） | 见下表 |
| `beat` | `float \| None` | 节拍点（秒） | `0.5` |
| `pause` | `float \| None` | 暂停时长（秒） | `0.3` |

#### 2.1 EmotionCue

| 字段 | 类型 | 说明 | 取值范围 |
|------|------|------|----------|
| `key` | `string` | 表情类型 | `"neutral"`, `"happy"`, `"angry"`, `"sad"`, `"relaxed"`, `"surprised"` |
| `intensity` | `float` | 强度 | `0.0 ~ 1.0` |
| `attack` | `float` | 淡入时间（秒） | `0.0 ~ 1.0` |
| `release` | `float` | 淡出时间（秒） | `0.0 ~ 1.0` |

#### 2.2 GestureCue

| 字段 | 类型 | 说明 | 取值范围 |
|------|------|------|----------|
| `clip` | `string` | 动作预设名 | 见下方预设列表 |
| `weight` | `float` | 权重 | `0.0 ~ 1.0` |
| `duration` | `float` | 持续时间（秒） | `> 0` |
| `loop` | `bool` | 是否循环 | `true`, `false` |

**可用动作预设 (18个)**:

| 分类 | 预设名称 | 描述 |
|------|----------|------|
| IDLE | `idle_breathe` | 平静呼吸 |
| IDLE | `idle_sway` | 轻微摇晃 |
| IDLE | `idle_look_around` | 环顾四周 |
| TALK | `talk_gesture_small` | 小幅度手势 |
| TALK | `talk_gesture_medium` | 中等手势 |
| TALK | `talk_gesture_big` | 大幅度手势 |
| TALK | `talk_point` | 指点手势 |
| EMOTE | `emote_nod` | 点头 |
| EMOTE | `emote_shake_head` | 摇头 |
| EMOTE | `emote_tilt_head` | 歪头 |
| EMOTE | `emote_shrug` | 耸肩 |
| REACT | `react_surprised` | 惊讶反应 |
| REACT | `react_laugh` | 大笑 |
| REACT | `react_think` | 思考 |
| REACT | `react_facepalm` | 捂脸 |
| POSE | `pose_confident` | 自信姿势 |
| POSE | `pose_shy` | 害羞姿势 |
| POSE | `pose_angry` | 生气姿势 |

#### 2.3 LookCue

| 字段 | 类型 | 说明 | 取值范围 |
|------|------|------|----------|
| `target` | `string \| [float, float]` | 视线目标 | `"camera"`, `"chat"`, `"offscreen"`, `"down"`, `"up"`, `"left"`, `"right"` 或 `[x, y]` 坐标 |
| `strength` | `float` | 强度 | `0.0 ~ 1.0` |

#### 2.4 BlinkCue

| 字段 | 类型 | 说明 | 取值范围 |
|------|------|------|----------|
| `mode` | `string` | 眨眼模式 | `"auto"`, `"hold"`, `"none"`, `"wink_left"`, `"wink_right"` |
| `extra` | `float` | 额外眨眼频率调整 | `0.0 ~ 1.0` |

#### 2.5 LipsyncCue（预留，由音频驱动）

| 字段 | 类型 | 说明 | 取值范围 |
|------|------|------|----------|
| `enabled` | `bool` | 是否启用 | `true`, `false` |
| `aa` | `float` | 口型 A | `0.0 ~ 1.0` |
| `ih` | `float` | 口型 I | `0.0 ~ 1.0` |
| `ou` | `float` | 口型 U | `0.0 ~ 1.0` |
| `ee` | `float` | 口型 E | `0.0 ~ 1.0` |
| `oh` | `float` | 口型 O | `0.0 ~ 1.0` |

#### 2.6 CameraCue（可选）

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `preset` | `string \| None` | 镜头预设 | `"closeup"`, `"medium"`, `"wide"` |
| `zoom` | `float \| None` | 缩放比例 | `1.0`, `1.5`, `2.0` |

### 3. MemorySnapshot 结构

`step["memory_snapshot"]` 包含记忆状态：

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `story_points` | `list[string]` | 已提及的剧情点 | `["上司PUA", "被开除"]` |
| `promises` | `list[dict]` | 未兑现的承诺 | `[{"content": "下次详细说"}]` |
| `emotion_trend` | `list[int]` | 最近5步情绪强度 | `[0, 1, 2, 3, 2]` |

### 4. VRM 控制指令

使用 `VRMExpressionMapper` 转换为前端指令：

```python
from echuu import VRMExpressionMapper, VRMVersion, EmotionKey

mapper = VRMExpressionMapper(version=VRMVersion.VRM1)
cmd = mapper.to_vrm_command(EmotionKey.HAPPY, intensity=0.9)
```

**输出格式**:

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `type` | `string` | 指令类型 | `"expression"` |
| `blendShape` | `string` | BlendShape 名称 | `"happy"` (VRM1) / `"Joy"` (VRM0) |
| `weight` | `float` | 权重 | `0.9` |
| `fadeIn` | `float` | 淡入时间（秒） | `0.2` |
| `fadeOut` | `float` | 淡出时间（秒） | `0.3` |
| `version` | `string` | VRM 版本 | `"vrm0"`, `"vrm1"` |

### 5. 完整输出示例

```json
{
  "speech": "他被公司开除了！哈哈哈哈！太解气了！",
  "stage": "Climax",
  "step": 2,
  "action": "continue",
  "line_idx": 2,
  "audio_url": "/audio/session_abc/step_2.mp3",
  "danmaku": null,
  "disfluencies": [],
  "emotion_break": {"level": 3, "trigger": "积压的不满释放"},
  "cue": {
    "emotion": {
      "key": "happy",
      "intensity": 1.0,
      "attack": 0.15,
      "release": 0.25
    },
    "gesture": {
      "clip": "react_laugh",
      "weight": 1.0,
      "duration": 1.5,
      "loop": false
    },
    "look": {
      "target": "camera",
      "strength": 0.9
    },
    "blink": {
      "mode": "hold",
      "extra": 0.0
    },
    "lipsync": {
      "enabled": true,
      "aa": 0.0, "ih": 0.0, "ou": 0.0, "ee": 0.0, "oh": 0.0
    },
    "beat": 0.5,
    "pause": null
  },
  "memory_snapshot": {
    "story_points": ["前上司PUA", "被开除"],
    "promises": [],
    "emotion_trend": [0, 1, 3]
  }
}
```

### 6. WebSocket 事件类型（Web 模式）

后端通过 WebSocket 推送以下事件：

| type | 说明 | data |
|------|------|------|
| `reasoning` | 推理过程 | `{"content": "Phase 1: 生成故事内核..."}` |
| `ready` | 剧本生成完成 | `{"session_id": "xxx", "content": "剧本已生成"}` |
| `step` | 每步执行结果 | 完整 Step Result 对象 |
| `finish` | 表演结束 | `{"session_id": "xxx", "content": "表演结束"}` |
| `error` | 错误 | `{"content": "错误信息"}` |

## 配置

### 环境变量

在 `.env` 文件中配置：

```bash
# LLM API
ANTHROPIC_API_KEY=your_key
# 或
OPENAI_API_KEY=your_key

# TTS 配置
TTS_MODEL=qwen3-tts-flash-realtime
TTS_VOICE=Cherry
TTS_RESPONSE_FORMAT=pcm
TTS_SAMPLE_RATE=24000
```

## 设计理念

### 核心公式

**精彩 = 分享欲 + 反常 + 内心戏**

- **分享欲**: 有强烈的表达冲动
- **反常**: 打破常规，制造意外
- **内心戏**: 展现内心思考过程

### Interruption Cost 机制

决定是否响应弹幕的动态代价系统：

```python
decision_value = urgency - cost
```

- `urgency`: 弹幕的紧急程度（0-1）
- `cost`: 打断当前表演的代价（0-1）
- 正数 → 回应弹幕
- 负数 → 继续剧本

### Inner Monologue

让观众看到 AI 的"思考过程"，这是 echuu 区别于传统 AI 主播的核心特性。

## 示例

### 完整示例

```python
from echuu import EchuuLiveEngine

engine = EchuuLiveEngine()

# 设置
engine.setup(
    name="六螺",
    persona="25岁主播，活泼自嘲，喜欢分享生活经历",
    topic="关于上司的超劲爆八卦",
    background="目前在一家外企市场部工作"
)

# 运行
for step in engine.run(max_steps=15, save_audio=True):
    print(f"\n[{step['stage']}] {step['speech']}")

    if step.get('inner_monologue'):
        print(f"💭 {step['inner_monologue']}")

    if step.get('audio_url'):
        print(f"🎵 音频: {step['audio_url']}")

    if step.get('memory_snapshot'):
        memory = step['memory_snapshot']
        print(f"📝 剧情点: {memory['story_points']}")
        print(f"💭 承诺: {memory['promises']}")

    # 新增：获取表演标注
    if step.get('cue'):
        cue = step['cue']
        if cue.get('emotion'):
            print(f"🎭 表情: {cue['emotion']['key']} ({cue['emotion']['intensity']*100:.0f}%)")
        if cue.get('gesture'):
            print(f"✋ 动作: {cue['gesture']['clip']}")
```

## 📖 更多示例

查看 `output/examples/` 目录获取更多完整案例：
- 中文案例：食堂打饭的有趣故事
- 日语案例：秋叶原买谷遇到同好
- 英文案例：跳舞视频被平台限流抱怨

每个案例都包含完整的角色设置、剧本生成过程和输出结果。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

Apache-2.0 License

## 相关链接

- **GitHub 仓库**: https://github.com/CoryLee1/Echuu-AIVtuber-SDK
- **安装**: `pip install git+https://github.com/CoryLee1/Echuu-AIVtuber-SDK.git`
