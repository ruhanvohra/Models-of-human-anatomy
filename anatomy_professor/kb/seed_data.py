"""
Verified Anatomical Knowledge Base Seed Data.
Contains peer-reviewed, ground-truth relationships for muscle actions,
innervations, spinal root levels, bodily systems, physiology pathways, and clinical correlations.
Used to strictly ground the Gemma Anatomical Professor.
"""

# Specific Physiological Pathways & Functional Sub-Mechanisms
VERIFIED_PHYSIOLOGY_PATHWAYS = [
    {
        "id": "blood_sugar_lowering",
        "keywords": [
            "lowering blood sugar", "lower blood sugar", "reduce blood sugar",
            "lowering glucose", "lower glucose", "insulin", "blood sugar",
            "glucose regulation", "glycogenesis", "endocrine pancreas"
        ],
        "system_category": "Digestive & Endocrine Systems",
        "primary_organ": "Pancreas",
        "related_organs": ["Liver"],
        "3d_structures": [
            "Pancreas",
            "Head of pancreas",
            "Body of pancreas",
            "Tail of pancreas",
            "Liver"
        ],
        "title": "Regulation of Blood Glucose: Endocrine Pancreas & Insulin Secretion",
        "functional_role": "Synthesis and secretion of Insulin by pancreatic Beta cells to lower systemic blood glucose",
        "cellular_mechanism": (
            "While the bulk of the pancreas is an exocrine digestive gland (acinar cells producing digestive enzymes), "
            "its endocrine function is localized in approximately 1 to 2 million microscopic clusters termed the "
            "**Islets of Langerhans (Pancreatic islets)**. Within these islets:\n"
            "- **Beta cells (β-cells)** constitute ~70% of islet cells and produce and secrete the peptide hormone **Insulin**.\n"
            "- When blood glucose rises after a meal, β-cells take up glucose via GLUT transporters, accelerating ATP production, "
            "which closes ATP-sensitive K+ channels, depolarizes the cell membrane, opens voltage-gated Ca2+ channels, "
            "and triggers exocytosis of insulin storage granules into the portal circulation."
        ),
        "target_action": (
            "1. **Skeletal Muscle & Adipose Tissue:** Insulin binds tyrosine kinase receptors, promoting GLUT4 translocation to cell surfaces for rapid glucose uptake.\n"
            "2. **Liver (Target Organ, highlighted in Cyan):** Insulin stimulates glycogen synthase (glycogenesis) and glycolysis, "
            "while potently suppressing gluconeogenesis and glycogenolysis—reversing hyperglycemia.\n"
            "3. **Counter-Regulation:** Pancreatic **Alpha cells (α-cells)** produce **Glucagon** to raise blood sugar when fasting."
        ),
        "peel_keywords": ["rectus abdominis", "external oblique", "internal oblique", "transversus abdominis", "stomach", "greater omentum"],
        "color_map": {
            "pancreas": (1.0, 0.75, 0.1, 1.0), # Gold/Amber (Primary endocrine producer)
            "liver": (0.2, 0.7, 1.0, 1.0)      # Cyan (Target effector organ)
        }
    },
    {
        "id": "bile_production_storage",
        "keywords": ["bile production", "produce bile", "bile synthesis", "store bile", "gallbladder bile"],
        "system_category": "Digestive System (Hepatobiliary)",
        "primary_organ": "Liver",
        "related_organs": ["Gallbladder"],
        "3d_structures": ["Liver", "Gallbladder"],
        "title": "Bile Synthesis and Concentration (Hepatobiliary Unit)",
        "functional_role": "Synthesis, concentration, and delivery of bile salts for dietary fat emulsification",
        "cellular_mechanism": "Hepatocytes synthesize bile acids from cholesterol; bile drains via hepatic ducts into the gallbladder for storage and concentration.",
        "target_action": "Cholecystokinin (CCK) stimulates gallbladder contraction and sphincter of Oddi relaxation when lipids enter the duodenum.",
        "peel_keywords": ["rectus abdominis", "external oblique", "internal oblique"],
        "color_map": {"liver": (0.8, 0.4, 0.2, 1.0), "gallbladder": (0.2, 0.9, 0.3, 1.0)}
    },
    {
        "id": "gastric_acid_proteolysis",
        "keywords": ["acid secretion", "gastric acid", "stomach acid", "pepsin", "hydrochloric acid"],
        "system_category": "Digestive System (Upper GI)",
        "primary_organ": "Stomach",
        "related_organs": ["Duodenum", "Oesophagus"],
        "3d_structures": ["Stomach", "Duodenum"],
        "title": "Gastric Acid Secretion and Chemical Proteolysis",
        "functional_role": "Denaturation of dietary proteins and pathogen destruction",
        "cellular_mechanism": "Parietal (oxyntic) cells in the gastric glands secrete HCl via H+/K+ ATPase proton pumps; Chief cells secrete pepsinogen.",
        "target_action": "Low luminal pH (1.5–2.0) cleaves pepsinogen to active pepsin, initiating peptide hydrolysis.",
        "peel_keywords": ["rectus abdominis", "external oblique"],
        "color_map": {"stomach": (1.0, 0.6, 0.2, 1.0), "duodenum": (0.4, 0.8, 1.0, 1.0)}
    }
]

