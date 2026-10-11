"""
Two-team verdict text for the Exploit Finder, Danger Map and Progress Trap.
"""


from sideline.metrics import FORCED_WIDE_MARGIN, FORCED_WIDE_MIN


def _exploit_verdict(teams_data: list) -> str:
    """Dynamic two-team verdict for Exploit Finder."""
    valid = [td for td in teams_data if td]
    if not valid:
        return "No data available."
    if len(valid) == 1:
        td = valid[0]
        return td.get("risk_desc", "")

    t0, t1 = valid[0], valid[1]
    name0, name1 = t0["team"], t1["team"]
    fhl0, fhl1   = t0.get("false_hl", False), t1.get("false_hl", False)
    gap0, gap1   = t0.get("gap_m", 0), t1.get("gap_m", 0)
    ppda0, ppda1 = t0.get("ppda", 99), t1.get("ppda", 99)
    v0, v1       = t0.get("v_state", ""), t1.get("v_state", "")
    comp0, comp1 = t0.get("comp_class", ""), t1.get("comp_class", "")
    line0, line1 = t0.get("def_line_m", 0), t1.get("def_line_m", 0)

    # Both have False High Line
    if fhl0 and fhl1:
        return (
            f"Both {name0} and {name1} were structurally exposed — high defensive lines "
            f"({line0}m and {line1}m respectively) with passive pressing (PPDA {ppda0} and {ppda1}). "
            f"Either side had the space to exploit balls in behind. A match defined by mutual vulnerability."
        )
    # One False High Line
    if fhl0:
        return (
            f"{name0}'s False High Line ({line0}m, PPDA {ppda0}) was the key structural finding. "
            f"By contrast, {name1} were more coherent — {comp1} shape ({gap1}m between lines), "
            f"PPDA {ppda1}. {name0}'s exposure to balls in behind was the defining tactical risk of this match."
        )
    if fhl1:
        return (
            f"{name1}'s False High Line ({line1}m, PPDA {ppda1}) was the key structural finding. "
            f"By contrast, {name0} were more coherent — {comp0} shape ({gap0}m between lines), "
            f"PPDA {ppda0}. {name1}'s exposure to balls in behind was the defining tactical risk of this match."
        )
    # Both gapped
    if comp0 == "Gapped" and comp1 == "Gapped":
        bigger_gap = name0 if gap0 >= gap1 else name1
        bigger_m   = max(gap0, gap1)
        smaller_m  = min(gap0, gap1)
        return (
            f"Both teams left space between their lines — {name0} {gap0}m, {name1} {gap1}m. "
            f"{bigger_gap}'s {bigger_m}m gap was the larger structural opening. "
            f"Creative midfielders on either side had room to operate."
        )
    # One gapped, one compact
    if comp0 == "Gapped" and comp1 == "Compact":
        return (
            f"A clear structural contrast: {name0} were Gapped ({gap0}m between lines) while "
            f"{name1} were Compact ({gap1}m). {name1}'s tight structure gave them a defensive "
            f"advantage — {name0} were the team with the exploitable space."
        )
    if comp1 == "Gapped" and comp0 == "Compact":
        return (
            f"A clear structural contrast: {name1} were Gapped ({gap1}m between lines) while "
            f"{name0} were Compact ({gap0}m). {name0}'s tight structure gave them a defensive "
            f"advantage — {name1} were the team with the exploitable space."
        )
    # Both compact
    if comp0 == "Compact" and comp1 == "Compact":
        return (
            f"Both {name0} and {name1} maintained compact defensive shapes — {gap0}m and {gap1}m "
            f"between lines respectively. This was a match where structural vulnerability was low "
            f"for both sides; the decisive moments came from individual errors rather than systemic gaps."
        )
    # Fallback
    return (
        f"{name0}: {comp0} shape ({gap0}m gap, PPDA {ppda0}). "
        f"{name1}: {comp1} shape ({gap1}m gap, PPDA {ppda1}). "
        f"{'Neither team showed a clear structural vulnerability.' if comp0 != 'Gapped' and comp1 != 'Gapped' else 'The space between the lines was the key battleground.'}"
    )


