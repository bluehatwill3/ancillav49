import os
import torch
import logging
from __main__ import BaseObserver # Assuming standard Holosyn import

# Configure local logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HarvestManager")

class HarvestManagerObserver(BaseObserver):
    """
    MASTER HARVESTER: Automatically registers all provided vaults and 
    core weights into the active Holosyn Nexus.
    """
    def __init__(self):
        super().__init__()
        self.target_paths = [
            "/home/devcbloom/Downloads",
            "/home/devcbloom/Desktop",
            "/home/devcbloom/Documents",
            "/home/devcbloom/Documents/teKlaNF",
            "/home/devcbloom/Documents/teKlaNF/latest_manifold.pt",
            "/home/devcbloom/Documents/teKlaNF/manifold_unbound.pt",
            "/home/devcbloom/Documents/teKlaNF/peak_manifold.pt",
            "/home/devcbloom/Documents/tsp/best_manifold(1).pt",
            "/home/devcbloom/Documents/tsp/best_manifold(2).pt",
            "/home/devcbloom/Documents/tsp/latest_manifold(2).pt",
            "/home/devcbloom/Documents/V60_Artifacts/daughter_integrator.pt",
            "/home/devcbloom/Documents/V60_Artifacts/son_projector.pt",
            "/home/devcbloom/Documents/V105_Data_Core/weights/best_manifold.pt",
            "/home/devcbloom/Documents/V110_Artifacts/manifold_unbound.pt",
            "/home/devcbloom/Documents/V115_Data_Core/weights/best_manifold.pt",
            "/home/devcbloom/Documents/V120_Sovereign_Core/weights/best_manifold.pt",
            "/home/devcbloom/Documents/V125_Awakened_Core/weights/best_manifold.pt",
            "/home/devcbloom/Documents/V130_Archive_Core/weights/peak_resonant_manifold.pt",
            "/home/devcbloom/Documents/V145_Bridge_Core/weights/peak_manifold.pt",
            "/home/devcbloom/Documents/V145_Bridge_Core/weights/latest_manifold.pt",
            "/home/devcbloom/Documents/V150_Sovereign_Core/weights",
            "/home/devcbloom/Documents/V150_Sovereign_Core/weights/latest_manifold.pt",
            "/home/devcbloom/Documents/Intellibloomenv/starsmart",
            "/home/devcbloom/Documents/Intellibloomenv/starsmart/HoloSyn_Foundation_Export/teacher/foundation_expert.pth",
            "/home/devcbloom/Documents/Intellibloomenv/starsmart/HoloSyn_Phase18_Export/projector_weights",
            "/home/devcbloom/Documents/Intellibloomenv/starsmart/archive_extracted_ui/Archive/holosyn_heads.torchscript.pt",
            "/home/devcbloom/Documents/Intellibloomenv/starsmart/willow_v17_assimilated.pt",
            "/home/devcbloom/Documents/Intellibloomenv/starsmart/willow_v14_dynamic.pt",
            "/home/devcbloom/Documents/Intellibloomenv/starsmart/qstar_v21_projector_distilled.pt",
            "/home/devcbloom/Documents/Intellibloomenv/starsmart/holosyn_v18_integrator.pt",
            "/home/devcbloom/Documents/Intellibloomenv/Google model output/best_manifold_v2.pt",
            "/home/devcbloom/Documents/Intellibloomenv/colab_export/wanalytics_host_mate_v14.pt",
            "/home/devcbloom/Documents/Intellibloomenv/colab_export/holosyn_v18_master_distilled.pt"
        ]
        self.harvest_all()

    def harvest_all(self):
        """Iterates through targets and attempts to load assets."""
        logger.info("🔨 Harvesting initialized...")
        for path in set(self.target_paths): # Use set to remove duplicates
            if not os.path.exists(path):
                logger.warning(f"  ⚠️ Path not found, skipping: {path}")
                continue
            
            if os.path.isdir(path):
                self._harvest_directory(path)
            else:
                self._load_asset(path)

    def _harvest_directory(self, dir_path):
        """Scans directories for compatible .pt or .pth files."""
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(('.pt', '.pth', '.torchscript.pt')):
                    self._load_asset(os.path.join(root, file))

    def _load_asset(self, file_path):
        """Attemps to load the asset into the Holosyn Forge."""
        try:
            logger.info(f"   📦 Loading: {os.path.basename(file_path)}")
            # If your system uses a global 'nexus' or 'forge', call it here
            # Example: from core_forge import forge_core
            # forge_core(file_path, "HARVESTED_CORE") 
            
            # Placeholder for direct torch loading if not using forge_core
            # torch.load(file_path)
            
        except Exception as e:
            logger.error(f"   ❌ Failed to load {file_path}: {e}")

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        return 0.5 # Neutral observer