# Verified Physiological Systems & Functional Knowledge
VERIFIED_SYSTEMS = {
    "respiratory": {
        "system_name": "Respiratory System (Systema respiratorium)",
        "ta2_id": 3133,
        "keywords": ["respirat", "lung", "oxygen", "alveol", "bronch", "trachea", "pulmon", "airway", "breath", "gas exchange"],
        "primary_3d_structures": [
            "Superior lobe of right lung",
            "Middle lobe of right lung",
            "Inferior lobe of right lung",
            "Superior lobe of left lung",
            "Inferior lobe of left lung",
            "Right main bronchus",
            "Left main bronchus",
            "Trachea",
            "Pulmonary trunk",
            "Left pulmonary artery",
            "Right pulmonary artery",
            "Left superior pulmonary vein",
            "Left inferior pulmonary vein",
            "Right superior pulmonary vein",
            "Right inferior pulmonary vein"
        ],
        "functional_subunits": [
            {
                "name": "Alveolar-Capillary Membrane (Blood-Air Barrier)",
                "type": "Microscopic Gas Exchange Unit",
                "role": "Site of oxygen infusion into blood and carbon dioxide clearance",
                "mechanism": (
                    "Oxygen crosses the extremely thin (0.2–0.5 μm) blood-air barrier by simple passive diffusion. "
                    "The barrier consists of Type I alveolar cells (squamous pneumocytes), the shared extracellular basement membrane, "
                    "and the capillary endothelial cells. Oxygen diffuses down its partial pressure gradient from the alveolar air "
                    "(pO2 ≈ 104 mmHg) into deoxygenated capillary blood (pO2 ≈ 40 mmHg), where >98% binds to hemoglobin in erythrocytes."
                )
            },
            {
                "name": "Bronchial Tree (Conducting Zone)",
                "type": "Airway Transport Conduit",
                "role": "Humidification, filtration, and transport of air to respiratory zones",
                "mechanism": (
                    "Extends from the trachea to the main bronchi, lobar bronchi, segmental bronchi, and terminal bronchioles. "
                    "Lined by pseudostratified ciliated columnar epithelium with goblet cells (the mucociliary escalator) "
                    "to capture particulates before air reaches the fragile gas-exchange parenchyma."
                )
            },
            {
                "name": "Pulmonary Circulation (Vascular Interface)",
                "type": "Blood Supply for Gas Exchange",
                "role": "Delivers deoxygenated blood from right ventricle and returns oxygen-rich blood to left atrium",
                "mechanism": (
                    "The pulmonary trunk bifurcates into the right and left pulmonary arteries, carrying venous/deoxygenated blood "
                    "into the pulmonary capillary plexus enveloping each alveolus. After oxygen uptake, four pulmonary veins "
                    "(two left, two right) carry newly oxygenated blood directly into the left atrium for systemic distribution."
                )
            }
        ],
        "peel_keywords": ["pectoralis", "rib", "intercostal", "costal", "sternum", "subclavius"],
        "default_camera": "anterior"
    },
    "cardiovascular": {
        "system_name": "Cardiovascular System (Systema cardiovasculare)",
        "ta2_id": 3889,
        "keywords": ["heart", "cardio", "aort", "ventricl", "atrium", "arter", "vein", "coronary", "valve", "circulat"],
        "primary_3d_structures": [
            "Ascending aorta",
            "Aortic arch",
            "Pulmonary trunk",
            "Superior vena cava",
            "Inferior vena cava",
            "Right ventricle",
            "Left ventricle",
            "Right atrium",
            "Left atrium",
            "Pulmonary valve",
            "Aortic valve"
        ],
        "functional_subunits": [
            {
                "name": "Heart Chambers & Valves",
                "type": "Central Muscular Pump",
                "role": "Propels blood through pulmonary and systemic circuits",
                "mechanism": (
                    "Right heart pumps deoxygenated blood to the lungs via the pulmonary trunk. "
                    "Left heart receives oxygenated blood from pulmonary veins and propels it at high pressure through the aorta."
                )
            }
        ],
        "peel_keywords": ["pectoralis", "rib", "intercostal", "sternum"],
        "default_camera": "anterior"
    },
    "digestive": {
        "system_name": "Digestive System (Systema digestorium)",
        "ta2_id": 2773,
        "keywords": ["digest", "stomach", "liver", "pancreas", "esophag", "intestin", "colon", "duodenum", "gallbladder"],
        "primary_3d_structures": [
            "Stomach",
            "Liver",
            "Gallbladder",
            "Pancreas",
            "Duodenum",
            "Oesophagus"
        ],
        "functional_subunits": [
            {
                "name": "Gastrointestinal Tract & Accessory Glands",
                "type": "Digestive & Metabolic Unit",
                "role": "Mechanical and chemical breakdown of food, nutrient absorption, and hepatic metabolism",
                "mechanism": "Enzymatic hydrolysis, acid secretion in stomach, bile and pancreatic enzyme neutralization in duodenum."
            }
        ],
        "peel_keywords": ["rectus abdominis", "external oblique", "internal oblique", "transversus abdominis"],
        "default_camera": "anterior"
    },
    "urinary": {
        "system_name": "Urinary System (Systema urinarium)",
        "ta2_id": 3351,
        "keywords": ["kidney", "urinary", "nephron", "ureter", "bladder", "renal", "filtrat"],
        "primary_3d_structures": [
            "Left kidney",
            "Right kidney",
            "Left ureter",
            "Right ureter",
            "Urinary bladder",
            "Renal artery",
            "Renal vein"
        ],
        "functional_subunits": [
            {
                "name": "Nephrons & Renal Parenchyma",
                "type": "Filtration and Osmoregulation Unit",
                "role": "Blood filtration, waste elimination, and electrolyte balance",
                "mechanism": "Glomerular ultrafiltration followed by tubular reabsorption and secretion in proximal/distal tubules."
            }
        ],
        "peel_keywords": ["rectus abdominis", "internal oblique", "external oblique", "quadratus lumborum"],
        "default_camera": "posterior"
    },
    "nervous": {
        "system_name": "Nervous System (Systema nervosum)",
        "ta2_id": 5519,
        "keywords": ["brain", "cerebr", "cerebell", "spinal cord", "nerve", "cranial", "plexus", "neural"],
        "primary_3d_structures": [
            "Brain",
            "Spinal cord",
            "Brainstem",
            "Cerebellum",
            "Cerebrum"
        ],
        "functional_subunits": [
            {
                "name": "Central and Peripheral Neural Networks",
                "type": "Signal Integration & Transmission",
                "role": "Sensorimotor integration, autonomic regulation, and cognitive processing",
                "mechanism": "Action potential generation, synaptic neurotransmitter release, and ascending/descending spinal tracts."
            }
        ],
        "peel_keywords": ["galea aponeurotica", "calvaria", "skull"],
        "default_camera": "superior"
    }
}

