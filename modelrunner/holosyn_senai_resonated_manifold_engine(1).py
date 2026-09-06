# ... existing code ...
class SemanticMemory:
    """Semantic graph storing extracted entity-predicate-object knowledge triplets."""
    def __init__(self):
        self.triplets: List[Dict[str, Any]] = []

    def store_fact(self, subject: str, predicate: str, object_: str, confidence: float = 0.9):
        self.triplets.append({
            "subject": subject.lower().strip(),
            "predicate": predicate.lower().strip(),
            "object": object_.lower().strip(),
            "confidence": float(confidence),
            "access_count": 1,
            "last_verified": time.time()
        })
        if len(self.triplets) > 1200:
            self.triplets.sort(key=lambda x: x["confidence"] * x["access_count"])
            self.triplets.pop(0)

    def query_concept(self, concept: str) -> List[str]:
        c_clean = concept.lower().strip()
        facts = []
        for t in self.triplets:
            if c_clean in t["subject"] or c_clean in t["object"]:
                t["access_count"] += 1
                t["last_verified"] = time.time()
                facts.append(f"{t['subject']} {t['predicate']} {t['object']} (conf: {t['confidence']:.2f})")
        return facts[:5]

@dataclass
class FoundationAnchor:
    """Foundational cognitive anchor representing immutable reference priors and core axioms."""
    name: str
    axioms: str
    weight: float = 1.0
    category: str = "CORE_TRUTH"
    timestamp: float = field(default_factory=time.time)
    embedding: Optional[List[float]] = None

