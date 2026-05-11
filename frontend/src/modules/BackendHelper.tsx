export async function resetSession() {
    await fetch("http://127.0.0.1:8000/session/reset", {
        method: "POST"
    })

    console.log("Session reset")
}

export async function initializeSession(
    {youtubeId, file, setLoading, setCurrentPage}:
    {youtubeId: string, file: File | null, setLoading: (value: boolean) => void, setCurrentPage: (page: string) => void}
) {
    if (file == null) return
    if (youtubeId == "") return
    setLoading(true)

    const formData = new FormData()
    formData.append("youtube_id", youtubeId)
    formData.append("file", file)

    const res = await fetch("http://127.0.0.1:8000/session/initialize", {method: "POST", body: formData})
    const data = await res.json()

    console.log("SESSION COMMITTED:", data)
    setLoading(false)
    setCurrentPage("Scope")
}

export async function downloadYouTubeVideo(
    {youtubeId, setLoading, setVideoSrc}: {youtubeId: string, setLoading: (value: boolean) => void, setVideoSrc: (value: string) => void}
) {
    if (!youtubeId) return
    setLoading(true)
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/input/youtube",
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ youtube_id: youtubeId }),
            }
        )

        const data = await response.json()
        console.log("YOUTUBE DOWNLOAD SUCCESS:", data)

        setVideoSrc(`http://127.0.0.1:8000/media/${data.backend_path}`)
    } catch (error) {
        console.error("YOUTUBE DOWNLOAD FAILED:", error)
    } finally {
        setLoading(false)
    }
}

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