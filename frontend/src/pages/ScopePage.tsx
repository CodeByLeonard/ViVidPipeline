import {type RefObject, useRef, useState} from "react";
import ScopeVideoPanel from "../components/ScopeVideoPanel";
import SegmentPanel from "../components/SegmentPanel";

export type Segment = {
    id: number
    start: number | null
    end: number | null
}

export default function ScopePage() {
    const originalVideoRef = useRef<HTMLVideoElement>(null);
    const [segments, setSegments] = useState<Segment[]>([]);

    const addSegment = () => {
        if (segments.length >= 6) return;
        setSegments(prev => [...prev, { id: Date.now(), start: null, end: null }]);
    };

    const setStart = (id: number) => {
        if (!originalVideoRef.current) return;
        const current = originalVideoRef.current.currentTime;
        setSegments(prev =>
            prev.map(segment =>
                segment.id === id
                    ? { ...segment, start: current }
                    : segment
            )
        );
    };

    const setEnd = (id: number) => {
        if (!originalVideoRef.current) return;
        const current = originalVideoRef.current.currentTime;
        setSegments(prev =>
            prev.map(segment =>
                segment.id === id
                    ? { ...segment, end: current }
                    : segment
            )
        );
    };

    const onFinish = async () => {
        for (const segment of segments) {
            await fetch(`http://0.0.0.0:8000/pipeline/scope/${segment.start}`, {method: "POST"})
        }
    }

    return (
        <div className="w-full h-full flex items-center justify-center p-8">
            <div className="
                w-[96%] h-[92%]
                rounded-2xl
                border border-dashed border-zinc-700
                bg-white/3 backdrop-blur-xl
                shadow-[0_8px_40px_rgba(0,0,0,0.35)]
                flex overflow-hidden
            ">
                <YouTubeSource />
                <OriginalMediaSource
                    originalVideoRef={originalVideoRef}
                    segments={segments}
                    addSegment={addSegment}
                    setStart={setStart}
                    setEnd={setEnd}
                    onFinish={onFinish}
                />
            </div>
        </div>
    );
}

function OriginalMediaSource(
    {originalVideoRef, segments, addSegment, setStart, setEnd, onFinish}:
    {originalVideoRef: RefObject<HTMLVideoElement | null>, segments: Segment[],
        addSegment: () => void, setStart: (id: number) => void, setEnd: (id: number) => void, onFinish: () => void }
) {
    return (
        <div className="flex-1 p-6 flex gap-6 overflow-hidden">
            <div className="flex-[1.8] min-h-0">
                <ScopeVideoPanel title="Original Media Source" src="http://localhost:8000/cache/original.mkv" videoRef={originalVideoRef}/>
            </div>

            <div className="flex-1 min-h-0 flex flex-col">
                <div className="flex-1 min-h-0 overflow-y-auto rounded-2xl border border-dashed border-zinc-700 bg-zinc-900/30 p-5">
                    <SegmentPanel segments={segments} addSegment={addSegment} setStart={setStart} setEnd={setEnd}/>
                </div>

                <div className="mt-4 flex gap-3 pt-4 border-t border-zinc-800">
                    <button onClick={onFinish} className="
                            flex-1 px-4 py-3 rounded-xl transition border border-dashed
                            border-cyan-700 bg-cyan-500/10 text-cyan-200 hover:bg-cyan-500/20"
                    >Finish and Map</button>
                </div>
            </div>
        </div>
    )
}

function YouTubeSource() {
    return (
        <div className="w-[25%] border-r border-zinc-800 p-6">
            <ScopeVideoPanel title="YouTube Reference" src="http://localhost:8000/cache/clip_Eon2EqOfGbs.mp4" compact/>
        </div>
    )
}