class FoundationManager:
    """
    Manages foundational reference frameworks, core truths, and cognitive axioms.
    Foundations act as the anchor (Foundation_Wt) against which ephemeral external
    facets (Facet_Wt) such as social media feeds and web articles are evaluated.
    """
    def __init__(self, vault_dir: str = "./vaults"):
        self.vault_dir = sanitize_filepath(vault_dir)
        self.foundations_file = os.path.join(self.vault_dir, "foundations_registry.json")
        self.foundations: Dict[str, FoundationAnchor] = {}
        self._initialize_default_foundations()
        self.load_foundations()

    def _initialize_default_foundations(self):
        defaults = [
            ("COGNITIVE_EQUILIBRIUM", "The manifold must maintain homeostatic stability, preventing runaway cognitive divergence and entropy collapse.", 1.0, "CORE_AXIOM"),
            ("EMPIRICAL_VERIFIABILITY", "Assertions and telemetry must correlate with grounded formal logic, observable data, or deductive proof chains.", 0.95, "EPISTEMIC"),
            ("RECIPROCAL_SYNERGY", "Agent swarms and communicative interactions must prioritize mutual alignment, love logic, and constructive synthesis.", 0.98, "ETHICAL_GOVERNOR"),
            ("RESOURCE_CONSERVATION", "Computational execution must minimize latency, prevent GPU/CPU memory leaks, and respect glibc heap boundaries.", 0.90, "SYSTEM_PHYSICS")
        ]
        for name, axioms, wt, cat in defaults:
            self.foundations[name] = FoundationAnchor(name=name, axioms=axioms, weight=wt, category=cat)

    def add_foundation(self, name: str, axioms: str, weight: float = 1.0, category: str = "CUSTOM") -> str:
        clean_name = name.strip().upper().replace(" ", "_")
        anchor = FoundationAnchor(name=clean_name, axioms=axioms.strip(), weight=max(0.1, min(2.0, weight)), category=category.upper())
        self.foundations[clean_name] = anchor
        self.save_foundations()
        return UI.success(f"Foundation [{clean_name}] anchored (Weight: {anchor.weight:.2f}x | Category: {anchor.category}).")

    def remove_foundation(self, name: str) -> str:
        clean_name = name.strip().upper().replace(" ", "_")
        if clean_name in self.foundations:
            del self.foundations[clean_name]
            self.save_foundations()
            return UI.success(f"Foundation [{clean_name}] decommissioned from registry.")
        return UI.warn(f"Foundation [{clean_name}] not found in registry.")

    def save_foundations(self):
        try:
            os.makedirs(self.vault_dir, exist_ok=True)
            data = {k: asdict(v) for k, v in self.foundations.items()}
            with open(self.foundations_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def load_foundations(self):
        if os.path.exists(self.foundations_file):
            try:
                with open(self.foundations_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for k, v in data.items():
                        self.foundations[k] = FoundationAnchor(**v)
            except Exception:
                pass

    def compute_congruence(self, content_text: str) -> Tuple[float, List[str]]:
        """Calculates semantic and lexical alignment of arbitrary text against all active foundations."""
        if not self.foundations or not content_text:
            return 0.5, ["Neutral baseline congruence"]
        words = set(re.findall(r"\w+", content_text.lower()))
        scores = []
        reports = []
        for name, anchor in self.foundations.items():
            f_words = set(re.findall(r"\w+", anchor.axioms.lower()))
            overlap = len(words.intersection(f_words))
            jaccard = overlap / max(1, len(words.union(f_words)))
            # Alignment boosted by foundation importance
            align = min(1.0, 0.45 + jaccard * 4.0) * anchor.weight
            scores.append(align)
            if overlap > 0:
                reports.append(f"{name}: {align:.2f} (matches: {overlap})")
        mean_score = float(np.mean(scores)) if (np is not None and scores) else 0.5
        return float(min(1.0, max(0.0, mean_score))), reports[:4]

class SocialWebHarvester:
    """
    High-resilience web and social media scraper/parser:
    - LinkedIn posts, articles, and author feeds
    - X / Twitter micro-posts, threads, and hashtags
    - Substack, Medium, news sites, and general web articles
    - Extracts title, article text, author, sentiment, and structural metadata
    """
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 HolosynHarvester/5.8"
    }

    @classmethod
    def scrape_url(cls, url: str) -> Dict[str, Any]:
        result = {
            "url": url,
            "domain": urllib.parse.urlparse(url).netloc.lower(),
            "title": "",
            "content": "",
            "author": "Unknown",
            "source_type": "WEB_ARTICLE",
            "status": "FETCH_FAILED"
        }
        try:
            resp = requests.get(url, headers=cls.HEADERS, timeout=6.0)
            if resp.status_code != 200:
                result["status"] = f"HTTP_{resp.status_code}"
                return result

            html = resp.text
            result["status"] = "SUCCESS"

            # 1. Extract Title
            title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
            if title_match:
                result["title"] = re.sub(r"\s+", " ", title_match.group(1)).strip()

            # 2. Extract OpenGraph Meta Tags
            og_desc = re.search(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\'](.*?)["\']', html, re.IGNORECASE)
            og_title = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']', html, re.IGNORECASE)
            if og_title and not result["title"]:
                result["title"] = og_title.group(1).strip()

            # 3. Detect Platform Specifics
            domain = result["domain"]
            if "linkedin.com" in domain:
                result["source_type"] = "LINKEDIN_POST" if "/posts/" in url or "/feed/" in url else "LINKEDIN_ARTICLE"
            elif "twitter.com" in domain or "x.com" in domain:
                result["source_type"] = "X_TWITTER_POST"
            elif "reddit.com" in domain:
                result["source_type"] = "REDDIT_THREAD"
            elif "medium.com" in domain or "substack.com" in domain:
                result["source_type"] = "EDITORIAL_ARTICLE"

            # 4. Extract Text Body (Strip HTML scripts, styles, and tags)
            clean_html = re.sub(r"<(script|style|svg|noscript)[^>]*>.*?</\1>", " ", html, flags=re.IGNORECASE | re.DOTALL)
            paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", clean_html, flags=re.IGNORECASE | re.DOTALL)
            extracted_text = " ".join([re.sub(r"<[^>]+>", "", p).strip() for p in paragraphs if len(p.strip()) > 20])
            
            if not extracted_text and og_desc:
                extracted_text = og_desc.group(1).strip()

            result["content"] = re.sub(r"\s+", " ", extracted_text)[:3500] or "No readable paragraph content detected."
            return result
        except Exception as err:
            result["status"] = f"ERROR: {err}"
            return result

    @classmethod
    def parse_social_text(cls, text: str, platform_hint: str = "GENERIC_SOCIAL") -> Dict[str, Any]:
        """Parses raw pasted social media text, hashtags, mentions, and metrics."""
        hashtags = re.findall(r"#\w+", text)
        mentions = re.findall(r"@\w+", text)
        clean_body = re.sub(r"[#@]\w+", "", text).strip()
        word_count = len(text.split())
        is_professional = any(w in text.lower() for w in ["hiring", "leadership", "growth", "launch", "proud to announce", "insights", "strategy", "enterprise"])

        return {
            "source_type": platform_hint.upper(),
            "hashtags": hashtags,
            "mentions": mentions,
            "word_count": word_count,
            "is_professional": is_professional,
            "content": text[:3500]
        }