# Verified Biomechanical Actions
VERIFIED_ACTIONS = [
    # Shoulder Abduction
    ("Supraspinatus muscle", "abduction", "glenohumeral", "0-15 degrees", "initiator",
     "Initiates shoulder abduction; stabilizes humeral head in glenoid cavity."),
    ("Acromial part of deltoid muscle", "abduction", "glenohumeral", "15-90 degrees", "prime mover",
     "Main driver of abduction from 15 to 90 degrees; multipennate fibers produce strong torque."),
    ("Deltoid muscle", "abduction", "glenohumeral", "15-90 degrees", "prime mover",
     "Middle acromial fibers drive abduction 15-90 degrees."),
    ("Serratus anterior", "abduction", "scapulothoracic", ">90 degrees", "synergist",
     "Rotates inferior angle of scapula laterally and upward to allow abduction beyond 90 degrees."),
    ("Trapezius muscle", "abduction", "scapulothoracic", ">90 degrees", "synergist",
     "Superior and inferior fibers rotate scapula upward, enabling elevation above horizontal plane."),

    # Shoulder Adduction
    ("Pectoralis major muscle", "adduction", "glenohumeral", "full range", "prime mover",
     "Powerful adductor and internal rotator of humerus."),
    ("Latissimus dorsi muscle", "adduction", "glenohumeral", "full range", "prime mover",
     "Adducts, extends, and internally rotates arm ('climbing muscle')."),
    ("Teres major muscle", "adduction", "glenohumeral", "full range", "synergist",
     "Synergist to latissimus dorsi in adduction and medial rotation."),

    # Shoulder External Rotation (Rotator Cuff)
    ("Infraspinatus muscle", "external rotation", "glenohumeral", "full range", "prime mover",
     "Primary external rotator of humerus; key rotator cuff dynamic stabilizer."),
    ("Teres minor muscle", "external rotation", "glenohumeral", "full range", "synergist",
     "Externally rotates humerus and stabilizes posterior glenohumeral joint."),

    # Shoulder Internal Rotation
    ("Subscapularis muscle", "internal rotation", "glenohumeral", "full range", "prime mover",
     "Primary internal rotator of rotator cuff; prevents anterior dislocation."),

    # Elbow Flexion
    ("Biceps brachii muscle", "flexion", "elbow", "full range", "prime mover",
     "Powerful flexor especially when forearm is supinated; also main supinator."),
    ("Brachialis muscle", "flexion", "elbow", "full range", "prime mover",
     "Pure elbow flexor in all forearm positions ('workhorse of the elbow')."),
    ("Brachioradialis", "flexion", "elbow", "full range", "synergist",
     "Flexes elbow semi-pronated; stabilizes joint during rapid movement."),

    # Elbow Extension
    ("Triceps brachii muscle", "extension", "elbow", "full range", "prime mover",
     "Primary elbow extensor; long head also adducts humerus."),
    ("Anconeus muscle", "extension", "elbow", "terminal range", "synergist",
     "Assists in terminal elbow extension and stabilizes joint capsule."),

    # Forearm Pronation / Supination
    ("Pronator teres muscle", "pronation", "radioulnar", "full range", "prime mover",
     "Pronates forearm and assists in weak elbow flexion."),
    ("Pronator quadratus muscle", "pronation", "radioulnar", "full range", "prime mover",
     "Deep pronator; binds radius and ulna together."),
    ("Supinator muscle", "supination", "radioulnar", "full range", "prime mover",
     "Supinates forearm in slow/unresisted movements; deep branch of radial n. pierces it."),

    # Hip Abduction
    ("Gluteus medius muscle", "abduction", "hip", "full range", "prime mover",
     "Major hip abductor; prevents pelvic tilt (Trendelenburg sign) during gait."),
    ("Gluteus minimus muscle", "abduction", "hip", "full range", "synergist",
     "Abducts and medially rotates thigh."),
    ("Tensor fasciae latae muscle", "abduction", "hip", "full range", "synergist",
     "Tenses iliotibial band and assists in hip abduction and flexion."),

    # Hip Extension
    ("Gluteus maximus muscle", "extension", "hip", "full range", "prime mover",
     "Most powerful hip extensor (rising from seated, climbing stairs)."),
    ("Biceps femoris muscle", "extension", "hip", "full range", "synergist",
     "Long head extends hip and flexes knee."),
    ("Semitendinosus muscle", "extension", "hip", "full range", "synergist",
     "Extends hip, flexes knee, medially rotates leg."),
    ("Semimembranosus muscle", "extension", "hip", "full range", "synergist",
     "Extends hip, flexes knee, medially rotates leg."),

    # Knee Extension
    ("Rectus femoris muscle", "extension", "knee", "full range", "prime mover",
     "Knee extensor and hip flexor (crosses two joints)."),
    ("Vastus lateralis muscle", "extension", "knee", "full range", "prime mover",
     "Largest quadriceps muscle; extends knee."),
    ("Vastus medialis muscle", "extension", "knee", "terminal range", "prime mover",
     "Extends knee; fibers (VMO) stabilize patella tracking."),
    ("Vastus intermedius muscle", "extension", "knee", "full range", "prime mover",
     "Deep quadriceps muscle; extends knee.")
]

