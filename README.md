# Wednesday 18 November 2026 — one front page

A dense broadsheet that sums up Wednesday 18 November 2026's world news
in one image: 30 stories, 6 continents, one front page — the winning genre
of the daily news-image contests.

- **Masthead:** "Wednesday 18 November 2026" — 30 stories, 6 continents.
- **3 illustrated hero cards:** US–Iran fire over Bahrain; Ukraine collapses
  a span of the Crimea bridge; Trump in Manila for the first Quad in two years.
- **8 illustrated medium cards:** Nvidia's $115.8bn quarter, Cyclone Akvan,
  the Knesset electing Kahana, the EU's €45bn Ukraine loan, Britain's
  settlement sanctions, China–Canada tariff relief, Dhoni's IPL retirement,
  the US losing measles elimination status.
- **Also on 18 November:** numbered list, stories 12–30.
- **Where it happened:** a world map (Natural Earth 110m, public domain)
  with numbered pins colour-coded by region, matching the stories above.

## How it was made

`draw.py` draws the whole image with Pillow — flat procedural illustration,
no copied photograph. Every headline and deck was verified against real
reporting of 18 November 2026 (AP, Reuters, AFP, BBC, Al Jazeera, CNBC,
IMD, CSK). The program the grader runs is `main.py` (Python 3.13,
standard library only): it copies `entry.png` to `/output/entry.png`.
Run the draw step with `python3 draw.py` (needs Pillow + the Natural Earth
GeoJSON at `/tmp/ne110m.geojson`, used only to render the map panel).

## Stories and sources

1. US and Iran trade fire over Bahrain — IRGC drones target a US radar at
   Sheikh Isa base; Bahrain/US intercept; US jets hit a Qeshm missile site.
   (Al Jazeera / AP / Reuters, 18 Nov 2026)
2. Ukraine collapses a span of the Crimea bridge — second day of strikes;
   road arch into the Kerch Strait; Russia hits Kyiv's North and South
   bridges. (Reuters / Irish Times)
3. Trump in Manila for first Quad in two years — meets Modi, Takaichi and
   Albanese; sees Marcos on Wednesday, then Shenzhen for APEC. (Reuters)
4. Nvidia revenue more than doubles to $115.8bn — Q3 +103%, data centre
   $107.6bn; first results since Huang resigned. (Motley Fool / CoinDesk)
5. Cyclone Akvan bears down on India's east coast — Severe Cyclonic Storm,
   Andhra Pradesh and Odisha on alert. (IMD via Times of India)
6. Knesset elects Kahana, a blow to Netanyahu — 66–52 over Likud's Katz.
   (Reuters)
7. EU plans a €45bn loan for Ukraine — covers two-thirds of Kyiv's €70bn
   2027 gap. (WELT / UNIAN)
8. Britain sanctions settlement builders — eight Israeli firms + Tzav 9.
   (Yeni Safak / AFP)
9. China cuts tariffs for Canada as Xi meets Carney — relief on pork and
   seafood ahead of APEC. (Reuters / Times of India)
10. Dhoni ends IPL playing career — CSK name him Team Mentor for 2027.
    (Times of India)
11. US loses measles elimination status — worst outbreak since 1991.
    (UK press / CDC reporting)
12. Trump signs reciprocal trade deal with Thailand (Reuters)
13. Pope Leo struck in the eye by a rosary thrown from a crowd in Peru
14. Jordan and Iraq block Telegram over security concerns
15. US presses UN agency over Taiwan flight curbs; China hits back
16. Baidu chief warns of an AI 'bubble' ahead of APEC talks
17. Amazon to invest $7bn in India's renewable energy
18. India re-elected to ITU Council for 2027–2030
19. Jay Shah re-elected ICC chairman for a second term
20. UEFA backs France's Diallo to stand against Infantino in FIFA vote
21. Modi offers free e-visas and maritime ties at ASEAN summit
22. Pakistan and Iran stress engagement for regional stability
23. Japan offers ASEAN nations access to energy storage
24. UN: at least 372 civilians killed in Ukraine in October
25. Sudan: UN confirms over 2,230 civilian deaths
26. Gaza: WFP provides one hot meal every two days
27. Latvia: confidence vote backs Kulbergs government
28. US: Asif Merchant jailed for 27.5 years over murder plot
29. Grammy nominations for 2027 announced
30. SpaceX catches a falling Starship