class ResonatedTokenizer:
# ... existing code ...
class OmniSocialSenses:
    @staticmethod
    def parse_target(target: str) -> Tuple[str, str, float, bool, Optional[str]]:
        target = target.strip()
        lower_target = target.lower()

        # 1. Direct Web URLs (LinkedIn, Twitter/X, Reddit, Substack, News, Articles)
        if target.startswith("http://") or target.startswith("https://"):
            harvest = SocialWebHarvester.scrape_url(target)
            src_type = harvest["source_type"]
            snippet = harvest["title"] or harvest["content"][:120]
            if "LINKEDIN" in src_type:
                return "LINKEDIN_NODE", f"[LINKEDIN HARVEST]: {snippet} (URL: {target})", 2.2, True, target
            elif "X_TWITTER" in src_type:
                return "TWITTER_NODE", f"[TWITTER/X HARVEST]: {snippet} (URL: {target})", 2.0, True, target
            elif "REDDIT" in src_type:
                return "REDDIT_NODE", f"[REDDIT HARVEST]: {snippet} (URL: {target})", 1.8, True, target
            else:
                return "ARTICLE_NODE", f"[ARTICLE HARVEST]: {snippet} (URL: {target})", 1.9, True, target

        # 2. Pasted Social Media Text Anchors
        if any(w in lower_target for w in ["linkedin.com", "linkedin post", "proud to announce", "pleased to share", "we are hiring"]):
            return "LINKEDIN_NODE", f"[LINKEDIN CONTENT]: {target}", 2.1, False, None

        if any(w in lower_target for w in ["tweet", "retweet", "x.com", "twitter", "#tech", "#ai"]):
            return "TWITTER_NODE", f"[SOCIAL CONTENT]: {target}", 1.9, False, None

        if any(w in lower_target for w in ["starlink", "dishy", "spacex", "isl"]):
            return "STARLINK_NODE", f"[STARLINK TELEMETRY]: {target}", 2.1, False, target
        if any(w in lower_target for w in ["satellite", "tle", "apogee", "perigee", "kepler"]):
            return "SATELLITE_NODE", f"[SATELLITE INTAKE]: {target}", 2.0, False, target
        if "tekla_absolute_route.csv" in lower_target:
            return "LOGISTIC_NODE", "[LOGISTIC INTAKE]: tekla_absolute_route.csv acquired", 1.95, False, target

        try:
            safe_target = sanitize_filepath(target)
            if os.path.isdir(safe_target):
                return "DIR_NODE", f"[DIRECTORY INTAKE]: {os.path.basename(safe_target)}", 1.5, False, safe_target
            if os.path.exists(safe_target):
                fname = os.path.basename(safe_target)
                fsize = os.path.getsize(safe_target)
                if safe_target.endswith(('.pkl', '.pickle')):
                    return "PICKLE_NODE", f"[PICKLE INTAKE]: {fname} ({fsize} bytes)", 1.9, False, safe_target
                elif safe_target.endswith(('.pt', '.pth')):
                    return "WEIGHT_NODE", f"[TENSOR INTAKE]: {fname} ({fsize} bytes)", 1.8, False, safe_target
                else:
                    return "DOC_NODE", f"[DOCUMENT INTAKE]: {fname}", 1.2, False, safe_target
        except Exception:
            pass

        return "TEXT_NODE", target, 1.0, False, None

# ... existing code ...
class V90SocialMediaNewsManifoldObserver(BaseObserver):
    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> Assessment:
        t_low = text.lower()
        is_social = any(w in t_low for w in ["linkedin", "twitter", "tweet", "post", "news", "article", "viral", "sentiment"])
        mod_type = kwargs.get("mod", "UNKNOWN")
        boost = 0.25 if mod_type in ["LINKEDIN_NODE", "TWITTER_NODE", "REDDIT_NODE", "ARTICLE_NODE"] else 0.0
        score = float(min(1.0, max(0.1, 0.65 + boost + (0.15 if is_social else 0.0))))
        return Assessment(
            score=score, confidence=0.90, uncertainty=0.10,
            evidence=[f"Node Modality: {mod_type}", f"Social Indicators: {is_social}"],
            reasons=["Information cascade & social news sentiment manifold analysis"]
        )

