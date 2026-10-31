"""
Verified Anatomical Knowledge Base Seed Data.
Contains peer-reviewed, ground-truth relationships for muscle actions,
innervations, spinal root levels, and clinical correlations.
Used to strictly ground the Gemma Anatomical Professor.
"""

# Verified Biomechanical Actions
# Format:
# (muscle_name, action, joint, phase_degrees, role, notes)
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
# Format:
# (muscle_name, nerve_name, spinal_roots, plexus_or_source)
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
    ("Soleus muscle", "Tibial nerve", "S1, S2", "Sciatic nerve tibial branch")
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

