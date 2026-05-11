import {type RefObject, useRef} from "react";

export function VideoPreviewCard({title, src}: {title: string; src: string}) {
    return (
        <div className="flex-1 flex flex-col mt-4">
            <div className="text-sm text-zinc-400 mb-2">{title}</div>
            <VideoPlayer src={src} />
        </div>
    );
}

export function VideoPlayer({ src }: { src: string }) {
    const videoRef = useRef<HTMLVideoElement>(null);
    return <Video videoRef={videoRef} src={src}/>
}

function Video({videoRef, src}: {videoRef: RefObject<HTMLVideoElement | null>, src: string})
{
    const frameClassName = "w-full h-128 {/*h-[460px]*/} border border-dashed border-zinc-700 bg-zinc-900/40"
    const videoClassName = "w-full h-full object-contain"
    return (
        <div className={frameClassName + "overflow-hidden flex items-center justify-center"}>
            <video ref={videoRef} src={src} className={videoClassName} controls={true}/>
        </div>
    )
}