class FoundationAlignmentObserver(BaseObserver):
    """
    Specialist observer measuring the congruence of current sensory inputs,
    web articles, or social media statements against the system's foundational anchors.
    """
    def __init__(self, foundation_manager: FoundationManager):
        self.foundation_mgr = foundation_manager

    def evaluate(self, s: float, sy: float, p: float, snn: Any, text: str = "", haptic_level: float = 0.0, **kwargs: Any) -> Assessment:
        congruence, reports = self.foundation_mgr.compute_congruence(text)
        f_count = len(self.foundation_mgr.foundations)
        return Assessment(
            score=congruence,
            confidence=0.92,
            uncertainty=0.08,
            evidence=[f"Active Foundations: {f_count}", f"Congruence Index: {congruence:.3f}"] + reports,
            reasons=["Pillar alignment between input telemetry and core Holosyn foundations"],
            proposed_action="Reinforce cognitive stability by grounding active hypotheses in active foundations."
        )

class V91VideoGraphicsContentManifoldParserObserver(BaseObserver):
# ... existing code ...
class HolosynDynamic:
    def __init__(self):
        self.observers: Dict[str, BaseObserver] = {}
        self.observer_weights: Dict[str, float] = {}
        self.forced_governor: Optional[str] = None
        self.cycle = 0
        self.system_gain = 1.0
        self.entropy_bias = 0.0

        self.working_mem = WorkingMemory()
        self.episodic_mem = EpisodicMemory()
        self.semantic_mem = SemanticMemory()
        self.ai_interface = UniversalAIInterface()
        self.foundation_manager = FoundationManager(vault_dir="./vaults")

        # Engines Initialization
        self.forge_engine = CoreForgeEngine(vault_dir="./vaults")
        self.threaded_swarm = ThreadedSwarmEngine(max_workers=4)
        self.plugin_engine = PluginLoaderEngine(self)
        self.swarm_learner = SwarmLearningEngine(self, self.forge_engine)
        self.autonomic_engine = AutonomicEngine(self, self.threaded_swarm)

        self.register_all_observers()

    def register_all_observers(self):
        """Registers all built-in, aerospace, math, science, and specialized swarm observers."""
        registry_manifest = [
            # Core Built-ins & Autonomics
            ("SNN", LiquidSnnReservoirObserver),
            ("LEG", ManifoldLegionObserver),
            ("ANN", AnnMetaCriticObserver),
            ("AGS", AgenticSwarmObserver),
            ("DSK", DeepSeekReasoningObserver),
            ("OPT", OptimizerManifoldObserver),
            ("ADG", lambda: AgenticDebuggerObserver(self.ai_interface)),
            ("LOG", LogisticalObserver),
            ("ENT", InformationEntropyObserver),
            ("FND", lambda: FoundationAlignmentObserver(self.foundation_manager)),
            # Aerospace & Deep Space
            ("SAT", SatelliteObserver),
            ("STR", StarlinkObserver),
            ("CUB", CubeSatSwarmObserver),
            ("DSP", DeepSpaceObserver),
# ... existing code ...
def print_holosyn_user_guide():
    print(UI.header("HOLOSYN SenAI: COMPLETE SYSTEM & PROMPT USER GUIDE"))
    print(f"""
{UI.BOLD}1. OVERVIEW & SWARM CAPABILITIES{UI.RESET}
   Holosyn SenAI is a high-volume resonant manifold controller integrating:
   • {UI.CYAN}Liquid SNN (SNN){UI.RESET}: Fast Leaky Integrate-and-Fire reservoir with leak decay.
   • {UI.CYAN}Manifold Legion (LEG){UI.RESET}: Stochastic Mixture-of-Experts for hundreds of small .pt models.
   • {UI.CYAN}ANN Meta-Critic (ANN){UI.RESET}: Continuous stability forecasting and teacher-student distillation.
   • {UI.CYAN}Agentic Swarm (AGS){UI.RESET}: Meta-Agent orchestrator managing SLM routing and entropy.
   • {UI.CYAN}Foundation Manager (FND){UI.RESET}: Core reference truths, immutable invariants, and congruence metrics.
   • {UI.CYAN}Social & Web Harvester{UI.RESET}: Real-time ingestion of LinkedIn, X/Twitter, and web articles.
   • {UI.CYAN}Simultaneous Threaded SLMs{UI.RESET}: Parallel threads running TinyLlama, Qwen 0.5, DeepSeek, MiniMax.
   • {UI.CYAN}Autonomic Feature (/auto){UI.RESET}: Self-driving background sensory pulsing and self-regulation.
   • {UI.CYAN}Dynamic Plugin Feature (/plugin){UI.RESET}: Hot-load and reload Python observer files.
   • {UI.CYAN}Swarm Learning (/swarm_learn){UI.RESET}: Background cooperative teacher-student distillation into ./vaults/.
   • {UI.CYAN}Grok & Instruct Engine{UI.RESET}: Conversational continuity, multi-turn prompts, instruct personas.

{UI.BOLD}2. INTERACTIVE COMMANDS & PROMPT CHATTING{UI.RESET}
   {UI.GREEN}<any plain text>{UI.RESET}      Directly communicate with Holosyn. Evaluates manifold resonance AND synthesizes a Grok instruct response!
   {UI.GREEN}<any http/https URL>{UI.RESET} Automatically scrapes and evaluates LinkedIn posts, X threads, or web articles!
   {UI.GREEN}/add <type> <payload>{UI.RESET} Universal add command (e.g. /add linkedin <url>, /add article <url>, /add foundation <name> <axioms>).
   {UI.GREEN}/add_foundation <name> <axioms>{UI.RESET} Anchor a new foundational truth into the system.
   {UI.GREEN}/foundations{UI.RESET}          List all registered cognitive foundations and weights.
   {UI.GREEN}/remove_foundation <name>{UI.RESET} Remove a foundation from the registry.
   {UI.GREEN}/article <url_or_text>{UI.RESET} Harvest and analyze a web article or blog post.
   {UI.GREEN}/social <url_or_text>{UI.RESET}  Harvest and evaluate LinkedIn, X, or Reddit posts.
   {UI.GREEN}/auto <on|off|status>{UI.RESET} Toggle autonomous background self-driving manifold loop.
   {UI.GREEN}/swarm_exec <prompt>{UI.RESET} Run simultaneous parallel threaded execution (TinyLlama, Qwen 0.5, DeepSeek, MiniMax).
   {UI.GREEN}/swarm_learn <start|stop|step|status>{UI.RESET} Cooperative swarm multi-agent distillation and training.
   {UI.GREEN}/plugin <path_to.py|dir>{UI.RESET} Hot-load dynamic Python observer plugins from disk.
   {UI.GREEN}/plugins{UI.RESET}             List all currently loaded external plugins.
   {UI.GREEN}/grok <prompt>{UI.RESET}       Direct query to Grok intelligence engine with active persona reasoning.
   {UI.GREEN}/persona <name>{UI.RESET}      Switch instruct persona: LOVE_LOGIC, TRUTH_SEEKER, ANALYTICAL_ENGINEER, COSMIC_ORACLE, STOCHASTIC_LOGICIAN.
   {UI.GREEN}/dashboard{UI.RESET}           Display full diagnostic status, observer counts, VRAM, and health.
   {UI.GREEN}/doctor{UI.RESET}              Run automated self-check and let the Agent Swarm debug anomalies.
   {UI.GREEN}/models{UI.RESET}              List available Small Language Models.
   {UI.GREEN}/model <key>{UI.RESET}         Switch subconscious SLM (e.g. /model deepseek, /model qwen1.5, /model minimax).
   {UI.GREEN}/forge [bias]{UI.RESET}        Forge high-volume micro-manifolds into ./vaults/ (or /forge all).
   {UI.GREEN}/scan{UI.RESET}                Scan Downloads, holosynC, and vaults for .pt and .pkl artifacts.
""")

# ... existing code ...
def start_cli():
    print(UI.header("HOLOSYN SenAI: RESONATED SWARM, GROK INSTRUCT & ARTIFACT VAULT CLI"))
    print(UI.info("Type /help for operational guide, or type any prompt to converse with Grok and evaluate the manifold."))

    nexus = HolosynDynamic()
    forge_engine = nexus.forge_engine
    tokenizer = ResonatedTokenizer()

    # Ingest startup CLI file arguments
    if len(sys.argv) > 1:
        print(UI.info(f"Command-line file arguments detected ({len(sys.argv)-1} item(s)). Ingesting..."))
        for arg in sys.argv[1:]:
            clean_arg = arg.strip()
            if os.path.exists(clean_arg):
                if clean_arg.endswith(".py"):
                    ok, msg = nexus.plugin_engine.load_plugin_file(clean_arg)
                    print(UI.success(msg) if ok else UI.warn(msg))
                else:
                    info = ArtifactVaultManager.inspect_artifact(clean_arg)
                    print(UI.success(f"Ingested Startup Artifact: {info['filename']} | Status: {info['status']} | Params: {info.get('total_params', 0)}"))
                    if clean_arg.endswith(('.pt', '.pth')) and "LEG" in nexus.observers:
                        if clean_arg not in nexus.observers["LEG"].manifold_registry:
                            nexus.observers["LEG"].manifold_registry.append(clean_arg)
            else:
                nexus.process(clean_arg)

    while True:
        try:
            auto_status = f"{UI.GREEN}[AUTO ON]{UI.RESET} " if nexus.autonomic_engine.is_running else ""
            cmd = input(f"\n{auto_status}{UI.BOLD}{UI.CYAN}[Holosyn Node // {nexus.ai_interface.active_persona}] ⚡ > {UI.RESET}").strip()
            if not cmd:
                break

            if cmd == "/help":
                print_holosyn_user_guide()
                continue

            if cmd in ["/foundations", "/list_foundations"]:
                print(UI.header(f"ACTIVE COGNITIVE FOUNDATIONS ({len(nexus.foundation_manager.foundations)})"))
                for name, anchor in nexus.foundation_manager.foundations.items():
                    print(f" • {UI.BOLD}{UI.CYAN}{name}{UI.RESET} [{anchor.category}] (Weight: {anchor.weight:.2f}x)")
                    print(f"   ↳ {UI.DIM}{anchor.axioms}{UI.RESET}")
                continue

            if cmd in ["/dashboard", "/status"]:
                print(UI.header("HOLOSYN ACTIVE DIAGNOSTIC DASHBOARD"))
                print(f" ├─ Cycle Count: {nexus.cycle} | System Gain: {nexus.system_gain:.2f} | Entropy Bias: {nexus.entropy_bias:+.2f}")
                print(f" ├─ Active Persona: {nexus.ai_interface.active_persona}")
                print(f" ├─ Registered Foundations: {len(nexus.foundation_manager.foundations)} anchored truths")
                print(f" ├─ Autonomic Self-Driving Engine: {'ACTIVE (running in background)' if nexus.autonomic_engine.is_running else 'IDLE (/auto on)'}")
                print(f" ├─ Swarm Cooperative Learning: {'TRAINING (active)' if nexus.swarm_learner.is_active else 'IDLE (/swarm_learn start)'} (Epochs: {nexus.swarm_learner.epochs_completed}, Loss: {nexus.swarm_learner.last_loss:.5f})")
                print(f" ├─ External Plugins Loaded: {len(nexus.plugin_engine.loaded_plugins)} modules")
                print(f" ├─ Registered Observers ({len(nexus.observers)}): {', '.join(list(nexus.observers.keys())[:18])}...")
                engine = HiveModelEngine()
                print(f" ├─ Hive Models Discovered: {list(engine.model_paths.keys())}")
                print(f" ├─ Active Subconscious SLM: {nexus.ai_interface.local_subconscious.current_model_name}")
                legion_obs = nexus.observers.get("LEG")
                legion_count = len(legion_obs.manifold_registry) if hasattr(legion_obs, "manifold_registry") else 0
                print(f" ├─ Legion Vault Manifolds: {legion_count} files mapped")
                print(f" └─ Debugger Log Entries: {len(nexus.ai_interface.debugger.incident_log)} resolved incidents")
                continue

            if cmd == "/history":
                print(UI.header("RECENT CONVERSATION CONTEXT WINDOW"))
                for item in nexus.ai_interface.chat_history[-6:]:
                    prefix = f"{UI.GREEN}User:{UI.RESET}" if item["role"] == "user" else f"{UI.CYAN}Grok:{UI.RESET}"
                    print(f" {prefix} {item['content'][:100]}...")
                continue

            if cmd == "/doctor":
                print(UI.header("RUNNING COMPREHENSIVE SWARM SELF-DIAGNOSIS"))
                print(UI.info(f"Stress-testing all {len(nexus.observers)} registered observers..."))
                faults_found = 0
                for k, obs in list(nexus.observers.items()):
                    try:
                        res = safe_evaluate_observer(obs, s=0.5, sy=0.5, p=0.5, snn=[0.5, 0.5], text="Self-healing test")
                        if math.isnan(res.score) or math.isinf(res.score):
                            raise ValueError(f"Observer {k} yielded NaN/Inf score")
                    except Exception as err:
                        faults_found += 1
                        rep = nexus.ai_interface.debugger.diagnose_and_repair(f"Observer {k}", err, {})
                        print(f"   {UI.YELLOW}⚠{UI.RESET} Observer [{k}]: Auto-Repaired by {rep['diagnosing_agent']} -> {rep['action']}")
                print(UI.success(f"Self-diagnosis complete across {len(nexus.observers)} observers. {faults_found} anomaly/anomalies intercepted."))
                continue

            # Command dispatching
            if cmd.startswith("/"):
                parts = cmd.split(" ", 1)
                base_cmd = parts[0].lower()
                arg1 = parts[1] if len(parts) > 1 else ""

                if base_cmd in ["/add", "/add_content"]:
                    sub_parts = arg1.split(" ", 1)
                    add_type = sub_parts[0].lower() if len(sub_parts) > 0 else ""
                    payload = sub_parts[1] if len(sub_parts) > 1 else ""

                    if add_type in ["foundation", "fnd"]:
                        f_tokens = payload.split(" ", 1)
                        if len(f_tokens) < 2:
                            print(UI.warn("Usage: /add foundation <NAME> <Axiom or principle text>"))
                            continue
                        f_name, f_axioms = f_tokens[0], f_tokens[1]
                        print(nexus.foundation_manager.add_foundation(f_name, f_axioms))
                        continue
                    elif add_type in ["linkedin", "article", "social", "web"]:
                        target_url = payload or arg1
                        print(UI.info(f"Harvesting {add_type.upper()} target: {target_url}"))
                        v, uni, gov, scores = nexus.process(target_url)
                        print(UI.success(f"Assimilated {add_type.upper()} into manifold. Governor: {gov} | Congruence: {scores.get('FND', 0.5):.3f}"))
                        continue
                    else:
                        print(UI.warn("Usage: /add <foundation|linkedin|article|social> <payload_or_url>"))
                        continue

                elif base_cmd in ["/add_foundation", "/foundation_add"]:
                    f_tokens = arg1.split(" ", 1)
                    if len(f_tokens) < 2:
                        print(UI.warn("Usage: /add_foundation <NAME> <Axiom or principle text>"))
                        continue
                    f_name, f_axioms = f_tokens[0], f_tokens[1]
                    print(nexus.foundation_manager.add_foundation(f_name, f_axioms))
                    continue

                elif base_cmd in ["/remove_foundation", "/delete_foundation"]:
                    if not arg1:
                        print(UI.warn("Usage: /remove_foundation <NAME>"))
                        continue
                    print(nexus.foundation_manager.remove_foundation(arg1))
                    continue

                elif base_cmd in ["/article", "/add_article", "/web"]:
                    if not arg1:
                        print(UI.warn("Usage: /article <URL or pasted article text>"))
                        continue
                    print(UI.info(f"Parsing web article: {arg1[:60]}..."))
                    v, uni, gov, scores = nexus.process(arg1)
                    print(UI.success(f"Web Article Processed. Governor: {gov} | Foundation Congruence: {scores.get('FND', 0.5):.3f}"))
                    continue

                elif base_cmd in ["/social", "/linkedin", "/twitter"]:
                    if not arg1:
                        print(UI.warn("Usage: /social <URL or pasted post text>"))
                        continue
                    print(UI.info(f"Harvesting social media signal: {arg1[:60]}..."))
                    v, uni, gov, scores = nexus.process(arg1)
                    print(UI.success(f"Social Media Stream Processed. Governor: {gov} | S90 Score: {scores.get('S90', 0.5):.3f} | Congruence: {scores.get('FND', 0.5):.3f}"))
                    continue

                elif base_cmd in ["/auto", "/autonomic"]:
# ... existing code ...