# Verified Innervations and Nerve Roots
VERIFIED_INNERVATIONS = [
    ("Supraspinatus muscle", "Suprascapular nerve", "C5, C6", "Superior trunk of brachial plexus"),
    ("Infraspinatus muscle", "Suprascapular nerve", "C5, C6", "Superior trunk of brachial plexus"),
    ("Deltoid muscle", "Axillary nerve", "C5, C6", "Posterior cord of brachial plexus"),
    ("Acromial part of deltoid muscle", "Axillary nerve", "C5, C6", "Posterior cord of brachial plexus"),
    ("Clavicular part of deltoid muscle", "Axillary nerve", "C5, C6", "Posterior cord of brachial plexus"),
    ("Scapular spinal part of deltoid muscle", "Axillary nerve", "C5, C6", "Posterior cord of brachial plexus"),
    ("Teres minor muscle", "Axillary nerve", "C5, C6", "Posterior cord of brachial plexus"),
    ("Subscapularis muscle", "Upper and lower subscapular nerves", "C5, C6", "Posterior cord of brachial plexus"),
    ("Teres major muscle", "Lower subscapular nerve", "C5, C6, C7", "Posterior cord of brachial plexus"),
    ("Latissimus dorsi muscle", "Thoracodorsal nerve", "C6, C7, C8", "Posterior cord of brachial plexus"),
    ("Serratus anterior", "Long thoracic nerve", "C5, C6, C7", "Roots of brachial plexus (Bell's nerve)"),
    ("Trapezius muscle", "Accessory nerve (XI)", "Cranial Nerve XI & C3, C4 proprioception", "Spinal accessory nerve"),
    ("Pectoralis major muscle", "Lateral and medial pectoral nerves", "C5, C6, C7, C8, T1", "Lateral and medial cords"),
    ("Pectoralis minor muscle", "Medial pectoral nerve", "C8, T1", "Medial cord of brachial plexus"),
    ("Biceps brachii muscle", "Musculocutaneous nerve", "C5, C6", "Lateral cord of brachial plexus"),
    ("Brachialis muscle", "Musculocutaneous nerve (dual: radial n. small lateral branch)", "C5, C6", "Lateral cord"),
    ("Coracobrachialis muscle", "Musculocutaneous nerve", "C5, C6, C7", "Lateral cord (pierces muscle)"),
    ("Triceps brachii muscle", "Radial nerve", "C6, C7, C8", "Posterior cord of brachial plexus"),
    ("Anconeus muscle", "Radial nerve", "C7, C8, T1", "Radial nerve via branch to medial triceps head"),
    ("Brachioradialis", "Radial nerve", "C5, C6", "Radial nerve trunk anterior to lateral epicondyle"),
    ("Supinator muscle", "Posterior interosseous nerve (deep radial)", "C7, C8", "Deep branch of radial nerve"),
    ("Pronator teres muscle", "Median nerve", "C6, C7", "Median nerve trunk"),
    ("Pronator quadratus muscle", "Anterior interosseous nerve", "C7, C8, T1", "Branch of median nerve"),
    ("Gluteus maximus muscle", "Inferior gluteal nerve", "L5, S1, S2", "Sacral plexus"),
    ("Gluteus medius muscle", "Superior gluteal nerve", "L4, L5, S1", "Sacral plexus"),
    ("Gluteus minimus muscle", "Superior gluteal nerve", "L4, L5, S1", "Sacral plexus"),
    ("Tensor fasciae latae muscle", "Superior gluteal nerve", "L4, L5, S1", "Sacral plexus"),
    ("Rectus femoris muscle", "Femoral nerve", "L2, L3, L4", "Lumbar plexus posterior divisions"),
    ("Vastus lateralis muscle", "Femoral nerve", "L2, L3, L4", "Lumbar plexus"),
    ("Vastus medialis muscle", "Femoral nerve", "L2, L3, L4", "Lumbar plexus"),
    ("Vastus intermedius muscle", "Femoral nerve", "L2, L3, L4", "Lumbar plexus"),
    ("Biceps femoris muscle", "Sciatic nerve (Tibial & Common fibular)", "L5, S1, S2", "Sacral plexus"),
    ("Semitendinosus muscle", "Tibial nerve (division of sciatic)", "L5, S1, S2", "Sacral plexus"),
    ("Semimembranosus muscle", "Tibial nerve (division of sciatic)", "L5, S1, S2", "Sacral plexus"),
    ("Tibialis anterior muscle", "Deep fibular (peroneal) nerve", "L4, L5", "Common fibular nerve"),
    ("Gastrocnemius muscle", "Tibial nerve", "S1, S2", "Sciatic nerve tibial branch"),
    ("Soleus muscle", "Tibial nerve", "S1, S2", "Sciatic nerve tibial branch"),
    ("Diaphragm", "Phrenic nerve", "C3, C4, C5", "Cervical plexus ('C3, 4, 5 keeps the diaphragm alive')")
]

