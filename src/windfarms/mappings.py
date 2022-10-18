labels_df = [
    "name",
    "sea",
    "country",
    "capacity",
    "type",
    "number_of_turbines",
    "coordinates",
    "status",
    "commissioning",
    "sources_remarks",
]

seas_de = [
    "Golf von Biskaya",
    "Ärmelkanal",
    "IJsselmeer",
    "Irische See",
    "Nordsee",
    "Großer Belt",
    "Kattegatt",
    "Ostsee",
    "Öresund",
    "Vänern (Binnensee)",
    "Kattegat/Grenaa",
    "Atlantischer Ozean",
    "Ostchinesisches Meer",
    "Gelbes Meer",
    "Südchinesisches Meer",
    "Formosastraße",
    "Golf von Bohai",
    "Japanisches Meer",
    "Pazifischer Ozean",
    "Mittelmeer",
]
seas_df = [
    "gulf_of_biskaya",
    "english_channel",
    "ijsselmeer",
    "irish_sea",
    "north_sea",
    "great_belt",
    "kattegatt",
    "baltic_sea",
    "oeresund",
    "vaenern",
    "kattegatt_grenaa",
    "atlantic",
    "east_china_sea",
    "yellow_sea",
    "south_china_sea",
    "formosa_strait",
    "gulf_of_bohai",
    "sea_of_japan",
    "pacific",
    "mediterranean",
]
seas_map = {de: df for de, df in zip(seas_de, seas_df)}

countries_de = [
    "Spanien",
    "Vereinigtes Königreich",
    "Frankreich",
    "Niederlande",
    "Irland",
    "Dänemark",
    "Deutschland",
    "Belgien",
    "Schweden",
    "Finnland",
    "Polen",
    "Vereinigte Staaten",
    "Südkorea",
    "Volksrepublik China",
    "Vietnam",
    "Taiwan",
    "Japan",
    "Italien",
]
countries_df = [
    "spain",
    "united_kingdom",
    "france",
    "netherlands",
    "ireland",
    "denmark",
    "germany",
    "belgium",
    "sweden",
    "finnland",
    "poland",
    "united_states",
    "south_korea",
    "china",
    "vietnam",
    "taiwan",
    "japan",
    "italy",
]
countries_map = {de: df for de, df in zip(countries_de, countries_df)}

status_de = [
    "in Betrieb",
    "in Teilbetrieb",
    "in Bau",
    "in Bauvor\xadbereitung",
    "in Planung",
    "außer Betrieb",
    "Planung eingestellt",
]
status_df = [
    "production",
    "partial_production",
    "construction",
    "pre_construction",
    "planning",
    "decommissioned",
    "planning_stopped",
]
status_map = {de: df for de, df in zip(status_de, status_df)}

