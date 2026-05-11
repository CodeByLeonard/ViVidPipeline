import type {Segment} from "../pages/ScopePage";

type SegmentPanelProps = {
    segments: Segment[]

    addSegment: () => void
    setStart: (id: number) => void
    setEnd: (id: number) => void
}

export default function SegmentPanel({
    segments,
    addSegment,
    setStart,
    setEnd
}: SegmentPanelProps) {
    const formatTime = (time: number | null) => {
        if (time === null) return "--:--.--";

        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60);
        const ms = Math.floor((time % 1) * 100);

        return `${minutes.toString().padStart(2, "0")}:${seconds
            .toString()
            .padStart(2, "0")}.${ms.toString().padStart(2, "0")}`;
    };

    return (
        <div className="
            rounded-2xl
            border border-dashed border-zinc-700
            bg-zinc-900/30
            p-5
        ">

            {/* HEADER */}
            <div className="flex items-center justify-between mb-5">

                <div>
                    <div className="text-zinc-200 font-semibold">
                        Segments
                    </div>

                    <div className="text-sm text-zinc-500 mt-1">
                        Create synchronization anchors
                    </div>
                </div>

                <button
                    onClick={addSegment}
                    disabled={segments.length >= 4}
                    className="
                        px-4 py-2 rounded-xl
                        border border-dashed border-zinc-700
                        bg-zinc-800/50
                        text-zinc-200
                        hover:bg-zinc-700/40
                        transition
                        disabled:opacity-40
                    "
                >
                    + Add Segment
                </button>

            </div>

            {/* SEGMENTS */}
            <div className="grid grid-cols-2 gap-4">

                {segments.map((segment, index) => (
                    <div
                        key={segment.id}
                        className="
                            rounded-xl
                            border border-dashed border-zinc-700
                            bg-black/20
                            p-4
                        "
                    >

                        <div className="text-zinc-300 font-medium mb-4">
                            Segment {index + 1}
                        </div>

                        {/* START */}
                        <div className="mb-4">

                            <div className="text-xs text-zinc-500 mb-2">
                                Start
                            </div>

                            <div className="flex gap-3">

                                <button
                                    onClick={() => setStart(segment.id)}
                                    className="
                                        px-3 py-2 rounded-lg
                                        border border-zinc-700
                                        bg-zinc-800/40
                                        text-zinc-200 text-sm
                                        hover:bg-zinc-700/40
                                        transition
                                    "
                                >
                                    Set Start
                                </button>

                                <div className="
                                    flex-1 rounded-lg
                                    border border-zinc-800
                                    bg-black/20
                                    px-3 py-2
                                    text-zinc-300 text-sm
                                ">
                                    {formatTime(segment.start)}
                                </div>

                            </div>

                        </div>

                        {/* END */}
                        <div>

                            <div className="text-xs text-zinc-500 mb-2">
                                End
                            </div>

                            <div className="flex gap-3">

                                <button
                                    onClick={() => setEnd(segment.id)}
                                    className="
                                        px-3 py-2 rounded-lg
                                        border border-zinc-700
                                        bg-zinc-800/40
                                        text-zinc-200 text-sm
                                        hover:bg-zinc-700/40
                                        transition
                                    "
                                >
                                    Set End
                                </button>

                                <div className="
                                    flex-1 rounded-lg
                                    border border-zinc-800
                                    bg-black/20
                                    px-3 py-2
                                    text-zinc-300 text-sm
                                ">
                                    {formatTime(segment.end)}
                                </div>

                            </div>

                        </div>

                    </div>
                ))}

            </div>

        </div>
    );
}