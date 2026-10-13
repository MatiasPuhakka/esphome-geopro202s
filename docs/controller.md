# How the Controller runs the heat pump

This document lists the rules the Controller follows to start and stop the compressor, the electric heater S1 and the JV. Terms follow `CONTEXT.md`; M-numbers are the Controller's measurements (M9 is the tank top, M4 the tank middle, M10 the tank bottom).

The source is the Käsikirja, transcribed in [`manuals/kasikirja.md`](../manuals/kasikirja.md) (ADR 0006). Each page number links to that page of the transcription. The Käsikirja's printed page numbers equal its PDF page indexes.

A line marked **Observed** comes from the Node or the owner, not from the manual, and names its source.

## Settings

The ML circuit's settings, as listed on [p. 21][s21]. The last column is what the Controller held in Bank 0x0B in the 2026-10-09 trace (`tests/traces/node-2026-10-09.log`). Settings change over time; the Bank Values in Home Assistant show the current ones.

| Label | Menu ([p. 21][s21]) | Factory ([p. 21][s21]) | Range ([p. 21][s21]) | Bank 0x0B offset | Held 2026-10-09 |
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
| ML Ohjaustapa | ML Ohjaustavat screen | Kompr.+sähköv. ([p. 29][s29]) | Kompr.+sähköv., Kompressori, Sähkövastus | 10 | 0 |
| Maaliuos häl | huoltotila | −6 °C | −10–0 °C | 11 | −6 °C |
| JV Esiavaus | huoltotila | 40 % | 25–100 % | 12 | 40 % |
| JV Esto | huoltotila | 60 s | 30–240 s | 13 | 60 s |
| Kompr.esto | huoltotila | 55 °C | 45–55 °C | 14 | 48 °C |

**Observed:** the ML Ohjaustapa codes follow the menu order: 0 Kompr.+sähköv., 1 Kompressori, 2 Sähkövastus. The owner confirmed them on 2026-10-11; 0 also matched the display in #10.

### Factory values that contradict each other

[Page 21][s21] gives VaraajaAlaEro 5 °C and VaraajaYläEro 3 °C, and so does the factory-reset list on [p. 29][s29]. [Page 26][s26] swaps them, in both its ML Asetusarvot screen and its table: VaraajaAlaEro 3 °C, VaraajaYläEro 5 °C. The examples on [p. 22][s22] use VaraajaYläEro 5 °C and VaraajaAlaEro 3 °C, but as example settings, not factory values. The Controller held VaraajaAlaEro 5 °C and VaraajaYläEro 3 °C (offsets 3 and 4 in the 2026-10-09 trace), which agrees with pp. [21][s21] and [29][s29]. Whether those are factory values or an installer's is unknown.

Two labels are spelled differently across pages: [p. 21][s21]'s text calls VarYläEroSv "VaraajaYläEroSv", and [p. 23][s23] writes SV_viiveaika as "SV-viiveaika".

## VaraajaYlä

The Controller computes VaraajaYlä from the outdoor temperature ([p. 21][s21]). It equals Var.ylä kesä when the outdoor temperature is +20 °C or above and Var.ylä talvi at −20 °C or below. The graph on [p. 21][s21] draws a straight line between the two and a flat line beyond them, so between −20 °C and +20 °C:

VaraajaYlä = Var.ylä kesä + (Var.ylä talvi − Var.ylä kesä) × (20 − outdoor) / 40

The manual doesn't say whether the outdoor value is M1 itself or the average set by Ulkolämpötilan hidastus ([p. 26][s26]).

