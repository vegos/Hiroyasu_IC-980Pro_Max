# 📡 Hiroyasu IC-980Pro Max S-Meter Calibration

## Overview

The original calibration procedure was proposed by **SP6PW** in the GitHub [discussion](https://github.com/vegos/Hiroyasu_IC-980Pro_Max/issues/1).

This document describes the calibration procedure that was followed, together with the measured results obtained on **my own radio**.

> **Important:** Calibration values are **radio-specific** and should **not** be copied blindly. Always calibrate your own unit.

---

## Tested Firmware

**Software Version:** `V20251031.01`

---

## ⚠️ Note

**Always read first the current service values and save them as a backup before making any changes.**

---

# Equipment Used

* Hiroyasu IC-980Pro Max
* TinySA Ultra+
* 30 dB SMA attenuator
* 40 dB SMA attenuator
* Total attenuation: **70 dB**
* SMA pigtail
* SMA-to-UHF adapter

---

# Radio Preparation

* Set **Squelch = 0**
* Switch to **Single VFO** mode (`MENU` → `V/M`)
* Tune to **145.000 MHz**
* Enter the hidden **WW01 Service Menu**
* Read and save (backup) the current calibration values

---

# TinySA Configuration

* Put TinySA in **Frequency Generator** mode
* Output Mode: **LOW Output ON**
* Frequency: **145.000 MHz**
* Modulation: **FM**
* Audio Tone: **1000 Hz**
* FM Deviation: **3.0 kHz**
* External Gain: **-70 dB**

The TinySA output was connected directly to the radio antenna connector through two fixed attenuators (30 dB + 40 dB, total 70dB).

---

# Calibration Procedure

## SQ-1

Set the TinySA output level to **-129 dBm**.

Adjust **SQ-1** until the radio displays exactly **S3**.

Verify the following levels:

| RF Level | Expected Display |
| -------: | ---------------- |
| -135 dBm | S2               |
| -129 dBm | S3               |
| -123 dBm | S4               |

Repeat changes on SQ-1 until all three levels are displayed correctly.

> **Important:** Unlike SQ-5 and SQ-9, **SQ-1 should not simply be copied from the CPS "Signal" value**. It must be adjusted manually until the displayed S-meter matches the expected levels.

---

## SQ-5

Set the TinySA output level to **-117 dBm**.

Open **Read Status** in the CPS.

Copy the **Signal** value into **SQ-5**.

Verify that the radio displays **S5**.

---

## SQ-9

Set the TinySA output level to **-93 dBm**.

Open **Read Status**.

Copy the **Signal** value into **SQ-9**.

---

# Final Calibration Values

| Parameter |   Value |
| --------- | ------: |
| SQ-1      |  **80** |
| SQ-5      | **119** |
| SQ-9      | **165** |

---

# Calibration Verification

The resulting calibration was verified on **both amateur bands**.

## VHF (145 MHz)

| RF Level | Display                           |
| -------: | --------------------------------- |
| -135 dBm | S2                                |
| -129 dBm | S3                                |
| -123 dBm | S4                                |
| -117 dBm | S5                                |
| -103 dBm | S8                                |
| -102 dBm | Beginning of MAX (2 red segments) |
|  -96 dBm | MAX (full scale)                  |

---

## UHF (435 MHz)

| RF Level | Display                                |
| -------: | -------------------------------------- |
| -129 dBm | S3                                     |
| -123 dBm | S4                                     |
| -117 dBm | S4/S5 initially, then stabilizes at S5 |
| -106 dBm | Beginning of S8                        |
| -103 dBm | S8                                     |
|  -96 dBm | Approximately half of the MAX region   |
|  -94 dBm | MAX (full scale)                       |

---

# Read Status Reference Values

These values were observed **before** calibration (using my old/*rough calibration procedure*).

## 145 MHz – Antenna Connected

| Parameter | Value |
| --------- | ----: |
| Signal    |   120 |
| Noise     |    64 |
| Glitch    |    44 |
| Volt      |   114 |
| VOX       |     0 |

---

## 145 MHz – No Antenna Connected

| Parameter | Value |
| --------- | ----: |
| Signal    |   101 |
| Noise     |    63 |
| Glitch    |    56 |

---

## 145 MHz – TinySA Connected (Generator OFF, 70 dB attenuation)

| Parameter | Value |
| --------- | ----: |
| Signal    |    90 |
| Noise     |    61 |
| Glitch    |    43 |

---

# Observations

* The calibration procedure proposed by **SP6PW** works correctly.
* The resulting calibration values differ from those measured on SP6PW's radio.
* This indicates that calibration is **radio-specific**. It might used for just a start point.
* **SQ-1** must be adjusted manually based on the displayed S-meter.
* **SQ-5** and **SQ-9** matched the values obtained from the CPS **Read Status → Signal** field.
* The calibration was successfully verified on **both 145 MHz and 435 MHz**.
* The upper end of the S-meter is compressed by the firmware. The display transitions directly from **S8** into the **MAX** region without a dedicated **S9** indication.

---

# Conclusion

After calibration, the S-meter behaves significantly better than the factory configuration.

Instead of switching almost directly from no indication to full scale, the radio now displays intermediate signal levels consistently across both VHF and UHF.

Although the upper part of the display remains compressed due to firmware behavior, the resulting calibration provides a much more useful and realistic indication of received signal strength.
