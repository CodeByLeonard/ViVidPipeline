from proc.sre.audio_matching.modules.corrections import load_corrections
from proc.sre.audio_matching.modules.matcher import get_rematches
from proc.sre.audio_matching.modules.rebuild import rebuild_original

def rematch():
    corrections = load_corrections()
    original_mono_filepath = "sessions/sre/working/extraction/original.mp3"
    clip_mono_filepath = "sessions/sre/working/extraction/clip.mp3"
    from proc.sre.audio_matching.modules.source import set_scope
    original_source, clip_source, scope = set_scope(original_mono_filepath, clip_mono_filepath)
    print(f"[RE-MATCHER] Initiated Rematch! Manual Corrections:")
    for index, correction in enumerate(corrections):
        print(f"Correction {index}: \n{correction}")
        get_rematches(clip_source, scope, corrections.match_corrections)

    print("\n")
    super_segments = []
    from proc.sre.audio_matching.modules.source import fill_super_segments
    fill_super_segments(super_segments)
    from proc.sre.audio_matching.modules.plot import super_segments_status
    super_segments_status(super_segments, clip_source, scope)
    rebuild_original(super_segments, scope, original_mono_filepath)
    return


def main():
    print("\n")

    cutoff = 0.2
    match_clip_duration = 2 + cutoff
    end_find_duration = 1
    next_find_duration = 1

    speed_preset = 0.97274376 * 0.99  # = 0.9630163224
    language = "eng"
    channel = "FC"
    original_mono_filepath = "sessions/sre/working/extraction/original.mp3"
    clip_mono_filepath = "sessions/sre/working/extraction/clip.mp3"
    from proc.sre.audio_matching.modules.extraction import initial_extraction
    initial_extraction(original_mono_filepath, clip_mono_filepath, speed_preset, language, channel)

    from proc.sre.audio_matching.modules.pyscenedetect import clip_cut_detect
    clip_cut_detect()

    from proc.sre.audio_matching.modules.source import set_scope
    original_source, clip_source, scope = set_scope(original_mono_filepath, clip_mono_filepath)

    from proc.sre.audio_matching.modules.matcher import get_matches
    get_matches(clip_source, scope)

    super_segments = []
    from proc.sre.audio_matching.modules.source import fill_super_segments
    fill_super_segments(super_segments)

    from proc.sre.audio_matching.modules.plot import super_segments_status
    super_segments_status(super_segments, clip_source, scope)

    rebuild_original(super_segments, scope, original_mono_filepath)

    return

if __name__ == "__main__":
    main()
