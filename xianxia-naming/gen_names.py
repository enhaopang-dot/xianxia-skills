# -*- coding: utf-8 -*-
"""仙侠命名生成器 —— 人名/法号/门派/国家/地名/功法/法宝/丹药/妖兽/材料/秘籍

组合规则为原创实现；词库数据来自 random_chinese_fantasy_names（MIT，见 DATA-LICENSE）。
用法：
  python gen_names.py --type 人名 -n 10
  python gen_names.py --type 门派 --seed 42 --json
  python gen_names.py --type all -n 5
"""
import argparse, json, random, sys, io, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def load(*parts):
    with open(os.path.join(DATA, *parts), encoding="utf-8") as f:
        return json.load(f)

# ---------- 版权黑名单（命中即重抽，依据武林霸图版权规避规则） ----------
BLACKLIST = {
    "少林", "武当", "丐帮", "华山", "峨眉", "昆仑", "崆峒", "青城", "唐门", "明教",
    "逍遥", "全真", "古墓", "桃花岛", "黑木崖", "绝情谷", "大理", "天龙", "射雕",
    "降龙", "打狗", "九阴", "九阳", "独孤", "六脉", "北冥", "凌波", "葵花", "辟邪",
    "太极", "易筋", "洗髓", "黯然销魂", "玉女", "玄铁", "倚天", "屠龙", "碧血",
    "鬼谷", "太吾", "合欢", "百兽",  # 合欢/百兽为对标产品特色宗门，规避
}

def safe(name, rng, regen):
    """命中黑名单则重抽，最多 20 次"""
    for _ in range(20):
        if not any(b in name for b in BLACKLIST):
            return name
        name = regen(rng)
    return name

# ---------- 稀有度加权 ----------
RARITY_W = [("uncommon", 40), ("rare", 30), ("epic", 15), ("legendary", 10), ("mythic", 4), ("exotic", 1)]

def pick_rarity(d: dict, rng):
    keys = [k for k, _ in RARITY_W if k in d]
    w = [v for k, v in RARITY_W if k in d]
    tier = rng.choices(keys, weights=w)[0]
    return rng.choice(d[tier])

# ---------- 各类型生成 ----------
def gen_person(rng, gender=None):
    gender = gender or rng.choice(["male", "female"])
    family = rng.choice(load("name", "family.json"))
    given_pool = load("name", "male.json" if gender == "male" else "female.json")
    if rng.random() < 0.2:  # 中间字模式：名只取单字
        return family + rng.choice(load("name", "middle.json")) + rng.choice(given_pool)
    given = rng.choice(given_pool)
    if rng.random() < 0.35:
        given += rng.choice(given_pool)
    return family + given

def gen_dao(rng, gender=None):
    gender = gender or rng.choice(["male", "female"])
    d = rng.choice(load("dao", "dao.json"))
    if rng.random() < 0.4:
        d += rng.choice(load("dao", "dao.json"))
    titles = load("dao", "title_male.json" if gender == "male" else "title_female.json")
    return d + pick_rarity(titles, rng)

def gen_sect(rng):
    clan = rng.choice(load("organization", "clan.json"))
    strange = rng.choice(load("shared", "strange.json"))
    r = rng.random()
    if r < 0.45:
        return strange + clan                      # 招摇宗
    elif r < 0.75:
        return rng.choice(load("shared", "spirit.json")) + strange + clan  # 玄招摇门
    else:
        return rng.choice(load("shared", "common.json")["dao"]) + clan     # 太清宫

def gen_nation(rng):
    return rng.choice(load("shared", "strange.json")) + rng.choice(load("organization", "nation.json"))

def gen_place(rng):
    strange = rng.choice(load("shared", "strange.json"))
    r = rng.random()
    if r < 0.35:   # 山系水系
        return strange + rng.choice(load("place", "location.json"))
    elif r < 0.6:  # 大域
        zone = load("place", "zone.json")
        return strange + rng.choice(zone[rng.choice(list(zone.keys()))])
    else:          # 聚落
        p = rng.choice(load("place", "place.json")) + rng.choice(load("place", "location.json"))
        if rng.random() < 0.3:
            p = rng.choice(load("place", "prefix.json")) + p
        elif rng.random() < 0.3:
            p += rng.choice(load("place", "postfix.json"))
        return p