def _danger_map_verdict(teams_data: list) -> str:
    """Dynamic two-team verdict for Danger Map."""
    valid = [td for td in teams_data if td and td.get("total_prog", 0) > 0]
    if not valid:
        return "Insufficient data."
    if len(valid) == 1:
        return valid[0].get("verdict", "")

    t0, t1     = valid[0], valid[1]
    n0, n1     = t0["team"], t1["team"]
    pct0, pct1 = t0["danger_pct"], t1["danger_pct"]
    tot0, tot1 = t0["total_prog"], t1["total_prog"]
    dc0, dc1   = t0["danger_count"], t1["danger_count"]
    gain0, gain1 = t0["avg_gain_m"], t1["avg_gain_m"]
    gap = abs(pct0 - pct1)
    more_clinical = n0 if pct0 >= pct1 else n1
    less_clinical = n1 if more_clinical == n0 else n0
    more_pct = max(pct0, pct1)
    less_pct = min(pct0, pct1)
    more_dc  = dc0 if more_clinical == n0 else dc1
    less_dc  = dc1 if more_clinical == n0 else dc0
    more_tot = tot0 if more_clinical == n0 else tot1
    less_tot = tot1 if more_clinical == n0 else tot0

    if gap >= 15:
        return (f"{more_clinical} were significantly more clinical — {more_pct}% of progressive passes "
                f"reached the danger corridor ({more_dc}/{more_tot}), compared to just {less_pct}% for "
                f"{less_clinical} ({less_dc}/{less_tot}). {less_clinical} moved the ball forward but "
                f"their progression repeatedly broke down before reaching a genuine threat position. "
                f"The {gap}% efficiency gap was the clearest tactical difference in this match.")
    elif gap >= 7:
        vol_leader = n0 if tot0 >= tot1 else n1
        vol_lagger = n1 if vol_leader == n0 else n0
        return (f"{more_clinical} edged clinical efficiency ({more_pct}% vs {less_pct}%). "
                f"{vol_leader} dominated in volume with {max(tot0,tot1)} progressive passes vs "
                f"{min(tot0,tot1)} for {vol_lagger}. "
                f"The combination of volume and efficiency tells the full story of who controlled progression.")
    elif abs(tot0 - tot1) >= 20:
        vol_leader = n0 if tot0 >= tot1 else n1
        vol_lagger = n1 if vol_leader == n0 else n0
        return (f"Clinical efficiency was similar — {pct0}% vs {pct1}% — but {vol_leader} "
                f"generated far more progressive passes ({max(tot0,tot1)} vs {min(tot0,tot1)}). "
                f"Volume of ball progression, not efficiency, was the key differentiator. "
                f"Average gain per pass: {gain0}m ({n0}) vs {gain1}m ({n1}).")
    else:
        return (f"Both teams were closely matched in danger corridor efficiency — {n0} {pct0}% "
                f"({dc0}/{tot0}) vs {n1} {pct1}% ({dc1}/{tot1}). "
                f"Average ground gained per progressive pass: {gain0}m vs {gain1}m. "
                f"Neither side found a clear edge in turning possession into genuine threat.")


def _progress_trap_verdict(teams_data: list) -> str:
    valid = [td for td in teams_data if td and td.get("total_attempts", 0) > 0]
    if not valid:
        return "Insufficient data."
    if len(valid) == 1:
        return valid[0].get("verdict", "")

    t0, t1   = valid[0], valid[1]
    n0, n1   = t0["team"], t1["team"]
    sr0, sr1 = t0["stall_rate"], t1["stall_rate"]
    zone0, zone1   = t0["primary_stall_zone"], t1["primary_stall_zone"]
    block0, block1 = t0["block_depth_m"], t1["block_depth_m"]
    label0, label1 = t0["block_label"], t1["block_label"]
    wide0, wide1   = t0["forced_wide_pct"], t1["forced_wide_pct"]

    stall_gap    = abs(sr0 - sr1)
    deeper_block = n0 if block0 <= block1 else n1
    deeper_m     = min(block0, block1)
    shallower_m  = max(block0, block1)
    higher_stall = n0 if sr0 >= sr1 else n1
    lower_stall  = n1 if higher_stall == n0 else n0
    higher_sr    = max(sr0, sr1)
    lower_sr     = min(sr0, sr1)

    if stall_gap >= 20:
        return (f"A sharp contrast in progression efficiency. {higher_stall} stalled on {higher_sr}% "
                f"of forward passes — primarily in the {zone0 if higher_stall==n0 else zone1} — "
                f"facing {deeper_block}'s block at {deeper_m}m. "
                f"{lower_stall}, by contrast, stalled on only {lower_sr}% despite facing a block at {shallower_m}m. "
                f"The difference in press resistance and build-up quality was decisive.")
    elif sr0 >= 40 and sr1 >= 40:
        return (f"Both teams struggled to progress the ball — {n0} {sr0}% stall rate, {n1} {sr1}%. "
                f"Forced wide percentages: {n0} {wide0}%, {n1} {wide1}%. "
                f"This was a match where the central corridor was largely shut down for both sides.")
    elif wide0 >= FORCED_WIDE_MIN and wide1 <= wide0 - FORCED_WIDE_MARGIN:
        return (f"{n0} were consistently forced wide ({wide0}% of completions) "
                f"while {n1} found the central route more accessible ({wide1}% forced wide). "
                f"Block depths: {n0} facing {block1}m ({label1}), {n1} facing {block0}m ({label0}).")
    elif wide1 >= FORCED_WIDE_MIN and wide0 <= wide1 - FORCED_WIDE_MARGIN:
        return (f"{n1} were consistently forced wide ({wide1}% of completions) "
                f"while {n0} found the central route more accessible ({wide0}% forced wide). "
                f"Block depths: {n1} facing {block0}m ({label0}), {n0} facing {block1}m ({label1}).")
    else:
        return (f"{n0}: {sr0}% stall rate (primary zone: {zone0}), block facing them {block1}m ({label1}), {wide0}% forced wide. "
                f"{n1}: {sr1}% stall rate (primary zone: {zone1}), block facing them {block0}m ({label0}), {wide1}% forced wide. "
                f"{'Both teams found progression similarly challenging.' if stall_gap < 10 else f'{lower_stall} were the more effective ball progressors.'}")
