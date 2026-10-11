# How the Controller runs the heat pump

This document lists the rules the Controller follows to start and stop the compressor, the electric heater S1 and the JV. Terms follow `CONTEXT.md`; M-numbers are the Controller's measurements (M9 is the tank top, M4 the tank middle, M10 the tank bottom).

The source is the Käsikirja, `manuals/Geopro 202S Käsikirja.pdf`. Page numbers here are PDF page indexes, counted from 1. In the Käsikirja they equal the printed page numbers. `manuals/geopro-202s-manual.md` paraphrases the Käsikirja section by section and points here for these rules instead of restating them.

A line marked **Observed** comes from the Node or the owner, not from the manual, and names its source.

## Settings

The ML circuit's settings, as listed on p. 21. The last column is what the Controller held in Bank 0x0B in the 2026-10-09 trace (`tests/traces/node-2026-10-09.log`). Settings change over time; the Bank Values in Home Assistant show the current ones.

| Label | Menu (p. 21) | Factory (p. 21) | Range (p. 21) | Bank 0x0B offset | Held 2026-10-09 |
|---|---|---|---|---|---|
| Var.ylä talvi | käyttäjätaso | 65 °C | 30–75 °C | 1 | 55 °C |
| Var.ylä kesä | käyttäjätaso | 55 °C | 30–75 °C | 2 | 50 °C |
| VaraajaAlaEro | huoltotila | 5 °C | 3–7 °C | 3 | 5 °C |
| VaraajaYläEro | huoltotila | 3 °C | 3–10 °C | 4 | 3 °C |
| VaraajaAlaMin | käyttäjätaso | 30 °C | 30–55 °C | 5 | 32 °C |
| SV_viiveaika | käyttäjätaso | 30 min | 0–120 min | 6 | 90 min |
| VarYläEroSv | huoltotila | 3 °C | 0–10 °C | 7 | 5 °C |
| Lisälämmitys | käyttäjätaso | 50 °C | 40–55 °C | 8 | 50 °C |
| Lisäläm.aika | käyttäjätaso | 2 h | 0–6 h | 9 | 2 h |
| ML Ohjaustapa | ML Ohjaustavat screen | not given | Kompr.+sähköv., Kompressori, Sähkövastus | 10 | 0 |
| Maaliuos häl | huoltotila | −6 °C | −10–0 °C | 11 | −6 °C |
| JV Esiavaus | huoltotila | 40 % | 25–100 % | 12 | 40 % |
| JV Esto | huoltotila | 60 s | 30–240 s | 13 | 60 s |
| Kompr.esto | huoltotila | 55 °C | 45–55 °C | 14 | 48 °C |

**Observed:** the ML Ohjaustapa codes follow the menu order: 0 Kompr.+sähköv., 1 Kompressori, 2 Sähkövastus. The owner confirmed them on 2026-10-11; 0 also matched the display in #10.

### Factory values that contradict each other

Page 21 gives VaraajaAlaEro 5 °C and VaraajaYläEro 3 °C, and so does the factory-reset list on p. 29. Page 26 swaps them, in both its ML Asetusarvot screen and its table: VaraajaAlaEro 3 °C, VaraajaYläEro 5 °C. The examples on p. 22 use VaraajaYläEro 5 °C and VaraajaAlaEro 3 °C, but as example settings, not factory values. The Controller held VaraajaAlaEro 5 °C and VaraajaYläEro 3 °C (offsets 3 and 4 in the 2026-10-09 trace), which agrees with pp. 21 and 29. Whether those are factory values or an installer's is unknown.

Two labels are spelled differently across pages: p. 21's text calls VarYläEroSv "VaraajaYläEroSv", and p. 23 writes SV_viiveaika as "SV-viiveaika".

## VaraajaYlä

The Controller computes VaraajaYlä from the outdoor temperature (p. 21). It equals Var.ylä kesä when the outdoor temperature is +20 °C or above and Var.ylä talvi at −20 °C or below. The graph on p. 21 draws a straight line between the two and a flat line beyond them, so between −20 °C and +20 °C:

