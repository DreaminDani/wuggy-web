import os
import time
import argparse
import fractions
from typing import Dict, Optional

from wuggy import WuggyGenerator

environment = os.environ.get("ENV", "development")
if environment == "production":
    print("Wuggy Server is set to production mode. All supported language plugins will be loaded.")
    language_plugins_to_load = WuggyGenerator.supported_language_plugins.keys()
else:
    print("Wuggy Server is set to development mode. Only a subset of language plugins will be loaded.")
    language_plugins_to_load = ["orthographic_english"]
    # Uncomment if your language plugin is missing
    # wuggy_downloader = WuggyGenerator()
    # wuggy_downloader.download_language_plugin("orthographic_english", True)

wuggy_generators: Dict[str, WuggyGenerator] = {}
for language_plugin_name in language_plugins_to_load:
    print(f"Loading language plugin {language_plugin_name}")
    generator = WuggyGenerator()
    generator.load(language_plugin_name)
    wuggy_generators[language_plugin_name] = generator

print(
    f"Starting Wuggy server with the following loaded language plugins: {wuggy_generators.keys()}")

def generate_simple_cli(reference_sequence: str, language_plugin: str = "orthographic_english", ncandidates: int = 10):
    """
    Example usage: python main.py --referenceSequence trumpet --ncandidates 5
    """
    if language_plugin in wuggy_generators:
        wuggy_generator = wuggy_generators[language_plugin]
        pseudowords = []
        # for sequence in wuggy_generator.generate_classic([reference_sequence]):
        for sequence in wuggy_generator.generate_classic([reference_sequence],
    ncandidates_per_sequence=ncandidates, max_search_time_per_sequence=25, match_letter_length=True, subsyllabic_segment_overlap_ratio=fractions.Fraction(2, 3)):
            pseudowords.append(sequence["pseudoword"])
        return { "word": reference_sequence, "matches": pseudowords }
    else:
        print(f"Language plugin {language_plugin} not found.")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate pseudowords using Wuggy.")
    parser.add_argument("--referenceSequence", type=str, required=True, help="The reference sequence to generate pseudowords for.")
    parser.add_argument("--languagePlugin", type=str, default="orthographic_english", help="The language plugin to use.")
    parser.add_argument("--ncandidates", type=int, default=10, help="The desired number of pseudowords to generate.")
    
    args = parser.parse_args()
    
    result = generate_simple_cli(args.referenceSequence, args.languagePlugin, args.ncandidates)
    if result:
        print(result)