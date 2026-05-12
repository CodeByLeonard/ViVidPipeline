type BackendSessionResponse = {
    clip_path: string
    original_path: string
}

async function getSession(youtubeId: string, file: File): Promise<BackendSessionResponse> {
    const formData = new FormData()
    formData.append("youtube_id", youtubeId)
    formData.append("file", file)
    const response = await fetch("http://0.0.0.0:8000/pipeline/session/initialize", {method: "POST", body: formData})
    // if (!response.ok) throw new Error("Request failed")
    return response.json()
}

export type SessionInitializer = {
    youtubeId: string,
    file: File | null,
    setLoading: (value: boolean) => void,
    setCurrentPage: (page: string) => void,
    setOriginalFile: (path: string) => void,
    setClipFile: (path: string) => void,
}

export async function initializeSession(initializer: SessionInitializer) {
    if (initializer.file == null || initializer.youtubeId == "") return
    initializer.setLoading(true)
    const response = await getSession(initializer.youtubeId, initializer.file)
    initializer.setLoading(false)
    initializer.setCurrentPage("Scope")
    initializer.setOriginalFile(response.original_path)
    initializer.setClipFile(response.clip_path)
}

export async function resetSession() {
    await fetch("http://0.0.0.0:8000/pipeline/session/reset", {
        method: "POST"
    })

    console.log("Session reset")
}



//
// export async function initializeSession(
//     {youtubeId, setYoutubeId, file, setFile, setLoading, setCurrentPage, setClipFile, setOriginalFile}:
//     {youtubeId: string, setYoutubeId: (v: string) => void, file: File | null, setFile: (file: File | null) => void, setLoading: (value: boolean) => void, setCurrentPage: (page: string) => void,
//     setClipFile: (path: string) => void, setOriginalFile: (path: string) => void}
// ) {
//     setYoutubeId("d9F6MpOw5oY");
//     if (file == null || youtubeId == "") return
//     setLoading(true)
//
//     const formData = new FormData()
//     formData.append("youtube_id", youtubeId)
//     formData.append("file", file)
//
//     const res = await fetch(
//         `http://172.0.0.1:8000/pipeline/session/initialize`,
//         {
//             method: "POST",
//             body: formData
//         }
//     )
//     if (!res.ok) console.error("Initializing session failed:", res.status)
//
//     const data = await res.json()
//     setClipFile(data.clip_path)
//     setOriginalFile(data.original_path)
//
//     setLoading(false)
//     setCurrentPage("Scope")
//     setFile(null)
// }

export async function downloadYouTubeVideo(
    {youtubeId, setLoading, setVideoSrc}: {youtubeId: string, setLoading: (value: boolean) => void, setVideoSrc: (value: string) => void}
) {
    if (!youtubeId) return
    setLoading(true)
    try {
        const response = await fetch(
            `http://127.0.0.1:8000/pipeline/reconstruct/${youtubeId}`,
            {
                method: "GET",
                // headers: { "Content-Type": "application/json" },
                // body: JSON.stringify({ youtube_id: youtubeId }),
            }
        )

        const data = await response.json()
        setVideoSrc("http://0.0.0.0:8000/cache/clip_d9F6MpOw5oY.mp4")
        setVideoSrc(`http://0.0.0.0:8000/${data.filename}`)
    } catch (error) {
        console.error("YOUTUBE DOWNLOAD FAILED:", error)
    } finally {
        setLoading(false)
    }
}

export async function uploadOriginalVideo() {}

// const uploadFile = async () => {
//     if (!file) return
//
//     const formData = new FormData()
//     formData.append("file", file)
//
//     try {
//         const response = await fetch(
//             "http://127.0.0.1:8000/input/original",
//             { method: "POST", body: formData }
//         )
//
//         const data = await response.json()
//         console.log("UPLOAD SUCCESS:", data)
//         setVideoSrc(`http://127.0.0.1:8000/media/${data.backend_path}`)
//     } catch (error) {
//         console.error("UPLOAD FAILED:", error)
//     }
// }