def gen_skill(rng):
    core = rng.choice(load("skill", "skill.json"))
    GOOD_SINGLE = ["劲", "气", "功", "拳", "掌", "指", "剑", "刀", "枪", "遁", "瞳", "音"]
    NUMFIX_OK = ["拳", "掌", "指", "剑", "刀", "枪", "式"]

    def prefixed(pool, core_):
        for _ in range(10):
            p = rng.choice(pool)
            if p != core_[0]:  # 防「神神功」式叠字
                return p + core_
        return core_

    spirits, colors = load("shared", "spirit.json"), load("shared", "color.json")
    if len(core) == 1:
        if core in NUMFIX_OK and rng.random() < 0.35:
            return rng.choice(load("skill", "numfix.json")) + core   # 七拳、十八掌
        if core not in GOOD_SINGLE:
            core = rng.choice(GOOD_SINGLE)
        return prefixed(spirits + colors, core)
    if rng.random() < 0.65:
        return prefixed(spirits, core)                               # 玄擒拿手
    return prefixed(colors, core)                                    # 紫内功

def gen_weapon(rng):
    t = load("talisman", "talisman.json")
    core = rng.choice(t[rng.choice(list(t.keys()))])
    r = rng.random()
    if r < 0.4:
        name = rng.choice(load("shared", "strange.json")) + core     # 祝余剑
    elif r < 0.7:
        name = rng.choice(load("shared", "common.json")["dao"]) + core  # 太清剑
    else:
        name = rng.choice(load("shared", "color.json")) + rng.choice(load("shared", "spirit.json")) + core
    if rng.random() < 0.08:  # 残次品
        pf = load("talisman", "postfix.json")
        name += "·" + rng.choice(pf[rng.choice(list(pf.keys()))])
    return name

def gen_pill(rng):
    plant = rng.choice(load("creature", "creature.json")["plant"])
    suffix = rng.choice(load("alchemy", "alchemy.json"))
    r = rng.random()
    if r < 0.5:
        return rng.choice(load("shared", "spirit.json")) + plant + suffix   # 玄参丹
    elif r < 0.8:
        return rng.choice(load("shared", "color.json")) + plant + suffix    # 紫芝丸
    else:
        return rng.choice(load("shared", "common.json")["dao"]) + suffix    # 太清丹

def gen_creature(rng):
    if rng.random() < 0.5:
        return rng.choice(load("creature", "strange.json"))           # 毕方
    c = load("creature", "creature.json")
    core = rng.choice(c[rng.choice(list(c.keys()))])
    return rng.choice(load("creature", "prefix.json")) + core         # 古蛟

def gen_material(rng):
    m = load("material", "material.json")
    core = rng.choice(m[rng.choice(list(m.keys()))])
    name = rng.choice(load("shared", "color.json") + load("shared", "spirit.json")) + core
    if rng.random() < 0.08:
        pf = load("material", "postfix.json")
        name += "·" + rng.choice(pf[rng.choice(list(pf.keys()))])
    return name

def gen_book(rng):
    base = rng.random() < 0.5 and rng.choice(load("shared", "common.json")["dao"]) or rng.choice(load("skill", "skill.json"))
    name = base + rng.choice(load("book", "book.json"))               # 太清经
    if rng.random() < 0.4:
        name = pick_rarity(load("book", "prefix.json"), rng) + name   # 秘太清经
    if rng.random() < 0.15:
        name += "·" + pick_rarity(load("book", "postfix.json"), rng)  # 太清经·残卷
    return name

GENS = {
    "人名": (gen_person, True), "法号": (gen_dao, True), "门派": (gen_sect, False),
    "国家": (gen_nation, False), "地名": (gen_place, False), "功法": (gen_skill, False),
    "法宝": (gen_weapon, False), "丹药": (gen_pill, False), "妖兽": (gen_creature, False),
    "材料": (gen_material, False), "秘籍": (gen_book, False),
}

def main():
    ap = argparse.ArgumentParser(description="仙侠命名生成器")
    ap.add_argument("--type", required=True, choices=list(GENS.keys()) + ["all"], help="命名类型")
    ap.add_argument("-n", type=int, default=10, help="数量（默认10）")
    ap.add_argument("--gender", choices=["male", "female"], help="性别（人名/法号）")
    ap.add_argument("--seed", type=int, help="随机种子（可复现）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    types = list(GENS.keys()) if args.type == "all" else [args.type]
    result = {}
    for t in types:
        gen, has_gender = GENS[t]
        out, seen = [], set()
        while len(out) < args.n and len(seen) < args.n * 30:
            name = safe(gen(rng, args.gender) if has_gender else gen(rng), rng,
                        lambda r: gen(r, args.gender) if has_gender else gen(r))
            if name not in seen:
                seen.add(name)
                out.append(name)
        result[t] = out

    if args.json:
        print(json.dumps(result if args.type == "all" else result[args.type], ensure_ascii=False, indent=2))
    else:
        for t, names in result.items():
            if args.type == "all":
                print(f"\n【{t}】")
            print("、".join(names))

if __name__ == "__main__":
    main()
