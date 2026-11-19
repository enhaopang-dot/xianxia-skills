---
name: xianxia-naming
description: 生成仙侠/修仙风格的中文命名——人名、法号、门派、国家、地名、功法、法宝、丹药、妖兽、材料、秘籍。当用户或任务需要为修仙/武侠/玄幻内容起名（游戏NPC、门派设定、小说角色、道具命名等）时使用；也用于批量生成后供 LLM 挑选，避免 AI 现场起名土味或撞版权。
---

# 仙侠命名生成

## 何时使用

- 为修仙/武侠/玄幻游戏、小说、剧本生成各类命名
- 需要「一批候选名供挑选」而不是 LLM 现场编造（现场起名易土味、易撞金庸/鬼谷八荒等版权雷区）

## 用法

```bash
python D:/Claude/配置/.claude/skills/xianxia-naming/gen_names.py --type <类型> [-n 数量] [--gender male|female] [--seed 种子] [--json]
```

类型（11 种）：`人名` `法号` `门派` `国家` `地名` `功法` `法宝` `丹药` `妖兽` `材料` `秘籍` `all`

示例：

```bash
python D:/Claude/配置/.claude/skills/xianxia-naming/gen_names.py --type 门派 -n 20          # 生成 20 个门派名
python D:/Claude/配置/.claude/skills/xianxia-naming/gen_names.py --type 人名 --gender female -n 10
python D:/Claude/配置/.claude/skills/xianxia-naming/gen_names.py --type all -n 5 --json     # 全类型各 5 个，JSON 输出
```

## 工作方式

1. 词库 + 原创组合规则生成候选（山海经风词根 + 道家词汇 + 稀有度加权）
2. 内置版权黑名单自动规避（少林/武当/降龙/九阴等 40+ 高危词，命中自动重抽）
3. **生成后由 LLM 按语境挑选**：生成 2-3 倍数量，从中挑最贴合设定气质的，不要直接用第一个

## 注意事项

- 生成物是「候选池」不是终稿，挑名时结合用途（正派用清正气、魔门用诡谲词）
- 黑名单只防高危词，商用前对最终选定的名字做一次搜索验证（规则：搜索引擎第一页出现知名作品关联则不可用）
- 词库数据来自 random_chinese_fantasy_names（MIT 协议，见 DATA-LICENSE），组合规则为原创