VaraajaYlä = Var.ylä kesä + (Var.ylä talvi − Var.ylä kesä) × (20 − outdoor) / 40

The manual doesn't say whether the outdoor value is M1 itself or the average set by Ulkolämpötilan hidastus (p. 26).

With Var.ylä kesä 50 °C and Var.ylä talvi 55 °C, the formula gives 52.1 °C at +3 °C outside. **Observed:** on 2026-10-10 at +3 to +5 °C, M9 cycled between 49.0 and 52.2 °C (#24 Notes), which fits a start at VaraajaYlä − VaraajaYläEro (3 °C) and a stop at VaraajaYlä.

## Compressor

All rules are on p. 23 unless noted. "L1 setpoint" is the supply temperature the Controller computes for heating circuit L1 (säätimen määräämä menoveden lämpötila L1); the Component doesn't read it. Every rule that uses the L1 setpoint has the same clause for L2.

| Rule | Condition | Page |
|---|---|---|
| Start on the tank top | M9 falls below VaraajaYlä − VaraajaYläEro. | 23 |
| Stop on the tank top | M9 rises above VaraajaYlä. | 23 |
| Start on the tank middle | At least 5 min have passed since the previous compressor run, and M4 falls below any of: L1 setpoint + 5 °C − VaraajaAlaEro, L2 setpoint + 5 °C − VaraajaAlaEro, VaraajaAlaMin, or Lisälämmitys while the Lisälämpöpainike is active. | 23 |
| Stop on the tank bottom | M10 rises above all of: L1 setpoint + 5 °C, L2 setpoint + 5 °C, VaraajaAlaMin + VaraajaAlaEro, and Lisälämmitys + VaraajaAlaEro while the Lisälämpöpainike is active. | 23 |
| Kompr.esto stop | When M10 reaches Kompr.esto, the compressor always stops, even if the tank top calls for it. | 21, 23 |
| Restart after a Kompr.esto stop | Only once M10 has fallen VaraajaAlaEro below Kompr.esto. | 23 |
| Can't start | M10 is above Kompr.esto, or ML Ohjaustapa is Sähkövastus (compressor control turns into heater control), or the running-feedback alarm is active. | 23 |
| Running-feedback alarm | If the compressor is switched on and M11 (Kompr.käynti) reports no running, the Controller raises Poikkeamahälytys and cuts the compressor. The alarm clears itself after 5 min and the compressor may start again. | 20 |
| M4/M10 fallback | If M4 fails, the Controller steers by M10, and the other way round. | 22 |

The manual lists the tank-top and tank-bottom rules separately and doesn't say how they combine, apart from Kompr.esto overriding the tank top. It states the 5-minute wait only for the tank-middle start.

The Lisälämpöpainike (Dig 1) swaps VaraajaAlaMin for Lisälämmitys for Lisäläm.aika (pp. 20, 21, 23).

## Electric heater S1

S1 sits in the line into the tank top, after the tulistin and before M7 (p. 22). All rules are on p. 23 unless noted.

| Rule | Condition | Page |
|---|---|---|
| On by the tank top | M9 falls below VaraajaYlä − VaraajaYläEro − VarYläEroSv. | 21, 23 |
| Off by the tank top | M9 rises above VaraajaYlä. | 23 |
| On by the tank middle | The compressor has been switched on for SV_viiveaika, and M4 falls below any of: L1 setpoint + 5 °C − VaraajaAlaEro − 1 °C, the same for L2, VaraajaAlaMin − 1 °C, or Lisälämmitys − 1 °C while the Lisälämpöpainike is active. | 21, 22, 23 |
| Off by the tank bottom | M10 rises above all of: L1 setpoint + 5 °C − ½ VaraajaAlaEro, the same for L2, VaraajaAlaMin + ½ VaraajaAlaEro, and Lisälämmitys + ½ VaraajaAlaEro while the Lisälämpöpainike is active. | 23 |
| Pre-run | Before S1 switches on, the Controller drives the JV open by JV Esiavaus, then switches S1 on, then stops the JV from closing for JV Esto. S1 can't switch on until this has finished. | 21, 23 |
| Can't switch on | The pre-run hasn't finished, or ML Ohjaustapa is Kompressori (heater control turns into compressor control). | 23 |

The tank-top rule has no SV_viiveaika condition, so S1 can switch on from M9 alone. With ML Ohjaustapa Kompr.+sähköv., S1 switches on when ground heat isn't enough (p. 21).

## JV

The condenser pump draws water from the tank bottom through the condenser. The JV (jakoventtiili) then sends it either through the tulistin, S1 and M7 into the tank top, or into the tank middle (p. 22). **Observed:** the owner confirmed on 2026-10-09 that this unit is plumbed like the p. 22 diagram.

- In Autom.säätö the Controller steers the JV by M7, with VaraajaYlä + 5 °C as the setpoint (pp. 23, 28).
- JV ohjaustapa has three modes: Autom.säätö, Käsiajo mek. (motor unpowered, hand operation only) and Käsiajo sähk. (driven from the keypad) (p. 28).
- The JV motor is on output Moott. JV (M3), terminals 59–62 (pp. 28, 39).
- JV Esiavaus and JV Esto apply only around S1 switching on (pp. 21, 23).

**Observed:** this unit's JV motor is 3-point, so its position Value reads 0 % (#16). In Autom.säätö the JV sat closed and compressor runs chattered; since 2026-10-09 it runs in Käsiajo sähk. until a technician has checked it (owner's diagnosis notes; #24 lists the repair as out of scope).

## Status word

The Status word is the Value at Address 0x2D. The manual doesn't describe it; everything here is observed.

- It reads 0xFE07 at idle (2026-10-09 trace, last Reply).
- During compressor runs it read 0xFE17. Bit 0x10 was the only bit that changed (Node logs from 2026-10-07, not in the repo).
- There's no alarm bit. Between the short runs of 2026-10-07, including the 5-minute Poikkeamahälytys lockouts, it read 0xFE07.
- Bit 0x08 went on when S1 joined a compressor run, reading 0xFE1F (Node log from 2026-10-08 10:16–10:19, not in the repo).
- Bits 0x01, 0x02 and 0x04 (`digi1`–`digi3`) are on at idle. Which Dig input each one reports is unverified.

## Inputs and relays

From the wiring diagram on p. 39 and the alarm list on p. 20.

| Input | Terminals | Connected to (p. 39) | What the Controller does with it |
|---|---|---|---|
| Mitt.11 (M11) | T11, 11 and ⊥ | Kompressorin käyntitieto | Running feedback for Poikkeamahälytys (p. 20). |
| Dig 1 | X1, 21–22 | Lisälämpöpainike | Swaps VaraajaAlaMin for Lisälämmitys for Lisäläm.aika (pp. 20, 21, 23). |
| Dig 2 | X2, 23–24 | Kompressorin ylivirtaussuoja | Alarm "Kompr. L-rele" when the compressor's thermal overload relay trips, on a closing contact (p. 20). |
| Dig 3 | X3, 25–26 | Sähkövastuksen ylikuumenemissuoja | Alarm "Sähköv.ylik" when the heater's overheat cut-out trips, on a closing contact. Only the heater's manual reset button clears it (p. 20). |

| Output | Terminals | Switches (p. 39) |
|---|---|---|
| Rele 2 | 71–72 | the compressor |
| Rele 1 | 73–75 | the electric heater |

## Open questions

- Whether VaraajaYlä uses M1 or the averaged outdoor temperature.
- How the tank-top and tank-bottom calls combine, and whether the 5-minute wait also applies to tank-top starts.
- Which factory values for VaraajaAlaEro and VaraajaYläEro are right.
- Which Dig input each of `digi1`–`digi3` reports.
- What the Bank bytes without a row hold. The end of `components/geopro_202s/register_map.py` lists them with their 2026-10-09 values.
