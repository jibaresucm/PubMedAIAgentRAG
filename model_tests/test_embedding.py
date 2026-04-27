from llama_cpp import Llama
from settings import config
import os

# Configuración técnica para tu RTX 4060
print("--- Iniciando carga del modelo Gemma 2 IQ4_XS ---")
model_path = os.path.join(config.EMBEDDING_MODELS_PATH, config.EMBEDDING_MODEL)
emb = Llama(
    model_path=model_path,
    n_ctx=2048, 
    n_gpu_layers=-1, 
    n_threads=8, 
    flash_attn=True,
    embedding= True,
    verbose=False,
    type_k=8,
    type_v= 8
)

texto_prueba = """1. J Korean Med Sci. 2026 Apr 13;41(14):e113. doi: 10.3346/jkms.2026.41.e113.

Trends in Acute Care and Rehabilitation for First-Ever Stroke Patients: A 
12-Year Perspective, the KOSCO Study.

Kim DH(1), Sohn MK(2), Lee J(3), Kim DY(4), Shin YI(5), Oh GJ(6), Lee YS(7), Joo 
MC(8), Lee SY(9), Song MK(10), Han J(11), Ahn J(12), Lee HS(1), Kim YH(13), 
Chang WH(1)(14).

Author information:
(1)Department of Physical and Rehabilitation Medicine, Center for Prevention and 
Rehabilitation, Heart Vascular Stroke Institute, Samsung Medical Center, 
Sungkyunkwan University School of Medicine, Seoul, Korea.
(2)Department of Rehabilitation Medicine, College of Medicine, Chungnam National 
University, Daejeon, Korea.
(3)Department of Rehabilitation Medicine, Konkuk University School of Medicine, 
Seoul, Korea.
(4)Department and Research Institute of Rehabilitation Medicine, Yonsei 
University College of Medicine, Seoul, Korea.
(5)Department of Rehabilitation Medicine, Pusan National University Yangsan 
Hospital, Yangsan, Korea.
(6)Department of Preventive Medicine, Wonkwang University, School of Medicine, 
Iksan, Korea.
(7)Department of Rehabilitation Medicine, Kyungpook National University 
Hospital, Daegu, Korea.
(8)Department of Rehabilitation Medicine, Wonkwang University School of 
Medicine, Iksan, Korea.
(9)Department of Rehabilitation Medicine, Jeju National University Hospital, 
Jeju National University School of Medicine, Jeju, Korea.
(10)Department of Physical and Rehabilitation Medicine, Chonnam National 
University Medical School, Gwangju, Korea.
(11)Department of Statistics, Hallym University, Chuncheon, Korea.
(12)Department of Health Convergence, Ewha Womans University, Seoul, Korea.
(13)Department of Physical and Rehabilitation Medicine, Sungkyunkwan University 
School of Medicine, Suwon, Korea. yunkim@skku.edu.
(14)Department of Health Science and Technology, Department of Medical Device 
Management and Research, SAIHST, Sungkyunkwan University, Seoul, Korea. 
wh.chang@samsung.com.

BACKGROUND: Updated data on stroke care trends are crucial for advancing stroke 
treatment. This study aimed to assess trends in inpatient care for first-ever 
stroke patients in South Korea over a 12-year period, focusing on demographic 
shifts and acute treatments including rehabilitation.
METHODS: This multicenter cohort study analyzed first-ever stroke patients 
admitted to three representative hospitals in South Korea during 2008 (n = 911), 
2014 (n = 1,489), and 2020 (n = 1,434). The 2008 data were collected 
retrospectively, while 2014 and 2020 data were obtained from a prospective 
cohort study. Data included demographics, risk factors, stroke characteristics, 
hospital course, and rehabilitation treatments.
RESULTS: From 2008 to 2020, the mean age of stroke patients increased from 62.0 
to 66.2 years. The proportion of ischemic stroke cases increased markedly from 
47.3% to 74.5% while risk factors such as diabetes mellitus and hyperlipidemia 
showed increasing prevalence. Mechanical thrombectomy increased from 0% to 3.3%. 
Mean hospital stay decreased from 25.2 to 14.9 days, while in-hospital mortality 
declined from 5.9% to 3.7%. Rehabilitation consultations increased from 27.8% to 
80.6%, occurring earlier during hospitalization. Rehabilitation therapy during 
hospitalization increased from 23.7% to 55.8%, and transfers to rehabilitation 
medicine rose from 12.8% to 19.1%. Home discharge increased from 34.8% to 60.0%.
CONCLUSION: Management of first-ever stroke patients in Korea improved 
substantially over 12 years, reflecting positive impacts of national quality 
initiatives and advancing stroke care.

© 2026 The Korean Academy of Medical Sciences.

DOI: 10.3346/jkms.2026.41.e113
PMID: 41978925 [Indexed for MEDLINE]

Conflict of interest statement: The authors have no potential conflicts of 
interest to disclose."""


embedding = emb.create_embedding(texto_prueba)["data"][0]["embedding"]
print(embedding, end="", flush=True)