type_de = [
    "Gamesa G80(2,0\xa0MW, 80,0 m)",
    "Vestas V112-3.45(3,45\xa0MW, 112,0 m)",
    "GE Haliade 150-6MW(6,0\xa0MW, 150,0 m)",
    "Siemens Gamesa SG 8.0-167 DD(8,0\xa0MW, 167,0 m)",
    "Siemens SWT-7.0-154(7,0\xa0MW, 154,0 m)",
    "Nedwind NW 40/500(500\xa0kW, 40,8 m)",
    "Nedwind NW 40/500(500\xa0kW, 40,8 m)",
    "Nordtank NTK 600(600\xa0kW, 43,0 m)",
    "Siemens SWT-3.0-108(3,0\xa0MW, 108,0 m)",
    "Siemens Gamesa SWT-DD-130(4,3\xa0MW, 130,0 m)",
    "GE Cypress(5,5\xa0MW, 158,0 m)",
    "GE 3.6sl Offshore(3,6\xa0MW, 111,0 m)",
    "Vestas V80-2.0(2,0\xa0MW, 80,0 m)",
    "Vestas V90-3.0(3,0\xa0MW, 90,0 m)",
    "Siemens SWT-3.6-107(3,6\xa0MW, 107,0 m)",
    "REpower 5M(5,08\xa0MW, 126,5 m)",
    "51 × Siemens SWT-3.6-107(3,6\xa0MW, 107,0 m) 51 × Siemens SWT-3.6-120(3,6\xa0MW, 120,0 m)",
    "Siemens SWT-3.6-120(3,6\xa0MW, 120,0 m)",
    "MHI Vestas V164-8.0 MW(8,0\xa0MW, 164,0 m)",
    "40 × MHI Vestas V164-8.0 MW(8,25\xa0MW, 164,0 m) 47 × Siemens SWT-7.0-154(7,0\xa0MW, 154,0 m)",
    "Vestas V66-2.0(2,0\xa0MW, 66,0 m)",
    "4 × Vestas V80-2.0(2,0\xa0MW, 80,0 m)4 × Bonus B82/2300(2,3\xa0MW, 82,0 m)",
    "6 × REpower 5M(5,08\xa0MW, 126,5 m)6 × AREVA Multibrid M5000-116(5,0\xa0MW, 116,0 m)",
    "55 × Vestas V90-3.0(3,0\xa0MW, 90,0 m)1 × Alstom Haliade 150(6,0\xa0MW, 150,0 m)",
    "BARD 5.0(5,0\xa0MW, 122,0 m)",
    "Siemens SWT-2.3-93(2,3\xa0MW, 93,0 m)",
    "48 × Siemens SWT-3.6-107(3,6\xa0MW, 107,0 m)2 × Siemens SWT-6.0-120(6,0\xa0MW, 120,0 m)",
    "6 × REpower 5M(5,08\xa0MW, 126,5 m)48 × REpower 6.2M126(6,15\xa0MW, 126,5 m)",
    "Siemens SWT-3.6-120(3,78\xa0MW, 120,0 m)",
    "Vestas V112-3.0(3,0\xa0MW, 112,0 m)",
    "AREVA Multibrid M5000-116(5,0\xa0MW, 116,0 m)",
    "Senvion 6.2M126(6,15\xa0MW, 126,0 m)",
    "Siemens SWT-6.0-154(6,0\xa0MW, 154,0 m)",
    "30 × Vestas V90-3.0(3,0\xa0MW, 90,0 m)15 × Vestas V112-3.3(3,3\xa0MW, 112,0 m)",
    "Siemens SWT-4.0-130(4,0\xa0MW, 130,0 m)",
    "Siemens SWT-6.0-154(6,3\xa0MW, 154,0 m)",
    "Vestas V112-3.3(3,3\xa0MW, 112,0 m)",
    "9 × MHI Vestas V164-8.0 MW(8,4\xa0MW, 164,0 m) 2 × MHI Vestas V164-8.0 MW(8,8\xa0MW, 164,0 m)",
    "MHI Vestas V164-8.0 MW(8,3\xa0MW, 164,0 m)",
    "78 × Siemens SWT-4.0-120(4,0\xa0MW, 120,0 m) 56 × MHI Vestas V164-8.0 MW(8,3\xa0MW, 164,0 m)",
    "MHI Vestas V164-8.0 MW(8,4\xa0MW, 164,0 m)",
    "80 × Vestas V80-2.0(2,0\xa0MW, 80,0 m)91 × Siemens SWT-2.3-93(2,3\xa0MW, 93,0 m)49 × MHI Vestas V164-8.0 MW(8,3\xa0MW, 164,0 m)",
    "GE Haliade 150-6MW(6,0\xa0MW, 151,0 m)",
    "Siemens SWT-7.0-154(7,35\xa0MW, 154,0 m)",
    "MHI Vestas V164-9.5 MW(9,5\xa0MW, 164,0 m)",
    "Siemens Gamesa SG 8.0-167 DD(8,4\xa0MW, 167,0 m)",
    "40 × AREVA Multibrid M5000-116(5,00\xa0MW, 116,0 m) 32 × Senvion 6.3M152(6,33\xa0MW, 152,0 m)",
    "MHI Vestas V164-9.5 MW(9,525\xa0MW, 164,0 m)",
    "Siemens Gamesa SG 8.0-167 DD Flex(9,0\xa0MW, 167,0 m)",
    "Siemens Gamesa SG 11.0-200 DD(11,0\xa0MW, 200,0\xa0m)",
    "MHI Vestas V164-10.0 MW(10,0\xa0MW, 164,0 m)",
    "GE Haliade-X 13 MW(13,0\xa0MW, 218,0 m)",
    "Siemens Gamesa SG 11.0-200 DD(11,0\xa0MW, 200,0 m)",
    "GE Haliade-X 14 MW(14,0\xa0MW, 218,0 m)",
    "Siemens Gamesa SG 14.0-222 DD(14,0\xa0MW, 222,0 m)",
    "Vestas V236-15.0 MW(15,0\xa0MW, 236,0 m)",
    "Siemens Gamesa SG 14.0-222 DD(14,7\xa0MW, 222,0 m)",
    "Siemens Gamesa SG 14.0-236 DD(15,0\xa0MW, 236,0 m)",
    "Bonus B35/450(450\xa0kW, 35,0 m)",
    "Vestas V39-500(500\xa0kW, 39,0 m)",
    "Vestas V47-660(660\xa0kW, 47,0 m) (zunächst Wind World 37/550\xa0kW);",
    "Enron Wind 1.5 s(1,5\xa0MW, 70,0 m)",
    "Bonus B76/2000(2,0\xa0MW, 76,0 m)",
    "NEG Micon NM 72/2000(2,0\xa0MW, 72,0 m)",
    "1 × Vestas V90-3.0(3,0\xa0MW, 90,0 m)1 × Bonus B82/2300(2,3\xa0MW, 82,4 m)1 × Nordex N90/2300(2,3\xa0MW, 90,0 m)",
    "Siemens SWT-2.3-82(2,3\xa0MW, 82,0 m)",
    "8 × Siemens SWT-3.3-130(3,3\xa0MW, 130,0 m)5 × Siemens SWT-3.2-113(3,2\xa0MW, 113,0 m)",
    "72 × Siemens SWT-2.3-82(2,3\xa0MW, 82,0 m)90 × Siemens SWT-2.3-93(2,3\xa0MW, 93,0 m)",
    "WinWinD WWD-3 D100(3,0\xa0MW, 100,0 m)",
    "21 × Siemens SWT-2.3-93(2,3\xa0MW, 93,0 m)",
    "80 × SWT-3.6-120(3,6\xa0MW, 120,0 m)",
    "Adwen AD 5-135(5,05\xa0MW, 135,0 m)",
    "Siemens SWT-6.0-154(6,4\xa0MW, 154,0 m)",
    "MHI Vestas V174-9.5 MW(9,525\xa0MW, 174,0 m)",
    "Siemens Gamesa SG 14.0-236 DD(14,0\xa0MW, 236,0 m)",
    "GE Haliade-X 13 MW(13,6\xa0MW, 218,0 m)",
    "je 8,4 MW",
    "Siemens Gamesa SG 14.0-222 DD(15,0\xa0MW, 222,0 m)",
    "Vestas V236-13.6 MW(13,6\xa0MW, 236,0 m)",
    "1 × Windpower STX 72 2\xa0MW(2,0\xa0MW, 70,7 m)1 × Doosan WinDS3000/91(3,0\xa0MW, 91,3 m)",
    "21 × Siemens SWT-2.3-101(2,3\xa0MW, 101,0 m)17 × Sinovel SL3000/90(3,0\xa0MW, 90,0 m)40 × Goldwind GW 109/2500(2,5\xa0MW, 109,0 m)2 × CSIC Haizhuang H128-5.0(5,0\xa0MW, 128,0 m)",
    "GE 1.6-82.5(1,6\xa0MW, 82,5 m)",
    "34 × Sinovel SL3000/90(3,0\xa0MW, 90,0 m)27 × Shanghai Electric W3600-116(3,6\xa0MW, 116,0 m) 1 × Sinovel SL5000/128(5,0\xa0MW, 128,0 m)",
    "10 × CSIC Haizhuang H102-2.0(2,0\xa0MW, 102,0 m)32 × Siemens SWT-2.5-108(2,5\xa0MW, 108,0 m)",
    "Diverse 2 × United Power UP1500-82(1,5\xa0MW, 82,0 m)2 × MingYang MY1.5Su 82.6(1,5\xa0MW, 82,6 m)2 × Shanghai Electric W2000-93(2,0\xa0MW, 93,0 m)2 × Envision EN82-1.5(1,5\xa0MW, 82,5 m)2 × Sany SE9320III-S3(2,0\xa0MW, 93,0 m)1 × Sinovel SL3000/90(3,0\xa0MW, 90,0 m)1 × Goldwind GW 100/2500(2,5\xa0MW, 100,0 m)1 × CSIC Haizhuang H93-2.0(2,0\xa0MW, 93,0 m)1 × BaoNan BN82-2\xa0MW(2,0\xa0MW, 82,0 m)1 × MingYang MY3.0-100 SCD(3,0\xa0MW, 100,0 m)1 × Goldwind GW 140/3000(3,0\xa0MW, 140,0 m)7 × Envision EN109-4.0(4,0\xa0MW, 109,0 m)2 × CSIC Haizhuang H151-5.0(5,0\xa0MW, 151,0 m)1 × MingYang MY6.0-140 SCD(6,0\xa0MW, 140,0 m)1 × Dongfang Electric FD140-5500(5,5\xa0MW, 140,0 m)",
    "25 × Siemens SWT-4.0-120(4,0\xa0MW, 120,0 m)25 × Envision EN136-4.0(4,0\xa0MW, 136,0 m)",
    "Siemens SWT-4.0-120(4,0\xa0MW, 120,0 m)",
    "XEMC Darwind XD115 5.0(5,0\xa0MW, 115,0 m)",
    "37 × Siemens SWT-4.0-130(4,0\xa0MW, 130,0 m)18 × Goldwind GW 109/2500(2,5\xa0MW, 109,0 m)",
    "38 × Siemens SWT-4.0-130(4,0\xa0MW, 130,0 m)12 × Envision EN136-4.2(4,2\xa0MW, 136,0 m)19 × CSIC Haizhuang H151-5.0(5,0\xa0MW, 151,0 m)1 × CSIC Haizhuang H171-5.0(5,0\xa0MW, 171,0 m)",
    "Doosan WinDS3000/91(3,0\xa0MW, 91,0 m)",
    "Envision EN136-4.0(4,0\xa0MW, 136,0 m)",
    "Envision EN136-4.2(4,2\xa0MW, 136,0 m)",
    "34 × MingYang MySE3.0-112(3,0\xa0MW, 112,0 m) 3 × United Power UP6000-136(6,0\xa0MW, 136,0 m)",
    "63 × Siemens SWT-4.0-130(4,0\xa0MW, 130,0 m)12 × Envision EN136-4.2(4,2\xa0MW, 136,0 m)",
    "2 × Siemens SWT-4.0-120(4,0\xa0MW, 120,0 m)20 × Siemens SWT-6.0-154(6,0\xa0MW, 154,0 m)",
    "Diverse 3 × GE Haliade 150-6MW(6,0\xa0MW, 150,0 m)2 × Goldwind GW 154/6700(6,7\xa0MW, 154,0 m)2 × CSIC Haizhuang H128-5.0(5,0\xa0MW, 128,0 m)2 × Taiyuan TZ5000/154(5,0\xa0MW, 154,0 m)2 × MingYang MySE5.5-155(5,5\xa0MW, 155,0 m)1 × Dongfang Electric FD140-5000(5,0\xa0MW, 140,0 m)2 × Siemens SWT-6.0-154(6,0\xa0MW, 154,0 m)",
    "MingYang MySE5.5-155(5,5\xa0MW, 155,0 m)",
    "80 × Goldwind GW 109/2500(2,5\xa0MW, 109,0 m) 80 × Goldwind GW 130/2500(2,5\xa0MW, 130,0 m)",
    "28 × Shanghai Electric W3600-122(3,6\xa0MW, 122,0 m) 25 × Siemens SWT-4.0-130(4,0\xa0MW, 130,0 m) 2 × Siemens SWT-6.0-154(6,0\xa0MW, 154,0 m)",
    "Siemens Gamesa G132-5.0MW(5,0\xa0MW, 132,0 m)",
    "54 × Goldwind GW 140/3300(3,3\xa0MW, 140,0 m)19 × Goldwind GW 171/6450(6,45\xa0MW, 171,0 m)",
    "20 × Goldwind GW 171/6450(6,45\xa0MW, 171,0 m)50 × Goldwind GW 140/3300(3,30\xa0MW, 140,0 m)2 × Goldwind GW 140/3000(3,00\xa0MW, 140,0 m)",
    "50 × MingYang MySE3.0-135(3,0\xa0MW, 135,0 m)46 × Goldwind GW 140/3300(3,3\xa0MW, 140,0 m)",
    "71 × Envision EN136-4.2(4,2\xa0MW, 136,0 m)20 × CSIC Haizhuang H151-5.0(5,0\xa0MW, 151,0 m)",
    "7 × Doosan WinDS3000/100(3,0\xa0MW, 100,0 m)13 × Doosan WinDS3000/134(3,0\xa0MW, 134,0 m)",
    "61 × Siemens SWT-4.0-130(4,0\xa0MW, 130,0 m)10 × MingYang MySE5.5-155(5,5\xa0MW, 155,0 m)",
    "40 × CSIC Haizhuang H171-5.0(5,0\xa0MW, 171,0 m)25 × Siemens SWT-4.0-130(4,0\xa0MW, 130,0 m)",
    "18 × XEMC Darwind XD140 4.0(4,0\xa0MW, 140,0 m)36 × Envision EN148-4.5(4,5\xa0MW, 148,0 m)",
    "Hitachi HTW5.2-127(5,2\xa0MW, 127,0 m)",
    "38 × Goldwind GW 155/4500(4,5\xa0MW, 155,0 m)10 × Goldwind GW 171/6450(6,45\xa0MW, 171,0 m)",
    "Shanghai Electric G4-146(4,0\xa0MW, 146,0 m)",
    "31 × MingYang MySE6.45-180(6,45\xa0MW, 178,0 m)31 × Goldwind GW 171/6450(6,45\xa0MW, 171,0 m)",
    "Dongfang Electric FD186-7000(7,00\xa0MW, 186,0 m)",
    "MingYang MySE6.45-180(6,45\xa0MW, 178,0 m)",
    "CSIC Haizhuang H151-5.0(5,0\xa0MW, 151,0 m)",
    "52 × Shanghai Electric G4-146(4,0\xa0MW, 146,0 m) 15 × Shanghai Electric SE-6.25MW-172(6,25\xa0MW, 172,0 m)",
    "22 × MingYang MySE7.0-158(7,0\xa0MW, 158,0 m)24 × CSIC Haizhuang H171-6.2(6,2\xa0MW, 171,0 m)",
    "37 × MingYang MySE6.8-158(6,8\xa0MW, 158,0 m)30 × MingYang MySE8.3-180(8,3\xa0MW, 178,0 m)",
    "Goldwind GW 171/6450(6,45\xa0MW, 171,0 m)",
    "Envision EN148-4.5(4,5\xa0MW, 148,0 m)",
    "1 × MingYang MySE5.5-155(5,5\xa0MW, 155,0 m) 46 × MingYang MySE6.45-180(6,45\xa0MW, 180,0 m)",
    "Shanghai Electric SE-6.25MW-172(6,25\xa0MW, 172,0 m)",
    "MingYang MySE6.45-180(6,45\xa0MW, 180,0 m)",
    "47 × MingYang MySE6.45-171(6,45\xa0MW, 171,0 m) 47 × MingYang MySE6.45-180(6,45\xa0MW, 180,0 m)",
    "38 × XEMC Darwind XD140 4.0(4,0\xa0MW, 140,0 m) 34 × Siemens SWT-4.0-130(4,0\xa0MW, 130,0 m)",
    "53 × CSIC Haizhuang H151-5.0(5,0\xa0MW, 151,0 m)25 × CSIC Haizhuang H171-5.0(5,0\xa0MW, 171,0 m)2 × CSIC Haizhuang H171-6.2(6,2\xa0MW, 171,0 m)",
    "10 × Dongfang Electric FD185-10000(10,0\xa0MW, 185,0 m)26 × Goldwind GW 175/8000(8,0\xa0MW, 175,0 m)",
    "Diverse 7 × Dongfang Electric FD186-7000(7,0\xa0MW, 186,0 m)1 × Dongfang Electric FD185-10000(10,0\xa0MW, 185,0 m)33 × Goldwind GW 171/6450(6,45\xa0MW, 171,0 m)1 × Goldwind GW 175/8000(8,0\xa0MW, 175,0 m)1 × MingYang MySE8.3-180(8,3\xa0MW, 178,0 m)",
    "44 × MingYang MySE6.45-180(6,45\xa0MW, 178,0 m)2 × MingYang MySE8.3-180(8,3\xa0MW, 178,0 m)",
    "MHI Vestas V174-9.5 MW(9,5\xa0MW, 174,0 m)",
    "MHI Vestas V174-9.5 MW(9,6\xa0MW, 174,0 m)",
    "Vestas V47-660(660\xa0kW, 47,0 m)",
    "7 × Fuji/Subaru 80/2.0(2,0\xa0MW, 80,0 m) 8 × Hitachi HWT2.0-80(2,0\xa0MW, 80,0 m)",
    "Siemens SWT-3.0-101(3,0\xa0MW, 101,0 m)",
    "MingYang MySE3.0-135(3,0\xa0MW, 135,0 m)",
    "MHI Vestas V117-4.2 MW(4,2\xa0MW, 117,0 m)",
    "GE Haliade-X 12 MW(12,6\xa0MW, 218,0 m)",
]

