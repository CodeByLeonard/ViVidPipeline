from proc.sre.audio_matching.modules.corrections import load_corrections
from proc.sre.audio_matching.modules.matcher import get_rematches
from proc.sre.audio_matching.modules.rebuild import rebuild_original
from proc.sre.audio_matching.super_segments import load_super_segments


def rematch():
    corrections = load_corrections()
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

    from proc.sre.audio_matching.extracter import extract
    extract()

    from proc.sre.audio_matching.modules.pyscenedetect import clip_cut_detect
    clip_cut_detect()

    from proc.sre.audio_matching.modules.matcher import get_matches
    get_matches()

    from proc.sre.audio_matching.super_segments import fill_super_segments
    fill_super_segments()

    return load_super_segments()
    # THE GREAT DIVIDE!



    from proc.sre.audio_matching.modules.plot import super_segments_status
    super_segments_status(super_segments)

    rebuild_original(super_segments)

    return

if __name__ == "__main__":
    main()
