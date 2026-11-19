# 修仙世界三件套 · Xianxia Toolkit

> 做修仙题材的游戏、小说、AI 世界模拟，最烦的三件事：起名土、数值崩、世界跑不起来。这里各给一个。

**关键词**：修仙 · 仙侠 · 玄幻 · 命名生成 · 修仙数值 · 境界体系 · 灵根 · 寿元 · 突破概率 · 灵石经济 · LLM 世界模拟 · 涌现叙事 · NPC 社会 · 世界观设计 · 游戏数值设计 · Xianxia · cultivation game · world simulator · emergent narrative

---

## 这是什么

三个独立 skill，可以单用也可以合用：

### 1. xianxia-naming · 仙侠命名生成

生成人名、法号、门派、国家、地名、功法、法宝、丹药、妖兽、材料、秘籍。

解决的是 LLM 现场起名土味重、容易撞金庸/鬼谷八荒等版权雷区的问题。做法是先批量出候选再筛选，不是让模型即兴发挥。

自带数据字典（`data/`），按类别组织。

### 2. xiuxian-rules · 修仙数值库

境界、灵根、寿元、突破概率、修为需求、战斗压制、五品阶、灵石经济、心魔——一套基准数值。

两个用途：
- 设计修仙游戏数值时当起点调参
- **校验 LLM 生成的修仙内容**，防止「筑基活五千年」「练气秒杀元婴」这类崩坏

### 3. llm-world-sim · LLM 世界模拟架构

设计「全员 LLM Agent + 规则锚定」类系统的架构范式。

提供五条铁律、决策网关模式、信息三层可见性、事实/叙事两层模型、无 LLM 降级方案。适合设计或审查 AI 小镇、世界模拟器、涌现叙事游戏。

## 目录

```
xianxia-skills/
├── xianxia-naming/   命名生成 + data/ 数据字典 + gen_names.py
├── xiuxian-rules/    数值库 + rules.json
└── llm-world-sim/    架构范式文档
```

## 为什么放在一起

三个 skill 解决的是同一条链上的问题：**先有一个能自洽的世界，再往里填名字和数值**。

- 世界怎么跑 → llm-world-sim
- 数值什么量级才对 → xiuxian-rules
- 人、门派、功法叫什么 → xianxia-naming

## 用法

放进 Agent 的 skills 目录即可。命名可以直接跑脚本：

```bash
python xianxia-naming/gen_names.py --type person --count 20
```

## 授权

MIT License。`xianxia-naming/DATA-LICENSE` 单独说明数据字典的授权范围，使用前看一眼。

## 联系

做修仙题材的游戏或内容，加微信：**enhaopang**

添加时请备注：GitHub-xianxia-skills

> 不提供免费技术支持。问题请走 Issue。
