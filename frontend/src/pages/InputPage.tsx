import {type RefObject, useRef, useState} from "react";
import {VideoPreviewCard} from "../components/VideoPlayer.tsx";
import type {DragEvent, ChangeEventHandler, ChangeEvent} from "react";
import {downloadYouTubeVideo} from "../modules/BackendHelper.tsx";
import {useAppContext} from "../context/AppContext.tsx";

const column = "rounded-2xl border border-dashed border-white/10 bg-white/3 backdrop-blur-xl p-6 flex flex-col"

export default function InputPage(
) {
    const { file, setFile  } = useAppContext()
    const container_outer = "w-full h-full flex items-center justify-center p-10"
    const container_inner = "w-[96%] h-[92%] flex gap-8"
    return (
        <div className={container_outer}>
            <div className={container_inner}>
                <YouTubeCard/>
                <OriginalMediaCard file={file} setFile={setFile} />
            </div>
        </div>
    )
}

function YouTubeCard() {
    const { youtubeId, setYoutubeId} = useAppContext()
    const [videoSrc, setVideoSrc] = useState<string>("")
    const [loading, setLoading] = useState(false)
    return (
        <div className={`${column} flex-1`}>
            <Title title="YouTube Source Eon2EqOfGbs" subtitle="Paste a Shorts or video ID (not the URL)"/>
            <div className="flex gap-3">
                <InputID value={youtubeId} onChange={(e) => setYoutubeId(e.target.value)}/>
                <DownloadButton onClick={() => downloadYouTubeVideo({youtubeId, setLoading, setVideoSrc})} loading={loading}/>
            </div>
            <VideoPreviewCard title="Downloaded video preview - downloaded by backend!" src={videoSrc} />
        </div>
    )
}

function OriginalMediaCard({file, setFile}: {file: File | null, setFile: (file: File | null) => void}) {
    const [videoUrl, setVideoUrl] = useState<string>("")
    const handleFile = (file: File) => {
        setFile(file)
        const url = URL.createObjectURL(file)
        setVideoUrl(url)
    }
    return (
        <div className={`${column} flex-[1.6]`}>
            <div className="flex items-start justify-between mb-4">
                <div> <Title title="Original Media" subtitle="Movie / TV / full-length source"/> </div>
                <DropZone onFileSelect={handleFile} selectedFile={file}/>
            </div>
            <VideoPreviewCard title="Original preview - local preview only!" src={videoUrl} />
        </div>
    )
}

function DropZone({ onFileSelect, selectedFile }: { onFileSelect: (file: File) => void, selectedFile: File | null }) {
    const handleDrop = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault()
        const file = e.dataTransfer.files?.[0]
        if (!file) return
        onFileSelect(file)
    }

    const handleInput = (e: ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (!file) return
        onFileSelect(file)
    }

    const fileInputReference: RefObject<HTMLInputElement | null> = useRef<HTMLInputElement>(null)
    const dropZoneContainer = "w-180 h-26.25 rounded-xl border border-dashed border-zinc-700 bg-zinc-900/40"
    const dropZoneAlign = "transition flex flex-col items-center justify-center gap-3 relative overflow-hidden cursor-pointer"

    return (
        <div onDrop={handleDrop}
             onClick={() => fileInputReference.current?.click()}
             onDragOver={(e: DragEvent<HTMLDivElement>) => e.preventDefault()}
             className={dropZoneContainer + dropZoneAlign}>
            <input ref={fileInputReference} type="file" className="hidden" onChange={handleInput}/>
            <div className="text-center text-xl"> {selectedFile ? selectedFile.name : "Click or drop file here"} </div>
        </div>
    )
}

function Title({title, subtitle}: {title: string, subtitle: string }) {
    const titleClassName = "text-xl font-semibold text-zinc-200 mb-2"
    const subtitleClassName = "text-zinc-400 text-sm mb-4"
    return (
        <>
            <div className={titleClassName}>{title}</div>
            <div className={subtitleClassName}>{subtitle}</div>
        </>
    )
}

function InputID({value, onChange}: {value: string, onChange: ChangeEventHandler<HTMLInputElement>}) {
    const inputClassName = "flex-1 px-4 py-3 rounded-xl bg-zinc-900/40 border border-dashed border-zinc-700 " +
        "text-zinc-200 placeholder:text-zinc-500 outline-none focus:border-zinc-500 transition"
    return <input type="text" value={value} onChange={onChange} placeholder="ID in https://youtube.com/shorts/ID" className={inputClassName}/>
}

function DownloadButton({ onClick, loading }: { onClick: () => void, loading?: boolean }) {
    const buttonClassName = "px-5 py-3 rounded-xl bg-zinc-800/60 border border-zinc-700 border-dashed text-zinc-200 transition"
    const disabledClassName = "opacity-50 cursor-not-allowed hover:bg-zinc-800/60"
    return (
        <button onClick={onClick} disabled={loading} className={buttonClassName + (loading ? " " + disabledClassName : " hover:bg-zinc-700/40")}>
            Download
        </button>
    )
}