With Var.ylä kesä 50 °C and Var.ylä talvi 55 °C, the formula gives 52.1 °C at +3 °C outside. **Observed:** on 2026-10-10 at +3 to +5 °C, M9 cycled between 49.0 and 52.2 °C (#24 Notes), which fits a start at VaraajaYlä − VaraajaYläEro (3 °C) and a stop at VaraajaYlä.

**Observed:** `tools/controller.py` replays this formula with M1 against the recorded day in `tools/tests/fixtures/history_2026-10-09_day.json`. With M1 steady, it switches within 2 s of the Status bit. From 20:59 on 2026-10-09 to 01:20 on 2026-10-10, while M1 fell from 8.7 to 5.4 °C, it switched 40 to 60 s apart from the Controller: the Controller started at M9 48.2 and 48.6 °C, where the formula gives start thresholds of 48.41 and 48.82 °C, and stopped at 51.4 and 51.8 °C, below the formula's 51.41 and 51.86 °C. A lagging outdoor value, such as an average of M1, would explain both.

## Compressor

All rules are on [p. 23][s23] unless noted. "L1 setpoint" is the supply temperature the Controller computes for heating circuit L1 (säätimen määräämä menoveden lämpötila L1); the Component doesn't read it. Every rule that uses the L1 setpoint has the same clause for L2.

| Rule | Condition | Page |
|---|---|---|
| Start on the tank top | M9 falls below VaraajaYlä − VaraajaYläEro. | [23][s23] |
| Stop on the tank top | M9 rises above VaraajaYlä. | [23][s23] |
| Start on the tank middle | At least 5 min have passed since the previous compressor run, and M4 falls below any of: L1 setpoint + 5 °C − VaraajaAlaEro, L2 setpoint + 5 °C − VaraajaAlaEro, VaraajaAlaMin, or Lisälämmitys while the Lisälämpöpainike is active. | [23][s23] |
| Stop on the tank bottom | M10 rises above all of: L1 setpoint + 5 °C, L2 setpoint + 5 °C, VaraajaAlaMin + VaraajaAlaEro, and Lisälämmitys + VaraajaAlaEro while the Lisälämpöpainike is active. | [23][s23] |
| Kompr.esto stop | When M10 reaches Kompr.esto, the compressor always stops, even if the tank top calls for it. | [21][s21], [23][s23] |
| Restart after a Kompr.esto stop | Only once M10 has fallen VaraajaAlaEro below Kompr.esto. | [23][s23] |
| Can't start | M10 is above Kompr.esto, or ML Ohjaustapa is Sähkövastus (compressor control turns into heater control), or the running-feedback alarm is active. | [23][s23] |
| Running-feedback alarm | If the compressor is switched on and M11 (Kompr.käynti) reports no running, the Controller raises Poikkeamahälytys and cuts the compressor. The alarm clears itself after 5 min and the compressor may start again. | [20][s20] |
| M4/M10 fallback | If M4 fails, the Controller steers by M10, and the other way round. | [22][s22] |

The manual lists the tank-top and tank-bottom rules separately and doesn't say how they combine, apart from Kompr.esto overriding the tank top. It states the 5-minute wait only for the tank-middle start.

The Lisälämpöpainike (Dig 1) swaps VaraajaAlaMin for Lisälämmitys for Lisäläm.aika (pp. [20][s20], [21][s21], [23][s23]).

## Electric heater S1

S1 sits in the line into the tank top, after the tulistin and before M7 ([p. 22][s22]). All rules are on [p. 23][s23] unless noted.

| Rule | Condition | Page |
|---|---|---|
| On by the tank top | M9 falls below VaraajaYlä − VaraajaYläEro − VarYläEroSv. | [21][s21], [23][s23] |
| Off by the tank top | M9 rises above VaraajaYlä. | [23][s23] |
| On by the tank middle | The compressor has been switched on for SV_viiveaika, and M4 falls below any of: L1 setpoint + 5 °C − VaraajaAlaEro − 1 °C, the same for L2, VaraajaAlaMin − 1 °C, or Lisälämmitys − 1 °C while the Lisälämpöpainike is active. | [21][s21], [22][s22], [23][s23] |
| Off by the tank bottom | M10 rises above all of: L1 setpoint + 5 °C − ½ VaraajaAlaEro, the same for L2, VaraajaAlaMin + ½ VaraajaAlaEro, and Lisälämmitys + ½ VaraajaAlaEro while the Lisälämpöpainike is active. | [23][s23] |
| Pre-run | Before S1 switches on, the Controller drives the JV open by JV Esiavaus, then switches S1 on, then stops the JV from closing for JV Esto. S1 can't switch on until this has finished. | [21][s21], [23][s23] |
| Can't switch on | The pre-run hasn't finished, or ML Ohjaustapa is Kompressori (heater control turns into compressor control). | [23][s23] |

The tank-top rule has no SV_viiveaika condition, so S1 can switch on from M9 alone. With ML Ohjaustapa Kompr.+sähköv., S1 switches on when ground heat isn't enough ([p. 21][s21]).

## JV

The condenser pump draws water from the tank bottom through the condenser. The JV (jakoventtiili) then sends it either through the tulistin, S1 and M7 into the tank top, or into the tank middle ([p. 22][s22]). **Observed:** the owner confirmed on 2026-10-09 that this unit is plumbed like the [p. 22][s22] diagram.

- In Autom.säätö the Controller steers the JV by M7, with VaraajaYlä + 5 °C as the setpoint (pp. [23][s23], [28][s28]).
- JV ohjaustapa has three modes: Autom.säätö, Käsiajo mek. (motor unpowered, hand operation only) and Käsiajo sähk. (driven from the keypad) ([p. 28][s28]).
- The JV motor is on output Moott. JV (M3), terminals 59–62 (pp. [28][s28], [39][s39]).
- JV Esiavaus and JV Esto apply only around S1 switching on (pp. [21][s21], [23][s23]).

**Observed:** this unit's JV motor is 3-point, so its position Value reads 0 % (#16). In Autom.säätö the JV sat closed and compressor runs chattered; since 2026-10-09 it runs in Käsiajo sähk. until a technician has checked it (owner's diagnosis notes; #24 lists the repair as out of scope).

## Status word

The Status word is the Value at Address 0x2D. The manual doesn't describe it; everything here is observed.

- It reads 0xFE07 at idle (2026-10-09 trace, last Reply).
- During compressor runs it read 0xFE17. Bit 0x10 was the only bit that changed (Node logs from 2026-10-07, not in the repo).
- There's no alarm bit. Between the short runs of 2026-10-07, including the 5-minute Poikkeamahälytys lockouts, it read 0xFE07.
- Bit 0x08 went on when S1 joined a compressor run, reading 0xFE1F (Node log from 2026-10-08 10:16–10:19, not in the repo).
- Bits 0x01, 0x02 and 0x04 (`digi1`–`digi3`) are on at idle. Which Dig input each one reports is unverified.

## Inputs and relays

From the wiring diagram on [p. 39][s39] and the alarm list on [p. 20][s20].

| Input | Terminals | Connected to ([p. 39][s39]) | What the Controller does with it |
|---|---|---|---|
| Mitt.11 (M11) | T11, 11 and ⊥ | Kompressorin käyntitieto | Running feedback for Poikkeamahälytys ([p. 20][s20]). |
| Dig 1 | X1, 21–22 | Lisälämpöpainike | Swaps VaraajaAlaMin for Lisälämmitys for Lisäläm.aika (pp. [20][s20], [21][s21], [23][s23]). |
| Dig 2 | X2, 23–24 | Kompressorin ylivirtaussuoja | Alarm "Kompr. L-rele" when the compressor's thermal overload relay trips, on a closing contact ([p. 20][s20]). |
| Dig 3 | X3, 25–26 | Sähkövastuksen ylikuumenemissuoja | Alarm "Sähköv.ylik" when the heater's overheat cut-out trips, on a closing contact. Only the heater's manual reset button clears it ([p. 20][s20]). |

| Output | Terminals | Switches ([p. 39][s39]) |
|---|---|---|
| Rele 2 | 71–72 | the compressor |
| Rele 1 | 73–75 | the electric heater |

## Frozen measurements

**Observed:** on 2026-10-12 the Controller served frozen temperatures over the bus for about two hours. From 09:52, when the Node booted (Component c974f4d), every Reply carried the same M1–M10 values until the owner power-cycled the Controller at about 11:45. Home Assistant's history shows each temperature Value holding one value from 09:52:24 to 11:46:29, M9 at 50.7 °C while the Controller's display showed 59 °C at about 11:45. The Node rebooted at 11:16 and went unavailable for a moment again at 11:20, and both times the same values came back. Over the same time the compressor hour counter kept counting (8209 h at 10:15, 8210 h at 11:15), and the Status word kept the compressor bit on, matching the running compressor. The first Replies after the power cycle carried live values (M9 59.4 °C). The request pacing was the same as in the earlier f3c1da8 build, so what triggers a freeze is unknown.

The overnight phase of the flash check (`docs/agents/verification.md`) fails when every temperature Value holds one value for longer than 60 minutes at once. Home Assistant's ESPHome integration skips a state that didn't change, so a hold is the time between two state changes in the history. An unavailable or unknown state ends a hold, so a Node reboot starts the count again.

The threshold comes from Home Assistant's raw history from 2026-10-03 05:58 to 2026-10-13 10:19, about 10 days. Up to the #11 flash at 19:21 on 2026-10-09 the Node ran the YAML protocol copy, which published about once a minute; after it, the Component. The measurement leaves out:

- the freeze, 2026-10-12 09:52 to 11:47;
- 2026-10-09 09:27 to 10:32 and 12:00 to 12:51. Every Value stopped at once and came back with a jump no plant makes in one step: brine went from 7.2 to 22.0 °C, then from 6.9 to 21.5 °C. The owner had switched the unit off around 09:30 (diagnosis notes); the cause of the second stretch isn't recorded. The overnight phase would fail on the first, which is right, since Home Assistant had no live temperatures;
- the time each Value was unavailable, such as the Node outage from 2026-10-06 08:43 to 2026-10-07 11:30.

The longest hold of each temperature Value in the rest. `node.yaml` doesn't publish M3 and M6, so they're not here:

| M | Value | Longest hold | When |
|---|---|---|---|
| M1 | outside_temp | 514 min | 2026-10-11 00:12–08:46 |
| M2 | l1_supply | 493 min | 2026-10-06 00:30–08:43 |
| M4 | tank_middle | 54 min | 2026-10-09 06:30–07:24 |
| M7 | tank_top_in | 200 min | 2026-10-05 11:45–15:05 |
| M8 | brine | 325 min | 2026-10-08 02:36–08:01 |
| M9 | tank_top | 82 min | 2026-10-09 04:25–05:47 |
| M10 | tank_bottom | 672 min | 2026-10-05 04:08–15:20 |

The check needs all seven to hold at once, so a threshold under the single holds above still passes normal running. The longest stretch in which no temperature Value changed was 19 min (2026-10-03 07:54–08:13), and 6.8 min since the Component (2026-10-12 05:17–05:23). The freeze's longest stretch between Node reboots was 83 min, 09:52:24 to 11:16:19. 60 minutes sits between the two and catches a freeze within the first hour of a night.

## Open questions

- What makes the Controller freeze its measurements on the bus, and whether anything short of a power cycle clears it.
- Whether VaraajaYlä uses M1 or the averaged outdoor temperature.
- How the tank-top and tank-bottom calls combine, and whether the 5-minute wait also applies to tank-top starts.
- Which factory values for VaraajaAlaEro and VaraajaYläEro are right.
- Which Dig input each of `digi1`–`digi3` reports.
- What the Bank bytes without a row hold. The end of `components/geopro_202s/register_map.py` lists them with their 2026-10-09 values.

[s20]: ../manuals/kasikirja.md#s20
[s21]: ../manuals/kasikirja.md#s21
[s22]: ../manuals/kasikirja.md#s22
[s23]: ../manuals/kasikirja.md#s23
[s26]: ../manuals/kasikirja.md#s26
[s28]: ../manuals/kasikirja.md#s28
[s29]: ../manuals/kasikirja.md#s29
[s39]: ../manuals/kasikirja.md#s39
