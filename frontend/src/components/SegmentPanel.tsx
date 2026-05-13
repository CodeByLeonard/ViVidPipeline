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

    const container = "" //rounded-2xl border border-dashed border-zinc-700 bg-zinc-900/30
    const button = "py-2 border border-zinc-700 text-zinc-200 hover:bg-zinc-700/40 transition"
    const add_segment_button = `${button} px-4 rounded-xl border-dashed bg-zinc-800/50 disabled:opacity-40`
    const set_button = `${button} px-3 rounded-lg bg-zinc-800/40 text-sm`
    const time = "flex-1 rounded-lg border border-zinc-800 bg-black/20 px-3 py-2 text-zinc-300 text-sm"

    return (
        <div className={container}>
            <div className="flex items-center justify-between mb-5">
                <div>
                    <div className="text-zinc-200 font-semibold">Segments</div>
                    <div className="text-sm text-zinc-500 mt-1">Create synchronization anchors</div>
                </div>
                <button onClick={addSegment} disabled={segments.length >= 6} className={add_segment_button}>
                    + Add Segment
                </button>
            </div>

            <div className="grid grid-cols-1 gap-4">
                {segments.map((segment, index) => (
                    <div key={segment.id} className="rounded-xl border border-dashed border-zinc-700 bg-black/20 p-4">
                        <div className="text-zinc-300 font-medium mb-4">
                            Segment {index + 1}
                        </div>

                        <div className="grid grid-cols-2 gap-4">

                            {/* START */}
                            <div>
                                <div className="text-xs text-zinc-500 mb-2">Start</div>
                                <div className="flex gap-3">
                                    <button onClick={() => setStart(segment.id)} className={set_button}>Set Start</button>
                                    <div className={time}>{formatTime(segment.start)}</div>
                                </div>
                            </div>

                            {/* END */}
                            <div>
                                <div className="text-xs text-zinc-500 mb-2">End</div>
                                <div className="flex gap-3">
                                    <button onClick={() => setEnd(segment.id)} className={set_button}>Set End</button>
                                    <div className={time}>{formatTime(segment.end)}</div>
                                </div>
                            </div>

                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}