# Verified Clinical Vignettes for Quizzing
VERIFIED_CLINICAL_CASES = [
    {
        "id": "case_shoulder_dislocation",
        "title": "Anterior Shoulder Dislocation & Badge Sensory Loss",
        "scenario": (
            "A 23-year-old rugby player sustains an anterior glenohumeral dislocation during a tackle. "
            "After closed reduction, he has numbness over the lateral deltoid area ('sergeant's patch') "
            "and severe weakness initiating abduction past 15 degrees."
        ),
        "target_structure": "Deltoid muscle",
        "target_nerve": "Axillary nerve",
        "spinal_roots": "C5, C6",
        "question": "Which nerve was injured, and which muscle's prime mover function is impaired?",
        "options": [
            "Axillary nerve; Deltoid muscle",
            "Suprascapular nerve; Supraspinatus muscle",
            "Musculocutaneous nerve; Biceps brachii",
            "Long thoracic nerve; Serratus anterior"
        ],
        "correct_index": 0,
        "explanation": (
            "The axillary nerve winds around the surgical neck of the humerus and is highly vulnerable to stretch or "
            "compression during anterior humeral head dislocations. It innervates the deltoid (abduction 15-90°) and "
            "teres minor, and gives off the superior lateral cutaneous nerve supplying the deltoid badge region."
        )
    },
    {
        "id": "case_empty_can_test",
        "title": "Rotator Cuff Impingement & Initiation Failure",
        "scenario": (
            "A 56-year-old tennis coach reports deep shoulder pain worsened by overhead serving. "
            "On physical examination, the 'empty can' (Jobe's) test is markedly positive with pain and weakness "
            "in the first 15 degrees of arm abduction."
        ),
        "target_structure": "Supraspinatus muscle",
        "target_nerve": "Suprascapular nerve",
        "spinal_roots": "C5, C6",
        "question": "Which muscle tendon is compromised, and which nerve provides its motor innervation?",
        "options": [
            "Supraspinatus muscle; Suprascapular nerve",
            "Infraspinatus muscle; Axillary nerve",
            "Subscapularis muscle; Upper subscapular nerve",
            "Teres major muscle; Lower subscapular nerve"
        ],
        "correct_index": 0,
        "explanation": (
            "The supraspinatus muscle tendon runs beneath the acromion and coracoacromial ligament, making it the most "
            "frequently impinged/torn rotator cuff tendon. It initiates the first 0-15° of abduction and is innervated "
            "by the suprascapular nerve (C5-C6) as it passes through the suprascapular notch."
        )
    },
    {
        "id": "case_winged_scapula",
        "title": "Post-Mastectomy Winged Scapula",
        "scenario": (
            "Following axillary lymph node dissection for breast carcinoma, a 48-year-old patient notes that her "
            "scapula protrudes posteriorly when pushing against a wall, and she struggles to abduct her arm above the horizontal."
        ),
        "target_structure": "Serratus anterior",
        "target_nerve": "Long thoracic nerve",
        "spinal_roots": "C5, C6, C7",
        "question": "Which nerve was injured during the axillary dissection, paralyzing which muscle?",
        "options": [
            "Long thoracic nerve; Serratus anterior",
            "Thoracodorsal nerve; Latissimus dorsi",
            "Medial pectoral nerve; Pectoralis minor",
            "Dorsal scapular nerve; Rhomboid major"
        ],
        "correct_index": 0,
        "explanation": (
            "The long thoracic nerve (roots C5-C7) runs superficially along the lateral thoracic wall on the surface of the "
            "serratus anterior muscle, putting it at risk during axillary surgery. Paralysis leads to medial winging of the "
            "scapula and inability to rotate the glenoid upward for overhead abduction (>90°)."
        )
    },
    {
        "id": "case_trendelenburg",
        "title": "Pelvic Drop During Gait (Trendelenburg Sign)",
        "scenario": (
            "Following a posterior-approach total hip arthroplasty, a patient displays an abnormal waddling gait where "
            "the right side of the pelvis drops when standing solely on the left leg."
        ),
        "target_structure": "Gluteus medius muscle",
        "target_nerve": "Superior gluteal nerve",
        "spinal_roots": "L4, L5, S1",
        "question": "Which muscle on the stance leg failed to stabilize the pelvis, and which nerve innervates it?",
        "options": [
            "Gluteus medius muscle; Superior gluteal nerve",
            "Gluteus maximus muscle; Inferior gluteal nerve",
            "Iliopsoas; Femoral nerve",
            "Obturator internus; Nerve to obturator internus"
        ],
        "correct_index": 0,
        "explanation": (
            "The gluteus medius and minimus (innervated by the superior gluteal nerve, L4-S1) are the primary hip abductors. "
            "During single-leg stance, they contract on the supported side to keep the pelvis level. Weakness results in a positive "
            "Trendelenburg sign (pelvis drops towards the unsupported contralateral side)."
        )
    }
]