type_df = [
    "gamesa_g80",
    "vestas_v112_3.45",
    "ge_haliade_150_6mw",
    "siemens_gamesa_sg_8.0_167_dd",
    "siemens_swt_7.0_154",
    "nedwind_nw_40/500",
    "nedwind_nw_40/500",
    "nordtank_ntk_600",
    "siemens_swt_3.0_108",
    "siemens_gamesa_swt_dd_130",
    "ge_cypress",
    "ge_3.6sl_offshore",
    "vestas_v80_2.0",
    "vestas_v90_3.0",
    "siemens_swt_3.6_107",
    "repower_5m",
    "siemens_swt_3.6_107",
    "siemens_swt_3.6_120",
    "mhi_vestas_v164_8.0_mw",
    "mhi_vestas_v164_8.0_mw",
    "vestas_v66_2.0",
    "vestas_v80_2.0",
    "repower_5m",
    "55_×_vestas_v90_3.0",
    "bard_5.0",
    "siemens_swt_2.3_93",
    "48_×_siemens_swt_3.6_107",
    "6_×_repower_5m",
    "siemens_swt_3.6_120",
    "vestas_v112_3.0",
    "areva_multibrid_m5000_116",
    "senvion_6.2m126",
    "siemens_swt_6.0_154",
    "30_×_vestas_v90_3.0",
    "siemens_swt_4.0_130",
    "siemens_swt_6.0_154",
    "vestas_v112_3.3",
    "9_×_mhi_vestas_v164_8.0_mw",
    "mhi_vestas_v164_8.0_mw",
    "78_×_siemens_swt_4.0_120",
    "mhi_vestas_v164_8.0_mw",
    "80_×_vestas_v80_2.0",
    "ge_haliade_150_6mw",
    "siemens_swt_7.0_154",
    "mhi_vestas_v164_9.5_mw",
    "siemens_gamesa_sg_8.0_167_dd",
    "40_×_areva_multibrid_m5000_116",
    "mhi_vestas_v164_9.5_mw",
    "siemens_gamesa_sg_8.0_167_dd_flex",
    "siemens_gamesa_sg_11.0_200_dd",
    "mhi_vestas_v164_10.0_mw",
    "ge_haliade_x_13_mw",
    "siemens_gamesa_sg_11.0_200_dd",
    "ge_haliade_x_14_mw",
    "siemens_gamesa_sg_14.0_222_dd",
    "vestas_v236_15.0_mw",
    "siemens_gamesa_sg_14.0_222_dd",
    "siemens_gamesa_sg_14.0_236_dd",
    "bonus_b35/450",
    "vestas_v39_500",
    "vestas_v47_660",
    "enron_wind_1.5_s",
    "bonus_b76/2000",
    "neg_micon_nm_72/2000",
    "1_×_vestas_v90_3.0",
    "siemens_swt_2.3_82",
    "8_×_siemens_swt_3.3_130",
    "72_×_siemens_swt_2.3_82",
    "winwind_wwd_3_d100",
    "21_×_siemens_swt_2.3_93",
    "80_×_swt_3.6_120",
    "adwen_ad_5_135",
    "siemens_swt_6.0_154",
    "mhi_vestas_v174_9.5_mw",
    "siemens_gamesa_sg_14.0_236_dd",
    "ge_haliade_x_13_mw",
    "je_8,4_mw",
    "siemens_gamesa_sg_14.0_222_dd",
    "vestas_v236_13.6_mw",
    "1_×_windpower_stx_72_2\xa0mw",
    "21_×_siemens_swt_2.3_101",
    "ge_1.6_82.5",
    "34_×_sinovel_sl3000/90",
    "10_×_csic_haizhuang_h102_2.0",
    "diverse_2_×_united_power_up1500_82",
    "25_×_siemens_swt_4.0_120",
    "siemens_swt_4.0_120",
    "xemc_darwind_xd115_5.0",
    "37_×_siemens_swt_4.0_130",
    "38_×_siemens_swt_4.0_130",
    "doosan_winds3000/91",
    "envision_en136_4.0",
    "envision_en136_4.2",
    "34_×_mingyang_myse3.0_112",
    "63_×_siemens_swt_4.0_130",
    "2_×_siemens_swt_4.0_120",
    "diverse_3_×_ge_haliade_150_6mw",
    "mingyang_myse5.5_155",
    "80_×_goldwind_gw_109/2500",
    "28_×_shanghai_electric_w3600_122",
    "siemens_gamesa_g132_5.0mw",
    "54_×_goldwind_gw_140/3300",
    "20_×_goldwind_gw_171/6450",
    "50_×_mingyang_myse3.0_135",
    "71_×_envision_en136_4.2",
    "7_×_doosan_winds3000/100",
    "61_×_siemens_swt_4.0_130",
    "40_×_csic_haizhuang_h171_5.0",
    "18_×_xemc_darwind_xd140_4.0",
    "hitachi_htw5.2_127",
    "38_×_goldwind_gw_155/4500",
    "shanghai_electric_g4_146",
    "31_×_mingyang_myse6.45_180",
    "dongfang_electric_fd186_7000",
    "mingyang_myse6.45_180",
    "csic_haizhuang_h151_5.0",
    "52_×_shanghai_electric_g4_146",
    "22_×_mingyang_myse7.0_158",
    "37_×_mingyang_myse6.8_158",
    "goldwind_gw_171/6450",
    "envision_en148_4.5",
    "1_×_mingyang_myse5.5_155",
    "shanghai_electric_se_6.25mw_172",
    "mingyang_myse6.45_180",
    "47_×_mingyang_myse6.45_171",
    "38_×_xemc_darwind_xd140_4.0",
    "53_×_csic_haizhuang_h151_5.0",
    "10_×_dongfang_electric_fd185_10000",
    "diverse_7_×_dongfang_electric_fd186_7000",
    "44_×_mingyang_myse6.45_180",
    "mhi_vestas_v174_9.5_mw",
    "mhi_vestas_v174_9.5_mw",
    "vestas_v47_660",
    "7_×_fuji/subaru_80/2.0",
    "siemens_swt_3.0_101",
    "mingyang_myse3.0_135",
    "mhi_vestas_v117_4.2_mw",
    "ge_haliade_x_12_mw",
]