import type {RefObject} from "react";

type ScopeVideoPanelProps = {
    title: string
    src: string
    compact?: boolean
    videoRef?: RefObject<HTMLVideoElement | null>
}

export default function ScopeVideoPanel(
    {title, src, compact = false, videoRef}: ScopeVideoPanelProps
) {
    return (
        <div className="
            h-full flex flex-col
            rounded-2xl
            border border-dashed border-white/10
            bg-white/3 backdrop-blur-xl
            overflow-hidden
        ">

            {/* HEADER */}
            <div className="px-5 py-4 border-b border-zinc-800">
                <div className="text-zinc-200 font-semibold">
                    {title}
                </div>
            </div>

            {/* VIDEO */}
            <div className={`
                flex-1
                bg-black/40
                overflow-hidden
                flex items-center justify-center
                ${compact ? "max-h-[650px]" : ""}
            `}>
                <video
                    ref={videoRef}
                    src={src}
                    controls
                    className="w-full h-full object-contain"
                />
            </div>

        </div>
    );
}