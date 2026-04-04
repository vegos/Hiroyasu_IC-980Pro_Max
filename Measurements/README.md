# Measurements for the Hiroyasu IC-980Pro Max
> Real-world measured output power. No marketing numbers.

---

| Frequency | Band   | Power | RF Power (W)<br/>(Nissei RX-503 - Antenna) | RF Power (W)<br>(Nissei RX-503 - Dummy Load) | SWR<br/>(Nissei RX-503) |  SWR<br/>(NanoVNA) | Comment          |
| --------- | ------ | ----- | ------------ | ------------------- | ------------- | --------------- | -- |
| 145 MHz   | VHF    | Low   | 7.1 W        | 7.4W | ~1.1–1.2            | ~1.32         | 🔥 Very Good    |
| 145 MHz   | VHF    | High  | 20 W         | 23W |   ~1.2–1.3            | ~1.32         | 👍 Stable      |
| 435 MHz   | UHF    | Low   | 9.8 W        | 9.9W |  ~1.15               | ~1.37         | 👍 Good         |
| 435 MHz   | UHF    | High  | 24 W         | 22 W |  ~1.05               | ~1.37         | 🔥 Very Good    |
| 446 MHz   | PMR    | High  | 17 W         | Not Measured |  ~1.7–1.8            | ~1.84         | :warning: Warning |
  
---

## :mag_right: Measurement Setup

- Antenna: Diamond VX50
- Dummy Load: 50Ω/200W (used for reference measurements)
- Coax: Hyperflex 5 (~15m)
- Chokes: Two chokes with FT240-43 ferrites on both ends  
- SWR/Power Meter: Nissei RX-503
- VNA: NanoVNA H4 (DiSlord v1.2.46)  

Measurements performed on:
- VHF (145 MHz)
- UHF (435 MHz)
- PMR (446 MHz)
